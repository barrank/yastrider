# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Martín Barranca Rábago

from unicodedata import (
    combining,
    normalize,
)

from yastrider.constants import (
    VALID_FORMS_DIACRITIC_REMOVAL, VALID_FORMS_DIACRITIC_REMOVAL_SET,
)
from yastrider._validation import validate, String


@validate(string=String())
def strip_diacritics(
    string: str,
    normalization_form: VALID_FORMS_DIACRITIC_REMOVAL = 'NFKD'
) -> str:
    """Removes any combining (diacritic) characters from the string, using
    *NFD* or *NFKD* normalization forms.

    References:
        - https://docs.python.org/library/unicodedata.html

    Args:
        string (str):
            The string on which diacritic removal will be applied.
        normalization_form: Literal['NFD', 'NFKD']:
            Normalization form to be passed to unicodedata.normalize().
            Must be one of the following values: 'NFD', 'NFKD', which are the
            only forms that allow decomposition into main-and-combining
            characters. Any other value will raise an exception.
            Default: 'NFKD'

    Raises:
        TypeError:
            If any argument is of an invalid type.
        ValueError:
            If 'normalization_form' is invalid.

    Returns:
        str:
            String with combining marks (diacritics) removed.
    """
    # Domain-specific validation (cannot be handled by decorator)
    if normalization_form not in VALID_FORMS_DIACRITIC_REMOVAL_SET:
        valid_forms = ', '.join(
            "'%s" % f for f in sorted(VALID_FORMS_DIACRITIC_REMOVAL_SET))
        raise ValueError(
            f"Invalid normalization form; must be one of the "
            f"following: {valid_forms}")
    # Early return for empty strings:
    if not string:
        return string
    # Keep all characters that are not combining marks (i.e. diacritics):
    return ''.join(
        char for char in normalize(normalization_form, string)
        if not combining(char)
    )
