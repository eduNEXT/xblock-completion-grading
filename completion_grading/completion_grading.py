"""CompletionGrading XBlock."""

from __future__ import annotations

import logging
from typing import Optional

import pkg_resources
from django.utils import translation
from web_fragments.fragment import Fragment
from xblock.completable import CompletableXBlockMixin
from xblock.core import XBlock
from xblock.fields import Float, Integer, Scope, String
from xblock.utils.resources import ResourceLoader
from xblock.utils.studio_editable import StudioEditableXBlockMixin

from completion_grading.edxapp_wrapper.submissions import create_submission, get_score, set_score
from completion_grading.utils import GradingMethod, _, get_anonymous_user_id, get_course_sequences

log = logging.getLogger(__name__)
loader = ResourceLoader(__name__)

ITEM_TYPE = "completion_grading"
MAX_SCORE = 1
MIN_SCORE = 0


@XBlock.needs("i18n", "user")
@XBlock.wants("completion")
class XBlockCompletionGrading(
    StudioEditableXBlockMixin, CompletableXBlockMixin, XBlock
):
    """
    CompletionGrading XBlock provides a way to grade completions in Open edX.
    """

    CATEGORY = "completion_grading"

    has_score = True
    icon_class = "problem"

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        scope=Scope.settings,
        default=_("Course Completion Grading"),
    )

    grading_method = String(
        display_name=_("Grading Method"),
        help=_(
            "Completion grading method for the component. There are two "
            "options: minimum completion and average completion. Minimum "
            "completion grades learners based on the minimum number of "
            "completed units, if the learner has completed the minimum "
            "number of units, they will get a grade of 1, otherwise 0. "
            "Average completion grades learners based on the average number "
            "of completed units, if the learner has completed a number of units "
            "grater or equal to the number of completed units required to get a grade, "
            "they will get a grade of 1, otherwise the grade will be the "
            "number of completed units divided by the number of completed "
            "units required to get a grade configured in the component."
            "If the value is not set, the component will use the minimum completion method."
            "The unit completions don't include the completion of the unit that contains the component."
        ),
        values=[
            {"display_name": grading_method.value, "value": grading_method.name}
            for grading_method in GradingMethod
        ],
        scope=Scope.settings,
        default=GradingMethod.MINIMUM_COMPLETION.name,
    )

    max_attempts = Integer(
        display_name=_("Maximum Attempts"),
        help=_(
            "Defines the number of times a student can attempt to "
            "calculate the grade. If the value is not set, infinite "
            "attempts are allowed."
        ),
        values={"min": 0},
        scope=Scope.settings,
        default=None,
    )

    unit_completions = Integer(
        display_name=_("Number of completed units"),
        help=_("Number of units that need to be completed to get a grade."),
        scope=Scope.settings,
        default=1,
    )

    weight = Integer(
        display_name=_("Problem Weight"),
        help=_(
            "Defines the number of points this problem is worth. If "
            "the value is not set, the problem is worth 1 point."
        ),
        default=1,
        scope=Scope.settings,
    )

    instructions_text = String(
        display_name=_("Instructions Text"),
        help=_("Instructions to be displayed to the student."),
        default=_(
            "Please press the button to calculate your grade according "
            "to the number of completed units in the course.",
        ),
        scope=Scope.settings,
    )

    button_text = String(
        display_name=_("Button Text"),
        help=_("Text to be displayed on the button."),
        default=_("Calculate Grade"),
        scope=Scope.settings,
    )

    attempts = Integer(
        help=_("Number of attempts taken by the student to calculate the grade."),
        default=0,
        scope=Scope.user_state,
    )

    raw_score = Float(
        display_name=_("Raw score"),
        help=_("The raw score for the assignment."),
        default=None,
        scope=Scope.user_state,
    )

    submission_uuid = String(
        display_name=_("Submission UUID"),
        help=_("The submission UUID for the assignment."),
        default=None,
        scope=Scope.user_state,
    )

    editable_fields = [
        "display_name",
        "grading_method",
        "max_attempts",
        "unit_completions",
        "weight",
        "instructions_text",
        "button_text",
    ]

    @property
    def block_id(self) -> str:
        """
        Return the usage_id of the block.
        """
        return str(self.scope_ids.usage_id)

    @property
    def block_course_id(self) -> str:
        """
        Return the course_id of the block.
        """
        return self.course_id

    @property
    def current_user(self):
        """
        Get the current user.
        """
        return self.runtime.service(self, "user").get_current_user()

    def resource_string(self, path: str) -> str:
        """
        Handy helper for getting resources from our kit.

        Args:
            path (str): A path to the resource.

        Returns:
            str: The resource as a string.
        """
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def render_template(
        self, template_path: str, context: Optional[dict] = None
    ) -> str:
        """
        Render a template with the given context.

        The template is translated according to the user's language.

        Args:
            template_path (str): The path to the template
            context(dict, optional): The context to render in the template

        Returns:
            str: The rendered template
        """
        return loader.render_django_template(
            template_path, context, i18n_service=self.runtime.service(self, "i18n")
        )

    def student_view(self, _context: dict = None) -> Fragment:
        """
        Create primary view of the XBlockCompletionGrading, shown to students when viewing courses.

        Args:
            context (dict, optional):
                A dict containing data to be used in the view. Defaults to None.

        Returns:
            Fragment: The fragment to be displayed.
        """
        frag = Fragment()

        # Add i18n js
        if statici18n_js_url := self._get_statici18n_js_url():
            frag.add_javascript_url(
                self.runtime.local_resource_url(self, statici18n_js_url)
            )

        context = {
            "block": self,
            "weighted_score": self.get_weighted_score(),
        }

        frag.add_content(
            self.render_template("static/html/completion_grading.html", context)
        )
        frag.add_css(self.resource_string("static/css/completion_grading.css"))
        frag.add_javascript(self.resource_string("static/js/src/completion_grading.js"))
        frag.initialize_js("XBlockCompletionGrading")
        return frag

    def get_weighted_score(self) -> int:
        """
        Return weighted score for the current user.

        Returns:
            int | None: The weighted score.
        """
        score = get_score(self.get_student_item_dict())
        return score.get("points_earned") if score else 0

    def get_student_item_dict(self) -> dict:
        """
        Return dict required by the submissions app.

        This allows creating and retrieving submissions for a particular student.

        Returns:
            dict: The student item dict.
        """
        return {
            "student_id": get_anonymous_user_id(self.current_user),
            "course_id": str(self.block_course_id),
            "item_id": self.block_id,
            "item_type": ITEM_TYPE,
        }

    @XBlock.json_handler
    def calculate_grade(self, _: dict, _suffix: str = "") -> dict:
        """
        Calculate the grade for the student.

        The grading is calculated according to the grading method and the number of completed units.

        Args:
            _data (dict): Additional data to be used in the calculation.
            _suffix (str, optional): Suffix for the handler. Defaults to "".

        Returns:
            dict: A dictionary containing the handler result.
        """
        if self.max_attempts and self.attempts >= self.max_attempts:
            return {
                "success": False,
                "message": _("You have reached the maximum number of attempts."),
            }

        self.raw_score = self.get_raw_score()

        if not self.submission_uuid:
            self.create_submission()
            self.emit_completion(1)

        self.set_score()

        self.attempts += 1

        return {
            "success": True,
            "message": _("Grade calculated successfully."),
        }

    def get_raw_score(self) -> int:
        """
        Get the grade for the current user based on the grading method and number of interventions.

        Returns:
            int: The grade for the current user.
        """
        unit_completions = self.get_unit_completions()

        if unit_completions >= self.unit_completions:
            return MAX_SCORE

        if self.grading_method == GradingMethod.MINIMUM_COMPLETION.name:
            return MAX_SCORE
        elif self.grading_method == GradingMethod.AVERAGE_COMPLETION.name:
            return unit_completions / self.unit_completions
        return MIN_SCORE

    def get_unit_completions(self):
        """
        Get the number of completed units for the current user.
        """
        completed_units = 0
        completion_service = self.runtime.service(self, "completion")
        for unit in get_course_sequences(self.block_course_id):
            if (
                self not in unit.get_children()
                and completion_service.vertical_is_complete(unit)
            ):
                completed_units += 1
        return completed_units

    def create_submission(self) -> None:
        """
        Get the submission for the current user.
        """
        submission_data = create_submission(
            self.get_student_item_dict(),
            {
                "completion": 1,
            },
        )
        self.submission_uuid = submission_data.get("uuid")

    def set_score(self) -> None:
        """
        Set the score for the current user.
        """
        set_score(
            self.submission_uuid, round(self.raw_score * self.weight), self.weight
        )

    @staticmethod
    def workbench_scenarios() -> list[tuple[str, str]]:
        """Create canned scenario for display in the workbench."""
        return [
            (
                "XBlockCompletionGrading",
                """<completion_grading/>
             """,
            ),
            (
                "Multiple XBlockCompletionGrading",
                """<vertical_demo>
                <completion_grading/>
                <completion_grading/>
                <completion_grading/>
                </vertical_demo>
             """,
            ),
        ]

    @staticmethod
    def _get_statici18n_js_url() -> str | None:
        """
        Return the Javascript translation file for the currently selected language, if any.

        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = "public/js/translations/{locale_code}/text.js"
        lang_code = locale_code.split("-")[0]
        for code in (translation.to_locale(locale_code), lang_code, "en"):
            if pkg_resources.resource_exists(
                loader.module_name, text_js.format(locale_code=code)
            ):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy() -> str:
        """
        Generate initial i18n with dummy method.
        """
        return translation.gettext_noop("Dummy")
