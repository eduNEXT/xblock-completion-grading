"""
Settings for the Completion Grading XBlock.
"""


def plugin_settings(settings):
    """
    Read / Update necessary common project settings.
    """
    settings.COMPLETION_GRADING_SUBMISSIONS_BACKEND = (
        "completion_grading.edxapp_wrapper.backends.submissions_q_v1"
    )
    settings.COMPLETION_GRADING_MODULESTORE_BACKEND = (
        "completion_grading.edxapp_wrapper.backends.modulestore_q_v1"
    )
    settings.COMPLETION_GRADING_COMPLETION_SERVICE_BACKEND = (
        "completion_grading.edxapp_wrapper.backends.completion_q_v1"
    )
