
import sys
import markdown2

def convert_markdown_to_html(file_path):
    with open(file_path, 'r') as f:
        markdown_text = f.read()
    html = markdown2.markdown(markdown_text)
    print(html)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python markdown_converter.py <source-markdown-file>')
    else:
        convert_markdown_to_html(sys.argv[1])
