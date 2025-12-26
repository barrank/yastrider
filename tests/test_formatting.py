import pytest

from yastrider.formatting import wrap_text


def test_basic_wrap():
    text = "This is a simple sentence"
    out = wrap_text(text, width=10)
    assert all(len(line) <= 10 for line in out.splitlines())


def test_preserve_paragraphs():
    text = "Para one.\n\nPara two is longer."
    out = wrap_text(text, width=10, preserve_paragraphs=True)
    assert "\n\n" in out


def test_no_preserve_paragraphs():
    text = "Para one.\n\nPara two."
    out = wrap_text(text, width=10, preserve_paragraphs=False)
    assert "\n\n" not in out


def test_hard_wrap():
    text = "abcdefghij"
    out = wrap_text(text, width=3, tab_size=2, wrap_words=False)
    assert out == "abc\ndef\nghi\nj"


def test_preserve_line_breaks():
    text = "a   b\nc    d"
    out = wrap_text(
        text,
        collapse_extra_spaces=True,
        preserve_line_breaks=True,
        width=80
    )
    assert "\n" in out


def test_remove_line_breaks_during_normalization():
    text = "a   b\nc    d"
    out = wrap_text(
        text,
        collapse_extra_spaces=True,
        preserve_line_breaks=False,
        width=80
    )
    assert "\n" not in out


def test_tab_expansion():
    text = "a\tb"
    out = wrap_text(
        text,
        expand_tabs=True,
        tab_size=4,
        preserve_tabs=True,
        collapse_extra_spaces=False)
    assert out == "a   b"


def test_preserve_tabs():
    text = "a\t\tb"
    out = wrap_text(
        text,
        preserve_tabs=True,
        expand_tabs=False,
        collapse_extra_spaces=True,
        collapse_multiple_tabs=True
    )
    assert "\t" in out


def test_windows_newlines_normalized():
    text = "a\r\nb\r\nc"
    out = wrap_text(text)
    assert "\r" not in out
    assert out.count("\n") == 2


def test_invalid_width():
    with pytest.raises(ValueError):
        wrap_text("test", width=0)


def test_invalid_tab_size():
    with pytest.raises(ValueError):
        wrap_text("test", tab_size=0)


def test_tab_size_larger_than_width():
    with pytest.raises(ValueError):
        wrap_text("test", width=4, tab_size=8)
