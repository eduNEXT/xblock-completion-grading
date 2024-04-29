"""
Utilities for completion grading.
"""

from enum import Enum

from completion_grading.edxapp_wrapper.modulestore import modulestore

ATTR_KEY_ANONYMOUS_USER_ID = "edx-platform.anonymous_user_id"


def _(text):
    """
    Make '_' a no-op so we can scrape strings.
    """
    return text


def get_course_sequences(course_key):
    """
    Extracts a list of 'subsections' from a course.
    """
    course = modulestore().get_course(course_key, depth=0)
    for section in course.get_children():
        for subsection in section.get_children():
            for unit in subsection.get_children():
                yield unit


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


class GradingMethod(Enum):
    """
    Enum for completion grading method.

    - MINIMUM_COMPLETION: Learners are graded based on the minimum number of completed units
    - AVERAGE_COMPLETION: Learners are graded based on the average number of completed units
    """

    MINIMUM_COMPLETION = _("Minimum number of completed units")
    AVERAGE_COMPLETION = _("Average number of completed units")
