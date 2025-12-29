# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Martín Barranca Rábago

import re
from functools import lru_cache
from unicodedata import normalize

from yastrider.constants import VALID_FORMS, VALID_FORMS_SET
from yastrider._validation import validate, String


@validate(char=String(single_char=True))
@lru_cache(maxsize=256)
def is_printable_character(
    char: str
) -> bool:
    """Detects if a character is printable or not.

    This function relies on 'str.is_printable()' function for convenience; it
    just validates that the string is a single character.

    Args:
        char (str): Character to be evaluated

    Raises:
        TypeError: If the argument is not of type 'str'.
        ValueError: If the argument is a string of length different than 1.

    Returns:
        bool: 'True' if the character is printable; 'False' otherwise.
    """
    return char.isprintable()


@validate(
    char=String(single_char=True),
    normalization_form=String(),
)
@lru_cache(maxsize=256)
def percent_encode(
    char: str,
    force: bool = False,
    normalization_form: VALID_FORMS = 'NFKD'
) -> str:
    """Percent-encode a character.

    The character will be first utf-8 encoded and then it will be
    percent-encoded.
    If 'force' is False, only non-ASCII characters will be percent-encoded.
    Notice that the result may be affected by the normalization form.
    Normalization is applied only when the character will be percent-encoded.

    References:
        - https://docs.python.org/3/library/unicodedata.html

    Args:
        char (str):
            Character to encode.
        force (bool, optional):
            If 'False', only non-ASCII characters will be percent-encoded.
            If 'True', the character will be forcefully percent-encoded,
            whether it's ASCII or not.
            Default: False.
        normalization_form (Literal['NFC', 'NFD', 'NFKC', 'NFKD'], optional):
            Defines which Unicode normalization form will be used to encode the
            character; this may alter the result.
            Default: 'NFKD'

    Raises:
        TypeError: If the argument is not of type 'str'.
        ValueError: If the argument is a string of length different than 1.

    Returns:
        str:
            If the character is ASCII (and 'force' is false), returns the
            character; otherwise, it will return the percent-code of the
            character. Notice that this may generate multiple percent-codes.
    """
    if normalization_form not in VALID_FORMS_SET:
        valid_forms = ', '.join(
            "'%s" % f for f in sorted(VALID_FORMS_SET))
        raise ValueError(
            f"Invalid normalization form; must be one of the "
            f"following: {valid_forms}")
    force = bool(force)
    if char.isascii() and not force:
        return char
    return ''.join(
        f"%{b:02X}"
        for b in normalize(
            normalization_form, char
        ).encode('utf-8'))


@validate(pattern=String(non_empty=True))
@lru_cache(maxsize=128)
def regex_pattern(
    pattern: str,
    unicode: bool = True,
    case_insensitive: bool = False,
    multi_line: bool = False,
    verbose: bool = False
) -> re.Pattern:
    """Returns a compiled re.Pattern object.

    This is a convenience function, meant only to explicitly generate compiled
    regular expressions. The flags for the regular expression are explicitly
    exposed as boolean arguments for ease. Only the most relevant flags are
    exposed; if you need to use other flags (e.g. re.DOTALL, re.ASCII), use
    're.compile()' directly.

    References:
        - https://docs.python.org/3/library/re.html

    Args:
        pattern (str):
            Regular expression string pattern
        unicode (bool, optional):
            Sets the 'U' (assume Unicode) flag.
            Default: True
        case_insensitive (bool, optional):
            Sets the 'I' (ignore case) flag.
            Default: False
        multi_line (bool, optional):
            Sets the 'M' (multi line) flag. This affects what '^' and '$'
            match.
            Default: False
        verbose (bool, optional):
            Sets the 'X' (verbose) flag. This allows to write regular
            expressions in a more legible way and allows comments
            (prepended by '#').
            Default: False.


    Returns:
        re.Pattern: Compiled regular expression pattern
    """
    flags = 0
    if unicode:
        flags |= re.UNICODE
    if case_insensitive:
        flags |= re.IGNORECASE
    if multi_line:
        flags |= re.MULTILINE
    if verbose:
        flags |= re.VERBOSE
    return re.compile(pattern, flags=flags)
