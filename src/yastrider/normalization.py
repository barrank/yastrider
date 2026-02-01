# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Martín Barranca Rábago

import re
import warnings
from collections.abc import Collection
from typing import cast
from unicodedata import (
    category,
    combining,
    normalize,
)

from yastrider.constants import (
    ALLOWED_NON_PRINTABLE_CHARACTERS,
    INTERNAL_TOKEN_MARKER,
    VALID_FORMS, VALID_FORMS_SET,
    VALID_FORMS_DIACRITIC_REMOVAL, VALID_FORMS_DIACRITIC_REMOVAL_SET,
    UNICODE_QUOTE_MAP,
)
from yastrider.utils import (
    is_printable_character,
    percent_encode,
    regex_pattern,
)
from yastrider.char_removal import (
    remove_non_printable_characters,
)
from yastrider.diacritics_processing import (
    strip_diacritics,
)
from yastrider._validation import validate, String


class _TokenManager:
    """Manages tokenization and restoration of preserved characters.

    This class encapsulates the logic for replacing characters with tokens
    during text normalization, allowing those characters to be preserved
    through transformations that would otherwise modify them.
    """

    def __init__(
        self,
        preserve: frozenset[str],
        use_non_printable_marker: bool = True
    ) -> None:
        """Initialize the token manager.

        Args:
            preserve: Set of characters to preserve during normalization.
            use_non_printable_marker: If True, use a non-printable character
                prefix for safer tokenization.
        """
        self._use_non_printable_marker = use_non_printable_marker
        self._token_map: dict[str, str] = {
            self._tokenize(c): c for c in preserve
        }
        self._pattern_chars = regex_pattern(
            '|'.join(re.escape(c) for c in preserve)
        )
        self._pattern_tokens = regex_pattern(
            '|'.join(re.escape(t) for t in self._token_map)
        )

    def _tokenize(self, char: str) -> str:
        """Create a unique token for a character."""
        prefix = '__preserved_'
        if self._use_non_printable_marker:
            prefix = f"{INTERNAL_TOKEN_MARKER}{prefix}"
        return f"{prefix}{percent_encode(char)}__"

    def _replace_with_token(self, match: re.Match) -> str:
        """Replacement callback: character -> token."""
        return self._tokenize(match.group(0))

    def _replace_with_char(self, match: re.Match) -> str:
        """Replacement callback: token -> character."""
        return self._token_map[match.group(0)]

    def tokenize_text(self, text: str) -> str:
        """Replace all preserved characters with their tokens."""
        return self._pattern_chars.sub(self._replace_with_token, text)

    def restore_text(self, text: str) -> str:
        """Restore all tokens back to their original characters."""
        return self._pattern_tokens.sub(self._replace_with_char, text)


def _normalize_hyphens(text: str) -> str:
    """Normalizes Unicode hyphens (category `Pd`) and `U+2212` to ASCII 
    hyphens.

    Args:
        text (str):
            Text on which hyphens will be normalized.

    Returns:
        Text with all Unicode hyphens replaced by `-` (ASCII minus sign).
    """
    if not text:
        return text
    return ''.join(
        '-' if (
            category(c) == 'Pd' or c == '\u2212'
        ) else c
        for c in text
    )


def _normalize_quotes(text: str) -> str:
    """Normalizes Unicode quotation marks to ASCII.

    Args:
        text (str):
            Text to be normalized.
    
    Returns:
        Text with Unicode quotation marks replaced with ASCII quotation marks.
    """
    if not text:
        return text
    return ''.join(
        UNICODE_QUOTE_MAP.get(c, c) 
        for c in text
    )


