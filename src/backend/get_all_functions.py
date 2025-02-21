"""
Gets available functions for use in an LLM prompt.

Skips private function names which can be used inside a module.
https://docs.python.org/3/reference/lexical_analysis.html#reserved-classes-of-identifiers

It supports to extract functions from two levels:
    src/backend/functions/
    ├── music
    │   ├── spotify.py
    └── alarm.py
"""

import os
from importlib import import_module
from inspect import getmembers, isfunction

import functions    # Import the package.


def get_functions_from_package(package):
    functions_list = []
    modules_names_list = []

    # Find all functions in the 'functions' package by scanning its modules.
    package_path = os.path.dirname(package.__file__)
    for item in os.listdir(package_path):
        item_path = os.path.join(package_path, item)

        # Handle Python files (excluding __init__.py).
        if item.endswith(".py") and item != "__init__.py":
            module_name = f"{package.__name__}.{item[:-3]}" # Convert filename to module path
            modules_names_list.append(module_name)

        # Handle subdirectories that contain an __init__.py file (Python packages).
        elif (os.path.isdir(item_path) and
              os.path.isfile(f"{item_path}/__init__.py")):
            for sub_item in os.listdir(item_path):
                if sub_item.endswith(".py") and sub_item != "__init__.py":
                    sub_module_name = f"{package.__name__}.{item}.{sub_item[:-3]}"  # Convert sub filename to module path
                    modules_names_list.append(sub_module_name)

    # Import modules dynamically and extract available function names.
    for module_name in modules_names_list:
        module = import_module(module_name)

        for function_name, _ in getmembers(module, isfunction):
            # Skip processing aka private functions names.
            if not function_name.startswith("__"):
                functions_list.append(f"{function_name}()")

    return functions_list

def get_list_of_functions():
    return ', '.join(get_functions_from_package(functions))
