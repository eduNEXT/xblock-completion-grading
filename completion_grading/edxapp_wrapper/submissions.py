"""
Comments module generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def create_submission(*args, **kwargs):
    """
    Wrapper for `submissions.api.create_submission` function in edx-submissions.
    """
    backend_function = settings.DISCUSSION_GRADING_SUBMISSIONS_BACKEND
    backend = import_module(backend_function)

    return backend.create_submission(*args, **kwargs)


def get_score(*args, **kwargs):
    """
    Wrapper for `submissions.api.get_score` function in edx-submissions.
    """
    backend_function = settings.DISCUSSION_GRADING_SUBMISSIONS_BACKEND
    backend = import_module(backend_function)

    return backend.get_score(*args, **kwargs)


def set_score(*args, **kwargs):
    """
    Wrapper for `submissions.api.set_score` function in edx-submissions.
    """
    backend_function = settings.DISCUSSION_GRADING_SUBMISSIONS_BACKEND
    backend = import_module(backend_function)

    return backend.set_score(*args, **kwargs)
