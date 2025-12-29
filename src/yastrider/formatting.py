# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Martín Barranca Rábago

import re
from textwrap import TextWrapper

from yastrider.char_removal import (
    remove_extra_spaces,
)
from yastrider._validation import validate, String, Int


@validate(
    text=String(),
    width=Int(positive=True),
    tab_size=Int(positive=True),
)
def wrap_text(
    text: str,
    width: int = 80,
    collapse_multiple_tabs: bool = False,
    collapse_extra_spaces: bool = True,
    expand_tabs: bool = True,
    preserve_paragraphs: bool = True,
    preserve_line_breaks: bool = True,
    preserve_tabs: bool = False,
    tab_size: int = 4,
    wrap_words: bool = True
) -> str:
    """Wraps and formats text to a given line width, with (optional) whitespace
    normalization and paragraph preservation.

    This function normalizes line endings and optionally collapses redundant
    whitespace before applying line wrapping.

    Both word-aware wrapping (default) and hard-wrapping (ignoring word
    boundaries) are supported.

    Line endings are normalized to `\\n` (removing "windows-like" `\\r\\n`
    sequences). Paragraph boundaries are preserved. Paragraphs are defined as
    blocks of text separated by one or more blank lines.

    This function implements word-aware wrapping using `textwrap.TextWrapper`
    with sensible defaults.

    When `preserve_paragraphs` is False, all line breaks are collapsed into
    single spaces before wrapping.

    Args:
        text (str):
            The input text to be wrapped.
        width (int, optional):
            Maximum line width. Must be a positive integer.
            Default: 80.
        collapse_multiple_tabs (bool, optional):
            Whether to collapse consecutive tab characters into a single tab
            during whitespace normalization.
            Default: False.
        collapse_extra_spaces (bool, optional):
            Whether to collapse redundant spaces before wrapping.
            Default: True.
        expand_tabs (bool, optional):
            Whether to expand tab characters to spaces when wrapping text.
            Default: True.
        preserve_paragraphs (bool, optional):
            Whether to preserve paragraph boundaries. If False, all new-line
            characters are collapsed into single spaces, effectively creating
            a single logical paragraph.
            Default: True.
        preserve_line_breaks (bool, optional):
            Whether to preserve line breaks during whitespace normalization.
            This affects preprocessing only.
            Default: True.
        preserve_tabs (bool, optional):
            Whether to preserve tab characters during whitespace normalization.
            Default: False.
        tab_size (int, optional):
            Number of spaces to which a tab character expands when
            `expand_tabs` is True.
            Default: 4.
        wrap_words (bool, optional):
            If True, wrapping respects word boundaries. If False, text is
            hard-wrapped at the specified width, ignoring word boundaries.
            Default: True.

    Raises:
        TypeError:
            If any argument has invalid types.
        ValueError:
            If `width` or `tab_size` are not positive integers.

    Returns:
        str:
            The wrapped and formatted text.
    """
    # Cross-parameter validation (cannot be handled by decorator):
    if tab_size >= width:
        raise ValueError("Argument `tab_size` cannot be larger than `width`.")
    # Defensive casting:
    wrap_words = bool(wrap_words)
    preserve_paragraphs = bool(preserve_paragraphs)
    collapse_extra_spaces = bool(collapse_extra_spaces)
    expand_tabs = bool(expand_tabs)
    preserve_line_breaks = bool(preserve_line_breaks)
    preserve_tabs = bool(preserve_tabs)
    collapse_multiple_tabs = bool(collapse_multiple_tabs)
    # Early return for empty input:
    if not text:
        return text
    # Normalize new-lines
    text = re.sub(r"\r\n?", r"\n", text, flags=re.MULTILINE|re.UNICODE)

    if collapse_extra_spaces:
        text = remove_extra_spaces(
            text,
            preserve_newlines=preserve_line_breaks,
            preserve_tabs=preserve_tabs,
            collapse_multiple_tabs=collapse_multiple_tabs
        )

    # Collapse paragraph separators into simple new lines:
    if not preserve_paragraphs:
        text = re.sub(r"\s*\n+\s*", " ", text)

    # Hard-wrap: Ignore word boundaries
    if not wrap_words:
        def _hard_wrap(s: str) -> str:
            return '\n'.join(s[i:(i + width)] for i in range(0, len(s), width))

        if preserve_paragraphs:
            return '\n\n'.join(
                _hard_wrap(p)
                for p in re.split(r"\n\s*\n", text, flags=re.MULTILINE)
            )
        else:
            return _hard_wrap(text)

    # Default wrap
    wrapper = TextWrapper(
        width=width,
        expand_tabs=expand_tabs,
        tabsize=tab_size,
        replace_whitespace=False,
        drop_whitespace=False,
        break_long_words=True,
        break_on_hyphens=True
    )
    if preserve_paragraphs:
        return '\n\n'.join(
            wrapper.fill(p)
            for p in re.split(r"\n\s*\n", text, flags=re.MULTILINE)
        )
    return wrapper.fill(text)
