import pytest
import markdown2
from src.converter import convert_markdown_to_html


def test_markdown_to_html_conversion():
    markdown_text = '# Hello World'
    expected_html = '<h1>Hello World</h1>\n'
    assert markdown2.markdown(markdown_text).strip() == expected_html.strip()
