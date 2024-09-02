import sys
from pathlib import Path
from textwrap import indent
import pytest

# Put root dir on the path so `pytest.importorskip` can run them
root_dir = Path(__file__).parents[1]
sys.path.append(str(root_dir))


def fmt_output(text: str) -> list[str]:
    """Provide a utility function for formatting output."""
    if "```" in text:
        # Logged script code: indent multi-line paragraphs (code blocks)
        return [
            indent(section, prefix=" " * 8).strip("\n")
            for section in text.split("code=")
        ]
    else:
        # Actual program output
        return text.splitlines()


pytest.fmt_output = fmt_output
