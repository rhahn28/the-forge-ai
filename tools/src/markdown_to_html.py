import markdown2
import sys

def convert_markdown_to_html(markdown_content):
    html_content = markdown2.markdown(markdown_content)
    return html_content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python markdown_to_html.py <source_markdown_file>")
        sys.exit(1)
    markdown_file_path = sys.argv[1]
    try:
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()
        html_content = convert_markdown_to_html(markdown_content)
        print(html_content)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
