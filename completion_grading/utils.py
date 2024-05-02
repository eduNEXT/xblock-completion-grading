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
    Extract a list of 'subsections' from a course.

    Args:
        course_key (CourseKey): Course key.

    Returns:
        iterable: List of subsections.
    """
    course = modulestore().get_course(course_key, depth=0)
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


class GradingMethod(Enum):
    """
    Enum for completion grading method.

    - MINIMUM_COMPLETION: Learners are graded based on the minimum number of completed units
    - WEIGHTED_COMPLETION: Learners are graded based on the weighted number of completed units
    """

    MINIMUM_COMPLETION = _("Minimum Number of Completed Units")
    WEIGHTED_COMPLETION = _("Weighted Number of Completed Units")
