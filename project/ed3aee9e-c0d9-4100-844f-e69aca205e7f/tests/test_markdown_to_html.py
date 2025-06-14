import unittest
import os
from src.markdown_to_html import convert_md_to_html

class TestMarkdownToHtml(unittest.TestCase):
    def test_conversion(self):
        test_md_path = 'test.md'
        test_html_path = 'test.html'
        with open(test_md_path, 'w') as f:
            f.write('# Title\n\nThis is a test.')
        convert_md_to_html(test_md_path)
        self.assertTrue(os.path.exists(test_html_path))
        with open(test_html_path, 'r') as f:
            html_content = f.read()
        self.assertIn('<h1>Title</h1>', html_content)
        self.assertIn('<p>This is a test.</p>', html_content)
        os.remove(test_md_path)
        os.remove(test_html_path)

if __name__ == '__main__':
    unittest.main()
