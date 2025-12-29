# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Martín Barranca Rábago

from typing import Literal, get_args

# Set of allowed non-printable characters.
# Although these characters may be "printable" (as per 'is_printable()'
# perspective), this set of characters will be used to ensure that they're not
# "accidentally" removed by functions.
ALLOWED_NON_PRINTABLE_CHARACTERS = {'\n', '\r', '\t'}

# Non-printable internal token marker.
# This will be used for safe tokenization of preserved characters
INTERNAL_TOKEN_MARKER = "\uE000"

# Allowed Unicode categories for removal:
#   C:  Control characters
#   P:  Punctuation characters
#   S:  Symbol characters
ALLOWED_UNICODE_CATEGORIES_FOR_REMOVAL = frozenset({'C', 'P', 'S'})

# Valid normalization forms.
VALID_FORMS = Literal['NFC', 'NFD', 'NFKC', 'NFKD']
# This set will be used for runtime validations
VALID_FORMS_SET = frozenset(get_args(VALID_FORMS))

# Valid normalization forms for diacritic removal; notice that this is a strict
# subset of 'VALID_FORMS'
VALID_FORMS_DIACRITIC_REMOVAL = Literal['NFD', 'NFKD']
VALID_FORMS_DIACRITIC_REMOVAL_SET = frozenset(
    get_args(VALID_FORMS_DIACRITIC_REMOVAL))


# Quotation marks normalization
UNICODE_QUOTE_MAP: dict[str, str] = {
    # Double quotes
    '“': '"',
    '”': '"',
    '„': '"',
    '«': '"',
    '»': '"',
    '″': '"',

    # Single quotes / apostrophes
    '‘': "'",
    '’': "'",
    '‚': "'",
    '′': "'",
}

