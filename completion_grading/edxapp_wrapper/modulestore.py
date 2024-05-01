"""
Modulestore module generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def modulestore():
    """
    Wrapper for `modulestore` function in xmodule.
    """
    backend_function = settings.COMPLETION_GRADING_MODULESTORE_BACKEND
    backend = import_module(backend_function)

    return backend.modulestore()
