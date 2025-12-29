# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Martín Barranca Rábago

"""Validation decorators for argument type and value checking.

This module provides a decorator-based validation system to reduce code
duplication across the codebase. Validators are composable and generate
consistent error messages.

Example usage:
    @validate(
        string=String(),
        categories=NonEmptyIterable(),
        width=PositiveInt(),
    )
    def my_function(string, categories, width=80):
        ...
"""

from collections.abc import Collection, Iterable
from functools import wraps
from inspect import signature
from typing import Any


class Validator:
    """Base class for validators."""

    def validate(self, value: Any, name: str) -> None:
        """Validate the value. Raises TypeError or ValueError on failure."""
        raise NotImplementedError


class String(Validator):
    """Validates that the argument is a string.

    Args:
        non_empty: If True, also validates that the string is non-empty.
        single_char: If True, validates that the string is exactly one character.
    """

    def __init__(
        self,
        non_empty: bool = False,
        single_char: bool = False
    ) -> None:
        self.non_empty = non_empty
        self.single_char = single_char

    def validate(self, value: Any, name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"Argument '{name}' must be a string.")
        if self.single_char and len(value) != 1:
            raise ValueError(f"Argument '{name}' must be a single character.")
        if self.non_empty and not value:
            raise ValueError(f"Argument '{name}' must be a non-empty string.")


class Int(Validator):
    """Validates that the argument is an integer.

    Args:
        positive: If True, validates that the integer is > 0.
        non_negative: If True, validates that the integer is >= 0.
    """

    def __init__(
        self,
        positive: bool = False,
        non_negative: bool = False
    ) -> None:
        self.positive = positive
        self.non_negative = non_negative

    def validate(self, value: Any, name: str) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Argument '{name}' must be an integer.")
        if self.positive and value <= 0:
            raise ValueError(f"Argument '{name}' must be a positive integer.")
        if self.non_negative and value < 0:
            raise ValueError(
                f"Argument '{name}' must be a non-negative integer.")


class NonEmptyIterable(Validator):
    """Validates that the argument is a non-empty iterable."""

    def validate(self, value: Any, name: str) -> None:
        if not isinstance(value, Iterable):
            raise TypeError(f"Argument '{name}' must be an iterable.")
        if not value:
            raise ValueError(f"Argument '{name}' cannot be empty.")


class StringOrCollection(Validator):
    """Validates that the argument is a string or a collection of strings.

    Args:
        non_empty_items: If True, validates that all items are non-empty strings.
    """

    def __init__(self, non_empty_items: bool = False) -> None:
        self.non_empty_items = non_empty_items

    def validate(self, value: Any, name: str) -> None:
        if not isinstance(value, (str, Collection)):
            raise TypeError(
                f"Argument '{name}' must be a string or a collection.")
        if isinstance(value, Collection) and not isinstance(value, str):
            if not all(isinstance(x, str) for x in value):
                raise TypeError(f"All items in '{name}' must be strings.")
            if self.non_empty_items and any(not x for x in value):
                raise ValueError(
                    f"All items in '{name}' must be non-empty strings.")


def validate(**validators: Validator):
    """Decorator that validates function arguments using the provided validators.

    Args:
        **validators: Mapping of parameter names to Validator instances.

    Returns:
        A decorator that wraps the function with validation logic.

    Example:
        @validate(
            text=String(),
            width=Int(positive=True),
        )
        def wrap_text(text, width=80):
            ...
    """
    def decorator(func):
        sig = signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Bind arguments to parameter names
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            # Validate each argument that has a validator
            for param_name, validator in validators.items():
                if param_name in bound.arguments:
                    validator.validate(bound.arguments[param_name], param_name)

            return func(*args, **kwargs)

        return wrapper
    return decorator
