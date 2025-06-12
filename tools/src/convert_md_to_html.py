
import markdown2
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_md_to_html.py <source-file-path>")
        sys.exit(1)

    source_file_path = sys.argv[1]
    with open(source_file_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()
    html_content = markdown2.markdown(markdown_content)
    print(html_content)


if __name__ == "__main__":
    main()
