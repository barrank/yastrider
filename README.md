# `yastrider`: Yet-another string tidier

***A small, predictable, dependency-free toolkit for defensive string cleansing and tidying.***

[![PyPI version](https://img.shields.io/pypi/v/yastrider.svg)](https://pypi.org/project/yastrider/)
[![Python versions](https://img.shields.io/pypi/pyversions/yastrider.svg)](https://pypi.org/project/yastrider/)
[![License](https://img.shields.io/pypi/l/yastrider.svg)](https://pypi.org/project/yastrider/)


```python
from yastrider import normalize_text

normalize_text("Hëllõ World!")
## "Hello World!"
```

**`yastrider`** is a lightweight, dependency-free (Python standard library *only*), hassle-free toolkit for cleaning, tidying, normalizing, redacting, and formatting (basic wrapping and whitespace normalization) real-world strings in Python.

---
## `yastrider` at a glance

`yastrider` is a focused alternative built on top of `unicodedata` plus regular expressions for string tidying tasks.

It is:

- Predictable, lossy-by-design normalization. This means that for the same input you can expect the same output (using the same Python version and Unicode database), and that transformations are irreversible.
- Small, composable functions.
- **Not for NLP or localization**.

Behavior follows the Unicode version bundled with the running Python interpreter.

**Important:** All transformations provided by `yastrider` are *lossy* and *irreversible* by design.

### Typical use cases

- Cleaning user input before storing it into a database.
- Normalizing text for comparison or indexing.
- Defensive preprocessing in ETL pipelines.

---

## Quick start

Before you can use `yastrider`, you must install it with `pip`:

```bash
pip install yastrider
```

Once installed, you can start using it immediately:

**Step 1:** Import the functions you need:

```python
from yastrider import normalize_text
```

**Step 2:** Use it:

```python
normalize_text("Hëllõ World!")
## "Hello World!"
```

That's it! There's no step 3. No configurations. No hassle. No dependencies... Zero surprises!

It is highly recommended you read the full README before using `yastrider` to understand how to use it effectively.

---

## Why another string tidier toolkit?

I've found myself writing small functions again and again for tidying text, because there's no single library that fulfills all my use cases:

- I need to remove diacritics... but I need to keep some of them!
- I need to remove whitespaces... but sometimes I need to keep tabs!
- I need to remove non-printable characters... but I don't want to search what to remove first.

... and so on.

Many utilities I found were either heavy or relied on external packages, or solved part of my needs... and I need a simple, small and pure-Python solution. So... I ended up writing my own!

`yastrider` is a toolkit that will help you tidy strings, with sensible default values. Every function does one thing and strives to do it in an efficient and least-surprising way, allowing for decent customization. All functions are deterministic and Unicode-driven; edge cases follow Unicode category rules.

This project also serves as a learning exercise in writing clean, explicit and dependency-free Python libraries, while still being useful for real-world string normalization tasks.

**Note:** `yastrider` targets Python 3.10+, and relies exclusively on Python's standard library (`unicodedata`, `re`, `textwrap`, etc.)... everything with sensible defaults.

This project is both a practical tool and a learning-driven effort in writing careful and dependency-free Python libraries.

---

## Philosophy

- String cleansing should be an *easy* task.
- String cleansing should be something you can do *fast*.
- String cleansing should be something you can do *without any fancy third-party tools*.
- String cleansing should be *predictable*.
- String cleansing is something you should be able to do right when you need it and where you need it.
- String cleansing should ***not*** take the fun away from your job.

So, with that in mind, I wrote functions that:

- Solve real-world situations.
- Streamline the string-cleaning process.
- Are efficient and straightforward, but also safe to use.
- Remove the hassle, so you can focus on your *real* problems.

---
## Features

- Apply Unicode normalization with sensible default parameters.
- Strip diacritics (accents, combining marks), with optional preservation of selected ones.
- Clean whitespace (collapse, trim), optionally keeping tabs.
- Remove non-printable characters from the string, preserving tabs, newlines, and carriage returns.
- Redact sensitive words or strings.
- Convert to ASCII, with optional percent-encoding.
- Wrap text neatly to a fixed width, with word and paragraph control

All features are exposed as small, composable functions, intended to streamline your string tidying tasks.

### Design decisions

When writing `yastrider` I took a few relevant decisions:

- Everything should be done *dependency-free*, using only "vanilla" Python.
- *Unicode-first*, not *locale-first*. This should be useful for everyone, not only for developers in a particular location.
- *Explicit is better than implicit* (as per "The Zen of Python")... in fact: ***Explicit*** always. No surprises, no unexpected behavior.
- All inputs are validated, and invalid inputs throw exceptions, and any potentially surprising or unsafe inputs issue warnings.

### Trade-offs

`yastrider` intentionally prioritizes:

- Determinism over linguistic accuracy,
- Clarity over performance, and
- Explicit composition over implicit pipelines.

These make `yastrider` suitable for defensive text normalization, but *not* for NLP, localization, or reversible transformations. If you need to do those, there are specialized tools for it.

These trade-offs are intentional and non-negotiable (*Practicality beats purity*, again, as per "The Zen of Python").

---
## Why would you want to use `yastrider` over other alternatives?

Here’s a quick idea of where `yastrider` fits compared to some other tools:

| Tool | Focus | Best for |
|------|-------|----------|
| **`yastrider`** | **Pure string tidying** | **Defensively normalize user input / pre-processing.** |
| `unicodedata` | Low-level Unicode handling | Custom normalization logic. |
| `python-slugify` / `smart-slugify` | Slugs | URLs and identifiers. |
| `textprettify` | String helpers | General string utilities. |
| NLP Toolkits | Linguistic processing | Locale-aware transformations, data science, etc. |

---

## When *not* to use `yastrider`

`yastrider` is best suited for tidying strings in memory and defensive text normalization, so there are some cases where `yastrider` might not be your best option. Here are some examples of these cases:

| | |
|:--|:--|
| **Locale-aware text processing** | `yastrider` avoids locale specific logic. This is intentional. If you need language-specific rules or locale-aware transformations, other libraries might work for you. |
| **Very large volumes of text** | `yastrider` strives for ease of use and predictability, not performance. It handles strings very well if they fit in memory, but if you're processing huge text files, maybe you should consider more robust options. |
| **Structured or semantic text processing** | `yastrider` is meant to work on raw strings; it doesn't parse markup, it doesn't understand grammar and has no NLP capabilities. |

Functions in `yastrider` are ***lossy by design***: removing diacritics, normalizing, ASCII conversions and redaction are irreversible. You won't be able to reconstruct the original string from a `yastrider` function result. Handle with care!

---

## Installation

You can install `yastrider` using `pip`:

```bash
pip install yastrider
```

Zero configurations. No dependencies. Install, import and go!

You can also clone the GIT repository if you want to check the full code. This is useful if you want to use it as a learning tool or to adjust the code to fit your particular needs.


---

## Some examples

```python
# Import the functions you need
from yastrider import (
    normalize_text,
    remove_extra_spaces,
    redact_text,
    strip_diacritics,
    to_ascii
)

# An example string:
text = "   Hëllõ   World!   "

# Normalize the text and remove diacritics... but keep that "õ":
cleaned_text = normalize_text(text, preserve=['õ'])
print(cleaned_text)
##> "   Hellõ   World!   "
# By default, all diacritics are removed, unless explicitly preserved.

# Now, remove those extra spaces
no_extra_spaces = remove_extra_spaces(cleaned_text)
print(no_extra_spaces)
##> "Hellõ World!"

# Finally, redact that "World" word:
redacted = redact_text(no_extra_spaces, "World")
print(redacted)
##> "Hellõ XXXXX!"
```

Of course, you could compose the functions to do everything in a single step:

```python
text = "   Hëllõ   World!   "

redact_text(
    remove_extra_spaces(
        normalize_text(text, preserve=['õ'])
    ), 'World'
)
##> "Hellõ XXXXX!"
```


## API Reference

Docstrings are the authoritative API reference. Full API documentation may be added in the future (once the API stabilizes further).

For now, here's a brief overview of the available functions:

| Function | Description |
|:---|:---|
| `normalize_text()` | Applies Unicode normalization and optionally strips combining characters (diacritics), with selective characters preservation. This is a convenience function that combines normalization, diacritic handling and basic cleanup, with sensible defaults. |
| `to_ascii()` | Converts a string to pure-ASCII, optionally (by default) encoding non-ASCII characters with percent-encoding. |
| `redact_text()` | Redacts the string, replacing the redacted text with fill characters. You can define the fill character to use, and the length of the string used to redact the text (by default, the length of the redaction string is the length of the string to be redacted), and also whether to make replacements case-insensitive. You can also pass regular expression pattern(s) for finer control. |
| `remove_chars_by_category()` | Remove any control, punctuation or symbol characters. Character category is configurable. |
| `remove_extra_spaces()` | Strips the string of any leading or trailing spaces, and removes duplicate spaces, replacing them by single space characters. Optionally, you can decide whether to keep new-lines (`\\n`) and tabs (`\\t`), and whether to collapse multiple tabs into one. |
| `remove_non_printable_characters()` | Removes any non-printable characters, except for tabs, carriage-returns or line-feeds. |
| `strip_diacritics()` | Strips diacritics from the string. Normalization form is configurable. |
| `wrap_text()` | Wraps a text to a fixed width. |

Each function comes with sensible default values, but all are customizable. Check each function docstring for further information.

---
## *FAQ*

### Why not just use `unicodedata` directly?

Well, of course you can. In fact, `yastrider` builds on top of Python's `unicodedata` module (part of the standard library).

`yastrider` does not try to hide Unicode machinery, but to wrap commonly used, error-prone, text-tidying and normalization patterns into small, reusable and well-tested functions with sensible defaults.

If you find yourself using repeatedly `unicodedata.normalize` + category filtering + cleanup with regular expressions, `yastrider` will save you from reimplementing them every single time!

### But then, why is this different from `unidecode`?

When using `unidecode` directly, almost always you are transliterating Unicode strings into approximate  ASCII equivalents. This is often a "means to an end".

`yastrider` takes things a notch higher:

- Selective diacritic removal.
- Selective preservation of combining marks.
- Avoids guessing transliterations.
- Prioritizes predictability over linguistic approximations.

`yastrider` is meant to be a defensive tool for string normalization and cleansing. If you need controlled and reproducible normalization for your systems, this package is for you!

### Why are operations lossy?

Because string normalization often *needs to be* lossy.

Removing diacritics, collapsing spaces, redacting content, wrapping text or converting to ASCII are irreversible by nature. `yastrider` is honest about it: it does not hide the fact, but embraces it.

`yastrider` is intended to be used at points where normalization is important (before storage, comparison or downstream processing), not as a reversible transformation layer.

### Is this safe for international text?

Yes... but be aware that it's not locale-aware (by design).

`yastrider` works purely on Unicode properties and categories. It does not apply any language specific rules, nor locale-based casing logic.

### What about scale? Is this fast enough for large-scale processing?

`yastrider` prioritizes predictability and ease of use. All operations strive to be linear over input size.

If your string fits in memory and you are not bound to CPU-constraints, `yastrider` should work just fine. This means you can use it for typical application workflows (ETL pipelines, form inputs, text cleansing before database storage, etc.).

If you need to process *HUGE* texts (gigabytes), you should look for streaming-oriented solutions.

### Why "no-dependencies"?

`yastrider` is meant to be used as a Python library, within the Python ecosystem. This means that everything is done using Python's standard library, and nothing more. The main reasons for this are:

- **Predictability:** Everything you do with `yastrider` behaves exactly as it would be done with Python standard library. No surprises.
- **Portability:** You can use `yastrider` within all your Python projects, with no external dependencies.

For some projects with tight constraints, `yastrider` is a good fit, because it doesn't rely on any cumbersome or heavy libraries, but just on what's already available.

### Can I use `yastrider` in a pipeline?

Yes, but explicitly.

`yastrider` functions are meant to take in strings and output strings, so they are easily composable:

```python
# First, normalize the text and then remove extra spaces:
clean = remove_extra_spaces(
    normalize_text(text)
)
```

This keeps transformations clear, readable, explicit and debuggable.

### Will it grow?

Maybe... but only if new features fit within the philosophy statement.

New features are welcome, as long as they remain:

- Dependency free,
- Predictable, and
- Focused on string tidying.

I'll try my best to implement new features, but these conditions are crucial.

Any NLP or parsing features **will not** be added. `yastrider` is meant to "do one thing and do it well".

### Why so many warnings?

`yastrider` is written with a defensive-programming mindset.

Warnings are deliberately emitted when the input string contains edge cases that may lead to surprising results if left unnoticed.

Warnings are **part of the public behavior of the library**, not an accident. They are meant to surface potentially surprising or problematic input early, without interrupting execution.

As the library evolves, some warnings may be refined, reworded or promoted to errors, but none will be added or removed without a clear reason.

**Important:** If you treat warnings as errors, be aware that some inputs will trigger warnings.

---
## License & changelog

This project is licensed under MIT License. See [LICENSE](LICENSE) for details.

See [CHANGELOG.md](CHANGELOG.md) for a detailed list of changes.

---
## Contributing

Of course, my code is not perfect, so if you find a better way to do things, feel free to propose them! Pull requests and feedback are welcome (in fact, I ask for them). Just remember that only self-contained, clean and dependency-free contributions are preferred.

If you find `yastrider` helpful, star it and tell your favorite fellow developer about it! (If you don't have a favorite fellow developer, just spread the word!)

Also, if you find `yastrider` useful, consider supporting its development. Donations will help sustain careful design and long-term maintenance.

---
## Contributors

- @vlshields — Shared validation module and `@validate` decorator.

