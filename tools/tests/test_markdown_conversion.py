import pytest
from markdown2 import markdown

def test_markdown_to_html():
    markdown_text = "# Hello World"
    expected_html = "<h1>Hello World</h1>\n"
    assert markdown(markdown_text) == expected_html
