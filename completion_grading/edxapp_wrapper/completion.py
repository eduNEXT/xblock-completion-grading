"""
Completion Service module generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def init_completion_service(*args, **kwargs):
    """
    Wrapper for `submissions.api.create_submission` function in edx-submissions.
    """
    backend_function = settings.COMPLETION_GRADING_COMPLETION_SERVICE_BACKEND
    backend = import_module(backend_function)

    return backend.CompletionService(*args, **kwargs)
