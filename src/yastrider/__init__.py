# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Martín Barranca Rábago

"""yastrider: Yet another string tidier

This package provides dependency-free utilities for string tidying tasks.

Features:

- Apply Unicode normalization with sensible default parameters.
- Strip diacritics with optional preservation of selected ones.
- Clean whitespace, optionally keeping tabs.
- Remove non-printable characters from the string.
- Redact sensitive words or strings.
- Convert to ASCII, with optional percent-encoding.
- Wrap text neatly to a fixed width, with word and paragraph control

Every function has comprehensive docstrings for reference.
"""

from .version import __version__
from .char_removal import (
    remove_chars_by_category,
    remove_extra_spaces,
    remove_non_printable_characters
)
from .diacritics_processing import (
    strip_diacritics,
)
from .formatting import (
    wrap_text,
)
from .normalization import (
    normalize_text,
    to_ascii,
)
from .redaction import (
    redact_text,
)


__all__ = [
    "__version__",
    "normalize_text",
    "remove_chars_by_category",
    "remove_extra_spaces",
    "remove_non_printable_characters",
    "redact_text",
    "strip_diacritics",
    "to_ascii",
    "wrap_text",
]
