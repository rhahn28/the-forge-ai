import sys
import markdown2

def convert_markdown_to_html(file_path):
    with open(file_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()
    html_content = markdown2.markdown(markdown_content)
    print(html_content)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python convert.py <markdown-file-path>')
    else:
        convert_markdown_to_html(sys.argv[1])