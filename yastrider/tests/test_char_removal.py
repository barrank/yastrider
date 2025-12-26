import pytest

from yastrider.char_removal import remove_extra_spaces


def test_basic_space_collapse():
    assert remove_extra_spaces("a   b") == "a b"


def test_preserve_newlines():
    text = "a   b\nc    d"
    out = remove_extra_spaces(text, preserve_newlines=True)
    assert "\n" in out


def test_remove_newlines():
    text = "a   b\nc    d"
    out = remove_extra_spaces(text, preserve_newlines=False)
    assert "\n" not in out


def test_preserve_tabs():
    text = "a\t\tb"
    out = remove_extra_spaces(text, preserve_tabs=True)
    assert "\t" in out


def test_collapse_multiple_tabs():
    text = "a\t\t\tb"
    out = remove_extra_spaces(text, collapse_multiple_tabs=True)
    assert "\t\t" not in out
