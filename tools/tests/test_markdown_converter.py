
from src.markdown_converter import convert_markdown_to_html
import markdown2
import pytest
import sys
from io import StringIO

def test_convert_markdown_to_html(monkeypatch):
    test_md_content = '# Hello World'
    expected_html_content = markdown2.markdown(test_md_content)
    with open('test.md', 'w') as f:
        f.write(test_md_content)
    monkeypatch.setattr(sys, 'argv', ['markdown_converter.py', 'test.md'])
    captured_output = StringIO()
    monkeypatch.setattr(sys.stdout, 'write', captured_output.write)
    convert_markdown_to_html('test.md')
    assert captured_output.getvalue().strip() == expected_html_content
