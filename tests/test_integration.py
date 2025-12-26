from yastrider.redaction import redact_text
from yastrider.formatting import wrap_text


def test_wrap_then_redact_pipeline():
    text = "My email is test@example.com and it should not leak."
    wrapped = wrap_text(text, width=20)
    redacted = redact_text(
        wrapped,
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+",
        assume_regex=True
    )
    assert "@" not in redacted


def test_redact_then_wrap_pipeline():
    text = "SSN: 123-45-6789 should be hidden"
    redacted = redact_text(
        text,
        r"\d{3}-\d{2}-\d{4}",
        assume_regex=True
    )
    wrapped = wrap_text(redacted, width=15)
    assert "123" not in wrapped