@validate(text=String())
def normalize_text(
    text: str,
    remove_diacritics: bool = True,
    preserve: Collection[str]|None = None,
    strip_non_printable_characters: bool = True,
    normalization_form: VALID_FORMS = 'NFKD',
    use_non_printable_for_token: bool = True
) -> str:
    """Applies Unicode normalization and optional diacritics removal.

    A set of preserved characters can be specified; this is useful if you need
    to selectively remove diacritics (i.e. you want to keep some of them).

    In any case, the function will apply Unicode normalization as a last step
    before returning the result.

    If 'preserve' is a non-empty collection of characters and
    'remove_diacritics' is True, an internal tokenization process will be
    applied to each character to be preserved. If 'use_non_printable_for_token'
    is True (default), a non-printable character will be used for safe
    tokenization. Notice that collisions are extremely unlikely but
    theoretically possible. It is highly recommended that non-printable
    character removal is performed before normalization. This can be done
    setting 'strip_non_printable_characters' to True (default).

    Notice that diacritic marks removal require the use of the *NFD* or *NFKD*
    normalization forms. If you try to use any other normalization form, a
    `ValueError` will be raised.

    Unicode normalization is applied after token restoration to ensure
    clean and canonical output.

    If you want to recombine diacritic marks, it is highly recommended that you
    pass the string twice through this function: the first one using 'NFKD' (or
    'NFD') for diacritic removal (with optional preservation of selected
    characters), and the second one using 'NFKC' (or 'NFC') for recombination.
    For example:

    ```python
    normalize_text(
        normalize_text(
            "León Niño",
            preserve=['ñ'],
            remove_diacritics=True,
            normalization_form='NFKD'
        ),
        remove_diacritics=False,
        normalization_form='NFKC'
    )
    ##> 'Leon Niño'
    ```

    Args:
        text (str):
            Text to be normalized.
        remove_diacritics (bool, optional):
            Whether to remove diacritics or not.
            Default: True.
        preserve (Collection[str] | None, optional):
            Iterable of characters to be preserved in 'text'. Characters in
            'preserve' are validated against the original input string, prior
            to any normalization or filtering.
            Default: None.
        strip_non_printable_characters (bool, optional):
            If True, non-printable characters will be removed before
            normalization and (optional) character preservation.
            Default: True
        normalization_form (VALID_FORMS, optional):
            Unicode normalization form to be applied. Must be one of the
            following: 'NFC', 'NFD', 'NFKC', 'NFKD'. Notice that if you want
            to remove diacritics, 'NFD' and 'NFKD' are the *only* forms that
            will allow you to do it. For more information, please check
            https://docs.python.org/3/library/unicodedata.html.
            Default: 'NFKD'.
        use_non_printable_for_token (bool, optional):
            If True, a non-printable character ("\\uE000") will be used as
            part of the tokenization of preserved characters. If the character
            is present in 'text' before tokenization, a warning will be issued.
            Default: True.

    Raises:
        TypeError:
            If any argument is of an invalid type.
        ValueError:
            If any argument has invalid values (invalid normalization form or
            invalid characters to be preserved)

    Returns:
        str:
            Normalized text, with preserved characters (if provided).
    """
    if normalization_form not in VALID_FORMS_SET:
        valid_forms = ', '.join(
            "'%s" % f for f in sorted(VALID_FORMS_SET))
        raise ValueError(
            f"Invalid normalization form; must be one of the "
            f"following: {valid_forms}")
    if preserve is None:
        preserve = []
    if isinstance(preserve, str):
        preserve = list(preserve)
    if any(not isinstance(x, str) for x in preserve):
        raise TypeError("Argument 'preserve' must contain only strings.")
    if any(len(x) != 1 for x in preserve):
        raise ValueError("Items in 'preserve' must be single characters.")
    if any(combining(x) for x in preserve):
        raise ValueError("Combining characters are not allowed in 'preserve'.")
    # Defensive casting:
    remove_diacritics = bool(remove_diacritics)
    use_non_printable_for_token = bool(use_non_printable_for_token)
    strip_non_printable_characters = bool(strip_non_printable_characters)
    # Form validation for diacritic removal:
    if (
        remove_diacritics and
        normalization_form not in VALID_FORMS_DIACRITIC_REMOVAL_SET
    ):
        valid_forms = ', '.join(
            "'%s" % f for f in sorted(VALID_FORMS_DIACRITIC_REMOVAL_SET))
        raise ValueError(
            f"Normalization form '{normalization_form}' doesn't decompose "
            f"combining marks (diacritics); if you want to remove diacritics, "
            f"please use one of the following normalization forms: "
            f"{valid_forms}")
    # Early return for empty strings:
    if not text:
        return text
    # Create a set of characters in 'text' for further usage:
    original_chars = set(text)
    # Optionally remove non-printable characters:
    if strip_non_printable_characters:
        text = remove_non_printable_characters(text)
    chars_in_text = set(text)
    # Ignore any characters in 'preserve' that are not present in the input
    # text
    preserve = frozenset(x for x in preserve if x in chars_in_text)
    # Check if there are any non-printable characters in 'text'.
    # This is done to prevent undesirable output. Notice that if non-printable
    # characters are detected, only warnings will be issued (not exceptions).
    # Also it is worth to notice that if 'strip_non_printable_characters' is
    # True, a warning will be issued if and only if there are non-printable
    # remnants in the string.
    non_printable_chars = {
        c for c in chars_in_text
        if not is_printable_character(c)
        and c not in ALLOWED_NON_PRINTABLE_CHARACTERS
    }
    if non_printable_chars:
        warnings.warn(
            "The original text contains non-printable characters. "
            "It is highly recommended removing non-printable characters "
            "before normalizing. "
            "Consider using 'remove_non_printable_characters()'.",
            UserWarning)
    if not preserve:
        if remove_diacritics:
            return strip_diacritics(
                text,
                # 'normalization_form' is defensively cast to match valid forms
                # for diacritic stripping:
                normalization_form=cast(
                    VALID_FORMS_DIACRITIC_REMOVAL,
                    normalization_form))
        return normalize(normalization_form, text)

    # Check if the INTERNAL_TOKEN_MARKER is present in 'text'.
    # A warning will be issued if it's present.
    if use_non_printable_for_token and INTERNAL_TOKEN_MARKER in original_chars:
        warnings.warn(
            "Internal token marker is present in 'text'. "
            "Be aware that this may lead to unexpected token substitution "
            "and incorrect preservation of characters. "
            "It is highly recommended to remove non-printable characters "
            "before normalizing. "
            "Consider using 'remove_non_printable_characters()'.",
            UserWarning)

    # Use TokenManager to handle character preservation:
    token_manager = _TokenManager(preserve, use_non_printable_for_token)
    # Replace all preserved characters with their tokens:
    ans = token_manager.tokenize_text(text)
    # Remove diacritics (except for those to be preserved):
    if remove_diacritics:
        ans = strip_diacritics(
            ans,
            # 'normalization_form' is defensively cast to match valid forms for
            # diacritic stripping:
            normalization_form=cast(
                VALID_FORMS_DIACRITIC_REMOVAL,
                normalization_form))
    # Restore preserved characters:
    ans = token_manager.restore_text(ans)
    # Normalize the processed string before returning it.
    ans = normalize(normalization_form, ans)
    return ans


