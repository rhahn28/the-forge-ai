import pytest
from markdown2 import markdown
from src.convert import convert_markdown_to_html
from io import StringIO
import sys

@pytest.fixture
def markdown_sample():
    return '# Hello World\nThis is a test.'

@pytest.fixture
def expected_html():
    return '<h1>Hello World</h1>\n\n<p>This is a test.</p>\n'

def test_conversion_to_html(markdown_sample, expected_html, capsys):
    sys.stdin = StringIO(markdown_sample)
    sys.argv = ['convert.py', 'dummy.md']
    convert_markdown_to_html('dummy.md')  # dummy.md simulates input
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_html.strip()