# Professional Python Project Structure

A professional Python application should not have all its code in the root directory. Instead, it should use a `src` (source) layout.

## The `src` Layout

The main application code resides inside a directory named `src`. This prevents many common import problems and ensures the project is properly installable.

An example structure:

my_project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt
└── README.md

## Why use a `src` layout?

1.  **Editable Installs:** It ensures that when you install the package in editable mode (`pip install -e .`), it works correctly.
2.  **Clarity:** It clearly separates your importable package code from other project files like `README.md`, `Dockerfile`, etc.
3.  **Avoids Accidental Imports:** It prevents you from accidentally importing your code as a top-level module when your current working directory is the project root.