
import markdown2
import sys

def convert_markdown_to_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as md_file:
            markdown_text = md_file.read()
        html = markdown2.markdown(markdown_text)
        return html
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python markdown_to_html.py <source-markdown-file>')
        sys.exit(1)
    source_file = sys.argv[1]
    html_output = convert_markdown_to_html(source_file)
    if html_output is not None:
        print(html_output)
