import re

from yastrider.utils import regex_pattern


def test_basic_pattern():
    pat = regex_pattern("abc")
    assert pat.search("xxabcxx")


def test_ignore_case():
    pat = regex_pattern("abc", case_insensitive=True)
    assert pat.search("ABC")


def test_multiline():
    pat = regex_pattern("^abc", multi_line=True)
    assert pat.search("x\nabc")


def test_unicode_enabled():
    pat = regex_pattern(r"\w+")
    assert pat.search("áéíóú")
