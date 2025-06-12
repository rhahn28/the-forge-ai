
import pytest
from src.markdown_to_html import convert_markdown_to_html


def test_markdown_to_html(tmp_path):
    md_content = '# Hello World\nThis is a test.'
    md_file = tmp_path / 'test.md'
    md_file.write_text(md_content, encoding='utf-8')

    expected_html = '<h1>Hello World</h1>\n<p>This is a test.</p>\n'
    result = convert_markdown_to_html(str(md_file))
    assert result == expected_html
