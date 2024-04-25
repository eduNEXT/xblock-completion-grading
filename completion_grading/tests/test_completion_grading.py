"""
Tests for XblockCompletionGrading
"""

from django.test import TestCase
from xblock.fields import ScopeIds
from xblock.test.toy_runtime import ToyRuntime

from completion_grading import XblockCompletionGrading


class TestXblockCompletionGrading(TestCase):
    """Tests for XblockCompletionGrading"""

    def test_my_student_view(self):
        """Test the basic view loads."""
        scope_ids = ScopeIds("1", "2", "3", "4")
        block = XblockCompletionGrading(ToyRuntime(), scope_ids=scope_ids)
        frag = block.student_view()
        as_dict = frag.to_dict()
        content = as_dict["content"]
        self.assertIn(
            '<div class="completion_grading_block"></div>',
            content,
            "XBlock did not render correct student view",
        )
