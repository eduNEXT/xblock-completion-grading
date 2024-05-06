"""
Tests for XBlockCompletionGrading
"""

from unittest.mock import Mock, patch

from ddt import data, ddt, unpack
from django.test import TestCase
from opaque_keys.edx.keys import UsageKey
from xblock.fields import ScopeIds
from xblock.test.toy_runtime import ToyRuntime

from completion_grading import XBlockCompletionGrading
from completion_grading.utils import GradingMethod, get_user_completions_by_verticals


@ddt
class TestXBlockCompletionGrading(TestCase):
    """Tests for XBlockCompletionGrading class."""

    def setUp(self) -> None:
        runtime = Mock(service=ToyRuntime().service)
        self.block = XBlockCompletionGrading(
            runtime=runtime,
            field_data={},
            scope_ids=ScopeIds("1", "2", "3", "4"),
        )
        self.block.get_student_item_dict = Mock(return_value={"student_item_id": "123"})
        self.block.course_id = "course-v1:edunext+101+2021"
        self.location_string = "block-v1:edunext+101+2021+type@unit+block@123"
        self.block.location = UsageKey.from_string(self.location_string)

    @patch("completion_grading.completion_grading.get_score")
    def test_student_view(self, mock_get_score):
        """Test the student view loads.

        Expected behavior:
        - The block should render the student view.
        - The block should display the grade if set.
        """
        mock_get_score.return_value = {
            "points_earned": 5,
            "points_possible": 10,
        }
        self.block.weight = 10

        self.block.student_view()

        self.assertTrue(mock_get_score.called)
        self.assertIn("5 / 10", self.block.student_view({}).content)

    @patch(
        "completion_grading.completion_grading.get_user_completions_by_verticals_task"
    )
    @patch("completion_grading.completion_grading.set_score")
    @patch(
        "completion_grading.completion_grading.CompletableXBlockMixin.emit_completion"
    )
    @patch("completion_grading.completion_grading.create_submission")
    def test_calculate_grade_async_process(
        self,
        mock_create_submission,
        mock_emit_completion,
        mock_set_score,
        mock_get_user_completions_by_verticals_task,
    ):
        """Test the JSON handler for calculating the grade asynchronously.

        Expected behavior:
        - The handler should return a JSON response with the status.
        - The handler should trigger the grade calculation task.
        """
        self.block.task_id = None
        self.block.runtime.service = Mock(
            return_value=Mock(
                get_current_user=Mock(
                    return_value=Mock(
                        opt_attrs={
                            "edx-platform.anonymous_user_id": "123",
                            "edx-platform.username": "test",
                        }
                    )
                )
            )
        )
        self.block.max_attempts = None
        expected_result = {
            "success": False,
            "message": (
                "Grade calculations for your latest completion state are in progress. "
                "Try again in a few seconds."
            ),
        }
        request = Mock(method="POST", body=b"{}")

        result = self.block.calculate_grade(request)

        mock_create_submission.assert_not_called()
        mock_emit_completion.assert_not_called()
        mock_set_score.assert_not_called()
        mock_get_user_completions_by_verticals_task.apply_async.assert_called_once()
        self.assertEqual(result.json, expected_result)

    @patch("completion_grading.completion_grading.celery")
    @patch(
        "completion_grading.completion_grading.get_user_completions_by_verticals_task"
    )
    @patch("completion_grading.completion_grading.set_score")
    @patch(
        "completion_grading.completion_grading.CompletableXBlockMixin.emit_completion"
    )
    @patch("completion_grading.completion_grading.create_submission")
    def test_get_calculated_grade(
        self,
        mock_create_submission,
        mock_emit_completion,
        mock_set_score,
        mock_get_user_completions_by_verticals_task,
        mock_celery,
    ):
        """Test the JSON handler for calculating the grade when the task is completed.

        Expected behavior:
        - The handler should return a JSON response with the status.
        - The handler should set the grade for the block.
        """
        self.block.max_attempts = None
        self.block.task_id = "123"
        self.block.get_raw_score = Mock(return_value=5)
        self.block.submission_uuid = None
        mock_create_submission.return_value = {
            "uuid": "123",
        }
        self.block.weight = 100
        expected_weighted_score = round(5 * 100)
        expected_result = {
            "success": True,
            "message": "Grade calculated successfully.",
        }
        request = Mock(method="POST", body=b"{}")
        mock_celery.current_app.AsyncResult.return_value = Mock(
            status="SUCCESS",
            result=5,
        )

        result = self.block.calculate_grade(request)

        mock_create_submission.assert_called_once()
        mock_emit_completion.assert_called_once()
        mock_set_score.assert_called_once_with(
            "123", expected_weighted_score, self.block.weight
        )
        mock_get_user_completions_by_verticals_task.apply_async.assert_not_called()
        self.assertEqual(result.json, expected_result)
        self.assertEqual(self.block.attempts, 1)

    @patch("completion_grading.completion_grading.celery")
    @patch(
        "completion_grading.completion_grading.get_user_completions_by_verticals_task"
    )
    @patch("completion_grading.completion_grading.set_score")
    @patch(
        "completion_grading.completion_grading.CompletableXBlockMixin.emit_completion"
    )
    def test_calculate_grade_failed_task(self, _, __, ___, mock_celery):
        """Test the JSON handler for calculating the grade when the task fails.

        Expected behavior:
        - The handler should return a JSON response with the status success False.
        """
        self.block.max_attempts = None
        self.block.task_id = "123"
        expected_result = {
            "success": False,
            "message": "Completion grade calculation failed. Try again later.",
        }
        mock_celery.current_app.AsyncResult.return_value = Mock(
            status="FAILURE",
        )
        request = Mock(method="POST", body=b"{}")

        result = self.block.calculate_grade(request)

        self.assertEqual(result.json, expected_result)

    def test_calculate_grade_max_attempts(self):
        """Test the JSON handler for calculating the grade when max attempts is reached.

        Expected behavior:
        - The handler should return a JSON response with the status success False.
        """
        self.block.max_attempts = 1
        self.block.attempts = 1
        expected_result = {
            "success": False,
            "message": "You have reached the maximum number of attempts.",
        }
        request = Mock(method="POST", body=b"{}")

        result = self.block.calculate_grade(request)

        self.assertEqual(result.json, expected_result)

    @data(
        (GradingMethod.WEIGHTED_COMPLETION.name, 10, 5, 5 / 10),
        (GradingMethod.WEIGHTED_COMPLETION.name, 5, 5, 5 / 5),
        (GradingMethod.MINIMUM_COMPLETION.name, 10, 5, 0),
        (GradingMethod.MINIMUM_COMPLETION.name, 5, 5, 1),
    )
    @unpack
    def test_get_raw_score(
        self, grading_method, unit_completions, user_unit_completions, expected_score
    ):
        """Test getting the raw score for both grading methods.

        Expected behavior:
        - The raw score should be 0 if the learner has not completed a number of units
        greater than the number of units configured.
        - The raw score should be 1 if the learner has completed a number of units
        greater than the number of units configured.
        - The raw score should be 0 if the learner has not the minimum number of units.
        - The raw score should be 1 if the learner has the minimum number of units.
        """
        self.block.unit_completions = unit_completions
        self.block.grading_method = grading_method

        raw_score = self.block.get_raw_score(user_unit_completions)

        self.assertEqual(raw_score, expected_score)

    @patch("completion_grading.utils.init_completion_service")
    @patch("completion_grading.utils.get_user_model")
    @patch("completion_grading.utils.get_course_sequences")
    def test_get_unit_completions(
        self, mock_get_course_sequences, _, mock_init_completion_service
    ):
        """Test getting the number of completed units for a user.

        Expected behavior:
        - The method should return the number of completed units for the user.
        """
        mock_verticals = [
            Mock(completed=True, get_children=Mock(return_value=[Mock()])),
            Mock(completed=False, get_children=Mock(return_value=[Mock()])),
            Mock(completed=True, get_children=Mock(return_value=[self.block])),
        ]
        mock_get_course_sequences.return_value = mock_verticals
        mock_init_completion_service.return_value = Mock(
            vertical_is_complete=Mock(side_effect=lambda unit: unit.completed),
        )

        completed_units = get_user_completions_by_verticals(
            "test",
            self.block.course_id,
            self.location_string,
        )

        self.assertEqual(completed_units, 1)