@validate(
    string=String(),
    fallback_char_for_non_ascii=String(),
)
def to_ascii(
    string: str,
    remove_diacritics_before_encoding: bool = True,
    normalize_hyphens: bool = True,
    normalize_quotes: bool = True,
    percent_code_non_ascii: bool = True,
    fallback_char_for_non_ascii: str = '?',
    normalization_form: VALID_FORMS = 'NFKD'
) -> str:
    """Converts a string to an ASCII-safe string.
    By default, non-ASCII characters are percent encoded.

    Args:
        string (str):
            String to be converted into ASCII-safe
        remove_diacritics_before_encoding (bool, optional):
            If True, diacritics will be removed from the string before
            processing.
            Default: True.
        normalize_hyphens (bool, optional):
            If True, Unicode hyphens (category `Pd`) and the Unicode minus 
            sign (`U+2212`) will be replaced by the ASCII minus sign.
            Default: True.
        normalize_quotes (bool, optional):
            If True, Unicode quotation marks will be normalized to ASCII 
            quotation marks.
            Default: True.
        percent_code_non_ascii (bool, optional):
            If True, any non-ASCII characters (after optional diacritic
            stripping) will be percent encoded.
            Default: True.
        fallback_char_for_non_ascii (str, optional):
            If 'percent_code_for_non_ascii' is False, any non-ASCII characters
            (after optional diacritic stripping, hyphen normalization and quote normalization) will be replaced by this
            character. Of course, this character must be ASCII-safe.
            Defaults to '?'.
        normalization_form (VALID_FORMS, optional):
            Unicode normalization form to be applied before processing.
            If you want to remove diacritics, you *must* use 'NFD' or 'NFKD'
            normalization forms.
            For more information, please check
            https://docs.python.org/3/library/unicodedata.html.
            Defaults to 'NFKD'.

    Raises:
        TypeError:
            If any argument is of an invalid type.
        ValueError:
            If an invalid normalization form is provided, or if a non-ASCII
            fallback character is provided.

    Returns:
        str:
            ASCII-safe version of the input string.
    """
    # Domain-specific validation (cannot be handled by decorator)
    if normalization_form not in VALID_FORMS_SET:
        valid_forms = ', '.join(
            "'%s" % f for f in sorted(VALID_FORMS_DIACRITIC_REMOVAL_SET))
        raise ValueError(
            f"Invalid normalization form; must be one of the "
            f"following: {valid_forms}")
    if not fallback_char_for_non_ascii.isascii():
        raise ValueError(
            "'fallback_char_for_non_ascii' must be an ASCII string.")
    if len(fallback_char_for_non_ascii) != 1:
        warnings.warn(
            "It is highly recommended that 'fallback_char_for_non_ascii' is a "
            "single character. Avoid empty strings or multi-char sequences.",
            UserWarning)
    # Defensive casting:
    remove_diacritics_before_encoding = bool(remove_diacritics_before_encoding)
    percent_code_non_ascii = bool(percent_code_non_ascii)
    normalize_hyphens = bool(normalize_hyphens)
    normalize_quotes = bool(normalize_quotes)

    # Form validation for diacritic removal:
    if (
        remove_diacritics_before_encoding and
        normalization_form not in VALID_FORMS_DIACRITIC_REMOVAL_SET
    ):
        valid_forms = ', '.join(
            "'%s" % f for f in sorted(VALID_FORMS_DIACRITIC_REMOVAL_SET))
        raise ValueError(
            f"Normalization form '{normalization_form}' doesn't decompose "
            f"combining marks (diacritics); if you want to remove diacritics, "
            f"please use one of the following normalization forms: "
            f"{valid_forms}")
    # Early return for empty strings:
    if not string:
        return string
    if remove_diacritics_before_encoding:
        ans = strip_diacritics(
            string,
            # 'normalization_form' is defensively cast to match valid forms for
            # diacritic stripping:
            normalization_form=cast(
                VALID_FORMS_DIACRITIC_REMOVAL,
                normalization_form))
    else:
        ans = normalize(normalization_form, string)
    
    if normalize_hyphens:
        ans = _normalize_hyphens(ans)
    
    if normalize_quotes:
        ans = _normalize_quotes(ans)

    if ans.isascii():
        return ans
    if not percent_code_non_ascii:
        return ''.join(
            char if char.isascii() else fallback_char_for_non_ascii
            for char in ans)
    return ''.join(
        percent_encode(
            char,
            force=False,
            normalization_form=normalization_form)
        for char in ans)
