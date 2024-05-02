"""
Utilities for completion grading.
"""

import logging
from enum import Enum

from django.contrib.auth import get_user_model
from opaque_keys.edx.keys import CourseKey, UsageKey

from completion_grading.edxapp_wrapper.modulestore import modulestore

ATTR_KEY_ANONYMOUS_USER_ID = "edx-platform.anonymous_user_id"
ATTR_KEY_USERNAME = "edx-platform.username"

log = logging.getLogger(__name__)


def _(text):
    """
    Make '_' a no-op so we can scrape strings.
    """
    return text


def get_course_sequences(course_key):
    """
    Extract a list of 'subsections' from a course.

    Args:
        course_key (CourseKey): Course key.

    Returns:
        iterable: List of subsections.
    """
    course = modulestore().get_course(course_key,depth=0)
    for section in course.get_children():
        for subsection in section.get_children():
            yield from subsection.get_children()


def _(text):
    """
    Make '_' a no-op so we can scrape strings.
    """
    return text


def get_anonymous_user_id(user) -> str:
    """
    Get anonymous user id from user object.

    Args:
        user (XBlockUser): XBlock User object.

    Returns:
        str: Anonymous user id.
    """
    return user.opt_attrs.get(ATTR_KEY_ANONYMOUS_USER_ID)


def get_username(user) -> str:
    """
    Get username from user object.

    Args:
        user (XBlockUser): XBlock User object.

    Returns:
        str: Username.
    """
    return user.opt_attrs.get(ATTR_KEY_USERNAME)


class GradingMethod(Enum):
    """
    Enum for completion grading method.

    - MINIMUM_COMPLETION: Learners are graded based on the minimum number of completed units
    - WEIGHTED_COMPLETION: Learners are graded based on the weighted number of completed units
    """

    MINIMUM_COMPLETION = _("Minimum Number of Completed Units")
    WEIGHTED_COMPLETION = _("Weighted Number of Completed Units")


def get_user_completions_by_verticals(username, course_key_string, usage_key):
    """
    Grade a submission with completions API.
    """
    # Import here to avoid apps not ready error
    from completion.services import CompletionService

    User = get_user_model()
    user = User.objects.get(username=username)

    usage_key = UsageKey.from_string(usage_key)
    course_key = CourseKey.from_string(course_key_string)

    completion_service = CompletionService(user, course_key)
    completed_units = 0

    for unit in get_course_sequences(course_key):
        if usage_key not in [
            child.location for child in unit.get_children()
        ] and completion_service.vertical_is_complete(unit):
            completed_units += 1

    return completed_units
