import sys
from pathlib import Path
from textwrap import indent
import pytest

# Put root dir on the path so `pytest.importorskip` can run them
root_dir = Path(__file__).parents[1]
sys.path.append(str(root_dir))


def fmt_output(text: str) -> list[str]:
    """Utility function for formatting subprocess output."""
    if "```" in text:
        # Logged script code: indent multi-line paragraphs (code blocks)
        # Use the 'script:\n' tag as a separator for individual scripts in the log
        formatted = []
        scripts = list(filter(None, text.split("script:\n")))
        # Use the 'code=' tag as a separator for the code block of a script in the log
        for script in scripts:
            preamble, code_block = script.strip("\n").strip().split("code=", 1)
            # List as a 2-tuple so that inline-snapshot formats them nicely in pairs
            formatted.append((preamble.strip(), code_block.strip()))
        return formatted
    else:
        # Actual program output
        return text.splitlines()


pytest.fmt_output = fmt_output
