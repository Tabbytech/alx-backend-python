#!/usr/bin/env python3
"""Defines utility functions for accessing nested data structures."""

from typing import Mapping, Sequence, Any, Tuple, Dict

def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Accesses a specific key in a nested dictionary using a list/tuple of keys.
    """
    for key in path:
        if not isinstance(nested_map, Mapping) or key not in nested_map:
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map

if __name__ == '__main__':
    nested = {"a": 1, "b": {"c": 3}}
    print(access_nested_map(nested, ("a",)))
    print(access_nested_map(nested, ("b", "c")))
    try:
        print(access_nested_map(nested, ("d",)))
    except KeyError as e:
        print(f"KeyError: {e}")
    try:
        print(access_nested_map(nested, ("b", "d")))
    except KeyError as e:
        print(f"KeyError: {e}")
