"""
Completion Grading Django application initialization.
"""

from django.apps import AppConfig


class CompletionGradingConfig(AppConfig):
    """
    Configuration for the Completion Grading Django application.
    """

    name = "completion_grading"

    plugin_app = {
        "settings_config": {
            "lms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
            "cms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
        },
    }

    def ready(self):
        """
        Import the completion grading XBlock.
        """
        from completion_grading import tasks
