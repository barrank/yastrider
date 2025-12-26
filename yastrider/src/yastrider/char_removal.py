# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Martín Barranca Rábago

import re
from collections.abc import Iterable
from unicodedata import category

from yastrider.constants import (
    ALLOWED_NON_PRINTABLE_CHARACTERS,
)
from yastrider.utils import (
    is_printable_character,
)


def remove_chars_by_category(
    string: str,
    categories: Iterable[str] = {'C', 'P', 'S'}
) -> str:
    """Removes characters by Unicode category.

    This function allows the removal for categories 'C' (control characters),
    'P' (punctuation characters) or 'S' (symbol characters).

    Args:
        string (str):
            String on which removal will be applied.
        categories (Iterable[str], optional):
            Iterable of categories to be removed from the string.
            Must contain only 'C', 'P' or 'S'.
            Default: {'C', 'P', 'S'}.

    Raises:
        TypeError:
            If any inputs are not of the required types.
        ValueError:
            If there are no categories to be removed, or if categories are
            invalid.

    Returns:
        str:
            String without characters of the specified categories.
    """
    # Validation
    if not isinstance(string, str):
        raise TypeError("Argument 'string' must be a string.")
    if not isinstance(categories, Iterable):
        raise TypeError("Argument 'categories' must be an iterable.")
    if not categories:
        raise ValueError("No categories specified for removal.")
    # Defensive casting (it's here to deduplicate entries and ease both
    # validation and further usage)
    categories = set(categories)
    # Category validation:
    if any(cat not in {'C', 'P', 'S'} for cat in categories):
        raise ValueError(
            "Invalid categories specified. Categories must be one (or more) "
            "of the following: 'C', 'P', 'S'.")
    # Early return for empty strings:
    if not string:
        return string
    # Keep all characters not belonging to the specified categories:
    return ''.join(
        char for char in string
        if not any(
            category(char).startswith(cat)
            for cat in categories)
    )


def remove_extra_spaces(
    string: str,
    preserve_newlines: bool = True,
    preserve_tabs: bool = False,
    collapse_multiple_tabs: bool = False
) -> str:
    """Replaces white space sequences with single spaces (optionally preserving
    tabs and newlines), and removes any leading or trailing white spaces.

    Args:
        string (str):
            String on which the extra spaces removal will be applied.
        preserve_newlines (bool, optional):
            If True, each new line is stripped of extra spaces; if False, new
            line characters (\\n) are replaced by spaces. Keep in mind that
            replacing new-line characters will make this function return a one
            line string, even if the string is multi-line.
            Default: True.
        preserve_tabs (bool, optional):
            If True, tabulations will be preserved; if False, tabs will be
            treated as spaces.
            Default: False.
        collapse_multiple_tabs (bool, optional):
            If True, sequences of multiple tabs will be collapsed into a single
            tab. Be aware that if 'preserve_tabs' is False, setting this
            argument to False is irrelevant.
            Default: False.

    Raises:
        TypeError:
            If input is not of a valid type.

    Returns:
        str:
            String without any extra spaces.
    """
    # Validation
    if not isinstance(string, str):
        raise TypeError("Argument 'string' must be a string.")
    # Defensive casting:
    preserve_newlines = bool(preserve_newlines)
    preserve_tabs = bool(preserve_tabs)
    collapse_multiple_tabs = bool(collapse_multiple_tabs)
    # Early return for empty strings:
    if not string:
        return string
    # Build the regular expression pattern for substitution:
    if preserve_tabs:
        pattern = r"[^\S\t]+"
    else:
        pattern = r"\s+"
    # Process the string:
    if preserve_tabs and collapse_multiple_tabs:
        string = re.sub(r"\t+", r"\t", string)
    if preserve_newlines:
        string = '\n'.join(
            re.sub(pattern, ' ', line).strip() for line in string.split('\n')
        )
    else:
        string = re.sub(pattern, ' ', string).strip()
    return string


def remove_non_printable_characters(
    string:str
) -> str:
    """Removes all non-printable characters from the string.

    This function relies on 'yastrider.is_printable_character()'; it also
    checks if a character in the string belongs to
    'ALLOWED_NON_PRINTABLE_CHARACTERS' as a precaution.

    Args:
        string (str):
            The string on which character removal will be applied.

    Raises:
        TypeError:
            If the input is of an invalid type.

    Returns:
        str:
            The string with all non-printable characters removed.
    """
    # Validation
    if not isinstance(string, str):
        raise TypeError("Argument 'string' must be a string.")
    # Early return for empty strings:
    if not string:
        return string
    # Keep only printable characters.
    # Explicitly check for characters in ALLOW_NON_PRINTABLE_CHARACTERS (as a
    # precaution):
    return ''.join(
        char for char in string
        if (is_printable_character(char) or
            char in ALLOWED_NON_PRINTABLE_CHARACTERS)
    )
