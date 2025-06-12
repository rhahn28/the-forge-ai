
import pytest
import markdown2
from src.convert_md_to_html import main
import sys
from io import StringIO


def test_conversion(monkeypatch):
    markdown_content = "# Hello World"
    expected_html_content = "<h1>Hello World</h1>\n"
    with monkeypatch.context() as m:
        m.setattr('sys.stdin', StringIO(markdown_content))
        m.setattr('sys.stdout', StringIO())
        m.setattr('sys.argv', ['convert_md_to_html.py', 'dummy_path'])
        m.setattr('builtins.open', lambda x, _: StringIO(markdown_content))
        main()
        output = sys.stdout.getvalue()
        assert output == expected_html_content
