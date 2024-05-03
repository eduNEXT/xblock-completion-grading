"""
Settings for the Completion Grading XBlock.
"""


def plugin_settings(settings):
    """
    Read / Update necessary common project settings.
    """
    settings.COMPLETION_GRADING_SUBMISSIONS_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "COMPLETION_GRADING_SUBMISSIONS_BACKEND",
        settings.COMPLETION_GRADING_SUBMISSIONS_BACKEND,
    )
    settings.COMPLETION_GRADING_MODULESTORE_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "COMPLETION_GRADING_MODULESTORE_BACKEND",
        settings.COMPLETION_GRADING_MODULESTORE_BACKEND,
    )
    settings.COMPLETION_SERVICE_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "COMPLETION_SERVICE_BACKEND",
        settings.COMPLETION_SERVICE_BACKEND,
    )
