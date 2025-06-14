#!/usr/bin/env python3
import sys
import markdown2

def convert_md_to_html(md_file_path):
    try:
        with open(md_file_path, 'r') as md_file:
            markdown_content = md_file.read()
        html_content = markdown2.markdown(markdown_content)
        html_file_path = md_file_path.rsplit('.', 1)[0] + '.html'
        with open(html_file_path, 'w') as html_file:
            html_file.write(html_content)
        print(f"Conversion successful: {html_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python markdown_to_html.py <markdown_file_path>")
    else:
        convert_md_to_html(sys.argv[1])
