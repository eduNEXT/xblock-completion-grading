from celery import shared_task
from edx_django_utils.monitoring import set_code_owner_attribute


@shared_task
@set_code_owner_attribute
def get_user_completions_by_verticals_task(username, course_key_string, usage_key):
    """
    Grade a submission with completions API.
    """
    from completion_grading.utils import get_user_completions_by_verticals

    return get_user_completions_by_verticals(username, course_key_string, usage_key)
