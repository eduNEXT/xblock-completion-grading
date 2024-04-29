"""
Tests for XBlockCompletionGrading
"""

from django.test import TestCase
from xblock.fields import ScopeIds
from xblock.test.toy_runtime import ToyRuntime

from completion_grading import XBlockCompletionGrading


class TestXBlockCompletionGrading(TestCase):
    """Tests for XBlockCompletionGrading"""

    def test_my_student_view(self):
        """Test the basic view loads."""
        scope_ids = ScopeIds("1", "2", "3", "4")
        block = XBlockCompletionGrading(ToyRuntime(), scope_ids=scope_ids)
        frag = block.student_view()
        as_dict = frag.to_dict()
        content = as_dict["content"]
        self.assertIn(
            '<div class="completion_grading_block"></div>',
            content,
            "XBlock did not render correct student view",
        )
