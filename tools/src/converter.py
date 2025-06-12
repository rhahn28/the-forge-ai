import sys
import markdown2

def convert_markdown_to_html(file_path):
    with open(file_path, 'r') as file:
        markdown_content = file.read()
    html_content = markdown2.markdown(markdown_content)
    print(html_content)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python converter.py <source-markdown-file>')
        sys.exit(1)
    convert_markdown_to_html(sys.argv[1])
