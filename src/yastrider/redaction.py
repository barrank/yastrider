# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Martín Barranca Rábago

import re
from collections.abc import Collection

from yastrider.utils import (
    regex_pattern
)


def redact_text(
    text: str,
    redacted: str|Collection[str],
    assume_regex: bool = False,
    case_insensitive: bool = True,
    redaction_char: str = 'X',
    fixed_redaction_length: int = 0
) -> str:
    """Redacts the text, replacing each occurrence of redacted strings with
    a sequence of `redaction_char`, with optional fixed length.

    This implementation relies on Python's `re` module. If `assume_regex` is
    False, redacted values are treated as literal strings and safely escaped
    before pattern compilation.

    Unicode matching is always enabled.

    Args:
        text (str):
            The text to be redacted.
        redacted (str | Collection[str]):
            A string or a collection (list, tuple, set) of strings that will
            be redacted. If it's a collection, it will be sorted in descending
            order by length. It must be either a non-empty string or a
            collection of non-empty strings. Empty strings will throw an error.
        assume_regex (bool, optional):
            If True, the redacted value(s) will be assumed to be (a) regular
            expression pattern(s); if false, redacted value(s) will be
            interpreted as literal strings.
            If this argument is True, flag 'M' (Multiline) will be activated.
            If case-insensitive redaction is needed, set `case_insensitive` to
            True; this will add the 'I' (case-insensitive) flag to the regex.
            Default: False.
        case_insensitive (bool, optional):
            Whether to redact the strings case-insensitively.
            Default: True.
        redaction_char (str, optional):
            Character that will be used to replace redacted strings. It must be
            a single character. If it's not a single character, it will raise
            an error.
            Default: 'X'.
        fixed_redaction_length (int, optional):
            Fixed length for the redaction. Must be a non-negative integer. If
            zero, the length of (each of) the redacted string(s) will be used.
            If negative, it will raise an error.
            Default: 0.

    Raises:
        TypeError:
            If any argument has an invalid type.
        ValueError:
            Invalid values for the arguments (empty `redacted` string(s),
            negative `fixed_redaction_length` or `redaction_char` not being a
            single character).

    Returns:
        str: The redacted text.
    """
    # Validation
    if not isinstance(text, str):
        raise TypeError("Argument 'text' must be a string.")
    if not isinstance(redacted, (str, Collection)):
        raise TypeError(
            "Argument 'redacted' must be a string or a collection.")
    if isinstance(redacted, Collection) and not isinstance(redacted, str):
        if not all(isinstance(x, str) for x in redacted):
            raise TypeError("All items in 'redacted' must be strings.")
        if any(not x for x in redacted):
            raise ValueError(
                "All items in 'redacted' must be non-empty strings.")
    if not isinstance(redaction_char, str):
        raise TypeError("Argument 'redaction_char' must be a string.")
    if len(redaction_char) != 1:
        raise ValueError(
            "Argument 'redaction_char' must be a single character.")
    if not isinstance(fixed_redaction_length, int):
        raise TypeError(
            "Argument 'fixed_redaction_length' must be an integer.")
    if fixed_redaction_length < 0:
        raise ValueError(
            "Argument 'fixed_redaction_length' must be a non-negative "
            "integer.")
    # Defensive casting:
    assume_regex = bool(assume_regex)
    case_insensitive = bool(case_insensitive)
    # Early return for empty input:
    if not text:
        return text
    # If 'redacted' is a single string, convert it to a list:
    if isinstance(redacted, str):
        redacted = [redacted]
    # Sort redacted by length (descending) to prevent undesirable collisions:
    redacted = sorted(redacted, key=len, reverse=True)

    def _redact_match(match: re.Match) -> str:
        length = fixed_redaction_length or len(match.group(0))
        return redaction_char * length

    for redacted_str in redacted:
        pattern = regex_pattern(
            redacted_str if assume_regex else re.escape(redacted_str),
            unicode=True,
            multi_line=assume_regex,
            case_insensitive=case_insensitive
        )
        text = pattern.sub(_redact_match, text)
    return text
