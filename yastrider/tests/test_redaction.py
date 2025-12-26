import pytest

from yastrider.redaction import redact_text


def test_basic_redaction_literal():
    text = "My password is secret"
    out = redact_text(text, "secret")
    assert out == "My password is XXXXXX"


def test_multiple_redactions():
    text = "foo bar baz"
    out = redact_text(text, ["foo", "baz"])
    assert out == "XXX bar XXX"


def test_case_insensitive_redaction():
    text = "Secret SECRET secret"
    out = redact_text(text, "secret", case_insensitive=True)
    assert out == "XXXXXX XXXXXX XXXXXX"


def test_case_sensitive_redaction():
    text = "Secret SECRET secret"
    out = redact_text(text, "secret", case_insensitive=False)
    assert out == "Secret SECRET XXXXXX"


def test_fixed_redaction_length():
    text = "123-45-6789"
    out = redact_text(text, r"\d+", assume_regex=True, fixed_redaction_length=4)
    assert out == "XXXX-XXXX-XXXX"


def test_custom_redaction_char():
    text = "token=abc123"
    out = redact_text(text, "abc123", redaction_char="*")
    assert out == "token=******"


def test_regex_redaction():
    text = "Order IDs: A-123, B-456"
    out = redact_text(text, r"[A-Z]-\d+", assume_regex=True)
    assert out == "Order IDs: XXXXX, XXXXX"


def test_redaction_order_longest_first():
    text = "foobar"
    out = redact_text(text, ["foo", "foobar"])
    assert out == "XXXXXX"


def test_empty_text_returns_empty():
    assert redact_text("", "x") == ""


def test_invalid_text_type():
    with pytest.raises(TypeError):
        redact_text(123, "x")


def test_invalid_redacted_collection_item():
    with pytest.raises(TypeError):
        redact_text("test", ["ok", 123])


def test_empty_redacted_string_raises():
    with pytest.raises(ValueError):
        redact_text("test", "")


def test_redaction_char_must_be_single_char():
    with pytest.raises(ValueError):
        redact_text("test", "t", redaction_char="XX")


def test_negative_fixed_length_raises():
    with pytest.raises(ValueError):
        redact_text("test", "t", fixed_redaction_length=-1)
