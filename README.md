# Unit Testing for Nested Dictionary Access

This project demonstrates unit testing for a Python function `access_nested_map` located in the `utils.py` module. The `access_nested_map` function is designed to safely access values within a nested dictionary using a tuple of keys as a path.

## Purpose

The goal of this project is to ensure the `access_nested_map` function behaves as expected for various valid and potentially edge-case inputs. This is achieved through the use of Python's `unittest` framework and the `parameterized` library for running tests with multiple input sets.

## Contents

* **`README.md`**: This file, providing an overview of the project and describing the tests.
* **`utils.py`**: Contains the `access_nested_map` function (implementation details are not covered here but should be present).
* **`test_utils.py`**: Contains the unit tests for the `access_nested_map` function, using the `unittest` framework and `parameterized`.

## How to Run the Tests

1.  Ensure you have Python 3.7 or higher installed.
2.  Install the `parameterized` library if you haven't already:
    ```bash
    pip install parameterized
    ```
3.  Save the `utils.py` and `test_utils.py` files in the same directory.
4.  Make both files executable:
    ```bash
    chmod +x utils.py test_utils.py
    ```
5.  Run the tests from your terminal:
    ```bash
    python3 test_utils.py
    ```

## Detailed Description of the Tests

The `test_utils.py` file contains the `TestAccessNestedMap` class, which includes a method called `test_access_nested_map`. This method is decorated with `@parameterized.expand` to run the same test logic with different sets of input data. Here's a breakdown of what each test case aims to verify:

* **`({"a": 1}, ("a",), 1)`**: This test case checks if `access_nested_map` correctly retrieves the value associated with the key `"a"` from a simple dictionary `{"a": 1}`. The expected output is `1`.

* **`({"a": {"b": 2}}, ("a",), {"b": 2})`**: This test case examines the scenario where the value associated with the key `"a"` is another dictionary `{"b": 2}`. The test ensures that the function returns this inner dictionary when the path is just `("a",)`.

* **`({"a": {"b": 2}}, ("a", "b"), 2)`**: This test case goes one level deeper into the nested dictionary. It verifies that `access_nested_map` correctly retrieves the value `2` associated with the key `"b"` within the dictionary accessed by the key `"a"`. The path used is `("a", "b")`.

The `assertEqual` method from the `unittest` framework is used within the `test_access_nested_map` method to compare the actual output of the `access_nested_map` function with the expected output for each test case. If the outputs do not match, the test will fail, indicating an issue with the `access_nested_map` function.

## Documentation

This project follows Python's documentation standards. Each module, class, and function includes a docstring explaining its purpose. You can view these docstrings using the `help()` function or by accessing the `__doc__` attribute.

## Code Style

The Python code in this project adheres to the `pycodestyle` (PEP 8) style guide.
