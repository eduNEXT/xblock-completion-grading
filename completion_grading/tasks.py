"""
Celery tasks for completion grading.
"""

from celery import shared_task

from completion_grading.utils import get_user_completions_by_verticals


@shared_task
def get_user_completions_by_verticals_task(username, course_key_string, usage_key):
    """
    Grade a submission with completions API.
    """
    return get_user_completions_by_verticals(
        username,
        course_key_string,
        usage_key,
    )
