# Original notebook evidence

Cell numbers include markdown and empty cells. Outputs below are saved evidence, not a rerun.

## Cell 1

```python
<a href="https://colab.research.google.com/github/Ans212121/Bayan-NLP-Anas-AI-Mutairi/blob/main/bayan_NLP_ANAS_AI_Mutairi.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
```

Saved output:

```text

```

## Cell 2

```python
**Name: Anas Ibrahim Al-Mutairi**

**Program: Applied Natural Language Processing**

**Project Name: Bayan**

```

Saved output:

```text

```

## Cell 3

```python
from __future__ import annotations

import importlib.util
import json
import os
import platform
import shutil
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

COURSE = "Bayan Applied NLP"
AUTHOR = "Meaad Al-Marri"

def package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "not-installed"

def gib(value: int) -> float:
    return round(value / (1024 ** 3), 2)

try:
    in_colab = importlib.util.find_spec("google.colab") is not None
except ModuleNotFoundError:
    in_colab = False
torch_version = package_version("torch")
cuda_available = False
gpu_name = None

if torch_version != "not-installed":
    import torch
    cuda_available = bool(torch.cuda.is_available())
    if cuda_available:
        gpu_name = torch.cuda.get_device_name(0)

disk = shutil.disk_usage("/")
report = {
    "course": COURSE,
    "author": AUTHOR,
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "in_colab": in_colab,
    "python": platform.python_version(),
    "platform": platform.platform(),
    "device": "cuda" if cuda_available else "cpu",
    "gpu_name": gpu_name,
    "disk_free_gib": gib(disk.free),
    "packages": {
        "numpy": package_version("numpy"),
        "pandas": package_version("pandas"),
        "scikit-learn": package_version("scikit-learn"),
        "torch": torch_version,
    },
}

print(json.dumps(report, ensure_ascii=False, indent=2))

```

Saved output:

```text
{
  "course": "Bayan Applied NLP",
  "author": "Meaad Al-Marri",
  "checked_at_utc": "2026-09-28T19:24:48.820912+00:00",
  "in_colab": true,
  "python": "3.13.15",
  "platform": "Linux-6.6.122+-x86_64-with-glibc2.39",
  "device": "cpu",
  "gpu_name": null,
  "disk_free_gib": 85.22,
  "packages": {
    "numpy": "2.1.3",
    "pandas": "2.2.3",
    "scikit-learn": "1.9.0",
    "torch": "2.11.0+cpu"
  }
}

```

## Cell 4

```python
# Core checks: these determine readiness. Network and GPU do not.
arabic_sample = "مرحبًا بكم في مشروع بيان"
core_checks = {
    "python_3_10_or_newer": sys.version_info >= (3, 10),
    "utf8_round_trip": arabic_sample.encode("utf-8").decode("utf-8") == arabic_sample,
    "numpy_available": report["packages"]["numpy"] != "not-installed",
    "pandas_available": report["packages"]["pandas"] != "not-installed",
    "sklearn_available": report["packages"]["scikit-learn"] != "not-installed",
    "torch_available": report["packages"]["torch"] != "not-installed",
    "disk_has_1_gib_free": report["disk_free_gib"] >= 1.0,
}

for name, passed in core_checks.items():
    print(("✅" if passed else "❌"), name)

BAYAN_ENV_READY = all(core_checks.values())
print("\nBAYAN_ENV_READY =", BAYAN_ENV_READY)
if not BAYAN_ENV_READY:
    raise RuntimeError("Environment check failed. Copy the failed check names and use the setup troubleshooting guide.")

```

Saved output:

```text
✅ python_3_10_or_newer
✅ utf8_round_trip
✅ numpy_available
✅ pandas_available
✅ sklearn_available
✅ torch_available
✅ disk_has_1_gib_free

BAYAN_ENV_READY = True

```

## Cell 5

```python
# Connectivity checks are warnings because classroom networks may filter sites.
# Test the exact services used by the notebooks, not only their home pages.
import requests

sites = {
    "github_raw": "https://raw.githubusercontent.com/almiyead-rgb/bayan-applied-nlp-course/main/README.md",
    "pypi": "https://pypi.org/simple/",
    "huggingface_models": "https://huggingface.co/api/models/google-bert/bert-base-multilingual-cased",
}
connectivity = {}
for name, url in sites.items():
    try:
        response = requests.get(
            url, headers={"User-Agent": "Bayan-Course-Runtime-Doctor/1.1"},
            timeout=15, stream=True,
        )
        connectivity[name] = 200 <= response.status_code < 400
        response.close()
    except requests.RequestException as exc:
        connectivity[name] = False
        print(f"⚠️ {name}: {type(exc).__name__}")

report["connectivity"] = connectivity
for name, passed in connectivity.items():
    print(("✅" if passed else "⚠️"), name)

print("\nA connectivity warning does not change BAYAN_ENV_READY.")

```

Saved output:

```text
✅ github_raw
✅ pypi
✅ huggingface_models

A connectivity warning does not change BAYAN_ENV_READY.

```

## Cell 6

```python
# Save a small, safe report. It contains no password, token, email, or Drive path.
report["core_checks"] = core_checks
report["bayan_env_ready"] = BAYAN_ENV_READY
report_path = Path("runtime_report.json")
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved:", report_path.name)
print("Size:", report_path.stat().st_size, "bytes")

```

Saved output:

```text
Saved: runtime_report.json
Size: 767 bytes

```

## Cell 7

```python
# تجهيز بيئة التشغيل / Setup environment

import importlib.util
import subprocess
import sys

required_versions = {
    "transformers": "5.15.1",
    "tokenizers": "0.22.2",
    "spacy": "3.8.7"
}

packages_to_install = []

for package_name, package_version in required_versions.items():
    if importlib.util.find_spec(package_name) is None:
        packages_to_install.append(
            f"{package_name}=={package_version}"
        )

if packages_to_install:
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            *packages_to_install
        ]
    )

print("Python version:", sys.version.split()[0])
print("Environment setup completed")
```

Saved output:

```text
Python version: 3.13.15
Environment setup completed

```

## Cell 8

```python
# Core imports for text preprocessing and tokenisation

import html
import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable

import numpy as np

from tokenizers import Tokenizer
from tokenizers.models import WordPiece
from tokenizers.pre_tokenizers import BertPreTokenizer
from tokenizers.processors import TemplateProcessing


# Keep random operations reproducible
RANDOM_SEED = 42
random_generator = np.random.default_rng(RANDOM_SEED)


# Small synthetic dataset used for testing
test_texts = [
    "أهلاً وسهلاً بكم في برنامج بيان!",
    "مرحبــاً\u00a0بكم",
    "Contact us at learner@example.org",
    "للتجربة فقط: 0551234567",
    "Natural language processing connects text and models."
]

print("Number of test samples:", len(test_texts))
```

Saved output:

```text
Number of test samples: 5

```

## Cell 9

```python
# Inspect Unicode information for each character

def get_unicode_details(text: str) -> list[dict[str, str]]:
    details = []

    for character in text:
        details.append({
            "character": character,
            "unicode_code": f"U+{ord(character):04X}",
            "unicode_name": unicodedata.name(character, "UNKNOWN")
        })

    return details


test_characters = "أé"
unicode_info = get_unicode_details(test_characters)

for item in unicode_info:
    print(item)

assert unicode_info[0]["unicode_code"] == "U+0623"

print("Unicode inspection=PASS")
```

Saved output:

```text
{'character': 'أ', 'unicode_code': 'U+0623', 'unicode_name': 'ARABIC LETTER ALEF WITH HAMZA ABOVE'}
{'character': 'é', 'unicode_code': 'U+00E9', 'unicode_name': 'LATIN SMALL LETTER E WITH ACUTE'}
Unicode inspection=PASS

```

## Cell 10

```python
# Text preparation and privacy protection

DIACRITIC_PATTERN = re.compile(
    r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]"
)

TATWEEL_CHAR = "\u0640"
SPACE_PATTERN = re.compile(r"\s+")
HTML_PATTERN = re.compile(r"<[^>]+>")

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+?966|00966|0)?5\d{8}(?!\d)"
)


@dataclass(frozen=True)
class TextRecord:
    raw_text: str
    model_text: str


def hide_private_info(text: str) -> str:
    cleaned_text = EMAIL_PATTERN.sub("<EMAIL>", text)
    cleaned_text = PHONE_PATTERN.sub("<PHONE>", cleaned_text)
    return cleaned_text


def prepare_text(
    text: str,
    remove_diacritics: bool = False,
    normalize_alef: bool = False
) -> TextRecord:

    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    original_text = text

    prepared_text = html.unescape(text)
    prepared_text = unicodedata.normalize("NFC", prepared_text)
    prepared_text = HTML_PATTERN.sub(" ", prepared_text)
    prepared_text = prepared_text.replace(TATWEEL_CHAR, "")

    if remove_diacritics:
        prepared_text = DIACRITIC_PATTERN.sub("", prepared_text)

    if normalize_alef:
        prepared_text = re.sub(r"[إأآٱ]", "ا", prepared_text)

    prepared_text = hide_private_info(prepared_text)
    prepared_text = SPACE_PATTERN.sub(" ", prepared_text).strip()

    return TextRecord(
        raw_text=original_text,
        model_text=prepared_text
    )


records = [prepare_text(text) for text in test_texts]

for record in records:
    print({
        "raw": record.raw_text,
        "model": record.model_text
    })


assert records[1].raw_text != records[1].model_text
assert "learner@example.org" not in records[2].model_text
assert "0551234567" not in records[3].model_text
assert records[2].raw_text == test_texts[2]

print("Two-copy preprocessing contract=PASS")
```

Saved output:

```text
{'raw': 'أهلاً وسهلاً بكم في برنامج بيان!', 'model': 'أهلاً وسهلاً بكم في برنامج بيان!'}
{'raw': 'مرحبــاً\xa0بكم', 'model': 'مرحباً بكم'}
{'raw': 'Contact us at learner@example.org', 'model': 'Contact us at <EMAIL>'}
{'raw': 'للتجربة فقط: 0551234567', 'model': 'للتجربة فقط: <PHONE>'}
{'raw': 'Natural language processing connects text and models.', 'model': 'Natural language processing connects text and models.'}
Two-copy preprocessing contract=PASS

```

## Cell 11

```python
import spacy

# Create a lightweight multilingual spaCy pipeline
sentence_processor = spacy.blank("xx")
sentence_processor.add_pipe("sentencizer")


def split_sentences(text: str) -> list[str]:
    cleaned_text = prepare_text(text).model_text

    return [
        sentence.text.strip()
        for sentence in sentence_processor(cleaned_text).sents
        if sentence.text.strip()
    ]


examples = {
    "ar": "الخدمة جيدة. لم يصل الرمز!",
    "en": "The portal stopped. Please retry."
}

sentence_results = {
    language: split_sentences(text)
    for language, text in examples.items()
}

for language, sentences in sentence_results.items():
    print(language, sentences)


abbreviation_test = split_sentences(
    "راجع د. أحمد. ثم أعد المحاولة."
)

print(
    "Abbreviation test:",
    abbreviation_test
)


assert sentence_results["ar"] == [
    "الخدمة جيدة.",
    "لم يصل الرمز!"
]

assert sentence_results["en"] == [
    "The portal stopped.",
    "Please retry."
]

print("SPACY_SENTENCE_PIPELINE=PASS")
```

Saved output:

```text
ar ['الخدمة جيدة.', 'لم يصل الرمز!']
en ['The portal stopped.', 'Please retry.']
Abbreviation test: ['راجع د.', 'أحمد.', 'ثم أعد المحاولة.']
SPACY_SENTENCE_PIPELINE=PASS

```

## Cell 12

```python
# Build a simple local WordPiece tokenizer

special_tokens = [
    "[PAD]",
    "[UNK]",
    "[CLS]",
    "[SEP]",
    "[MASK]"
]

base_tokens = [
    "أهلاً",
    "وسهلاً",
    "بكم",
    "في",
    "برنامج",
    "بيان",
    "!",
    "مرحبا",
    "Contact",
    "us",
    "at",
    "<",
    "EMAIL",
    ">",
    "Natural",
    "language",
    "processing",
    "connects",
    "text",
    "and",
    "models",
    "."
]

all_tokens = special_tokens + base_tokens

token_to_id = {
    token: index
    for index, token in enumerate(all_tokens)
}

wordpiece_tokenizer = Tokenizer(
    WordPiece(
        vocab=token_to_id,
        unk_token="[UNK]"
    )
)

wordpiece_tokenizer.pre_tokenizer = BertPreTokenizer()

wordpiece_tokenizer.post_processor = TemplateProcessing(
    single="[CLS] $A [SEP]",
    special_tokens=[
        ("[CLS]", token_to_id["[CLS]"]),
        ("[SEP]", token_to_id["[SEP]"])
    ]
)

for record in records:
    tokenized = wordpiece_tokenizer.encode(record.model_text)

    print("Text:", record.model_text)
    print("Tokens:", tokenized.tokens)
    print("IDs:", tokenized.ids)
    print("-" * 30)

test_encoding = wordpiece_tokenizer.encode("مرحبا بكم")

assert test_encoding.tokens == [
    "[CLS]",
    "مرحبا",
    "بكم",
    "[SEP]"
]

print("Local WordPiece demonstration=PASS")
```

Saved output:

```text
Text: أهلاً وسهلاً بكم في برنامج بيان!
Tokens: ['[CLS]', 'أهلاً', 'وسهلاً', 'بكم', 'في', 'برنامج', 'بيان', '!', '[SEP]']
IDs: [2, 5, 6, 7, 8, 9, 10, 11, 3]
------------------------------
Text: مرحباً بكم
Tokens: ['[CLS]', '[UNK]', 'بكم', '[SEP]']
IDs: [2, 1, 7, 3]
------------------------------
Text: Contact us at <EMAIL>
Tokens: ['[CLS]', 'Contact', 'us', 'at', '<', 'EMAIL', '>', '[SEP]']
IDs: [2, 13, 14, 15, 16, 17, 18, 3]
------------------------------
Text: للتجربة فقط: <PHONE>
Tokens: ['[CLS]', '[UNK]', '[UNK]', '[UNK]', '<', '[UNK]', '>', '[SEP]']
IDs: [2, 1, 1, 1, 16, 1, 18, 3]
------------------------------
Text: Natural language processing connects text and models.
Tokens: ['[CLS]', 'Natural', 'language', 'processing', 'connects', 'text', 'and', 'models', '.', '[SEP]']
IDs: [2, 19, 20, 21, 22, 23, 24, 25, 26, 3]
------------------------------
Local WordPiece demonstration=PASS

```

## Cell 13

```python
# Measure token fertility and truncation rate

def count_words(text: str) -> int:
    return max(1, len(text.split()))


def calculate_token_fertility(
    tokenizer: Tokenizer,
    text: str
) -> float:

    encoded_tokens = tokenizer.encode(text).tokens

    content_tokens = [
        token
        for token in encoded_tokens
        if token not in {"[CLS]", "[SEP]", "[PAD]"}
    ]

    return len(content_tokens) / count_words(text)


def calculate_truncation_rate(
    tokenizer: Tokenizer,
    texts: Iterable[str],
    max_length: int
) -> float:

    text_list = list(texts)

    if not text_list:
        raise ValueError("Text list must not be empty")

    too_long = sum(
        len(tokenizer.encode(text).ids) > max_length
        for text in text_list
    )

    return too_long / len(text_list)


model_texts = [
    record.model_text
    for record in records
]

fertilities = [
    calculate_token_fertility(wordpiece_tokenizer, text)
    for text in model_texts
]

rate_at_10 = calculate_truncation_rate(
    wordpiece_tokenizer,
    model_texts,
    max_length=10
)

print(
    "Token fertility per sample:",
    [round(value, 2) for value in fertilities]
)

print(
    "Average token fertility:",
    round(float(np.mean(fertilities)), 2)
)

print(
    "Truncation rate at length 10:",
    f"{rate_at_10:.0%}"
)

assert all(value > 0 for value in fertilities)
assert 0.0 <= rate_at_10 <= 1.0

print("Tokenisation metrics=PASS")
```

Saved output:

```text
Token fertility per sample: [1.17, 1.0, 1.5, 2.0, 1.14]
Average token fertility: 1.36
Truncation rate at length 10: 0%
Tokenisation metrics=PASS

```

## Cell 14

```python
# Padding, truncation, and simple embeddings

MAX_SEQUENCE_LENGTH = 12

wordpiece_tokenizer.enable_truncation(
    max_length=MAX_SEQUENCE_LENGTH
)

wordpiece_tokenizer.enable_padding(
    length=MAX_SEQUENCE_LENGTH,
    pad_id=token_to_id["[PAD]"],
    pad_token="[PAD]"
)

encoded_batch = [
    wordpiece_tokenizer.encode(text)
    for text in model_texts[:2]
]

input_ids = np.array(
    [item.ids for item in encoded_batch],
    dtype=np.int64
)

attention_mask = np.array(
    [item.attention_mask for item in encoded_batch],
    dtype=np.int64
)

embedding_matrix = random_generator.normal(
    0.0,
    0.02,
    size=(len(token_to_id), 8)
)

embeddings = embedding_matrix[input_ids]

print("Input IDs shape:", input_ids.shape)
print("Attention mask shape:", attention_mask.shape)
print("Embeddings shape:", embeddings.shape)
print("First attention mask:", attention_mask[0].tolist())

assert input_ids.shape == (2, MAX_SEQUENCE_LENGTH)
assert attention_mask.shape == input_ids.shape
assert embeddings.shape == (2, MAX_SEQUENCE_LENGTH, 8)

print("IDs-to-embeddings pipeline=PASS")
```

Saved output:

```text
Input IDs shape: (2, 12)
Attention mask shape: (2, 12)
Embeddings shape: (2, 12, 8)
First attention mask: [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
IDs-to-embeddings pipeline=PASS

```

## Cell 15

```python
# Optional comparison with multilingual BERT tokenizer

try:
    from transformers import AutoTokenizer

    multilingual_tokenizer = AutoTokenizer.from_pretrained(
        "google-bert/bert-base-multilingual-cased",
        use_fast=True
    )

    sample_text = (
        "معالجة اللغة الطبيعية مفيدة "
        "Natural language processing is useful"
    )

    bert_tokens = multilingual_tokenizer.tokenize(sample_text)

    print("mBERT tokens:", bert_tokens)
    print("mBERT token count:", len(bert_tokens))
    print("Fast tokenizer:", multilingual_tokenizer.is_fast)

except Exception as error:
    print("mBERT comparison skipped; Core pipeline can continue.")
    print("Reason:", type(error).__name__)
```

Saved output:

```text
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
WARNING:huggingface_hub.utils._http:Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.

config.json:   0%|          | 0.00/625 [00:00<?, ?B/s]
tokenizer_config.json:   0%|          | 0.00/49.0 [00:00<?, ?B/s]
vocab.txt:   0%|          | 0.00/996k [00:00<?, ?B/s]
tokenizer.json:   0%|          | 0.00/1.96M [00:00<?, ?B/s]
mBERT tokens: ['مع', '##الجة', 'اللغة', 'الطبيعية', 'م', '##فيد', '##ة', 'Natural', 'language', 'processing', 'is', 'useful']
mBERT token count: 12
Fast tokenizer: True

```

## Cell 16

```python
# Final core checks

core_checks = {
    "unicode":
        unicode_info[0]["unicode_code"] == "U+0623",

    "spacy_sentence_pipeline":
        all(len(value) == 2 for value in sentence_results.values()),

    "raw_copy_preserved":
        records[2].raw_text == test_texts[2],

    "pii_masked":
        "<EMAIL>" in records[2].model_text
        and "<PHONE>" in records[3].model_text,

    "token_metrics":
        all(value > 0 for value in fertilities)
        and 0.0 <= rate_at_10 <= 1.0,

    "embedding_shape":
        embeddings.shape == (2, MAX_SEQUENCE_LENGTH, 8)
}

for check_name, passed in core_checks.items():
    status = "PASS" if passed else "FAIL"
    print(f"{check_name}: {status}")

assert all(core_checks.values())

print("DAY1_NOTEBOOK1_CORE=PASS")
```

Saved output:

```text
unicode: PASS
spacy_sentence_pipeline: PASS
raw_copy_preserved: PASS
pii_masked: PASS
token_metrics: PASS
embedding_shape: PASS
DAY1_NOTEBOOK1_CORE=PASS

```

## Cell 17

```python
# Day 1 — Notebook 2: Attention & Transformers

This section continues the Day 1 work and focuses on:
- Scaled Dot-Product Attention
- Q, K, and V matrices
- Attention scores and weights
- Transformer concepts

Notebook 1 completed successfully:
`DAY1_NOTEBOOK1_CORE=PASS`
```

Saved output:

```text

```

## Cell 18

```python
import math
import numpy as np


def stable_softmax(values: np.ndarray, axis: int = -1) -> np.ndarray:
    shifted_values = values - np.max(values, axis=axis, keepdims=True)
    exp_values = np.exp(shifted_values)

    return exp_values / np.sum(
        exp_values,
        axis=axis,
        keepdims=True
    )


def compute_attention(
    queries: np.ndarray,
    keys: np.ndarray,
    values: np.ndarray,
    mask: np.ndarray | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:

    if queries.shape[-1] != keys.shape[-1]:
        raise ValueError(
            "Queries and keys must have the same feature size"
        )

    if keys.shape[-2] != values.shape[-2]:
        raise ValueError(
            "Keys and values must have the same sequence length"
        )

    attention_scores = (
        queries @ np.swapaxes(keys, -1, -2)
    ) / math.sqrt(queries.shape[-1])

    if mask is not None:
        mask_array = np.asarray(mask, dtype=bool)

        try:
            mask_array = np.broadcast_to(
                mask_array,
                attention_scores.shape
            )
        except ValueError as error:
            raise ValueError(
                "Mask shape cannot match attention scores"
            ) from error

        if np.any(mask_array.sum(axis=-1) == 0):
            raise ValueError(
                "Each query must keep at least one valid key"
            )

        attention_scores = np.where(
            mask_array,
            attention_scores,
            -np.inf
        )

    attention_weights = stable_softmax(
        attention_scores,
        axis=-1
    )

    attention_output = attention_weights @ values

    return (
        attention_output,
        attention_weights,
        attention_scores
    )


queries = np.array([
    [1.0, 0.0],
    [0.0, 1.0]
])

keys = np.array([
    [1.0, 0.0],
    [0.0, 1.0],
    [1.0, 1.0]
])

values = np.array([
    [10.0, 0.0],
    [0.0, 10.0],
    [5.0, 5.0]
])


attention_output, attention_weights, attention_scores = compute_attention(
    queries,
    keys,
    values
)


print("Scores shape:", attention_scores.shape)

print(
    "Attention weights:\n",
    np.round(attention_weights, 3)
)

print(
    "Weight row sums:",
    attention_weights.sum(axis=-1)
)

print(
    "Attention output:\n",
    np.round(attention_output, 3)
)


assert attention_output.shape == (2, 2)

assert np.allclose(
    attention_weights.sum(axis=-1),
    1.0
)

print("Scaled attention=PASS")
```

Saved output:

```text
Scores shape: (2, 3)
Attention weights:
 [[0.401 0.198 0.401]
 [0.198 0.401 0.401]]
Weight row sums: [1. 1.]
Attention output:
 [[6.017 3.983]
 [3.983 6.017]]
Scaled attention=PASS

```

## Cell 19

```python
# Compare attention with and without scaling

def calculate_entropy(probabilities: np.ndarray) -> float:
    safe_probs = np.clip(probabilities, 1e-12, 1.0)

    return float(
        -np.sum(
            safe_probs * np.log(safe_probs),
            axis=-1
        ).mean()
    )


query_matrix = np.random.default_rng(42).normal(
    size=(6, 64)
)

key_matrix = np.random.default_rng(43).normal(
    size=(6, 64)
)

raw_scores = query_matrix @ key_matrix.T

weights_without_scaling = stable_softmax(raw_scores)

weights_with_scaling = stable_softmax(
    raw_scores / math.sqrt(query_matrix.shape[-1])
)

entropy_without_scaling = calculate_entropy(
    weights_without_scaling
)

entropy_with_scaling = calculate_entropy(
    weights_with_scaling
)

print(
    "Mean entropy without scaling:",
    round(entropy_without_scaling, 3)
)

print(
    "Mean entropy with scaling:",
    round(entropy_with_scaling, 3)
)

print("Scaling comparison complete")
```

Saved output:

```text
Mean entropy without scaling: 0.516
Mean entropy with scaling: 1.589
Scaling comparison complete

```

## Cell 20

```python
# Causal mask example

causal_mask = np.tril(
    np.ones((2, 3), dtype=bool)
)

masked_output, masked_weights, _ = compute_attention(
    queries,
    keys,
    values,
    mask=causal_mask
)

print(
    "Keep mask:\n",
    causal_mask.astype(int)
)

print(
    "Masked attention weights:\n",
    np.round(masked_weights, 3)
)

assert masked_weights[0, 1] == 0.0
assert masked_weights[0, 2] == 0.0

print("Mask semantics=PASS")
```

Saved output:

```text
Keep mask:
 [[1 0 0]
 [1 1 0]]
Masked attention weights:
 [[1.   0.   0.  ]
 [0.33 0.67 0.  ]]
Mask semantics=PASS

```

## Cell 21

```python
# Split and combine Multi-Head representations

def split_into_heads(
    tensor: np.ndarray,
    num_heads: int
) -> np.ndarray:

    batch_size, seq_length, d_model = tensor.shape

    if d_model % num_heads != 0:
        raise ValueError(
            "d_model must be divisible by num_heads"
        )

    head_dim = d_model // num_heads

    reshaped = tensor.reshape(
        batch_size,
        seq_length,
        num_heads,
        head_dim
    )

    return reshaped.transpose(0, 2, 1, 3)


def combine_from_heads(
    tensor: np.ndarray
) -> np.ndarray:

    batch_size, num_heads, seq_length, head_dim = tensor.shape

    reordered = tensor.transpose(0, 2, 1, 3)

    return reordered.reshape(
        batch_size,
        seq_length,
        num_heads * head_dim
    )


random_generator = np.random.default_rng(42)

sample_tensor = random_generator.normal(
    size=(2, 5, 12)
)

head_tensor = split_into_heads(
    sample_tensor,
    num_heads=3
)

combined_tensor = combine_from_heads(
    head_tensor
)

print("Input shape:", sample_tensor.shape)

print(
    "Split shape:",
    head_tensor.shape,
    "= (batch, heads, tokens, head_dim)"
)

print("Combined shape:", combined_tensor.shape)

assert head_tensor.shape == (2, 3, 5, 4)
assert np.allclose(combined_tensor, sample_tensor)

print("Multi-head shape journey=PASS")
```

Saved output:

```text
Input shape: (2, 5, 12)
Split shape: (2, 3, 5, 4) = (batch, heads, tokens, head_dim)
Combined shape: (2, 5, 12)
Multi-head shape journey=PASS

```

## Cell 22

```python
# Optional Transformer Encoder test with PyTorch

try:
    import torch

    torch.manual_seed(42)

    encoder_layer = torch.nn.TransformerEncoderLayer(
        d_model=12,
        nhead=3,
        dim_feedforward=24,
        dropout=0.0,
        batch_first=True,
        norm_first=False
    )

    encoder_layer.eval()

    torch_input = torch.tensor(
        sample_tensor,
        dtype=torch.float32
    )

    with torch.no_grad():
        encoder_output = encoder_layer(torch_input)

    print(
        "PyTorch encoder output shape:",
        tuple(encoder_output.shape)
    )

    assert tuple(encoder_output.shape) == (2, 5, 12)

    print("Optional encoder layer=PASS")

except ModuleNotFoundError:
    print(
        "PyTorch is not installed; NumPy Core is still complete."
    )
```

Saved output:

```text
PyTorch encoder output shape: (2, 5, 12)
Optional encoder layer=PASS

```

## Cell 23

```python
# Compare our NumPy attention with PyTorch SDPA

try:
    import torch
    import torch.nn.functional as F

    torch_queries = torch.tensor(
        queries,
        dtype=torch.float64
    )[None, None, :, :]

    torch_keys = torch.tensor(
        keys,
        dtype=torch.float64
    )[None, None, :, :]

    torch_values = torch.tensor(
        values,
        dtype=torch.float64
    )[None, None, :, :]

    torch_result = F.scaled_dot_product_attention(
        torch_queries,
        torch_keys,
        torch_values,
        dropout_p=0.0
    )

    numpy_result = attention_output[None, None, :, :]

    max_difference = float(
        np.max(
            np.abs(
                torch_result.numpy() - numpy_result
            )
        )
    )

    print(
        "Maximum NumPy/PyTorch difference:",
        f"{max_difference:.3e}"
    )

    assert max_difference < 1e-9

    print("NumPy/PyTorch parity=PASS")

except ModuleNotFoundError:
    print(
        "PyTorch unavailable; parity check skipped without affecting Core."
    )
```

Saved output:

```text
Maximum NumPy/PyTorch difference: 4.441e-16
NumPy/PyTorch parity=PASS

```

## Cell 24

```python
from transformers import AutoConfig

CHECKPOINTS_TO_AUDIT = [
    "google-bert/bert-base-multilingual-cased",
    "CAMeL-Lab/bert-base-arabic-camelbert-da",
]

EXPECTED_PARAMETER_TOTALS = {
    "google-bert/bert-base-multilingual-cased": 177_853_440,
    "CAMeL-Lab/bert-base-arabic-camelbert-da": 109_081_344,
}


def count_bert_parameters(model_name: str) -> dict:
    config = AutoConfig.from_pretrained(model_name)

    assert config.model_type == "bert"

    hidden_size = config.hidden_size
    intermediate_size = config.intermediate_size

    embedding_parameters = (
        config.vocab_size * hidden_size
        + config.max_position_embeddings * hidden_size
        + config.type_vocab_size * hidden_size
        + 2 * hidden_size
    )

    parameters_per_layer = (
        3 * (hidden_size * hidden_size + hidden_size)
        + (hidden_size * hidden_size + hidden_size)
        + 2 * hidden_size
        + (hidden_size * intermediate_size + intermediate_size)
        + (intermediate_size * hidden_size + hidden_size)
        + 2 * hidden_size
    )

    pooler_parameters = (
        hidden_size * hidden_size + hidden_size
    )

    total_parameters = (
        embedding_parameters
        + config.num_hidden_layers * parameters_per_layer
        + pooler_parameters
    )

    return {
        "model_name": model_name,
        "vocab_size": config.vocab_size,
        "total_parameters": total_parameters,
        "embedding_ratio": embedding_parameters / total_parameters,
    }


audit_results = [
    count_bert_parameters(model_name)
    for model_name in CHECKPOINTS_TO_AUDIT
]

for result in audit_results:
    print(
        f'{result["model_name"]} | '
        f'vocab={result["vocab_size"]:,} | '
        f'total={result["total_parameters"]:,} | '
        f'embeddings={result["embedding_ratio"]:.1%}'
    )

assert all(
    result["total_parameters"]
    == EXPECTED_PARAMETER_TOTALS[result["model_name"]]
    for result in audit_results
)

print("TWO_CHECKPOINT_PARAMETER_AUDIT=PASS")
```

Saved output:

```text
config.json:   0%|          | 0.00/468 [00:00<?, ?B/s]
google-bert/bert-base-multilingual-cased | vocab=119,547 | total=177,853,440 | embeddings=51.8%
CAMeL-Lab/bert-base-arabic-camelbert-da | vocab=30,000 | total=109,081,344 | embeddings=21.5%
TWO_CHECKPOINT_PARAMETER_AUDIT=PASS

```

## Cell 25

```python
# Actual forward pass with a multilingual Transformer

import torch
import matplotlib.pyplot as plt

from transformers import AutoModel, AutoTokenizer
from transformers.utils import logging as hf_logging


hf_logging.set_verbosity_error()

MODEL_NAME = "distilbert/distilbert-base-multilingual-cased"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    use_fast=True
)

model = AutoModel.from_pretrained(
    MODEL_NAME,
    attn_implementation="eager"
)

model.eval()


example_sentences = [
    "الخدمة لم تتأخر.",
    "The service was not delayed."
]

model_inputs = tokenizer(
    example_sentences,
    padding=True,
    truncation=True,
    max_length=32,
    return_tensors="pt"
)


with torch.no_grad():
    model_output = model(
        **model_inputs,
        output_attentions=True
    )


total_parameters = sum(
    parameter.numel()
    for parameter in model.parameters()
)

hidden_state_shape = tuple(
    model_output.last_hidden_state.shape
)

attention_tensor_shape = tuple(
    model_output.attentions[0].shape
)

arabic_tokens = tokenizer.convert_ids_to_tokens(
    model_inputs["input_ids"][0]
)

valid_token_count = int(
    model_inputs["attention_mask"][0].sum()
)

first_head_attention = (
    model_output.attentions[0][
        0,
        0,
        :valid_token_count,
        :valid_token_count
    ]
    .cpu()
    .numpy()
)


print("Model:", MODEL_NAME)
print(f"Parameters: {total_parameters:,}")
print("Hidden-state shape:", hidden_state_shape)

print(
    "Attention tensor [batch, heads, query, key]:",
    attention_tensor_shape
)

print(
    "Arabic tokens:",
    arabic_tokens[:valid_token_count]
)

print(
    "Row-sum range:",
    float(first_head_attention.sum(-1).min()),
    float(first_head_attention.sum(-1).max())
)


fig, ax = plt.subplots(figsize=(8, 6))

heatmap = ax.imshow(
    first_head_attention,
    cmap="Blues",
    vmin=0.0
)

ax.set_xticks(
    range(valid_token_count),
    arabic_tokens[:valid_token_count],
    rotation=60,
    ha="right"
)

ax.set_yticks(
    range(valid_token_count),
    arabic_tokens[:valid_token_count]
)

ax.set_xlabel("Key token")
ax.set_ylabel("Query token")

ax.set_title(
    "Layer 1 · Head 1 · Attention Weights"
)

fig.colorbar(
    heatmap,
    ax=ax,
    fraction=0.046
)

fig.tight_layout()
plt.show()


assert total_parameters > 100_000_000

assert hidden_state_shape[:2] == tuple(
    model_inputs["input_ids"].shape
)

assert (
    attention_tensor_shape[0] == 2
    and attention_tensor_shape[2] == attention_tensor_shape[3]
)

assert np.allclose(
    first_head_attention.sum(-1),
    1.0,
    atol=1e-5
)

print("ACTUAL_TRANSFORMER_FORWARD=PASS")
```

Saved output:

```text
Loading weights:   0%|          | 0/100 [00:00<?, ?it/s]
Model: distilbert/distilbert-base-multilingual-cased
Parameters: 134,734,080
Hidden-state shape: (2, 10, 768)
Attention tensor [batch, heads, query, key]: (2, 12, 10, 10)
Arabic tokens: ['[CLS]', 'ال', '##خدمة', 'لم', 'ت', '##ت', '##أ', '##خر', '.', '[SEP]']
Row-sum range: 0.9999998211860657 1.0

<Figure size 800x600 with 2 Axes>
ACTUAL_TRANSFORMER_FORWARD=PASS

```

## Cell 26

```python
# Final checks for Notebook 2

core_checks = {
    "weights_sum_to_one":
        np.allclose(
            attention_weights.sum(axis=-1),
            1.0
        ),

    "two_checkpoint_parameter_audit":
        len(audit_results) == 2
        and all(
            result["total_parameters"]
            == EXPECTED_PARAMETER_TOTALS[result["model_name"]]
            for result in audit_results
        ),

    "actual_forward":
        total_parameters > 100_000_000
        and len(model_output.attentions) > 0,

    "output_shape":
        attention_output.shape == (2, 2),

    "masked_positions_zero":
        masked_weights[0, 1] == 0
        and masked_weights[0, 2] == 0,

    "heads_round_trip":
        np.allclose(
            combined_tensor,
            sample_tensor
        ),
}


for check_name, passed in core_checks.items():
    status = "PASS" if passed else "FAIL"
    print(f"{check_name}: {status}")


assert all(core_checks.values())

print("DAY1_NOTEBOOK2_CORE=PASS")
```

Saved output:

```text
weights_sum_to_one: PASS
two_checkpoint_parameter_audit: PASS
actual_forward: PASS
output_shape: PASS
masked_positions_zero: PASS
heads_round_trip: PASS
DAY1_NOTEBOOK2_CORE=PASS

```

## Cell 27

```python
# Challenge 9 - Core
# Change V values and observe how the attention output changes

new_values = np.array([
    [20.0, 0.0],
    [0.0, 20.0],
    [10.0, 10.0]
])

new_output, new_weights, _ = compute_attention(
    queries,
    keys,
    new_values
)

print("Original output:")
print(np.round(attention_output, 3))

print("\nNew output after changing V:")
print(np.round(new_output, 3))

print("\nAttention weights:")
print(np.round(new_weights, 3))

print("\nObservation:")
print("Changing V changes the final output, while the attention weights remain based on Q and K.")
```

Saved output:

```text
Original output:
[[6.017 3.983]
 [3.983 6.017]]

New output after changing V:
[[12.033  7.967]
 [ 7.967 12.033]]

Attention weights:
[[0.401 0.198 0.401]
 [0.198 0.401 0.401]]

Observation:
Changing V changes the final output, while the attention weights remain based on Q and K.

```

## Cell 28

```python
# Day 2 — Text Classification

This section starts Day 2 and focuses on text classification using a baseline model and multilingual DistilBERT.

Notebook 1 and Notebook 2 from Day 1 were completed successfully.
```

Saved output:

```text

```

## Cell 29

```python
# تثبيت نسخ اليوم الثاني فقط عند الحاجة

import importlib.metadata
import importlib.util
import subprocess
import sys

REQUIRED = {
    "transformers": "5.15.1",
    "tokenizers": "0.22.2",
    "scikit-learn": "1.9.0",
}

needs_install = []

for distribution, expected in REQUIRED.items():
    try:
        current = importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        current = None

    if current != expected:
        needs_install.append(f"{distribution}=={expected}")

if needs_install:
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            *needs_install
        ]
    )

if importlib.util.find_spec("torch") is None:
    raise RuntimeError(
        "PyTorch is required. Open this notebook in Google Colab."
    )

print("Python:", sys.version.split()[0])
print("Environment ready / البيئة جاهزة")
```

Saved output:

```text
Python: 3.13.15
Environment ready / البيئة جاهزة

```

## Cell 30

```python
import csv
import io
import json
import math
import os
import random
import urllib.request
from collections import Counter
from pathlib import Path

import numpy as np
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.svm import LinearSVC
from torch.optim import AdamW
from transformers import AutoModelForSequenceClassification, AutoTokenizer

os.environ["TOKENIZERS_PARALLELISM"] = "false"

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", DEVICE)
```

Saved output:

```text
Device: cpu

```

## Cell 31

```python
DATA_URL = "https://raw.githubusercontent.com/almiyead-rgb/bayan-applied-nlp-course/main/data/sample/bayan_day2_classification.csv"

FALLBACK_ROWS = [
    {
        "example_id": "F-001",
        "group_id": "DG-A",
        "split": "train",
        "language": "ar",
        "text": "تعذر تسجيل الدخول إلى البوابة",
        "topic": "digital_service",
        "sentiment": "negative",
    },
    {
        "example_id": "F-002",
        "group_id": "DG-A",
        "split": "train",
        "language": "en",
        "text": "I cannot sign in to the portal",
        "topic": "digital_service",
        "sentiment": "negative",
    },
    {
        "example_id": "F-003",
        "group_id": "DG-B",
        "split": "train",
        "language": "ar",
        "text": "الخدمة الإلكترونية سريعة وواضحة",
        "topic": "digital_service",
        "sentiment": "positive",
    },
    {
        "example_id": "F-004",
        "group_id": "DG-B",
        "split": "train",
        "language": "en",
        "text": "The online service is clear and fast",
        "topic": "digital_service",
        "sentiment": "positive",
    },
    {
        "example_id": "F-005",
        "group_id": "PG-A",
        "split": "train",
        "language": "ar",
        "text": "أحتاج معرفة حالة طلب التصريح",
        "topic": "permit",
        "sentiment": "neutral",
    },
    {
        "example_id": "F-006",
        "group_id": "PG-A",
        "split": "train",
        "language": "en",
        "text": "I need the status of my permit request",
        "topic": "permit",
        "sentiment": "neutral",
    },
    {
        "example_id": "F-007",
        "group_id": "PG-B",
        "split": "train",
        "language": "ar",
        "text": "تمت الموافقة على التصريح اليوم",
        "topic": "permit",
        "sentiment": "positive",
    },
    {
        "example_id": "F-008",
        "group_id": "PG-B",
        "split": "train",
        "language": "en",
        "text": "The permit was approved today",
        "topic": "permit",
        "sentiment": "positive",
    },
    {
        "example_id": "F-009",
        "group_id": "HG-A",
        "split": "train",
        "language": "ar",
        "text": "تأخر موعد العيادة هذا الصباح",
        "topic": "health",
        "sentiment": "negative",
    },
    {
        "example_id": "F-010",
        "group_id": "HG-A",
        "split": "train",
        "language": "en",
        "text": "My clinic appointment was delayed",
        "topic": "health",
        "sentiment": "negative",
    },
    {
        "example_id": "F-011",
        "group_id": "HG-B",
        "split": "train",
        "language": "ar",
        "text": "كانت خدمة العيادة ممتازة",
        "topic": "health",
        "sentiment": "positive",
    },
    {
        "example_id": "F-012",
        "group_id": "HG-B",
        "split": "train",
        "language": "en",
        "text": "The clinic service was excellent",
        "topic": "health",
        "sentiment": "positive",
    },
    {
        "example_id": "F-013",
        "group_id": "TG-A",
        "split": "train",
        "language": "ar",
        "text": "الحافلة لم تصل في الوقت المحدد",
        "topic": "transport",
        "sentiment": "negative",
    },
    {
        "example_id": "F-014",
        "group_id": "TG-A",
        "split": "train",
        "language": "en",
        "text": "The bus did not arrive on time",
        "topic": "transport",
        "sentiment": "negative",
    },
    {
        "example_id": "F-015",
        "group_id": "TG-B",
        "split": "train",
        "language": "ar",
        "text": "كانت الرحلة مريحة ومنظمة",
        "topic": "transport",
        "sentiment": "positive",
    },
    {
        "example_id": "F-016",
        "group_id": "TG-B",
        "split": "train",
        "language": "en",
        "text": "The trip was comfortable and organised",
        "topic": "transport",
        "sentiment": "positive",
    },
    {
        "example_id": "F-017",
        "group_id": "DG-V",
        "split": "validation",
        "language": "ar",
        "text": "لم يصل رمز التحقق الرقمي",
        "topic": "digital_service",
        "sentiment": "negative",
    },
    {
        "example_id": "F-018",
        "group_id": "PG-V",
        "split": "validation",
        "language": "en",
        "text": "How can I renew the permit",
        "topic": "permit",
        "sentiment": "neutral",
    },
    {
        "example_id": "F-019",
        "group_id": "HG-V",
        "split": "validation",
        "language": "ar",
        "text": "أحتاج إعادة جدولة الموعد الصحي",
        "topic": "health",
        "sentiment": "neutral",
    },
    {
        "example_id": "F-020",
        "group_id": "TG-V",
        "split": "validation",
        "language": "en",
        "text": "The bus route has changed",
        "topic": "transport",
        "sentiment": "neutral",
    },
    {
        "example_id": "F-021",
        "group_id": "DG-T",
        "split": "test",
        "language": "en",
        "text": "The verification code did not arrive",
        "topic": "digital_service",
        "sentiment": "negative",
    },
    {
        "example_id": "F-022",
        "group_id": "PG-T",
        "split": "test",
        "language": "ar",
        "text": "تأخر إصدار التصريح المطلوب",
        "topic": "permit",
        "sentiment": "negative",
    },
    {
        "example_id": "F-023",
        "group_id": "HG-T",
        "split": "test",
        "language": "en",
        "text": "The clinic appointment was cancelled",
        "topic": "health",
        "sentiment": "negative",
    },
    {
        "example_id": "F-024",
        "group_id": "TG-T",
        "split": "test",
        "language": "ar",
        "text": "توقفت الحافلة قبل المحطة",
        "topic": "transport",
        "sentiment": "negative",
    },
]

try:
    with urllib.request.urlopen(DATA_URL, timeout=20) as response:
        text = response.read().decode("utf-8")
        rows = list(csv.DictReader(io.StringIO(text)))

    DATA_SOURCE = "github_course_file"

except Exception as exc:
    rows = FALLBACK_ROWS
    DATA_SOURCE = f"embedded_fallback:{type(exc).__name__}"

print("Data source:", DATA_SOURCE)
print("Rows:", len(rows))
print("Topics:", Counter(row["topic"] for row in rows))

assert len(rows) >= 24
assert {"ar", "en"} <= {row["language"] for row in rows}
```

Saved output:

```text
Data source: github_course_file
Rows: 40
Topics: Counter({'digital_service': 10, 'permit': 10, 'health': 10, 'transport': 10})

```

## Cell 32

```python
def validate_splits(rows):
    required = {"train", "validation", "test"}

    group_owner = {}
    labels_by_split = {
        name: set()
        for name in required
    }

    counts = Counter()

    for row in rows:
        split = row["split"]
        group = row["group_id"]
        label = row["topic"]

        if split not in required:
            raise ValueError(
                f"Unknown split: {split}"
            )

        previous = group_owner.setdefault(
            group,
            split
        )

        if previous != split:
            raise ValueError(
                f"Group leakage: {group}"
            )

        labels_by_split[split].add(label)
        counts[split] += 1

    all_labels = set().union(
        *labels_by_split.values()
    )

    for split in required:
        if labels_by_split[split] != all_labels:
            raise ValueError(
                f"Missing label in {split}"
            )

    return {
        "rows": dict(counts),
        "groups": len(group_owner),
        "labels": sorted(all_labels),
        "group_overlap": 0,
    }


split_report = validate_splits(rows)

print(
    json.dumps(
        split_report,
        ensure_ascii=False,
        indent=2
    )
)

assert split_report["group_overlap"] == 0

print("Split contract=PASS")
```

Saved output:

```text
{
  "rows": {
    "train": 24,
    "validation": 8,
    "test": 8
  },
  "groups": 20,
  "labels": [
    "digital_service",
    "health",
    "permit",
    "transport"
  ],
  "group_overlap": 0
}
Split contract=PASS

```

## Cell 33

```python
train_rows = [row for row in rows if row["split"] == "train"]
validation_rows = [row for row in rows if row["split"] == "validation"]
test_rows = [row for row in rows if row["split"] == "test"]
LABELS = sorted({row["topic"] for row in rows})
label2id = {label: index for index, label in enumerate(LABELS)}
id2label = {index: label for label, index in label2id.items()}

baseline = make_pipeline(
    TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1),
    LinearSVC(random_state=SEED),
)
baseline.fit(
    [row["text"] for row in train_rows],
    [row["topic"] for row in train_rows],
)
baseline_val_pred = baseline.predict([row["text"] for row in validation_rows])
baseline_val_f1 = f1_score(
    [row["topic"] for row in validation_rows],
    baseline_val_pred,
    labels=LABELS,
    average="macro",
    zero_division=0,
)
print("Baseline validation macro-F1 (MEASURED_SMOKE):", round(baseline_val_f1, 4))
assert 0.0 <= baseline_val_f1 <= 1.0
print("Baseline=PASS")
```

Saved output:

```text
Baseline validation macro-F1 (MEASURED_SMOKE): 0.6667
Baseline=PASS

```

## Cell 34

```python

```

Saved output:

```text

```

## Cell 35

```python
MODEL_ID = "distilbert/distilbert-base-multilingual-cased"
MAX_LENGTH = 64
BATCH_SIZE = 4
NUM_EPOCHS = 2 if DEVICE.type == "cuda" else 12

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_ID,
        num_labels=len(LABELS),
        label2id=label2id,
        id2label=id2label,
    )
except Exception as exc:
    raise RuntimeError(
        "Checkpoint download failed. Reconnect the runtime and run this cell once. "
        "No API key is required."
    ) from exc

TRAINING_MODE = "full_finetune" if DEVICE.type == "cuda" else "partial_finetune_cpu"
if TRAINING_MODE == "partial_finetune_cpu":
    for parameter in model.base_model.parameters():
        parameter.requires_grad = False
    for parameter in model.base_model.transformer.layer[-1].parameters():
        parameter.requires_grad = True

model.to(DEVICE)
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print("Training mode:", TRAINING_MODE)
print("Epochs:", NUM_EPOCHS)
print(f"Trainable parameters: {trainable:,} / {total:,}")
assert trainable > 0
```

Saved output:

```text
Loading weights:   0%|          | 0/100 [00:00<?, ?it/s]
Training mode: partial_finetune_cpu
Epochs: 12
Trainable parameters: 7,681,540 / 135,327,748

```

## Cell 36

```python
def iter_batches(examples, batch_size, *, shuffle=False, seed=SEED):
    indexes = np.arange(len(examples))
    if shuffle:
        np.random.default_rng(seed).shuffle(indexes)
    for start in range(0, len(indexes), batch_size):
        yield [examples[index] for index in indexes[start:start + batch_size]]


def encode_batch(batch):
    encoded = tokenizer(
        [row["text"] for row in batch],
        padding=True,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )
    encoded["labels"] = torch.tensor(
        [label2id[row["topic"]] for row in batch], dtype=torch.long
    )
    return {key: value.to(DEVICE) for key, value in encoded.items()}


def predict(examples):
    model.eval()
    predictions = []
    with torch.no_grad():
        for batch in iter_batches(examples, BATCH_SIZE):
            encoded = encode_batch(batch)
            logits = model(**encoded).logits
            predictions.extend(logits.argmax(-1).cpu().tolist())
    return [id2label[index] for index in predictions]

print("Batch functions=PASS")
```

Saved output:

```text
Batch functions=PASS

```

## Cell 37

```python
learning_rate = 2e-5 if TRAINING_MODE == "full_finetune" else 1e-4
trainable_parameters = [p for p in model.parameters() if p.requires_grad]
optimizer = AdamW(trainable_parameters, lr=learning_rate)
losses = []
train_steps = 0
epoch_history = []
best_validation_f1 = -1.0
best_epoch = 0
best_trainable_state = None

for epoch_index in range(NUM_EPOCHS):
    model.train()
    epoch_losses = []
    for batch in iter_batches(
        train_rows, BATCH_SIZE, shuffle=True, seed=SEED + epoch_index + 1
    ):
        optimizer.zero_grad(set_to_none=True)
        encoded = encode_batch(batch)
        output = model(**encoded)
        loss = output.loss
        if not torch.isfinite(loss):
            raise RuntimeError("Non-finite training loss")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(trainable_parameters, max_norm=1.0)
        optimizer.step()
        loss_value = float(loss.detach().cpu())
        losses.append(loss_value)
        epoch_losses.append(loss_value)
        train_steps += 1

    epoch_predictions = predict(validation_rows)
    epoch_f1 = f1_score(
        [row["topic"] for row in validation_rows], epoch_predictions,
        labels=LABELS, average="macro", zero_division=0,
    )
    epoch_history.append({
        "epoch": epoch_index + 1,
        "mean_loss": float(np.mean(epoch_losses)),
        "validation_macro_f1": float(epoch_f1),
    })
    if epoch_f1 > best_validation_f1:
        best_validation_f1 = float(epoch_f1)
        best_epoch = epoch_index + 1
        if TRAINING_MODE == "partial_finetune_cpu":
            best_trainable_state = {
                name: parameter.detach().cpu().clone()
                for name, parameter in model.named_parameters()
                if parameter.requires_grad
            }
    print(
        f"epoch={epoch_index + 1:02d} mean_loss={np.mean(epoch_losses):.4f} "
        f"validation_macro_f1={epoch_f1:.4f}"
    )

if best_trainable_state is not None:
    with torch.no_grad():
        for name, parameter in model.named_parameters():
            if name in best_trainable_state:
                parameter.copy_(best_trainable_state[name].to(parameter.device))
    selected_epoch = best_epoch
else:
    selected_epoch = NUM_EPOCHS

assert train_steps >= 1 and all(math.isfinite(value) for value in losses)
assert any(parameter.requires_grad for parameter in model.base_model.parameters())
print("Transformer optimizer steps=PASS", {"steps": train_steps, "selected_epoch": selected_epoch})
```

Saved output:

```text
epoch=01 mean_loss=1.4031 validation_macro_f1=0.2917
epoch=02 mean_loss=1.3156 validation_macro_f1=0.4167
epoch=03 mean_loss=1.2396 validation_macro_f1=0.4167
epoch=04 mean_loss=1.1272 validation_macro_f1=0.6250
epoch=05 mean_loss=0.9523 validation_macro_f1=0.6250
epoch=06 mean_loss=0.7202 validation_macro_f1=0.7500
epoch=07 mean_loss=0.4770 validation_macro_f1=0.8667
epoch=08 mean_loss=0.2488 validation_macro_f1=0.8667
epoch=09 mean_loss=0.1160 validation_macro_f1=1.0000
epoch=10 mean_loss=0.0552 validation_macro_f1=1.0000
epoch=11 mean_loss=0.0225 validation_macro_f1=1.0000
epoch=12 mean_loss=0.0115 validation_macro_f1=0.8667
Transformer optimizer steps=PASS {'steps': 72, 'selected_epoch': 9}

```

## Cell 38

```python
transformer_val_pred = predict(validation_rows)
transformer_val_f1 = f1_score(
    [row["topic"] for row in validation_rows],
    transformer_val_pred,
    labels=LABELS,
    average="macro",
    zero_division=0,
)
validation_delta = transformer_val_f1 - baseline_val_f1
print("Selected epoch:", selected_epoch)
print("Transformer validation macro-F1 (MEASURED_SMOKE):", round(transformer_val_f1, 4))
print("Validation delta vs TF-IDF baseline:", round(validation_delta, 4))
print("Validation predictions:", list(zip(
    [row["topic"] for row in validation_rows], transformer_val_pred
)))
assert 0.0 <= transformer_val_f1 <= 1.0
```

Saved output:

```text
Selected epoch: 9
Transformer validation macro-F1 (MEASURED_SMOKE): 1.0
Validation delta vs TF-IDF baseline: 0.3333
Validation predictions: [('digital_service', 'digital_service'), ('digital_service', 'digital_service'), ('permit', 'permit'), ('permit', 'permit'), ('health', 'health'), ('health', 'health'), ('transport', 'transport'), ('transport', 'transport')]

```

## Cell 39

```python
test_truth = [row["topic"] for row in test_rows]
baseline_test_pred = baseline.predict([row["text"] for row in test_rows]).tolist()
transformer_test_pred = predict(test_rows)

results = {
    "result_type": "MEASURED_SMOKE",
    "data_source": DATA_SOURCE,
    "model_id": MODEL_ID,
    "device": str(DEVICE),
    "training_mode": TRAINING_MODE,
    "seed": SEED,
    "epochs_run": NUM_EPOCHS,
    "selected_epoch": selected_epoch,
    "train_steps": train_steps,
    "mean_train_loss": float(np.mean(losses)),
    "baseline_validation_macro_f1": float(baseline_val_f1),
    "transformer_validation_macro_f1": float(transformer_val_f1),
    "validation_delta_vs_baseline": float(validation_delta),
    "baseline_beaten_on_validation": bool(validation_delta > 0),
    "baseline_test_macro_f1": float(f1_score(
        test_truth, baseline_test_pred, labels=LABELS,
        average="macro", zero_division=0,
    )),
    "transformer_test_macro_f1": float(f1_score(
        test_truth, transformer_test_pred, labels=LABELS,
        average="macro", zero_division=0,
    )),
    "transformer_test_accuracy": float(accuracy_score(test_truth, transformer_test_pred)),
    "limitations": [
        "synthetic tiny dataset",
        "small validation set used for epoch selection",
        "not an estimate of production quality",
    ],
}
print(json.dumps(results, ensure_ascii=False, indent=2))
Path("day2_classification_metrics.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
)
```

Saved output:

```text
{
  "result_type": "MEASURED_SMOKE",
  "data_source": "github_course_file",
  "model_id": "distilbert/distilbert-base-multilingual-cased",
  "device": "cpu",
  "training_mode": "partial_finetune_cpu",
  "seed": 42,
  "epochs_run": 12,
  "selected_epoch": 9,
  "train_steps": 72,
  "mean_train_loss": 0.6407361574496867,
  "baseline_validation_macro_f1": 0.6666666666666666,
  "transformer_validation_macro_f1": 1.0,
  "validation_delta_vs_baseline": 0.33333333333333337,
  "baseline_beaten_on_validation": true,
  "baseline_test_macro_f1": 0.7333333333333333,
  "transformer_test_macro_f1": 0.8666666666666667,
  "transformer_test_accuracy": 0.875,
  "limitations": [
    "synthetic tiny dataset",
    "small validation set used for epoch selection",
    "not an estimate of production quality"
  ]
}

800
```

## Cell 40

```python
core_checks = {
    "split_isolation": split_report["group_overlap"] == 0,
    "baseline_valid": 0.0 <= baseline_val_f1 <= 1.0,
    "training_ran": train_steps >= 1,
    "transformer_weights_updated": any(
        parameter.requires_grad for parameter in model.base_model.parameters()
    ),
    "loss_is_finite": all(math.isfinite(value) for value in losses),
    "validation_valid": 0.0 <= transformer_val_f1 <= 1.0,
    "baseline_comparison_recorded": math.isfinite(validation_delta),
    "result_is_honest": results["result_type"] == "MEASURED_SMOKE",
    "bilingual_data": {"ar", "en"} <= {row["language"] for row in rows},
}
for name, passed in core_checks.items():
    print(f"{name}: {'PASS' if passed else 'FAIL'}")
assert all(core_checks.values())
print("DAY2_NOTEBOOK3_CORE=PASS")
```

Saved output:

```text
split_isolation: PASS
baseline_valid: PASS
training_ran: PASS
transformer_weights_updated: PASS
loss_is_finite: PASS
validation_valid: PASS
baseline_comparison_recorded: PASS
result_is_honest: PASS
bilingual_data: PASS
DAY2_NOTEBOOK3_CORE=PASS

```

## Cell 41

```python
# اليوم الثاني — المختبر 3B: NER و Extractive QA

في هذا الجزء سأكمل مهام اليوم الثاني المتعلقة بـ:
- التعرف على الكيانات المسماة NER
- الإجابة الاستخراجية عن الأسئلة Extractive QA
- التحقق من النتائج والوصول إلى علامة النجاح المطلوبة
```

Saved output:

```text

```

## Cell 42

```python
import importlib.metadata
import importlib.util
import subprocess
import sys

REQUIRED = {
    "transformers": "5.15.1",
    "tokenizers": "0.22.2",
    "scikit-learn": "1.9.0",
}

needs_install = []

for distribution, expected in REQUIRED.items():
    try:
        current = importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        current = None

    if current != expected:
        needs_install.append(
            f"{distribution}=={expected}"
        )

if needs_install:
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            *needs_install
        ]
    )

if importlib.util.find_spec("torch") is None:
    raise RuntimeError(
        "PyTorch is required. Open this notebook in Google Colab."
    )

print("Environment ready / البيئة جاهزة")
```

Saved output:

```text
Environment ready / البيئة جاهزة

```

## Cell 43

```python
import gc
import json
import math
import os
import random
import urllib.request
from pathlib import Path

import numpy as np
import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from transformers import (
    AutoModelForQuestionAnswering,
    AutoModelForTokenClassification,
    AutoTokenizer,
    DataCollatorForTokenClassification,
)

os.environ["TOKENIZERS_PARALLELISM"] = "false"
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_ID = "distilbert/distilbert-base-multilingual-cased"
TRAINING_MODE = "full_finetune" if DEVICE.type == "cuda" else "partial_finetune_cpu"
print("Device:", DEVICE)
print("Training mode:", TRAINING_MODE)
```

Saved output:

```text
Device: cpu
Training mode: partial_finetune_cpu

```

## Cell 44

```python
NER_URL = "https://raw.githubusercontent.com/almiyead-rgb/bayan-applied-nlp-course/main/data/sample/bayan_day2_ner.jsonl"
NER_FALLBACK = [{"split":"train","language":"ar","tokens":["تعطلت","بوابة","التصاريح","في","الرياض"],"ner_tags":["O","B-SERVICE","I-SERVICE","O","B-LOCATION"]},{"split":"train","language":"en","tokens":["The","permit","portal","failed","in","Riyadh"],"ner_tags":["O","B-SERVICE","I-SERVICE","O","O","B-LOCATION"]},{"split":"train","language":"ar","tokens":["المرجع","BAYAN-204","بتاريخ","2026-08-20"],"ner_tags":["O","B-REF_NUM","O","B-DATE"]},{"split":"train","language":"en","tokens":["Reference","BAYAN-205","was","created","today"],"ner_tags":["O","B-REF_NUM","O","O","B-DATE"]},{"split":"train","language":"ar","tokens":["راجعت","وزارة","الصحة","أمس"],"ner_tags":["O","B-ORG","I-ORG","B-DATE"]},{"split":"train","language":"en","tokens":["The","Ministry","of","Health","replied","yesterday"],"ner_tags":["O","B-ORG","I-ORG","I-ORG","O","B-DATE"]},{"split":"train","language":"ar","tokens":["تعطل","تطبيق","المواعيد","في","جدة"],"ner_tags":["O","B-SERVICE","I-SERVICE","O","B-LOCATION"]},{"split":"train","language":"en","tokens":["The","appointments","app","failed","in","Jeddah"],"ner_tags":["O","B-SERVICE","I-SERVICE","O","O","B-LOCATION"]},{"split":"validation","language":"ar","tokens":["رقم","الطلب","BAYAN-301","في","الدمام"],"ner_tags":["O","O","B-REF_NUM","O","B-LOCATION"]},{"split":"validation","language":"en","tokens":["Case","BAYAN-302","belongs","to","the","transport","service"],"ner_tags":["O","B-REF_NUM","O","O","O","B-SERVICE","I-SERVICE"]},{"split":"test","language":"ar","tokens":["أرسلت","البلدية","الرد","يوم","الأحد"],"ner_tags":["O","B-ORG","O","O","B-DATE"]},{"split":"test","language":"en","tokens":["The","digital","service","is","available","in","Makkah"],"ner_tags":["O","B-SERVICE","I-SERVICE","O","O","O","B-LOCATION"]}]
try:
    with urllib.request.urlopen(NER_URL, timeout=20) as response:
        ner_rows = [
            json.loads(line) for line in response.read().decode("utf-8").splitlines()
            if line.strip()
        ]
    NER_DATA_SOURCE = "github_course_file"
except Exception as exc:
    ner_rows = NER_FALLBACK
    NER_DATA_SOURCE = f"embedded_fallback:{type(exc).__name__}"

LABELS = [
    "O", "B-SERVICE", "I-SERVICE", "B-LOCATION", "I-LOCATION",
    "B-DATE", "I-DATE", "B-REF_NUM", "I-REF_NUM", "B-ORG", "I-ORG",
]
label2id = {label: index for index, label in enumerate(LABELS)}
id2label = {index: label for label, index in label2id.items()}
for row in ner_rows:
    assert len(row["tokens"]) == len(row["ner_tags"])
    assert set(row["ner_tags"]) <= set(LABELS)
print("NER source:", NER_DATA_SOURCE, "rows:", len(ner_rows))
```

Saved output:

```text
NER source: github_course_file rows: 12

```

## Cell 45

```python
def align_word_labels(word_ids, word_labels, ignore_index=-100):
    aligned = []
    previous = None
    for word_id in word_ids:
        if word_id is None:
            aligned.append(ignore_index)
        else:
            if word_id < 0 or word_id >= len(word_labels):
                raise ValueError(f"word id out of range: {word_id}")
            aligned.append(word_labels[word_id] if word_id != previous else ignore_index)
        previous = word_id
    return aligned

alignment_example = align_word_labels(
    [None, 0, 1, 1, 2, None], [0, 3, 0]
)
print(alignment_example)
assert alignment_example == [-100, 0, 3, -100, 0, -100]
print("NER alignment contract=PASS")
```

Saved output:

```text
[-100, 0, 3, -100, 0, -100]
NER alignment contract=PASS

```

## Cell 46

```python
def bio_entities(tags):
    entities, current_type, start = set(), None, -1
    for index, tag in enumerate(list(tags) + ["O"]):
        if tag == "O":
            if current_type is not None:
                entities.add((current_type, start, index))
            current_type, start = None, -1
            continue
        prefix, entity_type = tag.split("-", 1)
        if prefix == "B" or current_type != entity_type:
            if current_type is not None:
                entities.add((current_type, start, index))
            current_type, start = entity_type, index
    return entities


def entity_report(true_sequences, predicted_sequences):
    gold, predicted = set(), set()
    for sequence_id, (truth, guess) in enumerate(zip(true_sequences, predicted_sequences)):
        gold |= {(sequence_id, *span) for span in bio_entities(truth)}
        predicted |= {(sequence_id, *span) for span in bio_entities(guess)}
    tp, fp, fn = len(gold & predicted), len(predicted - gold), len(gold - predicted)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1,
            "true_entities": len(gold), "predicted_entities": len(predicted)}

boundary_test = entity_report(
    [["B-ORG", "I-ORG", "O"]],
    [["B-ORG", "O", "O"]],
)
assert boundary_test["f1"] == 0.0
print("Strict entity-boundary test=PASS")
```

Saved output:

```text
Strict entity-boundary test=PASS

```

## Cell 47

```python
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)
    ner_model = AutoModelForTokenClassification.from_pretrained(
        MODEL_ID,
        num_labels=len(LABELS),
        label2id=label2id,
        id2label=id2label,
    )
except Exception as exc:
    raise RuntimeError(
        "Checkpoint download failed. No API key is required; reconnect and retry once."
    ) from exc

if TRAINING_MODE == "partial_finetune_cpu":
    for parameter in ner_model.base_model.parameters():
        parameter.requires_grad = False
    for parameter in ner_model.base_model.transformer.layer[-1].parameters():
        parameter.requires_grad = True
ner_model.to(DEVICE)
print("NER model ready")
```

Saved output:

```text
Loading weights:   0%|          | 0/100 [00:00<?, ?it/s]
NER model ready

```

## Cell 48

```python
def encode_ner(row):
    encoded = tokenizer(
        row["tokens"],
        is_split_into_words=True,
        truncation=True,
        max_length=64,
    )
    word_labels = [label2id[tag] for tag in row["ner_tags"]]
    encoded["labels"] = align_word_labels(encoded.word_ids(), word_labels)
    return dict(encoded)

ner_train = [encode_ner(row) for row in ner_rows if row["split"] == "train"]
ner_test_rows = [row for row in ner_rows if row["split"] == "test"]
collator = DataCollatorForTokenClassification(tokenizer=tokenizer)
generator = torch.Generator().manual_seed(SEED)
ner_loader = DataLoader(
    ner_train, batch_size=2, shuffle=True,
    collate_fn=collator, generator=generator,
)

first = next(iter(ner_loader))
assert (first["labels"] == -100).any()
print("NER features and padding=PASS")
```

Saved output:

```text
NER features and padding=PASS

```

## Cell 49

```python
NER_EPOCHS = 2 if TRAINING_MODE == "full_finetune" else 12
ner_lr = 2e-5 if TRAINING_MODE == "full_finetune" else 1e-4
ner_optimizer = AdamW(
    [p for p in ner_model.parameters() if p.requires_grad], lr=ner_lr
)
ner_losses = []
ner_steps = 0
for epoch_index in range(NER_EPOCHS):
    epoch_loader = DataLoader(
        ner_train, batch_size=2, shuffle=True, collate_fn=collator,
        generator=torch.Generator().manual_seed(SEED + epoch_index + 1),
    )
    ner_model.train()
    epoch_losses = []
    for batch in epoch_loader:
        batch = {key: value.to(DEVICE) for key, value in batch.items()}
        ner_optimizer.zero_grad(set_to_none=True)
        output = ner_model(**batch)
        loss = output.loss
        if not torch.isfinite(loss):
            raise RuntimeError("Non-finite NER loss")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            [p for p in ner_model.parameters() if p.requires_grad], 1.0
        )
        ner_optimizer.step()
        loss_value = float(loss.detach().cpu())
        ner_losses.append(loss_value)
        epoch_losses.append(loss_value)
        ner_steps += 1
    print(f"NER epoch={epoch_index + 1:02d} mean_loss={np.mean(epoch_losses):.4f}")
assert ner_steps >= 1
assert any(parameter.requires_grad for parameter in ner_model.base_model.parameters())
print("NER optimizer steps=PASS", {"epochs": NER_EPOCHS, "steps": ner_steps})
```

Saved output:

```text
NER epoch=01 mean_loss=2.2637
NER epoch=02 mean_loss=1.8038
NER epoch=03 mean_loss=1.5641
NER epoch=04 mean_loss=1.3335
NER epoch=05 mean_loss=1.0610
NER epoch=06 mean_loss=0.7984
NER epoch=07 mean_loss=0.6044
NER epoch=08 mean_loss=0.4012
NER epoch=09 mean_loss=0.2601
NER epoch=10 mean_loss=0.1418
NER epoch=11 mean_loss=0.0711
NER epoch=12 mean_loss=0.0427
NER optimizer steps=PASS {'epochs': 12, 'steps': 48}

```

## Cell 50

```python
def predict_ner(rows):
    truths, predictions = [], []
    ner_model.eval()
    with torch.no_grad():
        for row in rows:
            feature = encode_ner(row)
            batch = collator([feature])
            labels = batch["labels"][0].tolist()
            model_inputs = {
                key: value.to(DEVICE) for key, value in batch.items()
                if key != "labels"
            }
            pred_ids = ner_model(**model_inputs).logits.argmax(-1)[0].cpu().tolist()
            keep = [index for index, label in enumerate(labels) if label != -100]
            truths.append([id2label[labels[index]] for index in keep])
            predictions.append([id2label[pred_ids[index]] for index in keep])
    return truths, predictions

ner_truth, ner_predictions = predict_ner(ner_test_rows)
ner_metrics = entity_report(ner_truth, ner_predictions)
print("NER entity metrics (MEASURED_SMOKE):")
print(json.dumps(ner_metrics, indent=2))
assert 0.0 <= ner_metrics["f1"] <= 1.0
```

Saved output:

```text
NER entity metrics (MEASURED_SMOKE):
{
  "precision": 0.6666666666666666,
  "recall": 0.5,
  "f1": 0.5714285714285715,
  "true_entities": 4,
  "predicted_entities": 3
}

```

## Cell 51

```python
del ner_optimizer
ner_model.to("cpu")
del ner_model
gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()
print("NER model released / تم تحرير نموذج NER")
```

Saved output:

```text
NER model released / تم تحرير نموذج NER

```

## Cell 52

```python
QA_URL = "https://raw.githubusercontent.com/almiyead-rgb/bayan-applied-nlp-course/main/data/sample/bayan_day2_qa.json"
QA_FALLBACK = [{"split":"train","language":"ar","context":"يمكن تجديد التصريح إلكترونيا من بوابة الخدمات بعد تسجيل الدخول.","question":"من أين يمكن تجديد التصريح؟","answer_text":"بوابة الخدمات","id":"Q-001","answer_start":32},{"split":"train","language":"en","context":"A clinic appointment can be rescheduled through the appointments service.","question":"Where can the clinic appointment be rescheduled?","answer_text":"the appointments service","id":"Q-002","answer_start":48},{"split":"train","language":"ar","context":"يعمل مركز الدعم من الساعة الثامنة صباحا حتى الرابعة مساء.","question":"متى يبدأ عمل مركز الدعم؟","answer_text":"الساعة الثامنة صباحا","id":"Q-003","answer_start":19},{"split":"train","language":"en","context":"Bus route updates are published every Monday on the transport portal.","question":"When are bus route updates published?","answer_text":"every Monday","id":"Q-004","answer_start":32},{"split":"train","language":"ar","context":"تظهر حالة الطلب في صفحة طلباتي بعد إدخال رقم المرجع.","question":"أين تظهر حالة الطلب؟","answer_text":"صفحة طلباتي","id":"Q-005","answer_start":19},{"split":"train","language":"en","context":"The verification code remains valid for five minutes.","question":"How long is the verification code valid?","answer_text":"five minutes","id":"Q-006","answer_start":40},{"split":"validation","language":"ar","context":"يمكن تقديم بلاغ النقل عبر التطبيق أو مركز الاتصال.","question":"كيف يمكن تقديم بلاغ النقل؟","answer_text":"عبر التطبيق أو مركز الاتصال","id":"Q-007","answer_start":22},{"split":"validation","language":"en","context":"Permit documents must be uploaded as PDF files.","question":"Which file format is required?","answer_text":"PDF","id":"Q-008","answer_start":37},{"split":"test","language":"ar","context":"تعمل العيادة من الأحد إلى الخميس.","question":"ما رقم هاتف العيادة؟","answer_text":None,"id":"Q-009","answer_start":None},{"split":"test","language":"en","context":"The digital portal supports Arabic and English.","question":"What is the annual fee?","answer_text":None,"id":"Q-010","answer_start":None}]
try:
    with urllib.request.urlopen(QA_URL, timeout=20) as response:
        qa_rows = json.loads(response.read().decode("utf-8"))["examples"]
    QA_DATA_SOURCE = "github_course_file"
except Exception as exc:
    qa_rows = QA_FALLBACK
    QA_DATA_SOURCE = f"embedded_fallback:{type(exc).__name__}"

for row in qa_rows:
    if row["answer_text"] is not None:
        start = row["answer_start"]
        assert row["context"][start:start + len(row["answer_text"])] == row["answer_text"]
print("QA source:", QA_DATA_SOURCE, "rows:", len(qa_rows))
print("No-answer examples:", sum(row["answer_text"] is None for row in qa_rows))
```

Saved output:

```text
QA source: github_course_file rows: 10
No-answer examples: 2

```

## Cell 53

```python
def prepare_qa_batch(examples):
    encoded = tokenizer(
        [row["question"].strip() for row in examples],
        [row["context"] for row in examples],
        padding=True,
        truncation="only_second",
        max_length=96,
        return_offsets_mapping=True,
        return_tensors="pt",
    )
    offset_mapping = encoded.pop("offset_mapping")
    starts, ends = [], []
    for index, row in enumerate(examples):
        sequence_ids = encoded.sequence_ids(index)
        offsets = offset_mapping[index].tolist()
        cls_candidates = (encoded["input_ids"][index] == tokenizer.cls_token_id).nonzero()
        cls_index = int(cls_candidates[0].item()) if len(cls_candidates) else 0
        if row["answer_text"] is None:
            starts.append(cls_index)
            ends.append(cls_index)
            continue

        answer_start = int(row["answer_start"])
        answer_end = answer_start + len(row["answer_text"])
        context_indexes = [i for i, sid in enumerate(sequence_ids) if sid == 1]
        context_start, context_end = context_indexes[0], context_indexes[-1]
        if offsets[context_start][0] > answer_start or offsets[context_end][1] < answer_end:
            starts.append(cls_index)
            ends.append(cls_index)
            continue
        while context_start <= context_end and offsets[context_start][0] <= answer_start:
            context_start += 1
        while context_end >= 0 and offsets[context_end][1] >= answer_end:
            context_end -= 1
        starts.append(context_start - 1)
        ends.append(context_end + 1)

    encoded["start_positions"] = torch.tensor(starts, dtype=torch.long)
    encoded["end_positions"] = torch.tensor(ends, dtype=torch.long)
    return encoded

qa_train_rows = [row for row in qa_rows if row["split"] == "train"]
qa_features = prepare_qa_batch(qa_train_rows)
assert qa_features["start_positions"].shape[0] == len(qa_train_rows)
print("QA offsets-to-token positions=PASS")
```

Saved output:

```text
QA offsets-to-token positions=PASS

```

## Cell 54

```python
try:
    qa_model = AutoModelForQuestionAnswering.from_pretrained(MODEL_ID)
except Exception as exc:
    raise RuntimeError("QA model head could not be loaded.") from exc
if TRAINING_MODE == "partial_finetune_cpu":
    for parameter in qa_model.base_model.parameters():
        parameter.requires_grad = False
    for parameter in qa_model.base_model.transformer.layer[-1].parameters():
        parameter.requires_grad = True
qa_model.to(DEVICE)
QA_STEPS = 1 if TRAINING_MODE == "full_finetune" else 3
qa_lr = 2e-5 if TRAINING_MODE == "full_finetune" else 1e-4
qa_optimizer = AdamW(
    [p for p in qa_model.parameters() if p.requires_grad], lr=qa_lr
)
qa_batch = {key: value.to(DEVICE) for key, value in qa_features.items()}
qa_losses = []
for step_index in range(QA_STEPS):
    qa_model.train()
    qa_optimizer.zero_grad(set_to_none=True)
    qa_output = qa_model(**qa_batch)
    qa_loss = qa_output.loss
    assert torch.isfinite(qa_loss)
    qa_loss.backward()
    torch.nn.utils.clip_grad_norm_(
        [p for p in qa_model.parameters() if p.requires_grad], 1.0
    )
    qa_optimizer.step()
    qa_losses.append(float(qa_loss.detach().cpu()))
    print(f"QA step={step_index + 1} loss={qa_losses[-1]:.4f}")
qa_loss_value = float(np.mean(qa_losses))
qa_steps = len(qa_losses)
assert any(parameter.requires_grad for parameter in qa_model.base_model.parameters())
print("QA optimizer steps=PASS", {"steps": qa_steps})
```

Saved output:

```text
Loading weights:   0%|          | 0/100 [00:00<?, ?it/s]
QA step=1 loss=3.7731
QA step=2 loss=3.6224
QA step=3 loss=3.5397
QA optimizer steps=PASS {'steps': 3}

```

## Cell 55

```python
def best_span(start_logits, end_logits, offsets, context,
              null_threshold=0.0, max_answer_length=48, top_k=20):
    if not start_logits or len(start_logits) != len(end_logits) or len(offsets) != len(start_logits):
        raise ValueError("logits and offsets must have the same non-zero length")
    null_score = float(start_logits[0]) + float(end_logits[0])
    starts = sorted(range(len(start_logits)), key=lambda i: start_logits[i], reverse=True)[:top_k]
    ends = sorted(range(len(end_logits)), key=lambda i: end_logits[i], reverse=True)[:top_k]
    best = None
    for start in starts:
        for end in ends:
            if start == 0 or end == 0 or end < start or end - start + 1 > max_answer_length:
                continue
            if offsets[start] is None or offsets[end] is None:
                continue
            char_start, char_end = offsets[start][0], offsets[end][1]
            if char_end <= char_start or char_end > len(context):
                continue
            score = float(start_logits[start]) + float(end_logits[end])
            if best is None or score > best["score"]:
                best = {"answer": context[char_start:char_end], "score": score,
                        "start": char_start, "end": char_end}
    if best is None:
        return {"answer": None, "reason": "no_valid_span", "margin": float("inf")}
    margin = null_score - best["score"]
    if margin > null_threshold:
        return {"answer": None, "reason": "no_answer_in_context", "margin": margin}
    return {**best, "null_margin": margin}

context = "الخدمة متاحة في الرياض"
offsets = [None, (0, 6), (7, 12), (13, 15), (16, 22)]
span_result = best_span(
    [0.0, 0.1, 0.1, 0.2, 4.0],
    [0.0, 0.1, 0.1, 0.2, 4.5],
    offsets,
    context,
)
null_result = best_span(
    [5.0, 1.0, 2.0], [5.0, 1.0, 2.0],
    [None, (0, 6), (7, 12)], "الخدمة متاحة",
)
print("Valid span:", span_result)
print("No answer:", null_result)
assert span_result["answer"] == "الرياض"
assert null_result["answer"] is None
assert null_result["reason"] == "no_answer_in_context"
print("QA post-processing tests=PASS")
```

Saved output:

```text
Valid span: {'answer': 'الرياض', 'score': 8.5, 'start': 16, 'end': 22, 'null_margin': -8.5}
No answer: {'answer': None, 'reason': 'no_answer_in_context', 'margin': 6.0}
QA post-processing tests=PASS

```

## Cell 56

```python
qa_validation = next(row for row in qa_rows if row["split"] == "validation")
qa_model.eval()
inference = tokenizer(
    qa_validation["question"], qa_validation["context"],
    truncation="only_second", max_length=96,
    return_offsets_mapping=True, return_tensors="pt",
)
sequence_ids = inference.sequence_ids(0)
raw_offsets = inference.pop("offset_mapping")[0].tolist()
context_offsets = [tuple(offset) if sequence_ids[i] == 1 else None
                   for i, offset in enumerate(raw_offsets)]
with torch.no_grad():
    model_inputs = {key: value.to(DEVICE) for key, value in inference.items()}
    logits = qa_model(**model_inputs)
model_span = best_span(
    logits.start_logits[0].cpu().tolist(),
    logits.end_logits[0].cpu().tolist(),
    context_offsets,
    qa_validation["context"],
)
print("Unscored model span (SMOKE ONLY):", model_span)
```

Saved output:

```text
Unscored model span (SMOKE ONLY): {'answer': 'اغ النقل عبر التطبيق أو مركز الاتصال', 'score': 0.4323903098702431, 'start': 13, 'end': 49, 'null_margin': -0.14094754308462143}

```

## Cell 57

```python
results = {
    "result_type": "MEASURED_SMOKE",
    "model_id": MODEL_ID,
    "device": str(DEVICE),
    "training_mode": TRAINING_MODE,
    "seed": SEED,
    "ner_data_source": NER_DATA_SOURCE,
    "ner_steps": ner_steps,
    "ner_epochs": NER_EPOCHS,
    "ner_mean_loss": float(np.mean(ner_losses)),
    "ner_entity_metrics": ner_metrics,
    "qa_data_source": QA_DATA_SOURCE,
    "qa_steps": qa_steps,
    "qa_loss": qa_loss_value,
    "qa_span_test": span_result,
    "qa_null_test": null_result,
    "limitations": [
        "synthetic tiny datasets",
        "short training smoke",
        "NER and QA quality are not production estimates",
    ],
}
Path("day2_ner_qa_metrics.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps(results, ensure_ascii=False, indent=2))
```

Saved output:

```text
{
  "result_type": "MEASURED_SMOKE",
  "model_id": "distilbert/distilbert-base-multilingual-cased",
  "device": "cpu",
  "training_mode": "partial_finetune_cpu",
  "seed": 42,
  "ner_data_source": "github_course_file",
  "ner_steps": 48,
  "ner_epochs": 12,
  "ner_mean_loss": 0.862140710077559,
  "ner_entity_metrics": {
    "precision": 0.6666666666666666,
    "recall": 0.5,
    "f1": 0.5714285714285715,
    "true_entities": 4,
    "predicted_entities": 3
  },
  "qa_data_source": "github_course_file",
  "qa_steps": 3,
  "qa_loss": 3.6450522740681968,
  "qa_span_test": {
    "answer": "الرياض",
    "score": 8.5,
    "start": 16,
    "end": 22,
    "null_margin": -8.5
  },
  "qa_null_test": {
    "answer": null,
    "reason": "no_answer_in_context",
    "margin": 6.0
  },
  "limitations": [
    "synthetic tiny datasets",
    "short training smoke",
    "NER and QA quality are not production estimates"
  ]
}

```

## Cell 58

```python
core_checks = {
    "alignment": alignment_example == [-100, 0, 3, -100, 0, -100],
    "strict_boundaries": boundary_test["f1"] == 0.0,
    "ner_training_ran": ner_steps >= 1,
    "transformer_finetune_mode": TRAINING_MODE in {
        "full_finetune", "partial_finetune_cpu"
    },
    "ner_loss_finite": all(math.isfinite(value) for value in ner_losses),
    "ner_metric_valid": 0.0 <= ner_metrics["f1"] <= 1.0,
    "qa_training_ran": qa_steps >= 1,
    "qa_loss_finite": math.isfinite(qa_loss_value),
    "valid_span": span_result["answer"] == "الرياض",
    "honest_null": null_result["answer"] is None,
    "honest_label": results["result_type"] == "MEASURED_SMOKE",
}
for name, passed in core_checks.items():
    print(f"{name}: {'PASS' if passed else 'FAIL'}")
assert all(core_checks.values())
print("DAY2_NOTEBOOK4_CORE=PASS")
```

Saved output:

```text
alignment: PASS
strict_boundaries: PASS
ner_training_ran: PASS
transformer_finetune_mode: PASS
ner_loss_finite: PASS
ner_metric_valid: PASS
qa_training_ran: PASS
qa_loss_finite: PASS
valid_span: PASS
honest_null: PASS
honest_label: PASS
DAY2_NOTEBOOK4_CORE=PASS

```

## Cell 59

```python
# اليوم الثالث — البحث الدلالي

في هذا الجزء سأكمل مختبر البحث الدلالي Semantic Search، ويتضمن:
- إنشاء تمثيلات الجمل Sentence Embeddings
- التطبيع L2 Normalization
- بناء فهرس FAISS
- اختبار البحث والاسترجاع
- تقييم الأداء باستخدام Recall@3 و MRR@3
```

Saved output:

```text

```

## Cell 60

```python
import importlib.metadata
import subprocess
import sys

REQUIRED = {
    "camel-tools": "1.6.0",
    "sentence-transformers": "6.0.0",
    "faiss-cpu": "1.15.0",
    "transformers": "5.15.1",
    "tokenizers": "0.22.2",
}
to_install = []
for distribution, expected in REQUIRED.items():
    try:
        current = importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        current = None
    if current != expected:
        to_install.append(f"{distribution}=={expected}")
if to_install:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", *to_install]
    )
for distribution, expected in REQUIRED.items():
    assert importlib.metadata.version(distribution) == expected
print("SETUP=PASS", {name: importlib.metadata.version(name) for name in REQUIRED})

```

Saved output:

```text
SETUP=PASS {'camel-tools': '1.6.0', 'sentence-transformers': '6.0.0', 'faiss-cpu': '1.15.0', 'transformers': '5.15.1', 'tokenizers': '0.22.2'}

```

## Cell 61

```python
import csv
import hashlib
import io
import json
import urllib.request
import statistics
import time
from collections import defaultdict
from pathlib import Path

import faiss
import numpy as np
import torch
from camel_tools.utils.dediac import dediac_ar
from camel_tools.utils.normalize import (
    normalize_alef_ar,
    normalize_alef_maksura_ar,
    normalize_unicode,
)
from sentence_transformers import SentenceTransformer

DATA_KIND = "MEASURED_SMOKE"
MODEL_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
K = 3
print("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")

```

Saved output:

```text
DEVICE cpu

```

## Cell 62

```python
CASES_URL = "https://raw.githubusercontent.com/almiyead-rgb/bayan-applied-nlp-course/main/data/sample/bayan_day3_cases.csv"
QUERIES_URL = "https://raw.githubusercontent.com/almiyead-rgb/bayan-applied-nlp-course/main/data/sample/bayan_day3_queries.jsonl"
CASES_FALLBACK = [{'case_id': 'AR-001', 'language': 'ar', 'variant': 'MSA', 'topic': 'digital_service', 'summary': 'تعذر تسجيل الدخول إلى البوابة بعد تحديث كلمة المرور', 'resolution': 'تمت إعادة مزامنة الحساب وإرسال رابط دخول جديد'}, {'case_id': 'AR-002', 'language': 'ar', 'variant': 'Gulf', 'topic': 'digital_service', 'summary': 'ما وصل رمز التحقق للجوال عند محاولة الدخول', 'resolution': 'تم تحديث رقم التواصل وإعادة إرسال الرمز'}, {'case_id': 'AR-003', 'language': 'ar', 'variant': 'MSA', 'topic': 'digital_service', 'summary': 'يفشل رفع ملف PDF في صفحة الطلب', 'resolution': 'تم ضغط الملف وتغيير اسمه ثم اكتمل الرفع'}, {'case_id': 'AR-004', 'language': 'ar', 'variant': 'Gulf', 'topic': 'transport', 'summary': 'الباص تأخر عن المحطة أكثر من نصف ساعة', 'resolution': 'تمت إضافة رحلة بديلة وإشعار المستفيدين'}, {'case_id': 'AR-005', 'language': 'ar', 'variant': 'MSA', 'topic': 'transport', 'summary': 'لا يظهر مسار الحافلة الجديد في التطبيق', 'resolution': 'تم تحديث بيانات المسار وإعادة تحميل الخريطة'}, {'case_id': 'AR-006', 'language': 'ar', 'variant': 'Gulf', 'topic': 'transport', 'summary': 'موقع موقف الحافلة غير واضح في الحي', 'resolution': 'تم إرسال رابط الموقع وإضافة لوحة إرشادية'}, {'case_id': 'AR-007', 'language': 'ar', 'variant': 'MSA', 'topic': 'health', 'summary': 'لا توجد مواعيد متاحة في العيادة المطلوبة', 'resolution': 'تم فتح قائمة انتظار واقتراح عيادة قريبة'}, {'case_id': 'AR-008', 'language': 'ar', 'variant': 'Gulf', 'topic': 'health', 'summary': 'نتيجة التحليل ما ظهرت في التطبيق الصحي', 'resolution': 'تمت مزامنة النتيجة مع الملف الصحي'}, {'case_id': 'AR-009', 'language': 'ar', 'variant': 'MSA', 'topic': 'health', 'summary': 'تعذر تجديد الوصفة من خلال التطبيق', 'resolution': 'تم التحقق من الأهلية وإعادة تفعيل طلب التجديد'}, {'case_id': 'AR-010', 'language': 'ar', 'variant': 'MSA', 'topic': 'permit', 'summary': 'رُفض المستند المرفق بطلب التصريح', 'resolution': 'تم توضيح صيغة المستند وإعادة فتح الطلب للرفع'}, {'case_id': 'AR-011', 'language': 'ar', 'variant': 'Gulf', 'topic': 'permit', 'summary': 'طلب التصريح واقف عند المراجعة من أسبوع', 'resolution': 'تم تصعيد الطلب وتحديث الحالة في اليوم التالي'}, {'case_id': 'AR-012', 'language': 'ar', 'variant': 'MSA', 'topic': 'permit', 'summary': 'تم احتساب رسوم التصريح مرتين', 'resolution': 'أعيد المبلغ المكرر وثُبتت عملية دفع واحدة'}, {'case_id': 'EN-001', 'language': 'en', 'variant': 'English', 'topic': 'digital_service', 'summary': 'Cannot sign in to the portal after changing the password', 'resolution': 'The account was resynchronised and a new sign-in link was sent'}, {'case_id': 'EN-002', 'language': 'en', 'variant': 'English', 'topic': 'digital_service', 'summary': 'The verification code never arrived on the registered phone', 'resolution': 'The contact number was verified and the code was resent'}, {'case_id': 'EN-003', 'language': 'en', 'variant': 'English', 'topic': 'digital_service', 'summary': 'The portal rejects a PDF attachment during upload', 'resolution': 'The file was compressed and renamed before a successful upload'}, {'case_id': 'EN-004', 'language': 'en', 'variant': 'English', 'topic': 'transport', 'summary': 'The bus arrived more than thirty minutes late', 'resolution': 'An additional trip was assigned and passengers were notified'}, {'case_id': 'EN-005', 'language': 'en', 'variant': 'English', 'topic': 'transport', 'summary': 'The new bus route is missing from the mobile map', 'resolution': 'The route dataset was refreshed and the map was reloaded'}, {'case_id': 'EN-006', 'language': 'en', 'variant': 'English', 'topic': 'transport', 'summary': 'The location of the neighbourhood bus stop is unclear', 'resolution': 'A location link was sent and a sign was added'}, {'case_id': 'EN-007', 'language': 'en', 'variant': 'English', 'topic': 'health', 'summary': 'No appointments are available at the requested clinic', 'resolution': 'A waiting list was opened and a nearby clinic was suggested'}, {'case_id': 'EN-008', 'language': 'en', 'variant': 'English', 'topic': 'health', 'summary': 'The laboratory result is missing from the health application', 'resolution': 'The result was synchronised with the health record'}, {'case_id': 'EN-009', 'language': 'en', 'variant': 'English', 'topic': 'health', 'summary': 'The prescription renewal action fails in the application', 'resolution': 'Eligibility was checked and the renewal request was reactivated'}, {'case_id': 'EN-010', 'language': 'en', 'variant': 'English', 'topic': 'permit', 'summary': 'The permit request rejected the uploaded document', 'resolution': 'The required format was explained and upload was reopened'}, {'case_id': 'EN-011', 'language': 'en', 'variant': 'English', 'topic': 'permit', 'summary': 'The permit status has remained under review for a week', 'resolution': 'The request was escalated and its status was updated the next day'}, {'case_id': 'EN-012', 'language': 'en', 'variant': 'English', 'topic': 'permit', 'summary': 'The permit fee was charged twice', 'resolution': 'The duplicate amount was refunded and one payment was retained'}]
QUERIES_FALLBACK = [{'query_id': 'QV-001', 'split': 'validation', 'query': 'ما وصلني كود الدخول على الجوال', 'language': 'ar', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['AR-002']}, {'query_id': 'QV-002', 'split': 'validation', 'query': 'The portal will not accept my PDF file', 'language': 'en', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['EN-003']}, {'query_id': 'QV-003', 'split': 'validation', 'query': 'The bus was over thirty minutes late', 'language': 'en', 'retrieval_mode': 'cross_lingual', 'relevant_case_ids': ['AR-004']}, {'query_id': 'QV-004', 'split': 'validation', 'query': 'انخصمت رسوم التصريح مرتين', 'language': 'ar', 'retrieval_mode': 'cross_lingual', 'relevant_case_ids': ['EN-012']}, {'query_id': 'QV-005', 'split': 'validation', 'query': 'أحتاج موعد عيادة ولا يوجد وقت متاح', 'language': 'ar', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['AR-007']}, {'query_id': 'QV-006', 'split': 'validation', 'query': 'My permit has been under review for a week', 'language': 'en', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['EN-011']}, {'query_id': 'QV-007', 'split': 'validation', 'query': 'ما ساعات عمل المكتبة؟', 'language': 'ar', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}, {'query_id': 'QV-008', 'split': 'validation', 'query': "What is tomorrow's weather?", 'language': 'en', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}, {'query_id': 'QV-009', 'split': 'validation', 'query': 'أرغب في التقديم على وظيفة', 'language': 'ar', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}, {'query_id': 'QV-010', 'split': 'validation', 'query': 'Where can I renew my passport?', 'language': 'en', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}, {'query_id': 'QT-001', 'split': 'test', 'query': 'رمز التحقق لا يصل لهاتفي', 'language': 'ar', 'retrieval_mode': 'cross_lingual', 'relevant_case_ids': ['EN-002']}, {'query_id': 'QT-002', 'split': 'test', 'query': 'The new route is absent from the map', 'language': 'en', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['EN-005']}, {'query_id': 'QT-003', 'split': 'test', 'query': 'نتيجة المختبر غير موجودة في الملف الصحي', 'language': 'ar', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['AR-008']}, {'query_id': 'QT-004', 'split': 'test', 'query': 'The uploaded permit document was refused', 'language': 'en', 'retrieval_mode': 'cross_lingual', 'relevant_case_ids': ['AR-010']}, {'query_id': 'QT-005', 'split': 'test', 'query': 'وين موقع موقف الباص في الحي؟', 'language': 'ar', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['AR-006']}, {'query_id': 'QT-006', 'split': 'test', 'query': 'I cannot renew my prescription in the app', 'language': 'en', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['EN-009']}, {'query_id': 'QT-007', 'split': 'test', 'query': 'أحتاج وصفة طبخ سريعة', 'language': 'ar', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}, {'query_id': 'QT-008', 'split': 'test', 'query': 'How do I reserve a football field?', 'language': 'en', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}]

def load_course_data():
    try:
        with urllib.request.urlopen(CASES_URL, timeout=15) as response:
            cases = list(csv.DictReader(io.StringIO(response.read().decode("utf-8"))))
        with urllib.request.urlopen(QUERIES_URL, timeout=15) as response:
            queries = [json.loads(line) for line in response.read().decode("utf-8").splitlines() if line.strip()]
        return cases, queries, "github"
    except Exception as exc:
        return CASES_FALLBACK, QUERIES_FALLBACK, f"embedded_fallback:{type(exc).__name__}"

cases, queries, data_source = load_course_data()
assert len(cases) == 24 and len(queries) == 18
assert len({row["case_id"] for row in cases}) == len(cases)
assert {row["split"] for row in queries} == {"validation", "test"}
assert all(isinstance(row["relevant_case_ids"], list) for row in queries)
print({"source": data_source, "cases": len(cases), "queries": len(queries)})

```

Saved output:

```text
{'source': 'github', 'cases': 24, 'queries': 18}

```

## Cell 63

```python
def normalise_for_search(text, language):
    text = normalize_unicode(text, compatibility=False)
    text = " ".join(text.replace("ـ", "").split())
    if language == "ar":
        text = dediac_ar(text)
        text = normalize_alef_ar(text)
        text = normalize_alef_maksura_ar(text)
    return text

corpus_ids = [row["case_id"] for row in cases]
corpus_texts = [
    normalise_for_search(f'{row["summary"]} [SEP] {row["resolution"]}', row["language"])
    for row in cases
]
assert len(corpus_ids) == len(corpus_texts) == 24
print(corpus_ids[0], corpus_texts[0])

```

Saved output:

```text
AR-001 تعذر تسجيل الدخول الي البوابة بعد تحديث كلمة المرور [SEP] تمت اعادة مزامنة الحساب وارسال رابط دخول جديد

```

## Cell 64

```python
try:
    model = SentenceTransformer(MODEL_ID)
except Exception as exc:
    raise RuntimeError(
        "تعذر تنزيل نموذج البحث. افحص اتصال Hugging Face ثم أعد هذه الخلية مرة واحدة؛ "
        "لا تستخدم vectors عشوائية كبديل لـCore."
    ) from exc

corpus_vectors = model.encode(
    corpus_texts,
    batch_size=16,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True,
).astype("float32")
vector_norms = np.linalg.norm(corpus_vectors, axis=1)
assert corpus_vectors.shape[0] == len(cases)
assert corpus_vectors.shape[1] > 0
assert np.allclose(vector_norms, 1.0, atol=1e-5)
print({"shape": corpus_vectors.shape, "norm_min": float(vector_norms.min()), "norm_max": float(vector_norms.max())})

```

Saved output:

```text
Loading weights:   0%|          | 0/199 [00:00<?, ?it/s]
Batches:   0%|          | 0/2 [00:00<?, ?it/s]
{'shape': (24, 384), 'norm_min': 0.9999999403953552, 'norm_max': 1.0000001192092896}

```

## Cell 65

```python
dimension = corpus_vectors.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(corpus_vectors)
assert index.ntotal == len(cases)
print({"index_type": type(index).__name__, "vectors": index.ntotal, "dimension": dimension})

```

Saved output:

```text
{'index_type': 'IndexFlatIP', 'vectors': 24, 'dimension': 384}

```

## Cell 66

```python
def search(query, language, k=K):
    clean_query = normalise_for_search(query, language)
    query_vector = model.encode(
        [clean_query], convert_to_numpy=True, normalize_embeddings=True
    ).astype("float32")
    assert np.allclose(np.linalg.norm(query_vector, axis=1), 1.0, atol=1e-5)
    scores, positions = index.search(query_vector, min(k, len(cases)))
    return [
        {
            "rank": rank,
            "case_id": corpus_ids[position],
            "score": float(score),
            "summary": cases[position]["summary"],
            "language": cases[position]["language"],
        }
        for rank, (position, score) in enumerate(zip(positions[0], scores[0]), start=1)
    ]

for demo_query, language in [
    ("رمز الدخول لم يصل إلى جوالي", "ar"),
    ("The bus route is absent from the map", "en"),
    ("تم خصم رسوم التصريح مرتين", "ar"),
]:
    print("\nQUERY:", demo_query)
    for result in search(demo_query, language):
        print(result)

```

Saved output:

```text

QUERY: رمز الدخول لم يصل إلى جوالي
{'rank': 1, 'case_id': 'AR-001', 'score': 0.5912884473800659, 'summary': 'تعذر تسجيل الدخول إلى البوابة بعد تحديث كلمة المرور', 'language': 'ar'}
{'rank': 2, 'case_id': 'EN-001', 'score': 0.5889511108398438, 'summary': 'Cannot sign in to the portal after changing the password', 'language': 'en'}
{'rank': 3, 'case_id': 'AR-002', 'score': 0.5306751728057861, 'summary': 'ما وصل رمز التحقق للجوال عند محاولة الدخول', 'language': 'ar'}

QUERY: The bus route is absent from the map
{'rank': 1, 'case_id': 'EN-005', 'score': 0.7517008781433105, 'summary': 'The new bus route is missing from the mobile map', 'language': 'en'}
{'rank': 2, 'case_id': 'AR-005', 'score': 0.691257655620575, 'summary': 'لا يظهر مسار الحافلة الجديد في التطبيق', 'language': 'ar'}
{'rank': 3, 'case_id': 'AR-006', 'score': 0.6660596132278442, 'summary': 'موقع موقف الحافلة غير واضح في الحي', 'language': 'ar'}

QUERY: تم خصم رسوم التصريح مرتين
{'rank': 1, 'case_id': 'AR-012', 'score': 0.5929687023162842, 'summary': 'تم احتساب رسوم التصريح مرتين', 'language': 'ar'}
{'rank': 2, 'case_id': 'EN-012', 'score': 0.5329747200012207, 'summary': 'The permit fee was charged twice', 'language': 'en'}
{'rank': 3, 'case_id': 'AR-010', 'score': 0.31019294261932373, 'summary': 'رُفض المستند المرفق بطلب التصريح', 'language': 'ar'}

```

## Cell 67

```python
def retrieval_metrics(ranked_ids, relevant_ids, k=3):
    hits, reciprocal_ranks = [], []
    for ranking, relevant in zip(ranked_ids, relevant_ids):
        relevant = set(relevant)
        if not relevant:
            continue
        first = next((rank for rank, item in enumerate(ranking[:k], 1) if item in relevant), None)
        hits.append(float(first is not None))
        reciprocal_ranks.append(1.0 / first if first else 0.0)
    if not hits:
        raise ValueError("at least one answerable query is required")
    return {
        f"recall@{k}": float(np.mean(hits)),
        f"mrr@{k}": float(np.mean(reciprocal_ranks)),
        "answerable_queries": len(hits),
    }

def rank_queries(query_subset):
    rows = []
    for query in query_subset:
        ranking = search(query["query"], query["language"], k=K)
        rows.append({
            **query,
            "ranked_case_ids": [item["case_id"] for item in ranking],
            "best_score": ranking[0]["score"],
        })
    return rows

validation_rankings = rank_queries([row for row in queries if row["split"] == "validation"])
test_rankings = rank_queries([row for row in queries if row["split"] == "test"])
print("ranked", len(validation_rankings), "validation and", len(test_rankings), "test queries")

```

Saved output:

```text
ranked 10 validation and 8 test queries

```

## Cell 68

```python
def tune_no_answer_threshold(best_scores, has_relevant):
    scores = np.asarray(best_scores, dtype=float)
    labels = np.asarray(has_relevant, dtype=bool)
    unique = sorted(set(float(score) for score in scores))
    candidates = [unique[0] - 1e-6]
    candidates += [(left + right) / 2 for left, right in zip(unique, unique[1:])]
    candidates += [unique[-1] + 1e-6]
    scored = []
    for threshold in candidates:
        accuracy = float(np.mean((scores >= threshold) == labels))
        scored.append((accuracy, threshold))
    accuracy, threshold = max(scored, key=lambda item: (item[0], item[1]))
    return {"threshold": float(threshold), "validation_accuracy": accuracy}

threshold_result = tune_no_answer_threshold(
    [row["best_score"] for row in validation_rankings],
    [bool(row["relevant_case_ids"]) for row in validation_rankings],
)
FROZEN_THRESHOLD = threshold_result["threshold"]
print("VALIDATION_ONLY", threshold_result)

test_no_answer_accuracy = float(np.mean([
    (row["best_score"] >= FROZEN_THRESHOLD) == bool(row["relevant_case_ids"])
    for row in test_rankings
]))
print("TEST_WITH_FROZEN_THRESHOLD", {"no_answer_accuracy": test_no_answer_accuracy})

```

Saved output:

```text
VALIDATION_ONLY {'threshold': 0.4592095613479614, 'validation_accuracy': 1.0}
TEST_WITH_FROZEN_THRESHOLD {'no_answer_accuracy': 1.0}

```

## Cell 69

```python
answerable_test = [row for row in test_rankings if row["relevant_case_ids"]]
overall_metrics = retrieval_metrics(
    [row["ranked_case_ids"] for row in answerable_test],
    [row["relevant_case_ids"] for row in answerable_test],
    k=K,
)

slice_metrics = []
for key in ["language", "retrieval_mode"]:
    for value in sorted({row[key] for row in answerable_test}):
        group = [row for row in answerable_test if row[key] == value]
        metric = retrieval_metrics(
            [row["ranked_case_ids"] for row in group],
            [row["relevant_case_ids"] for row in group],
            k=K,
        )
        slice_metrics.append({"slice": f"{key}={value}", "n": len(group), "flag": "SMALL_SLICE" if len(group) < 10 else "", **metric})

print("MEASURED_SMOKE overall", overall_metrics)
for row in slice_metrics:
    print("MEASURED_SMOKE", row)

```

Saved output:

```text
MEASURED_SMOKE overall {'recall@3': 1.0, 'mrr@3': 0.6666666666666666, 'answerable_queries': 6}
MEASURED_SMOKE {'slice': 'language=ar', 'n': 3, 'flag': 'SMALL_SLICE', 'recall@3': 1.0, 'mrr@3': 0.5, 'answerable_queries': 3}
MEASURED_SMOKE {'slice': 'language=en', 'n': 3, 'flag': 'SMALL_SLICE', 'recall@3': 1.0, 'mrr@3': 0.8333333333333334, 'answerable_queries': 3}
MEASURED_SMOKE {'slice': 'retrieval_mode=cross_lingual', 'n': 2, 'flag': 'SMALL_SLICE', 'recall@3': 1.0, 'mrr@3': 0.5, 'answerable_queries': 2}
MEASURED_SMOKE {'slice': 'retrieval_mode=monolingual', 'n': 4, 'flag': 'SMALL_SLICE', 'recall@3': 1.0, 'mrr@3': 0.75, 'answerable_queries': 4}

```

## Cell 70

```python
dataset_bytes = json.dumps(cases, ensure_ascii=False, sort_keys=True).encode("utf-8")
manifest = {
    "manifest_version": "1.0.0",
    "model_id": MODEL_ID,
    "embedding_dimension": int(dimension),
    "normalization": "l2",
    "preprocessing_profile": "arabic-search/1.0.0 + english-nfc-whitespace/1.0.0",
    "dataset_id": "bayan_day3_cases.csv",
    "dataset_sha256": hashlib.sha256(dataset_bytes).hexdigest(),
    "vector_count": int(index.ntotal),
    "index_type": "IndexFlatIP",
    "data_kind": DATA_KIND,
    "libraries": {name: importlib.metadata.version(name) for name in REQUIRED},
}
retrieval_report = {
    "data_kind": DATA_KIND,
    "k": K,
    "threshold_tuned_on": "validation",
    "frozen_no_answer_threshold": FROZEN_THRESHOLD,
    "validation_no_answer_accuracy": threshold_result["validation_accuracy"],
    "test_no_answer_accuracy": test_no_answer_accuracy,
    "test_retrieval": overall_metrics,
    "test_slices": slice_metrics,
}

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)
(reports_dir / "search_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
(reports_dir / "retrieval_metrics.json").write_text(json.dumps(retrieval_report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(manifest, ensure_ascii=False, indent=2))

```

Saved output:

```text
{
  "manifest_version": "1.0.0",
  "model_id": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
  "embedding_dimension": 384,
  "normalization": "l2",
  "preprocessing_profile": "arabic-search/1.0.0 + english-nfc-whitespace/1.0.0",
  "dataset_id": "bayan_day3_cases.csv",
  "dataset_sha256": "7708cbe884a3c268d24ed2cb87ad2f0a8b64b2e6fa6b37a32393b6ae3bd50e5b",
  "vector_count": 24,
  "index_type": "IndexFlatIP",
  "data_kind": "MEASURED_SMOKE",
  "libraries": {
    "camel-tools": "1.6.0",
    "sentence-transformers": "6.0.0",
    "faiss-cpu": "1.15.0",
    "transformers": "5.15.1",
    "tokenizers": "0.22.2"
  }
}

```

## Cell 71

```python
from sentence_transformers import CrossEncoder
from transformers.utils import logging as hf_logging

hf_logging.set_verbosity_error()
RERANKER_ID = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
RERANK_CANDIDATES = 6
reranker = CrossEncoder(RERANKER_ID)

def rerank_one(query_row, *, measure=True):
    candidates = search(query_row["query"], query_row["language"], k=RERANK_CANDIDATES)
    case_lookup = {row["case_id"]: row for row in cases}
    pairs = [
        (query_row["query"], f'{case_lookup[item["case_id"]]["summary"]} {case_lookup[item["case_id"]]["resolution"]}')
        for item in candidates
    ]
    started = time.perf_counter()
    scores = reranker.predict(pairs, show_progress_bar=False)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    reranked = sorted(
        zip([item["case_id"] for item in candidates], scores),
        key=lambda item: float(item[1]), reverse=True,
    )
    return {
        **query_row,
        "before_ids": [item["case_id"] for item in candidates],
        "after_ids": [case_id for case_id, _ in reranked],
        "rerank_ms": elapsed_ms if measure else None,
    }

# Warm-up is excluded from latency, then the frozen answerable test slice is measured.
_ = rerank_one(next(row for row in validation_rankings if row["relevant_case_ids"]), measure=False)
reranked_test = [rerank_one(row) for row in answerable_test]
before_rerank = retrieval_metrics(
    [row["before_ids"] for row in reranked_test],
    [row["relevant_case_ids"] for row in reranked_test], k=K,
)
after_rerank = retrieval_metrics(
    [row["after_ids"] for row in reranked_test],
    [row["relevant_case_ids"] for row in reranked_test], k=K,
)
rerank_latencies = [row["rerank_ms"] for row in reranked_test]
rerank_report = {
    "result_type": DATA_KIND,
    "reranker_id": RERANKER_ID,
    "candidate_count": RERANK_CANDIDATES,
    "answerable_test_queries": len(reranked_test),
    "mrr_at_3_before": before_rerank["mrr@3"],
    "mrr_at_3_after": after_rerank["mrr@3"],
    "mrr_at_3_delta": after_rerank["mrr@3"] - before_rerank["mrr@3"],
    "median_rerank_ms": float(statistics.median(rerank_latencies)),
    "p95_rerank_ms": float(np.percentile(rerank_latencies, 95)),
    "warmup_excluded": True,
    "decision": "ADOPT_FOR_EXPERIMENT" if after_rerank["mrr@3"] > before_rerank["mrr@3"] else "REJECT_NO_MEASURED_LIFT",
    "limitations": ["six answerable test queries", "CPU timing depends on runtime", "MEASURED_SMOKE only"],
}
retrieval_report["reranking"] = rerank_report
(reports_dir / "retrieval_metrics.json").write_text(
    json.dumps(retrieval_report, ensure_ascii=False, indent=2), encoding="utf-8"
)
rerank_display = {
    key: rerank_report[key]
    for key in [
        "result_type", "reranker_id", "candidate_count",
        "answerable_test_queries", "mrr_at_3_before",
        "mrr_at_3_after", "mrr_at_3_delta",
        "warmup_excluded", "decision",
    ]
}
rerank_display["latency_note"] = "measured on CPU; runtime-dependent"
print(json.dumps(rerank_display, ensure_ascii=False, indent=2))
print("RERANKING_TRADEOFF=MEASURED_SMOKE")
```

Saved output:

```text
Loading weights:   0%|          | 0/201 [00:00<?, ?it/s]
{
  "result_type": "MEASURED_SMOKE",
  "reranker_id": "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",
  "candidate_count": 6,
  "answerable_test_queries": 6,
  "mrr_at_3_before": 0.6666666666666666,
  "mrr_at_3_after": 0.7222222222222223,
  "mrr_at_3_delta": 0.05555555555555569,
  "warmup_excluded": true,
  "decision": "ADOPT_FOR_EXPERIMENT",
  "latency_note": "measured on CPU; runtime-dependent"
}
RERANKING_TRADEOFF=MEASURED_SMOKE

```

## Cell 72

```python
core_checks = {
    "actual_sentence_model": getattr(model, "encode", None) is not None,
    "reranking_measured": len(reranked_test) > 0 and rerank_report["warmup_excluded"],
    "all_corpus_vectors_created": corpus_vectors.shape[0] == len(cases),
    "l2_normalised": bool(np.allclose(np.linalg.norm(corpus_vectors, axis=1), 1.0, atol=1e-5)),
    "faiss_count_matches": int(index.ntotal) == len(cases),
    "manifest_matches": manifest["vector_count"] == int(index.ntotal) and manifest["embedding_dimension"] == dimension,
    "validation_only_threshold": retrieval_report["threshold_tuned_on"] == "validation",
    "metrics_in_range": all(0.0 <= overall_metrics[key] <= 1.0 for key in ["recall@3", "mrr@3"]),
    "reports_written": all((reports_dir / name).exists() for name in ["search_manifest.json", "retrieval_metrics.json"]),
}
assert all(core_checks.values()), core_checks
print(core_checks)
print("DAY3_NOTEBOOK6_CORE=PASS")

```

Saved output:

```text
{'actual_sentence_model': True, 'reranking_measured': True, 'all_corpus_vectors_created': True, 'l2_normalised': True, 'faiss_count_matches': True, 'manifest_matches': True, 'validation_only_threshold': True, 'metrics_in_range': True, 'reports_written': True}
DAY3_NOTEBOOK6_CORE=PASS

```

## Cell 73

```python
# اليوم الثالث — التقييم وتحليل الأخطاء

سأبدأ الآن مختبر Evaluation and Error Analysis، وأركز على:
- تقييم أداء النموذج
- تحليل الأخطاء
- مقارنة النتائج
- فهم نقاط القوة والضعف في النظام
```

Saved output:

```text

```

## Cell 74

```python
import importlib.metadata
import subprocess
import sys

REQUIRED = {
    "camel-tools": "1.6.0",
    "sentence-transformers": "6.0.0",
    "faiss-cpu": "1.15.0",
    "transformers": "5.15.1",
    "tokenizers": "0.22.2",
}
to_install = []
for distribution, expected in REQUIRED.items():
    try:
        current = importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        current = None
    if current != expected:
        to_install.append(f"{distribution}=={expected}")
if to_install:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", *to_install]
    )
for distribution, expected in REQUIRED.items():
    assert importlib.metadata.version(distribution) == expected
print("SETUP=PASS", {name: importlib.metadata.version(name) for name in REQUIRED})

```

Saved output:

```text
SETUP=PASS {'camel-tools': '1.6.0', 'sentence-transformers': '6.0.0', 'faiss-cpu': '1.15.0', 'transformers': '5.15.1', 'tokenizers': '0.22.2'}

```

## Cell 75

```python
import csv
import hashlib
import io
import json
import urllib.request
import statistics
import time
from collections import defaultdict
from pathlib import Path

import faiss
import numpy as np
import torch
from camel_tools.utils.dediac import dediac_ar
from camel_tools.utils.normalize import (
    normalize_alef_ar,
    normalize_alef_maksura_ar,
    normalize_unicode,
)
from sentence_transformers import SentenceTransformer

DATA_KIND = "MEASURED_SMOKE"
MODEL_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
K = 3
print("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")

```

Saved output:

```text
DEVICE cpu

```

## Cell 76

```python
CASES_URL = "https://raw.githubusercontent.com/almiyead-rgb/bayan-applied-nlp-course/main/data/sample/bayan_day3_cases.csv"
QUERIES_URL = "https://raw.githubusercontent.com/almiyead-rgb/bayan-applied-nlp-course/main/data/sample/bayan_day3_queries.jsonl"
CASES_FALLBACK = [{'case_id': 'AR-001', 'language': 'ar', 'variant': 'MSA', 'topic': 'digital_service', 'summary': 'تعذر تسجيل الدخول إلى البوابة بعد تحديث كلمة المرور', 'resolution': 'تمت إعادة مزامنة الحساب وإرسال رابط دخول جديد'}, {'case_id': 'AR-002', 'language': 'ar', 'variant': 'Gulf', 'topic': 'digital_service', 'summary': 'ما وصل رمز التحقق للجوال عند محاولة الدخول', 'resolution': 'تم تحديث رقم التواصل وإعادة إرسال الرمز'}, {'case_id': 'AR-003', 'language': 'ar', 'variant': 'MSA', 'topic': 'digital_service', 'summary': 'يفشل رفع ملف PDF في صفحة الطلب', 'resolution': 'تم ضغط الملف وتغيير اسمه ثم اكتمل الرفع'}, {'case_id': 'AR-004', 'language': 'ar', 'variant': 'Gulf', 'topic': 'transport', 'summary': 'الباص تأخر عن المحطة أكثر من نصف ساعة', 'resolution': 'تمت إضافة رحلة بديلة وإشعار المستفيدين'}, {'case_id': 'AR-005', 'language': 'ar', 'variant': 'MSA', 'topic': 'transport', 'summary': 'لا يظهر مسار الحافلة الجديد في التطبيق', 'resolution': 'تم تحديث بيانات المسار وإعادة تحميل الخريطة'}, {'case_id': 'AR-006', 'language': 'ar', 'variant': 'Gulf', 'topic': 'transport', 'summary': 'موقع موقف الحافلة غير واضح في الحي', 'resolution': 'تم إرسال رابط الموقع وإضافة لوحة إرشادية'}, {'case_id': 'AR-007', 'language': 'ar', 'variant': 'MSA', 'topic': 'health', 'summary': 'لا توجد مواعيد متاحة في العيادة المطلوبة', 'resolution': 'تم فتح قائمة انتظار واقتراح عيادة قريبة'}, {'case_id': 'AR-008', 'language': 'ar', 'variant': 'Gulf', 'topic': 'health', 'summary': 'نتيجة التحليل ما ظهرت في التطبيق الصحي', 'resolution': 'تمت مزامنة النتيجة مع الملف الصحي'}, {'case_id': 'AR-009', 'language': 'ar', 'variant': 'MSA', 'topic': 'health', 'summary': 'تعذر تجديد الوصفة من خلال التطبيق', 'resolution': 'تم التحقق من الأهلية وإعادة تفعيل طلب التجديد'}, {'case_id': 'AR-010', 'language': 'ar', 'variant': 'MSA', 'topic': 'permit', 'summary': 'رُفض المستند المرفق بطلب التصريح', 'resolution': 'تم توضيح صيغة المستند وإعادة فتح الطلب للرفع'}, {'case_id': 'AR-011', 'language': 'ar', 'variant': 'Gulf', 'topic': 'permit', 'summary': 'طلب التصريح واقف عند المراجعة من أسبوع', 'resolution': 'تم تصعيد الطلب وتحديث الحالة في اليوم التالي'}, {'case_id': 'AR-012', 'language': 'ar', 'variant': 'MSA', 'topic': 'permit', 'summary': 'تم احتساب رسوم التصريح مرتين', 'resolution': 'أعيد المبلغ المكرر وثُبتت عملية دفع واحدة'}, {'case_id': 'EN-001', 'language': 'en', 'variant': 'English', 'topic': 'digital_service', 'summary': 'Cannot sign in to the portal after changing the password', 'resolution': 'The account was resynchronised and a new sign-in link was sent'}, {'case_id': 'EN-002', 'language': 'en', 'variant': 'English', 'topic': 'digital_service', 'summary': 'The verification code never arrived on the registered phone', 'resolution': 'The contact number was verified and the code was resent'}, {'case_id': 'EN-003', 'language': 'en', 'variant': 'English', 'topic': 'digital_service', 'summary': 'The portal rejects a PDF attachment during upload', 'resolution': 'The file was compressed and renamed before a successful upload'}, {'case_id': 'EN-004', 'language': 'en', 'variant': 'English', 'topic': 'transport', 'summary': 'The bus arrived more than thirty minutes late', 'resolution': 'An additional trip was assigned and passengers were notified'}, {'case_id': 'EN-005', 'language': 'en', 'variant': 'English', 'topic': 'transport', 'summary': 'The new bus route is missing from the mobile map', 'resolution': 'The route dataset was refreshed and the map was reloaded'}, {'case_id': 'EN-006', 'language': 'en', 'variant': 'English', 'topic': 'transport', 'summary': 'The location of the neighbourhood bus stop is unclear', 'resolution': 'A location link was sent and a sign was added'}, {'case_id': 'EN-007', 'language': 'en', 'variant': 'English', 'topic': 'health', 'summary': 'No appointments are available at the requested clinic', 'resolution': 'A waiting list was opened and a nearby clinic was suggested'}, {'case_id': 'EN-008', 'language': 'en', 'variant': 'English', 'topic': 'health', 'summary': 'The laboratory result is missing from the health application', 'resolution': 'The result was synchronised with the health record'}, {'case_id': 'EN-009', 'language': 'en', 'variant': 'English', 'topic': 'health', 'summary': 'The prescription renewal action fails in the application', 'resolution': 'Eligibility was checked and the renewal request was reactivated'}, {'case_id': 'EN-010', 'language': 'en', 'variant': 'English', 'topic': 'permit', 'summary': 'The permit request rejected the uploaded document', 'resolution': 'The required format was explained and upload was reopened'}, {'case_id': 'EN-011', 'language': 'en', 'variant': 'English', 'topic': 'permit', 'summary': 'The permit status has remained under review for a week', 'resolution': 'The request was escalated and its status was updated the next day'}, {'case_id': 'EN-012', 'language': 'en', 'variant': 'English', 'topic': 'permit', 'summary': 'The permit fee was charged twice', 'resolution': 'The duplicate amount was refunded and one payment was retained'}]
QUERIES_FALLBACK = [{'query_id': 'QV-001', 'split': 'validation', 'query': 'ما وصلني كود الدخول على الجوال', 'language': 'ar', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['AR-002']}, {'query_id': 'QV-002', 'split': 'validation', 'query': 'The portal will not accept my PDF file', 'language': 'en', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['EN-003']}, {'query_id': 'QV-003', 'split': 'validation', 'query': 'The bus was over thirty minutes late', 'language': 'en', 'retrieval_mode': 'cross_lingual', 'relevant_case_ids': ['AR-004']}, {'query_id': 'QV-004', 'split': 'validation', 'query': 'انخصمت رسوم التصريح مرتين', 'language': 'ar', 'retrieval_mode': 'cross_lingual', 'relevant_case_ids': ['EN-012']}, {'query_id': 'QV-005', 'split': 'validation', 'query': 'أحتاج موعد عيادة ولا يوجد وقت متاح', 'language': 'ar', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['AR-007']}, {'query_id': 'QV-006', 'split': 'validation', 'query': 'My permit has been under review for a week', 'language': 'en', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['EN-011']}, {'query_id': 'QV-007', 'split': 'validation', 'query': 'ما ساعات عمل المكتبة؟', 'language': 'ar', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}, {'query_id': 'QV-008', 'split': 'validation', 'query': "What is tomorrow's weather?", 'language': 'en', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}, {'query_id': 'QV-009', 'split': 'validation', 'query': 'أرغب في التقديم على وظيفة', 'language': 'ar', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}, {'query_id': 'QV-010', 'split': 'validation', 'query': 'Where can I renew my passport?', 'language': 'en', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}, {'query_id': 'QT-001', 'split': 'test', 'query': 'رمز التحقق لا يصل لهاتفي', 'language': 'ar', 'retrieval_mode': 'cross_lingual', 'relevant_case_ids': ['EN-002']}, {'query_id': 'QT-002', 'split': 'test', 'query': 'The new route is absent from the map', 'language': 'en', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['EN-005']}, {'query_id': 'QT-003', 'split': 'test', 'query': 'نتيجة المختبر غير موجودة في الملف الصحي', 'language': 'ar', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['AR-008']}, {'query_id': 'QT-004', 'split': 'test', 'query': 'The uploaded permit document was refused', 'language': 'en', 'retrieval_mode': 'cross_lingual', 'relevant_case_ids': ['AR-010']}, {'query_id': 'QT-005', 'split': 'test', 'query': 'وين موقع موقف الباص في الحي؟', 'language': 'ar', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['AR-006']}, {'query_id': 'QT-006', 'split': 'test', 'query': 'I cannot renew my prescription in the app', 'language': 'en', 'retrieval_mode': 'monolingual', 'relevant_case_ids': ['EN-009']}, {'query_id': 'QT-007', 'split': 'test', 'query': 'أحتاج وصفة طبخ سريعة', 'language': 'ar', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}, {'query_id': 'QT-008', 'split': 'test', 'query': 'How do I reserve a football field?', 'language': 'en', 'retrieval_mode': 'no_answer', 'relevant_case_ids': []}]

def load_course_data():
    try:
        with urllib.request.urlopen(CASES_URL, timeout=15) as response:
            cases = list(csv.DictReader(io.StringIO(response.read().decode("utf-8"))))
        with urllib.request.urlopen(QUERIES_URL, timeout=15) as response:
            queries = [json.loads(line) for line in response.read().decode("utf-8").splitlines() if line.strip()]
        return cases, queries, "github"
    except Exception as exc:
        return CASES_FALLBACK, QUERIES_FALLBACK, f"embedded_fallback:{type(exc).__name__}"

cases, queries, data_source = load_course_data()
assert len(cases) == 24 and len(queries) == 18
assert len({row["case_id"] for row in cases}) == len(cases)
assert {row["split"] for row in queries} == {"validation", "test"}
assert all(isinstance(row["relevant_case_ids"], list) for row in queries)
print({"source": data_source, "cases": len(cases), "queries": len(queries)})

```

Saved output:

```text
{'source': 'github', 'cases': 24, 'queries': 18}

```

## Cell 77

```python
def normalise_for_search(text, language):
    text = normalize_unicode(text, compatibility=False)
    text = " ".join(text.replace("ـ", "").split())
    if language == "ar":
        text = dediac_ar(text)
        text = normalize_alef_ar(text)
        text = normalize_alef_maksura_ar(text)
    return text

corpus_ids = [row["case_id"] for row in cases]
corpus_texts = [
    normalise_for_search(f'{row["summary"]} [SEP] {row["resolution"]}', row["language"])
    for row in cases
]
assert len(corpus_ids) == len(corpus_texts) == 24
print(corpus_ids[0], corpus_texts[0])

```

Saved output:

```text
AR-001 تعذر تسجيل الدخول الي البوابة بعد تحديث كلمة المرور [SEP] تمت اعادة مزامنة الحساب وارسال رابط دخول جديد

```

## Cell 78

```python

```

Saved output:

```text

```

## Cell 79

```python
try:
    model = SentenceTransformer(MODEL_ID)
except Exception as exc:
    raise RuntimeError(
        "تعذر تنزيل نموذج البحث. افحص اتصال Hugging Face ثم أعد هذه الخلية مرة واحدة؛ "
        "لا تستخدم vectors عشوائية كبديل لـCore."
    ) from exc

corpus_vectors = model.encode(
    corpus_texts,
    batch_size=16,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True,
).astype("float32")
vector_norms = np.linalg.norm(corpus_vectors, axis=1)
assert corpus_vectors.shape[0] == len(cases)
assert corpus_vectors.shape[1] > 0
assert np.allclose(vector_norms, 1.0, atol=1e-5)
print({"shape": corpus_vectors.shape, "norm_min": float(vector_norms.min()), "norm_max": float(vector_norms.max())})

```

Saved output:

```text
Loading weights:   0%|          | 0/199 [00:00<?, ?it/s]
Batches:   0%|          | 0/2 [00:00<?, ?it/s]
{'shape': (24, 384), 'norm_min': 0.9999999403953552, 'norm_max': 1.0000001192092896}

```

## Cell 80

```python
dimension = corpus_vectors.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(corpus_vectors)
assert index.ntotal == len(cases)
print({"index_type": type(index).__name__, "vectors": index.ntotal, "dimension": dimension})

```

Saved output:

```text
{'index_type': 'IndexFlatIP', 'vectors': 24, 'dimension': 384}

```

## Cell 81

```python
def search(query, language, k=K):
    clean_query = normalise_for_search(query, language)
    query_vector = model.encode(
        [clean_query], convert_to_numpy=True, normalize_embeddings=True
    ).astype("float32")
    assert np.allclose(np.linalg.norm(query_vector, axis=1), 1.0, atol=1e-5)
    scores, positions = index.search(query_vector, min(k, len(cases)))
    return [
        {
            "rank": rank,
            "case_id": corpus_ids[position],
            "score": float(score),
            "summary": cases[position]["summary"],
            "language": cases[position]["language"],
        }
        for rank, (position, score) in enumerate(zip(positions[0], scores[0]), start=1)
    ]

for demo_query, language in [
    ("رمز الدخول لم يصل إلى جوالي", "ar"),
    ("The bus route is absent from the map", "en"),
    ("تم خصم رسوم التصريح مرتين", "ar"),
]:
    print("\nQUERY:", demo_query)
    for result in search(demo_query, language):
        print(result)

```

Saved output:

```text

QUERY: رمز الدخول لم يصل إلى جوالي
{'rank': 1, 'case_id': 'AR-001', 'score': 0.5912884473800659, 'summary': 'تعذر تسجيل الدخول إلى البوابة بعد تحديث كلمة المرور', 'language': 'ar'}
{'rank': 2, 'case_id': 'EN-001', 'score': 0.5889511108398438, 'summary': 'Cannot sign in to the portal after changing the password', 'language': 'en'}
{'rank': 3, 'case_id': 'AR-002', 'score': 0.5306751728057861, 'summary': 'ما وصل رمز التحقق للجوال عند محاولة الدخول', 'language': 'ar'}

QUERY: The bus route is absent from the map
{'rank': 1, 'case_id': 'EN-005', 'score': 0.7517008781433105, 'summary': 'The new bus route is missing from the mobile map', 'language': 'en'}
{'rank': 2, 'case_id': 'AR-005', 'score': 0.691257655620575, 'summary': 'لا يظهر مسار الحافلة الجديد في التطبيق', 'language': 'ar'}
{'rank': 3, 'case_id': 'AR-006', 'score': 0.6660596132278442, 'summary': 'موقع موقف الحافلة غير واضح في الحي', 'language': 'ar'}

QUERY: تم خصم رسوم التصريح مرتين
{'rank': 1, 'case_id': 'AR-012', 'score': 0.5929687023162842, 'summary': 'تم احتساب رسوم التصريح مرتين', 'language': 'ar'}
{'rank': 2, 'case_id': 'EN-012', 'score': 0.5329747200012207, 'summary': 'The permit fee was charged twice', 'language': 'en'}
{'rank': 3, 'case_id': 'AR-010', 'score': 0.31019294261932373, 'summary': 'رُفض المستند المرفق بطلب التصريح', 'language': 'ar'}

```

## Cell 82

```python
def retrieval_metrics(ranked_ids, relevant_ids, k=3):
    hits, reciprocal_ranks = [], []
    for ranking, relevant in zip(ranked_ids, relevant_ids):
        relevant = set(relevant)
        if not relevant:
            continue
        first = next((rank for rank, item in enumerate(ranking[:k], 1) if item in relevant), None)
        hits.append(float(first is not None))
        reciprocal_ranks.append(1.0 / first if first else 0.0)
    if not hits:
        raise ValueError("at least one answerable query is required")
    return {
        f"recall@{k}": float(np.mean(hits)),
        f"mrr@{k}": float(np.mean(reciprocal_ranks)),
        "answerable_queries": len(hits),
    }

def rank_queries(query_subset):
    rows = []
    for query in query_subset:
        ranking = search(query["query"], query["language"], k=K)
        rows.append({
            **query,
            "ranked_case_ids": [item["case_id"] for item in ranking],
            "best_score": ranking[0]["score"],
        })
    return rows

validation_rankings = rank_queries([row for row in queries if row["split"] == "validation"])
test_rankings = rank_queries([row for row in queries if row["split"] == "test"])
print("ranked", len(validation_rankings), "validation and", len(test_rankings), "test queries")

```

Saved output:

```text
ranked 10 validation and 8 test queries

```

## Cell 83

```python
def tune_no_answer_threshold(best_scores, has_relevant):
    scores = np.asarray(best_scores, dtype=float)
    labels = np.asarray(has_relevant, dtype=bool)
    unique = sorted(set(float(score) for score in scores))
    candidates = [unique[0] - 1e-6]
    candidates += [(left + right) / 2 for left, right in zip(unique, unique[1:])]
    candidates += [unique[-1] + 1e-6]
    scored = []
    for threshold in candidates:
        accuracy = float(np.mean((scores >= threshold) == labels))
        scored.append((accuracy, threshold))
    accuracy, threshold = max(scored, key=lambda item: (item[0], item[1]))
    return {"threshold": float(threshold), "validation_accuracy": accuracy}

threshold_result = tune_no_answer_threshold(
    [row["best_score"] for row in validation_rankings],
    [bool(row["relevant_case_ids"]) for row in validation_rankings],
)
FROZEN_THRESHOLD = threshold_result["threshold"]
print("VALIDATION_ONLY", threshold_result)

test_no_answer_accuracy = float(np.mean([
    (row["best_score"] >= FROZEN_THRESHOLD) == bool(row["relevant_case_ids"])
    for row in test_rankings
]))
print("TEST_WITH_FROZEN_THRESHOLD", {"no_answer_accuracy": test_no_answer_accuracy})

```

Saved output:

```text
VALIDATION_ONLY {'threshold': 0.4592095613479614, 'validation_accuracy': 1.0}
TEST_WITH_FROZEN_THRESHOLD {'no_answer_accuracy': 1.0}

```

## Cell 84

```python
answerable_test = [row for row in test_rankings if row["relevant_case_ids"]]
overall_metrics = retrieval_metrics(
    [row["ranked_case_ids"] for row in answerable_test],
    [row["relevant_case_ids"] for row in answerable_test],
    k=K,
)

slice_metrics = []
for key in ["language", "retrieval_mode"]:
    for value in sorted({row[key] for row in answerable_test}):
        group = [row for row in answerable_test if row[key] == value]
        metric = retrieval_metrics(
            [row["ranked_case_ids"] for row in group],
            [row["relevant_case_ids"] for row in group],
            k=K,
        )
        slice_metrics.append({"slice": f"{key}={value}", "n": len(group), "flag": "SMALL_SLICE" if len(group) < 10 else "", **metric})

print("MEASURED_SMOKE overall", overall_metrics)
for row in slice_metrics:
    print("MEASURED_SMOKE", row)

```

Saved output:

```text
MEASURED_SMOKE overall {'recall@3': 1.0, 'mrr@3': 0.6666666666666666, 'answerable_queries': 6}
MEASURED_SMOKE {'slice': 'language=ar', 'n': 3, 'flag': 'SMALL_SLICE', 'recall@3': 1.0, 'mrr@3': 0.5, 'answerable_queries': 3}
MEASURED_SMOKE {'slice': 'language=en', 'n': 3, 'flag': 'SMALL_SLICE', 'recall@3': 1.0, 'mrr@3': 0.8333333333333334, 'answerable_queries': 3}
MEASURED_SMOKE {'slice': 'retrieval_mode=cross_lingual', 'n': 2, 'flag': 'SMALL_SLICE', 'recall@3': 1.0, 'mrr@3': 0.5, 'answerable_queries': 2}
MEASURED_SMOKE {'slice': 'retrieval_mode=monolingual', 'n': 4, 'flag': 'SMALL_SLICE', 'recall@3': 1.0, 'mrr@3': 0.75, 'answerable_queries': 4}

```

## Cell 85

```python
dataset_bytes = json.dumps(cases, ensure_ascii=False, sort_keys=True).encode("utf-8")
manifest = {
    "manifest_version": "1.0.0",
    "model_id": MODEL_ID,
    "embedding_dimension": int(dimension),
    "normalization": "l2",
    "preprocessing_profile": "arabic-search/1.0.0 + english-nfc-whitespace/1.0.0",
    "dataset_id": "bayan_day3_cases.csv",
    "dataset_sha256": hashlib.sha256(dataset_bytes).hexdigest(),
    "vector_count": int(index.ntotal),
    "index_type": "IndexFlatIP",
    "data_kind": DATA_KIND,
    "libraries": {name: importlib.metadata.version(name) for name in REQUIRED},
}
retrieval_report = {
    "data_kind": DATA_KIND,
    "k": K,
    "threshold_tuned_on": "validation",
    "frozen_no_answer_threshold": FROZEN_THRESHOLD,
    "validation_no_answer_accuracy": threshold_result["validation_accuracy"],
    "test_no_answer_accuracy": test_no_answer_accuracy,
    "test_retrieval": overall_metrics,
    "test_slices": slice_metrics,
}

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)
(reports_dir / "search_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
(reports_dir / "retrieval_metrics.json").write_text(json.dumps(retrieval_report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(manifest, ensure_ascii=False, indent=2))

```

Saved output:

```text
{
  "manifest_version": "1.0.0",
  "model_id": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
  "embedding_dimension": 384,
  "normalization": "l2",
  "preprocessing_profile": "arabic-search/1.0.0 + english-nfc-whitespace/1.0.0",
  "dataset_id": "bayan_day3_cases.csv",
  "dataset_sha256": "7708cbe884a3c268d24ed2cb87ad2f0a8b64b2e6fa6b37a32393b6ae3bd50e5b",
  "vector_count": 24,
  "index_type": "IndexFlatIP",
  "data_kind": "MEASURED_SMOKE",
  "libraries": {
    "camel-tools": "1.6.0",
    "sentence-transformers": "6.0.0",
    "faiss-cpu": "1.15.0",
    "transformers": "5.15.1",
    "tokenizers": "0.22.2"
  }
}

```

## Cell 86

```python
from sentence_transformers import CrossEncoder
from transformers.utils import logging as hf_logging

hf_logging.set_verbosity_error()
RERANKER_ID = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
RERANK_CANDIDATES = 6
reranker = CrossEncoder(RERANKER_ID)

def rerank_one(query_row, *, measure=True):
    candidates = search(query_row["query"], query_row["language"], k=RERANK_CANDIDATES)
    case_lookup = {row["case_id"]: row for row in cases}
    pairs = [
        (query_row["query"], f'{case_lookup[item["case_id"]]["summary"]} {case_lookup[item["case_id"]]["resolution"]}')
        for item in candidates
    ]
    started = time.perf_counter()
    scores = reranker.predict(pairs, show_progress_bar=False)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    reranked = sorted(
        zip([item["case_id"] for item in candidates], scores),
        key=lambda item: float(item[1]), reverse=True,
    )
    return {
        **query_row,
        "before_ids": [item["case_id"] for item in candidates],
        "after_ids": [case_id for case_id, _ in reranked],
        "rerank_ms": elapsed_ms if measure else None,
    }

# Warm-up is excluded from latency, then the frozen answerable test slice is measured.
_ = rerank_one(next(row for row in validation_rankings if row["relevant_case_ids"]), measure=False)
reranked_test = [rerank_one(row) for row in answerable_test]
before_rerank = retrieval_metrics(
    [row["before_ids"] for row in reranked_test],
    [row["relevant_case_ids"] for row in reranked_test], k=K,
)
after_rerank = retrieval_metrics(
    [row["after_ids"] for row in reranked_test],
    [row["relevant_case_ids"] for row in reranked_test], k=K,
)
rerank_latencies = [row["rerank_ms"] for row in reranked_test]
rerank_report = {
    "result_type": DATA_KIND,
    "reranker_id": RERANKER_ID,
    "candidate_count": RERANK_CANDIDATES,
    "answerable_test_queries": len(reranked_test),
    "mrr_at_3_before": before_rerank["mrr@3"],
    "mrr_at_3_after": after_rerank["mrr@3"],
    "mrr_at_3_delta": after_rerank["mrr@3"] - before_rerank["mrr@3"],
    "median_rerank_ms": float(statistics.median(rerank_latencies)),
    "p95_rerank_ms": float(np.percentile(rerank_latencies, 95)),
    "warmup_excluded": True,
    "decision": "ADOPT_FOR_EXPERIMENT" if after_rerank["mrr@3"] > before_rerank["mrr@3"] else "REJECT_NO_MEASURED_LIFT",
    "limitations": ["six answerable test queries", "CPU timing depends on runtime", "MEASURED_SMOKE only"],
}
retrieval_report["reranking"] = rerank_report
(reports_dir / "retrieval_metrics.json").write_text(
    json.dumps(retrieval_report, ensure_ascii=False, indent=2), encoding="utf-8"
)
rerank_display = {
    key: rerank_report[key]
    for key in [
        "result_type", "reranker_id", "candidate_count",
        "answerable_test_queries", "mrr_at_3_before",
        "mrr_at_3_after", "mrr_at_3_delta",
        "warmup_excluded", "decision",
    ]
}
rerank_display["latency_note"] = "measured on CPU; runtime-dependent"
print(json.dumps(rerank_display, ensure_ascii=False, indent=2))
print("RERANKING_TRADEOFF=MEASURED_SMOKE")
```

Saved output:

```text
Loading weights:   0%|          | 0/201 [00:00<?, ?it/s]
{
  "result_type": "MEASURED_SMOKE",
  "reranker_id": "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",
  "candidate_count": 6,
  "answerable_test_queries": 6,
  "mrr_at_3_before": 0.6666666666666666,
  "mrr_at_3_after": 0.7222222222222223,
  "mrr_at_3_delta": 0.05555555555555569,
  "warmup_excluded": true,
  "decision": "ADOPT_FOR_EXPERIMENT",
  "latency_note": "measured on CPU; runtime-dependent"
}
RERANKING_TRADEOFF=MEASURED_SMOKE

```

## Cell 87

```python
core_checks = {
    "actual_sentence_model": getattr(model, "encode", None) is not None,
    "reranking_measured": len(reranked_test) > 0 and rerank_report["warmup_excluded"],
    "all_corpus_vectors_created": corpus_vectors.shape[0] == len(cases),
    "l2_normalised": bool(np.allclose(np.linalg.norm(corpus_vectors, axis=1), 1.0, atol=1e-5)),
    "faiss_count_matches": int(index.ntotal) == len(cases),
    "manifest_matches": manifest["vector_count"] == int(index.ntotal) and manifest["embedding_dimension"] == dimension,
    "validation_only_threshold": retrieval_report["threshold_tuned_on"] == "validation",
    "metrics_in_range": all(0.0 <= overall_metrics[key] <= 1.0 for key in ["recall@3", "mrr@3"]),
    "reports_written": all((reports_dir / name).exists() for name in ["search_manifest.json", "retrieval_metrics.json"]),
}
assert all(core_checks.values()), core_checks
print(core_checks)
print("DAY3_NOTEBOOK6_CORE=PASS")

```

Saved output:

```text
{'actual_sentence_model': True, 'reranking_measured': True, 'all_corpus_vectors_created': True, 'l2_normalised': True, 'faiss_count_matches': True, 'manifest_matches': True, 'validation_only_threshold': True, 'metrics_in_range': True, 'reports_written': True}
DAY3_NOTEBOOK6_CORE=PASS

```

## Cell 88

```python
# اليوم الثالث — التقييم وتحليل الأخطاء

سأبدأ الآن مختبر Evaluation & Error Analysis، وأركز على تقييم أداء النموذج، تحليل الأخطاء، مقارنة النتائج، وتحديد نقاط الضعف التي تحتاج تحسين.
```

Saved output:

```text

```

## Cell 89

```python
import importlib.metadata
import subprocess
import sys

REQUIRED = {"scikit-learn": "1.9.0"}
try:
    current = importlib.metadata.version("scikit-learn")
except importlib.metadata.PackageNotFoundError:
    current = None
if current != REQUIRED["scikit-learn"]:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "--quiet", "scikit-learn==1.9.0"
    ])
assert importlib.metadata.version("scikit-learn") == "1.9.0"
print("SETUP=PASS", importlib.metadata.version("scikit-learn"))

```

Saved output:

```text
SETUP=PASS 1.9.0

```

## Cell 90

```python
import csv
import io
import json
import urllib.request
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.metrics import f1_score

DATA_KIND = "COURSE_FIXTURE"
print("IMPORTS=PASS")

```

Saved output:

```text
IMPORTS=PASS

```

## Cell 91

```python
DATA_URL = "https://raw.githubusercontent.com/almiyead-rgb/bayan-applied-nlp-course/main/data/sample/bayan_day3_predictions.csv"
FALLBACK_ROWS = [{'example_id': 'EV-001', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'short', 'topic': 'digital_service', 'prediction_a': 'permit', 'prediction_b': 'digital_service', 'text': 'ما وصلني رمز التحقق'}, {'example_id': 'EV-002', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'long', 'topic': 'health', 'prediction_a': 'health', 'prediction_b': 'health', 'text': 'أبي أغير موعد العيادة لأن الوقت الحالي ما يناسبني'}, {'example_id': 'EV-003', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'short', 'topic': 'permit', 'prediction_a': 'permit', 'prediction_b': 'permit', 'text': 'طلبي واقف بالمراجعة'}, {'example_id': 'EV-004', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'long', 'topic': 'transport', 'prediction_a': 'transport', 'prediction_b': 'transport', 'text': 'الباص تأخر علينا أكثر من ساعة وما وصل إشعار'}, {'example_id': 'EV-005', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'short', 'topic': 'digital_service', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'التطبيق يعلق عند الدخول'}, {'example_id': 'EV-006', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'long', 'topic': 'health', 'prediction_a': 'transport', 'prediction_b': 'transport', 'text': 'النتيجة للحين ما ظهرت بالتطبيق رغم مرور يومين'}, {'example_id': 'EV-007', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'short', 'topic': 'permit', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'المرفق انرفض'}, {'example_id': 'EV-008', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'long', 'topic': 'transport', 'prediction_a': 'transport', 'prediction_b': 'transport', 'text': 'المسار الجديد مو موجود في الخريطة بعد التحديث'}, {'example_id': 'EV-009', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'short', 'topic': 'digital_service', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'الكود ما وصل'}, {'example_id': 'EV-010', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'long', 'topic': 'health', 'prediction_a': 'health', 'prediction_b': 'digital_service', 'text': 'أحتاج أجدد الوصفة من التطبيق لكن الزر ما يشتغل'}, {'example_id': 'EV-011', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'short', 'topic': 'permit', 'prediction_a': 'permit', 'prediction_b': 'permit', 'text': 'انخصمت الرسوم مرتين'}, {'example_id': 'EV-012', 'split': 'validation', 'language': 'ar', 'variant': 'Gulf', 'length_bucket': 'long', 'topic': 'transport', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'وين موقف الباص الجديد في الحي؟'}, {'example_id': 'EV-013', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'short', 'topic': 'digital_service', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'تعذر الدخول إلى البوابة'}, {'example_id': 'EV-014', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'long', 'topic': 'health', 'prediction_a': 'health', 'prediction_b': 'health', 'text': 'لا تتوفر مواعيد مناسبة في العيادة المطلوبة'}, {'example_id': 'EV-015', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'short', 'topic': 'permit', 'prediction_a': 'permit', 'prediction_b': 'permit', 'text': 'رُفض المستند المرفق'}, {'example_id': 'EV-016', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'long', 'topic': 'transport', 'prediction_a': 'transport', 'prediction_b': 'transport', 'text': 'تأخرت الحافلة عن الموعد المحدد بنصف ساعة'}, {'example_id': 'EV-017', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'short', 'topic': 'digital_service', 'prediction_a': 'permit', 'prediction_b': 'digital_service', 'text': 'يفشل رفع الملف'}, {'example_id': 'EV-018', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'long', 'topic': 'health', 'prediction_a': 'health', 'prediction_b': 'health', 'text': 'لم تظهر نتيجة الفحص في الملف الصحي الإلكتروني'}, {'example_id': 'EV-019', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'short', 'topic': 'permit', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'حالة التصريح معلقة'}, {'example_id': 'EV-020', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'long', 'topic': 'transport', 'prediction_a': 'transport', 'prediction_b': 'digital_service', 'text': 'لا يظهر مسار الحافلة في التطبيق'}, {'example_id': 'EV-021', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'short', 'topic': 'digital_service', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'لم يصل رمز التحقق'}, {'example_id': 'EV-022', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'long', 'topic': 'health', 'prediction_a': 'health', 'prediction_b': 'health', 'text': 'تعذر تجديد الوصفة الطبية عبر الخدمة الإلكترونية'}, {'example_id': 'EV-023', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'short', 'topic': 'permit', 'prediction_a': 'permit', 'prediction_b': 'permit', 'text': 'تم خصم الرسم مرتين'}, {'example_id': 'EV-024', 'split': 'validation', 'language': 'ar', 'variant': 'MSA', 'length_bucket': 'long', 'topic': 'transport', 'prediction_a': 'transport', 'prediction_b': 'transport', 'text': 'أرغب في معرفة موقع أقرب محطة للحافلات'}, {'example_id': 'EV-025', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'short', 'topic': 'digital_service', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'The sign in code did not arrive'}, {'example_id': 'EV-026', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'long', 'topic': 'health', 'prediction_a': 'health', 'prediction_b': 'health', 'text': 'I need to move my clinic appointment to another day'}, {'example_id': 'EV-027', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'short', 'topic': 'permit', 'prediction_a': 'permit', 'prediction_b': 'permit', 'text': 'My permit document was rejected'}, {'example_id': 'EV-028', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'long', 'topic': 'transport', 'prediction_a': 'transport', 'prediction_b': 'transport', 'text': 'The bus arrived forty minutes after the scheduled time'}, {'example_id': 'EV-029', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'short', 'topic': 'digital_service', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'The portal freezes'}, {'example_id': 'EV-030', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'long', 'topic': 'health', 'prediction_a': 'transport', 'prediction_b': 'transport', 'text': 'My laboratory result is still missing from the health record'}, {'example_id': 'EV-031', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'short', 'topic': 'permit', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'The request is stuck'}, {'example_id': 'EV-032', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'long', 'topic': 'transport', 'prediction_a': 'transport', 'prediction_b': 'transport', 'text': 'The new bus route is missing from the mobile map'}, {'example_id': 'EV-033', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'short', 'topic': 'digital_service', 'prediction_a': 'digital_service', 'prediction_b': 'digital_service', 'text': 'PDF upload failed'}, {'example_id': 'EV-034', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'long', 'topic': 'health', 'prediction_a': 'health', 'prediction_b': 'health', 'text': 'The prescription renewal button does not work in the application'}, {'example_id': 'EV-035', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'short', 'topic': 'permit', 'prediction_a': 'permit', 'prediction_b': 'permit', 'text': 'I was charged twice'}, {'example_id': 'EV-036', 'split': 'validation', 'language': 'en', 'variant': 'English', 'length_bucket': 'long', 'topic': 'transport', 'prediction_a': 'transport', 'prediction_b': 'transport', 'text': 'I cannot find the neighbourhood bus stop'}]

try:
    with urllib.request.urlopen(DATA_URL, timeout=15) as response:
        rows = list(csv.DictReader(io.StringIO(response.read().decode("utf-8"))))
    data_source = "github"
except Exception as exc:
    rows = FALLBACK_ROWS
    data_source = f"embedded_fallback:{type(exc).__name__}"

required = {"example_id", "split", "language", "variant", "length_bucket", "topic", "prediction_a", "prediction_b", "text"}
assert len(rows) == 36 and required <= set(rows[0])
assert {row["split"] for row in rows} == {"validation"}
print({"data_kind": DATA_KIND, "source": data_source, "rows": len(rows)})

```

Saved output:

```text
{'data_kind': 'COURSE_FIXTURE', 'source': 'github', 'rows': 36}

```

## Cell 92

```python
def macro_f1(y_true, y_pred):
    return float(f1_score(y_true, y_pred, average="macro", zero_division=0))


def bootstrap_ci(y_true, y_pred, metric_fn, n_boot=1000, alpha=0.05, seed=42):
    truth = np.asarray(y_true, dtype=object)
    prediction = np.asarray(y_pred, dtype=object)
    if len(truth) == 0 or len(truth) != len(prediction):
        raise ValueError("paired non-empty arrays are required")
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(n_boot):
        indexes = rng.integers(0, len(truth), len(truth))
        values.append(metric_fn(truth[indexes], prediction[indexes]))
    low, high = np.percentile(values, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {
        "estimate": metric_fn(truth, prediction),
        "ci_low": float(low),
        "ci_high": float(high),
        "n_boot": n_boot,
    }

y_true = [row["topic"] for row in rows]
interval_a = bootstrap_ci(y_true, [row["prediction_a"] for row in rows], macro_f1)
interval_b = bootstrap_ci(y_true, [row["prediction_b"] for row in rows], macro_f1)
print("COURSE_FIXTURE A", interval_a)
print("COURSE_FIXTURE B", interval_b)

```

Saved output:

```text
COURSE_FIXTURE A {'estimate': 0.7807469040247678, 'ci_low': 0.6212498015141271, 'ci_high': 0.8982313491237977, 'n_boot': 1000}
COURSE_FIXTURE B {'estimate': 0.7819444444444444, 'ci_low': 0.6169212785382484, 'ci_high': 0.9042122693118788, 'n_boot': 1000}

```

## Cell 93

```python
def paired_bootstrap_difference(y_true, prediction_a, prediction_b, metric_fn, n_boot=1000, alpha=0.05, seed=42):
    truth = np.asarray(y_true, dtype=object)
    first = np.asarray(prediction_a, dtype=object)
    second = np.asarray(prediction_b, dtype=object)
    if len(truth) == 0 or not (len(truth) == len(first) == len(second)):
        raise ValueError("three paired non-empty arrays are required")
    rng = np.random.default_rng(seed)
    differences = []
    for _ in range(n_boot):
        indexes = rng.integers(0, len(truth), len(truth))
        differences.append(metric_fn(truth[indexes], second[indexes]) - metric_fn(truth[indexes], first[indexes]))
    low, high = np.percentile(differences, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    observed = metric_fn(truth, second) - metric_fn(truth, first)
    return {
        "difference_b_minus_a": float(observed),
        "ci_low": float(low),
        "ci_high": float(high),
        "supports_directional_claim": bool(low > 0 or high < 0),
    }

paired_result = paired_bootstrap_difference(
    y_true,
    [row["prediction_a"] for row in rows],
    [row["prediction_b"] for row in rows],
    macro_f1,
)
verdict = (
    "The interval excludes zero; report the observed direction with scope and limitations."
    if paired_result["supports_directional_claim"]
    else "The interval includes zero; this fixture does not support a directional superiority claim."
)
print("COURSE_FIXTURE paired B-A", paired_result)
print("VERDICT:", verdict)

```

Saved output:

```text
COURSE_FIXTURE paired B-A {'difference_b_minus_a': 0.0011975404196766792, 'ci_low': -0.10472316166062473, 'ci_high': 0.09963005211966207, 'supports_directional_claim': False}
VERDICT: The interval includes zero; this fixture does not support a directional superiority claim.

```

## Cell 94

```python
def sliced_report(rows, pred_key, slice_keys, min_slice_size=15, n_boot=500):
    groups = [("ALL", rows)]
    for key in slice_keys:
        for value in sorted({row[key] for row in rows}):
            groups.append((f"{key}={value}", [row for row in rows if row[key] == value]))
    report = []
    for offset, (name, group) in enumerate(groups):
        interval = bootstrap_ci(
            [row["topic"] for row in group],
            [row[pred_key] for row in group],
            macro_f1,
            n_boot=n_boot,
            seed=42 + offset,
        )
        report.append({
            "slice": name,
            "n": len(group),
            "flag": "SMALL_SLICE" if len(group) < min_slice_size else "",
            **interval,
        })
    return report

slice_report = sliced_report(rows, "prediction_b", ["language", "variant", "length_bucket"])
for item in slice_report:
    print(item)

```

Saved output:

```text
{'slice': 'ALL', 'n': 36, 'flag': '', 'estimate': 0.7819444444444444, 'ci_low': 0.6111751181328388, 'ci_high': 0.8961752409994097, 'n_boot': 500}
{'slice': 'language=ar', 'n': 24, 'flag': '', 'estimate': 0.758288770053476, 'ci_low': 0.5606515151515151, 'ci_high': 0.9265451388888888, 'n_boot': 500}
{'slice': 'language=en', 'n': 12, 'flag': 'SMALL_SLICE', 'estimate': 0.8285714285714286, 'ci_low': 0.49999999999999994, 'ci_high': 1.0, 'n_boot': 500}
{'slice': 'variant=English', 'n': 12, 'flag': 'SMALL_SLICE', 'estimate': 0.8285714285714286, 'ci_low': 0.496540854978355, 'ci_high': 1.0, 'n_boot': 500}
{'slice': 'variant=Gulf', 'n': 12, 'flag': 'SMALL_SLICE', 'estimate': 0.6583333333333333, 'ci_low': 0.29405906593406594, 'ci_high': 0.8951767676767677, 'n_boot': 500}
{'slice': 'variant=MSA', 'n': 12, 'flag': 'SMALL_SLICE', 'estimate': 0.8374999999999999, 'ci_low': 0.5304166666666666, 'ci_high': 1.0, 'n_boot': 500}
{'slice': 'length_bucket=long', 'n': 18, 'flag': '', 'estimate': 0.525925925925926, 'ci_low': 0.3918026418026418, 'ci_high': 0.830800530738611, 'n_boot': 500}
{'slice': 'length_bucket=short', 'n': 18, 'flag': '', 'estimate': 0.8285714285714285, 'ci_low': 0.625, 'ci_high': 1.0, 'n_boot': 500}

```

## Cell 95

```python
by_id = {row["example_id"]: row for row in rows}
BEHAVIOURAL_CASES = [
    {"case": "Gulf verification code → digital_service", "example_id": "EV-001", "expected": "digital_service"},
    {"case": "MSA upload failure → digital_service", "example_id": "EV-017", "expected": "digital_service"},
    {"case": "Gulf missing health result → health", "example_id": "EV-006", "expected": "health"},
    {"case": "English missing lab result → health", "example_id": "EV-030", "expected": "health"},
    {"case": "MSA bus route → transport", "example_id": "EV-020", "expected": "transport"},
    {"case": "English double charge → permit", "example_id": "EV-035", "expected": "permit"},
]
behavioural_results = []
for case in BEHAVIOURAL_CASES:
    actual = by_id[case["example_id"]]["prediction_b"]
    behavioural_results.append({**case, "actual": actual, "passed": actual == case["expected"]})
behavioural_summary = {
    "passed": sum(row["passed"] for row in behavioural_results),
    "total": len(behavioural_results),
}
behavioural_summary["pass_rate"] = behavioural_summary["passed"] / behavioural_summary["total"]
for row in behavioural_results:
    print(row)
print("COURSE_FIXTURE behavioural", behavioural_summary)

```

Saved output:

```text
{'case': 'Gulf verification code → digital_service', 'example_id': 'EV-001', 'expected': 'digital_service', 'actual': 'digital_service', 'passed': True}
{'case': 'MSA upload failure → digital_service', 'example_id': 'EV-017', 'expected': 'digital_service', 'actual': 'digital_service', 'passed': True}
{'case': 'Gulf missing health result → health', 'example_id': 'EV-006', 'expected': 'health', 'actual': 'transport', 'passed': False}
{'case': 'English missing lab result → health', 'example_id': 'EV-030', 'expected': 'health', 'actual': 'transport', 'passed': False}
{'case': 'MSA bus route → transport', 'example_id': 'EV-020', 'expected': 'transport', 'actual': 'digital_service', 'passed': False}
{'case': 'English double charge → permit', 'example_id': 'EV-035', 'expected': 'permit', 'actual': 'permit', 'passed': True}
COURSE_FIXTURE behavioural {'passed': 3, 'total': 6, 'pass_rate': 0.5}

```

## Cell 96

```python
ALLOWED_TAGS = {
    "label_noise", "class_confusion", "dialect_gap", "negation",
    "truncation", "preprocessing", "entity_boundary", "hard_or_ambiguous",
}
TAGGED_ERRORS = [
    {"example_id": "EV-006", "taxonomy_tag": "dialect_gap", "rationale": "Gulf phrasing for a missing health result confused with transport."},
    {"example_id": "EV-007", "taxonomy_tag": "hard_or_ambiguous", "rationale": "The attachment mention lacks an explicit permit cue."},
    {"example_id": "EV-010", "taxonomy_tag": "dialect_gap", "rationale": "Gulf app wording obscures the prescription-renewal intent."},
    {"example_id": "EV-012", "taxonomy_tag": "dialect_gap", "rationale": "Colloquial location question lacks the formal transport terms."},
    {"example_id": "EV-019", "taxonomy_tag": "class_confusion", "rationale": "Status language overlaps generic digital-service failures."},
    {"example_id": "EV-020", "taxonomy_tag": "class_confusion", "rationale": "Map/application cue dominates the route intent."},
    {"example_id": "EV-030", "taxonomy_tag": "hard_or_ambiguous", "rationale": "Missing-record wording overlaps multiple service domains."},
    {"example_id": "EV-031", "taxonomy_tag": "hard_or_ambiguous", "rationale": "The short request omits the permit noun."},
]

seen = set()
for item in TAGGED_ERRORS:
    assert item["taxonomy_tag"] in ALLOWED_TAGS
    assert item["example_id"] not in seen
    source_row = by_id[item["example_id"]]
    assert source_row["prediction_b"] != source_row["topic"]
    seen.add(item["example_id"])
taxonomy_counts = Counter(item["taxonomy_tag"] for item in TAGGED_ERRORS)
print("COURSE_FIXTURE taxonomy", dict(taxonomy_counts))

```

Saved output:

```text
COURSE_FIXTURE taxonomy {'dialect_gap': 3, 'hard_or_ambiguous': 3, 'class_confusion': 2}

```

## Cell 97

```python
recommendations = [
    {
        "priority": 1,
        "issue": "Gulf coverage for health and transport",
        "evidence": "dialect_gap tags in validation fixture",
        "change": "collect/review targeted Gulf examples",
        "acceptance_test": "new behavioural cases plus sliced CI",
    },
    {
        "priority": 2,
        "issue": "class confusion around app/status wording",
        "evidence": "EV-019 and EV-020",
        "change": "add contrastive examples and review label guide",
        "acceptance_test": "paired comparison without regression in other slices",
    },
    {
        "priority": 3,
        "issue": "underspecified short requests",
        "evidence": "hard_or_ambiguous tags",
        "change": "request context or abstain when confidence is low",
        "acceptance_test": "ambiguity behavioural suite",
    },
]
print(json.dumps(recommendations, ensure_ascii=False, indent=2))

```

Saved output:

```text
[
  {
    "priority": 1,
    "issue": "Gulf coverage for health and transport",
    "evidence": "dialect_gap tags in validation fixture",
    "change": "collect/review targeted Gulf examples",
    "acceptance_test": "new behavioural cases plus sliced CI"
  },
  {
    "priority": 2,
    "issue": "class confusion around app/status wording",
    "evidence": "EV-019 and EV-020",
    "change": "add contrastive examples and review label guide",
    "acceptance_test": "paired comparison without regression in other slices"
  },
  {
    "priority": 3,
    "issue": "underspecified short requests",
    "evidence": "hard_or_ambiguous tags",
    "change": "request context or abstain when confidence is low",
    "acceptance_test": "ambiguity behavioural suite"
  }
]

```

## Cell 98

```python
reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)
evaluation_report = {
    "data_kind": DATA_KIND,
    "split": "validation",
    "rows": len(rows),
    "macro_f1_a": interval_a,
    "macro_f1_b": interval_b,
    "paired_b_minus_a": paired_result,
    "paired_verdict": verdict,
    "behavioural": behavioural_summary,
    "taxonomy_counts": dict(taxonomy_counts),
    "top_fixes": recommendations,
}
(reports_dir / "day3_evaluation_fixture.json").write_text(
    json.dumps(evaluation_report, ensure_ascii=False, indent=2), encoding="utf-8"
)

with (reports_dir / "day3_slice_report.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(slice_report[0]))
    writer.writeheader()
    writer.writerows(slice_report)
with (reports_dir / "day3_error_taxonomy.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(TAGGED_ERRORS[0]))
    writer.writeheader()
    writer.writerows(TAGGED_ERRORS)
print("REPORTS_WRITTEN", sorted(path.name for path in reports_dir.glob("day3_*")))

```

Saved output:

```text
REPORTS_WRITTEN ['day3_error_taxonomy.csv', 'day3_evaluation_fixture.json', 'day3_slice_report.csv']

```

## Cell 99

```python
core_checks = {
    "fixture_disclosed": evaluation_report["data_kind"] == "COURSE_FIXTURE",
    "validation_only": evaluation_report["split"] == "validation",
    "confidence_intervals": interval_a["ci_low"] <= interval_a["estimate"] <= interval_a["ci_high"],
    "paired_comparison": "supports_directional_claim" in paired_result,
    "slices_present": len(slice_report) >= 8,
    "small_slice_flags_present": any(row["flag"] == "SMALL_SLICE" for row in slice_report),
    "behavioural_tests": behavioural_summary["total"] >= 5,
    "manual_taxonomy": len(TAGGED_ERRORS) >= 5 and bool(taxonomy_counts),
    "three_ranked_fixes": [row["priority"] for row in recommendations] == [1, 2, 3],
    "reports_written": all((reports_dir / name).exists() for name in [
        "day3_evaluation_fixture.json", "day3_slice_report.csv", "day3_error_taxonomy.csv"
    ]),
}
assert all(core_checks.values()), core_checks
print(core_checks)
print("DAY3_NOTEBOOK7_CORE=PASS")

```

Saved output:

```text
{'fixture_disclosed': True, 'validation_only': True, 'confidence_intervals': True, 'paired_comparison': True, 'slices_present': True, 'small_slice_flags_present': True, 'behavioural_tests': True, 'manual_taxonomy': True, 'three_ranked_fixes': True, 'reports_written': True}
DAY3_NOTEBOOK7_CORE=PASS

```

## Cell 100

```python
# اليوم الرابع — تحسين الاستدلال والخدمة

سأبدأ الآن مختبر Inference Optimisation & Serving، وأركز على تحسين سرعة الاستدلال، تجربة ONNX و INT8، وقياس الأداء وتجهيز الخدمة.
```

Saved output:

```text

```

## Cell 101

```python
# تثبيت النسخ المراجعة لليوم الرابع عند الحاجة فقط
import importlib.metadata
import os
import subprocess
import sys

os.environ.setdefault("DO_NOT_TRACK", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("ORT_DISABLE_TELEMETRY", "1")

assert sys.version_info >= (3, 11), "Day 4 Core requires Python 3.11+ (use the current Colab runtime)."
REQUIRED = {
    "transformers": "5.15.1",
    "tokenizers": "0.22.2",
    "onnx": "1.22.0",
    "onnxruntime": "1.29.0",
    "fastapi": "0.141.1",
    "httpx2": "2.12.0",
    "psutil": "7.2.2",
}
needs_install = []
for distribution, expected in REQUIRED.items():
    try:
        current = importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        current = None
    if current != expected:
        needs_install.append(f"{distribution}=={expected}")

if needs_install:
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", *needs_install
    ])

installed = {name: importlib.metadata.version(name) for name in REQUIRED}
assert installed == REQUIRED, (installed, REQUIRED)
print("DAY4_SETUP=PASS", installed)

```

Saved output:

```text
DAY4_SETUP=PASS {'transformers': '5.15.1', 'tokenizers': '0.22.2', 'onnx': '1.22.0', 'onnxruntime': '1.29.0', 'fastapi': '0.141.1', 'httpx2': '2.12.0', 'psutil': '7.2.2'}

```

## Cell 102

```python
import csv
import hashlib
import json
import os
import platform
import sys
import urllib.request
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from time import perf_counter_ns
from typing import Literal

import numpy as np
import onnx
import onnxruntime as ort
import psutil
import torch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from onnxruntime.quantization import QuantType, quantize_dynamic
from onnxruntime.quantization.preprocess import quant_pre_process
from pydantic import BaseModel, Field, field_validator
from transformers import AutoModelForSequenceClassification, AutoTokenizer

ort.disable_telemetry_events()

print("PYTHON", sys.version.split()[0])
print("TORCH", torch.__version__)
print("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
print("ORT_PROVIDERS", ort.get_available_providers())

```

Saved output:

```text
PYTHON 3.13.15
TORCH 2.11.0+cpu
DEVICE cpu
ORT_PROVIDERS ['AzureExecutionProvider', 'CPUExecutionProvider']

```

## Cell 103

```python
# ===== Student configuration =====
PROJECT_MODE = False
PROJECT_MODEL_SOURCE = ""       # e.g. /content/drive/MyDrive/bayan/model-v1
PROJECT_TOKENIZER_SOURCE = ""   # usually the same directory
PROJECT_VALIDATION_CSV = ""      # example_id,split,language,text,label
PROJECT_PREPROCESSING_VERSION = "ar-en-v1"

# Write these TARGET values before measuring project candidates.
PERFORMANCE_BUDGET = {
    "max_p95_ms": 1000.0,
    "min_throughput_items_s": 0.1,
    "max_quality_tax": 0.05,
    "target_device": "colab-cpu",
}
BUDGET_PROVENANCE = "COURSE_EXAMPLE_FOR_SYSTEMS_SMOKE"

WARMUP = 5
REPETITIONS = 30
MAX_LENGTH = 96
BATCH_SIZE = 4

if PROJECT_MODE:
    assert PROJECT_MODEL_SOURCE, "Set PROJECT_MODEL_SOURCE"
    assert PROJECT_TOKENIZER_SOURCE, "Set PROJECT_TOKENIZER_SOURCE"
    assert PROJECT_VALIDATION_CSV, "Set PROJECT_VALIDATION_CSV"
    assert BUDGET_PROVENANCE == "STUDENT_DEFINED_BEFORE_MEASUREMENT", (
        "For Gate D, record your own budget before measuring candidates."
    )
    ARTEFACT_ROLE = "PROJECT_ARTIFACT"
    RESULT_LABEL = "MEASURED"
else:
    ARTEFACT_ROLE = "SYSTEMS_SMOKE"
    RESULT_LABEL = "SYSTEMS_SMOKE"

assert WARMUP >= 1 and REPETITIONS >= 30
print("ARTEFACT_ROLE", ARTEFACT_ROLE)
print("BUDGET_PROVENANCE", BUDGET_PROVENANCE)
print("TARGET", PERFORMANCE_BUDGET)

```

Saved output:

```text
ARTEFACT_ROLE SYSTEMS_SMOKE
BUDGET_PROVENANCE COURSE_EXAMPLE_FOR_SYSTEMS_SMOKE
TARGET {'max_p95_ms': 1000.0, 'min_throughput_items_s': 0.1, 'max_quality_tax': 0.05, 'target_device': 'colab-cpu'}

```

## Cell 104

```python
COURSE_RAW = "https://raw.githubusercontent.com/almiyead-rgb/bayan-applied-nlp-course/main"
local_src = Path("src")
if not (local_src / "bayan" / "benchmarking.py").exists():
    local_src = Path("_bayan_course_src")
    package_dir = local_src / "bayan"
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "__init__.py").write_text("", encoding="utf-8")
    for module in ("benchmarking.py", "serving.py"):
        destination = package_dir / module
        urllib.request.urlretrieve(
            f"{COURSE_RAW}/src/bayan/{module}", destination
        )
sys.path.insert(0, str(local_src.resolve()))

from bayan.benchmarking import (
    artifact_size_mb,
    assess_budget,
    benchmark_callable,
    quality_tax,
    speedup,
)
from bayan.serving import (
    ServingManifest,
    build_prediction_response,
    run_canaries,
    sha256_file,
    validate_manifest,
    validate_request_text,
)

print("BAYAN_HELPERS=PASS", local_src)

```

Saved output:

```text
BAYAN_HELPERS=PASS _bayan_course_src

```

## Cell 105

```python
SYSTEMS_ROWS = [
    {"example_id": "S-01", "split": "validation", "language": "ar", "text": "الخدمة الإلكترونية واضحة وسريعة", "label": ""},
    {"example_id": "S-02", "split": "validation", "language": "en", "text": "The online service is clear and fast", "label": ""},
    {"example_id": "S-03", "split": "validation", "language": "ar", "text": "تعذر تسجيل الدخول إلى البوابة", "label": ""},
    {"example_id": "S-04", "split": "validation", "language": "en", "text": "I cannot sign in to the portal", "label": ""},
    {"example_id": "S-05", "split": "validation", "language": "ar", "text": "أحتاج معرفة حالة طلب التصريح", "label": ""},
    {"example_id": "S-06", "split": "validation", "language": "en", "text": "I need the status of my permit request", "label": ""},
    {"example_id": "S-07", "split": "validation", "language": "ar", "text": "تأخر موعد العيادة هذا الصباح", "label": ""},
    {"example_id": "S-08", "split": "validation", "language": "en", "text": "My clinic appointment was delayed this morning", "label": ""},
]

if PROJECT_MODE:
    validation_path = Path(PROJECT_VALIDATION_CSV)
    assert validation_path.is_file(), validation_path
    with validation_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required_columns = {"example_id", "split", "language", "text", "label"}
    assert rows and required_columns.issubset(rows[0]), required_columns
    assert all(row["split"] == "validation" for row in rows), (
        "Candidate selection must use validation only."
    )
    assert {"ar", "en"}.issubset({row["language"] for row in rows})
    assert all(row["label"].strip() for row in rows)
else:
    rows = SYSTEMS_ROWS

WORKLOAD_TEXTS = [row["text"] for row in rows]
workload_payload = json.dumps(rows, ensure_ascii=False, sort_keys=True).encode("utf-8")
WORKLOAD_SHA256 = hashlib.sha256(workload_payload).hexdigest()
assert len({row["example_id"] for row in rows}) == len(rows)
print("WORKLOAD", {"rows": len(rows), "languages": sorted({r["language"] for r in rows}), "sha256": WORKLOAD_SHA256})

```

Saved output:

```text
WORKLOAD {'rows': 8, 'languages': ['ar', 'en'], 'sha256': '1d1d1c3bef8a582931f6a1c1803671e8fe194fc36ae59cdc4f4feca9fc4d6785'}

```

## Cell 106

```python
if PROJECT_MODE:
    MODEL_SOURCE = PROJECT_MODEL_SOURCE
    TOKENIZER_SOURCE = PROJECT_TOKENIZER_SOURCE
else:
    MODEL_SOURCE = "google/bert_uncased_L-2_H-128_A-2"
    TOKENIZER_SOURCE = MODEL_SOURCE

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_SOURCE, use_fast=True)
model_kwargs = {"attn_implementation": "eager"}
if not PROJECT_MODE:
    model_kwargs.update(num_labels=3, ignore_mismatched_sizes=True)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_SOURCE, **model_kwargs
)
model.eval()
device = torch.device("cpu")  # Same target for PyTorch and ORT Core comparison.
model.to(device)

LABEL_MAP = {int(key): str(value) for key, value in model.config.id2label.items()}
assert LABEL_MAP
state_digest = hashlib.sha256()
for parameter_name, tensor in sorted(model.state_dict().items()):
    state_digest.update(parameter_name.encode("utf-8"))
    state_digest.update(tensor.detach().cpu().contiguous().numpy().tobytes())
PYTORCH_STATE_SHA256 = state_digest.hexdigest()
PYTORCH_PARAMETER_SIZE_MIB = sum(
    tensor.numel() * tensor.element_size() for tensor in model.state_dict().values()
) / (1024 ** 2)
print("MODEL_SOURCE", MODEL_SOURCE)
print("TOKENIZER_SOURCE", TOKENIZER_SOURCE)
print("LABEL_MAP", LABEL_MAP)
print("PYTORCH_REFERENCE", {"sha256": PYTORCH_STATE_SHA256, "parameter_size_mib": round(PYTORCH_PARAMETER_SIZE_MIB, 3)})

```

Saved output:

```text
Loading weights:   0%|          | 0/39 [00:00<?, ?it/s]
MODEL_SOURCE google/bert_uncased_L-2_H-128_A-2
TOKENIZER_SOURCE google/bert_uncased_L-2_H-128_A-2
LABEL_MAP {0: 'LABEL_0', 1: 'LABEL_1', 2: 'LABEL_2'}
PYTORCH_REFERENCE {'sha256': 'bb4406857d0fac886c61f11d5b2da6c6453988cf72b5772303eeb7ed0f9bf87b', 'parameter_size_mib': 16.732}

```

## Cell 107

```python
token_lists = tokenizer(WORKLOAD_TEXTS, add_special_tokens=True, truncation=False)["input_ids"]
token_lengths = np.asarray([len(tokens) for tokens in token_lists])
length_report = {
    "p50_tokens": float(np.percentile(token_lengths, 50)),
    "p95_tokens": float(np.percentile(token_lengths, 95)),
    "max_tokens": int(token_lengths.max()),
    "configured_max_length": MAX_LENGTH,
    "would_truncate": int((token_lengths > MAX_LENGTH).sum()),
}
assert length_report["would_truncate"] == 0 or PROJECT_MODE, (
    "Systems fixture should not truncate; inspect your project truncation deliberately."
)

encoded_batches = []
for start in range(0, len(WORKLOAD_TEXTS), BATCH_SIZE):
    batch = tokenizer(
        WORKLOAD_TEXTS[start:start + BATCH_SIZE],
        padding=True,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )
    encoded_batches.append({
        key: value.to(device)
        for key, value in batch.items()
        if key in {"input_ids", "attention_mask"}
    })
encoded = encoded_batches[0]  # Example inputs for export; dynamic axes handle later batches.
assert sum(batch["input_ids"].shape[0] for batch in encoded_batches) == len(WORKLOAD_TEXTS)
print("LENGTH_REPORT", length_report)
print("DYNAMIC_BATCH_SHAPES", [tuple(batch["input_ids"].shape) for batch in encoded_batches])

```

Saved output:

```text
LENGTH_REPORT {'p50_tokens': 18.0, 'p95_tokens': 28.95, 'max_tokens': 30, 'configured_max_length': 96, 'would_truncate': 0}
DYNAMIC_BATCH_SHAPES [(4, 30), (4, 26)]

```

## Cell 108

```python
try:
    process = psutil.Process(os.getpid())
    process.memory_info()
    memory_reader = lambda: process.memory_info().rss
    MEMORY_METHOD = "process RSS start and observed peak; approximate"
except (psutil.Error, OSError) as exc:
    process = None
    memory_reader = None
    MEMORY_METHOD = f"RSS unavailable in this runtime: {type(exc).__name__}"
if PROJECT_MODE:
    assert memory_reader is not None, "Gate D requires a documented memory measurement."

def pytorch_logits_from_encoded():
    outputs = []
    with torch.inference_mode():
        for batch in encoded_batches:
            outputs.append(model(**batch).logits.detach().cpu().numpy())
    return np.concatenate(outputs, axis=0)

def pytorch_end_to_end():
    outputs = []
    with torch.inference_mode():
        for start in range(0, len(WORKLOAD_TEXTS), BATCH_SIZE):
            fresh = tokenizer(
                WORKLOAD_TEXTS[start:start + BATCH_SIZE],
                padding=True,
                truncation=True,
                max_length=MAX_LENGTH,
                return_tensors="pt",
            )
            fresh = {
                key: value.to(device)
                for key, value in fresh.items()
                if key in {"input_ids", "attention_mask"}
            }
            outputs.append(model(**fresh).logits.detach().cpu().numpy())
    return np.concatenate(outputs, axis=0)

baseline_logits = pytorch_logits_from_encoded()
baseline_predictions = baseline_logits.argmax(axis=1)
baseline_model_report = benchmark_callable(
    pytorch_logits_from_encoded,
    warmup=WARMUP,
    repetitions=REPETITIONS,
    items_per_call=len(baseline_predictions),
    memory_reader=memory_reader,
)
baseline_e2e_report = benchmark_callable(
    pytorch_end_to_end,
    warmup=WARMUP,
    repetitions=REPETITIONS,
    items_per_call=len(baseline_predictions),
    memory_reader=memory_reader,
)
print("PYTORCH_MODEL_ONLY", {"p95_ms": round(baseline_model_report["p95_ms"], 3), "warmup": WARMUP, "repetitions": REPETITIONS, "items_per_call": len(WORKLOAD_TEXTS)})
print("PYTORCH_END_TO_END", {"measured": True, "boundary": "tokenisation + model", "saved_in": "reports/benchmark_results.json"})

```

Saved output:

```text
PYTORCH_MODEL_ONLY {'p95_ms': 18.995, 'warmup': 5, 'repetitions': 30, 'items_per_call': 8}
PYTORCH_END_TO_END {'measured': True, 'boundary': 'tokenisation + model', 'saved_in': 'reports/benchmark_results.json'}

```

## Cell 109

```python
ARTIFACT_DIR = Path("/content/bayan_day4_artifacts")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
FP32_ONNX = ARTIFACT_DIR / "bayan_model_fp32.onnx"
FP32_ONNX_PREPROCESSED = ARTIFACT_DIR / "bayan_model_fp32_preprocessed.onnx"
INT8_ONNX = ARTIFACT_DIR / "bayan_model_dynamic_int8.onnx"

class LogitsWrapper(torch.nn.Module):
    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def forward(self, input_ids, attention_mask):
        return self.inner(input_ids=input_ids, attention_mask=attention_mask).logits

wrapper = LogitsWrapper(model).eval()
torch.onnx.export(
    wrapper,
    (encoded["input_ids"], encoded["attention_mask"]),
    str(FP32_ONNX),
    input_names=["input_ids", "attention_mask"],
    output_names=["logits"],
    dynamic_axes={
        "input_ids": {0: "batch", 1: "sequence"},
        "attention_mask": {0: "batch", 1: "sequence"},
        "logits": {0: "batch"},
    },
    opset_version=17,
    do_constant_folding=True,
    dynamo=False,
)
onnx_model = onnx.load(str(FP32_ONNX))
onnx.checker.check_model(onnx_model)
assert FP32_ONNX.is_file() and FP32_ONNX.stat().st_size > 0
quant_pre_process(
    str(FP32_ONNX), str(FP32_ONNX_PREPROCESSED), skip_symbolic_shape=True
)
assert FP32_ONNX_PREPROCESSED.is_file() and FP32_ONNX_PREPROCESSED.stat().st_size > 0
print("ONNX_CHECKER=PASS", FP32_ONNX.name, round(artifact_size_mb(FP32_ONNX), 3), "MiB")
print("QUANT_PREPROCESS=PASS", FP32_ONNX_PREPROCESSED.name)

```

Saved output:

```text
/tmp/ipykernel_31035/986061057.py:16: DeprecationWarning: You are using the legacy TorchScript-based ONNX export. Starting in PyTorch 2.9, the new torch.export-based ONNX exporter has become the default. Learn more about the new export logic: https://docs.pytorch.org/docs/stable/onnx_export.html. For exporting control flow: https://pytorch.org/tutorials/beginner/onnx/export_control_flow_model_to_onnx_tutorial.html
  torch.onnx.export(
/usr/local/lib/python3.13/dist-packages/transformers/masking_utils.py:212: TracerWarning: Converting a tensor to a Python boolean might cause the trace to be incorrect. We can't record the data flow of Python values, so this value will be treated as a constant in the future. This means that the trace might not generalize to other inputs!
  if (padding_length := kv_length + kv_offset - attention_mask.shape[-1]) > 0:
/usr/local/lib/python3.13/dist-packages/transformers/masking_utils.py:603: TracerWarning: torch.tensor results are registered as constants in the trace. You can safely ignore this warning if you use this function to create tensors out of constant variables that would be the same every time you call this function. In any other case, this might cause the trace to be incorrect.
  mask = torch.where(mask, torch.tensor(0.0, device=mask.device, dtype=dtype), min_dtype)
/usr/local/lib/python3.13/dist-packages/torch/onnx/_internal/torchscript_exporter/symbolic_opset11.py:954: UserWarning: Exporting aten::index operator of advanced indexing in opset 17 is achieved by combination of multiple ONNX operators, including Reshape, Transpose, Concat, and Gather. If indices include negative values, the exported graph will produce incorrect results.
  return opset9.index(g, self, index)

ONNX_CHECKER=PASS bayan_model_fp32.onnx 16.788 MiB
QUANT_PREPROCESS=PASS bayan_model_fp32_preprocessed.onnx

```

## Cell 110

```python
def ort_inputs(batch):
    return {
        "input_ids": batch["input_ids"].detach().cpu().numpy().astype(np.int64),
        "attention_mask": batch["attention_mask"].detach().cpu().numpy().astype(np.int64),
    }

fp32_session = ort.InferenceSession(
    str(FP32_ONNX), providers=["CPUExecutionProvider"]
)
expected_inputs = {item.name for item in fp32_session.get_inputs()}
assert expected_inputs == {"input_ids", "attention_mask"}, expected_inputs

def fp32_ort_logits():
    return np.concatenate([
        fp32_session.run(["logits"], ort_inputs(batch))[0]
        for batch in encoded_batches
    ], axis=0)

fp32_logits = fp32_ort_logits()
fp32_predictions = fp32_logits.argmax(axis=1)
fp32_parity = {
    "max_abs_logits_diff": float(np.max(np.abs(baseline_logits - fp32_logits))),
    "mean_abs_logits_diff": float(np.mean(np.abs(baseline_logits - fp32_logits))),
    "prediction_agreement": float(np.mean(baseline_predictions == fp32_predictions)),
}
assert fp32_parity["max_abs_logits_diff"] < 1e-3, fp32_parity
assert fp32_parity["prediction_agreement"] == 1.0, fp32_parity

fp32_ort_report = benchmark_callable(
    fp32_ort_logits,
    warmup=WARMUP,
    repetitions=REPETITIONS,
    items_per_call=len(fp32_predictions),
    memory_reader=memory_reader,
)
print("ONNX_FP32_PARITY=PASS", {"max_abs_logits_diff": fp32_parity["max_abs_logits_diff"], "prediction_agreement": fp32_parity["prediction_agreement"]})
print("ONNX_FP32_MODEL_ONLY", {"p95_ms": round(fp32_ort_report["p95_ms"], 3), "warmup": WARMUP, "repetitions": REPETITIONS})

```

Saved output:

```text
ONNX_FP32_PARITY=PASS {'max_abs_logits_diff': 1.6391277313232422e-07, 'prediction_agreement': 1.0}
ONNX_FP32_MODEL_ONLY {'p95_ms': 9.541, 'warmup': 5, 'repetitions': 30}

```

## Cell 111

```python
int8_status = {"attempted": True, "available": False, "error": None}
int8_session = None
int8_report = None
int8_parity = None
try:
    quantize_dynamic(
        model_input=str(FP32_ONNX_PREPROCESSED),
        model_output=str(INT8_ONNX),
        weight_type=QuantType.QInt8,
    )
    int8_session = ort.InferenceSession(
        str(INT8_ONNX), providers=["CPUExecutionProvider"]
    )

    def int8_ort_logits():
        return np.concatenate([
            int8_session.run(["logits"], ort_inputs(batch))[0]
            for batch in encoded_batches
        ], axis=0)

    int8_logits = int8_ort_logits()
    int8_predictions = int8_logits.argmax(axis=1)
    int8_parity = {
        "max_abs_logits_diff": float(np.max(np.abs(baseline_logits - int8_logits))),
        "mean_abs_logits_diff": float(np.mean(np.abs(baseline_logits - int8_logits))),
        "prediction_agreement": float(np.mean(baseline_predictions == int8_predictions)),
    }
    int8_report = benchmark_callable(
        int8_ort_logits,
        warmup=WARMUP,
        repetitions=REPETITIONS,
        items_per_call=len(int8_predictions),
        memory_reader=memory_reader,
    )
    int8_status["available"] = True
    print("INT8_ATTEMPT=PASS", round(artifact_size_mb(INT8_ONNX), 3), "MiB")
    print("INT8_PARITY", {"prediction_agreement": int8_parity["prediction_agreement"]})
    print("INT8_MODEL_ONLY", {"p95_ms": round(int8_report["p95_ms"], 3), "warmup": WARMUP, "repetitions": REPETITIONS})
except Exception as exc:
    int8_status["error"] = f"{type(exc).__name__}: {exc}"
    print("INT8_ATTEMPT=DOCUMENTED_UNSUPPORTED", int8_status["error"])

assert int8_status["attempted"] is True
assert int8_status["available"] or int8_status["error"]

```

Saved output:

```text
INT8_ATTEMPT=PASS 4.287 MiB
INT8_PARITY {'prediction_agreement': 1.0}
INT8_MODEL_ONLY {'p95_ms': 7.922, 'warmup': 5, 'repetitions': 30}

```

## Cell 112

```python
def macro_f1(y_true, y_pred):
    labels = sorted(set(y_true) | set(y_pred))
    scores = []
    for label in labels:
        tp = sum(t == label and p == label for t, p in zip(y_true, y_pred))
        fp = sum(t != label and p == label for t, p in zip(y_true, y_pred))
        fn = sum(t == label and p != label for t, p in zip(y_true, y_pred))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return float(np.mean(scores)) if scores else 0.0

if PROJECT_MODE:
    y_true = [row["label"] for row in rows]
    baseline_labels = [LABEL_MAP[int(index)] for index in baseline_predictions]
    fp32_labels = [LABEL_MAP[int(index)] for index in fp32_predictions]
    baseline_quality = macro_f1(y_true, baseline_labels)
    fp32_quality = macro_f1(y_true, fp32_labels)
    quality_metric = "macro_f1_validation_full_workload"
else:
    baseline_quality = 1.0
    fp32_quality = fp32_parity["prediction_agreement"]
    quality_metric = "prediction_agreement_to_fp32_not_task_quality"

fp32_quality_tax = quality_tax(baseline_quality, fp32_quality)
fp32_budget = assess_budget(
    fp32_ort_report,
    quality_tax_value=fp32_quality_tax,
    max_p95_ms=PERFORMANCE_BUDGET["max_p95_ms"],
    max_quality_tax=PERFORMANCE_BUDGET["max_quality_tax"],
    min_throughput_items_s=PERFORMANCE_BUDGET["min_throughput_items_s"],
)

if int8_status["available"]:
    if PROJECT_MODE:
        int8_labels = [LABEL_MAP[int(index)] for index in int8_predictions]
        int8_quality = macro_f1(y_true, int8_labels)
    else:
        int8_quality = int8_parity["prediction_agreement"]
    int8_quality_tax = quality_tax(baseline_quality, int8_quality)
    int8_budget = assess_budget(
        int8_report,
        quality_tax_value=int8_quality_tax,
        max_p95_ms=PERFORMANCE_BUDGET["max_p95_ms"],
        max_quality_tax=PERFORMANCE_BUDGET["max_quality_tax"],
        min_throughput_items_s=PERFORMANCE_BUDGET["min_throughput_items_s"],
    )
else:
    int8_quality = None
    int8_quality_tax = None
    int8_budget = None

if int8_status["available"] and int8_budget["budget_met"]:
    selected_name = "onnx-dynamic-int8"
    selected_session = int8_session
    selected_sha256 = sha256_file(str(INT8_ONNX))
    adoption_decision = "ADOPT_INT8"
elif fp32_budget["budget_met"]:
    selected_name = "onnx-fp32"
    selected_session = fp32_session
    selected_sha256 = sha256_file(str(FP32_ONNX))
    adoption_decision = "ADOPT_ONNX_FP32"
else:
    selected_name = "pytorch-fp32"
    selected_session = None
    selected_sha256 = PYTORCH_STATE_SHA256
    adoption_decision = "KEEP_PYTORCH_FP32"

ship_decision = (
    "PROJECT_BUDGET_DECISION" if PROJECT_MODE else "SYSTEMS_SMOKE_NOT_A_SHIP_DECISION"
)
print("QUALITY_METRIC", quality_metric)
print("FP32_ORT_BUDGET", fp32_budget)
print("INT8_BUDGET", int8_budget)
print("SELECTED_FOR_SERVICE", selected_name, adoption_decision, ship_decision)

```

Saved output:

```text
QUALITY_METRIC prediction_agreement_to_fp32_not_task_quality
FP32_ORT_BUDGET {'latency_ok': True, 'quality_ok': True, 'throughput_ok': True, 'budget_met': True}
INT8_BUDGET {'latency_ok': True, 'quality_ok': True, 'throughput_ok': True, 'budget_met': True}
SELECTED_FOR_SERVICE onnx-dynamic-int8 ADOPT_INT8 SYSTEMS_SMOKE_NOT_A_SHIP_DECISION

```

## Cell 113

```python
manifest = ServingManifest(
    model_id=str(MODEL_SOURCE),
    model_version="project-v1" if PROJECT_MODE else "systems-smoke-v1",
    preprocessing_version=PROJECT_PREPROCESSING_VERSION,
    runtime=selected_name,
    label_map=LABEL_MAP,
    artifact_sha256=selected_sha256,
)
validate_manifest(
    manifest,
    expected_preprocessing_version=PROJECT_PREPROCESSING_VERSION,
)

def softmax(array):
    shifted = array - np.max(array, axis=-1, keepdims=True)
    values = np.exp(shifted)
    return values / values.sum(axis=-1, keepdims=True)

def service_predict(text, language="auto"):
    clean = validate_request_text(text, max_chars=1000)
    item = tokenizer(
        clean,
        padding=False,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="np",
    )
    inputs = {
        "input_ids": item["input_ids"].astype(np.int64),
        "attention_mask": item["attention_mask"].astype(np.int64),
    }
    start = perf_counter_ns()
    if selected_session is not None:
        logits = selected_session.run(["logits"], inputs)[0]
    else:
        torch_inputs = {key: torch.from_numpy(value).to(device) for key, value in inputs.items()}
        with torch.inference_mode():
            logits = model(**torch_inputs).logits.detach().cpu().numpy()
    latency_ms = (perf_counter_ns() - start) / 1_000_000
    probabilities = softmax(logits)[0]
    index = int(probabilities.argmax())
    return build_prediction_response(
        request_id=str(uuid.uuid4()),
        text=clean,
        language=language,
        label=LABEL_MAP[index],
        confidence=float(probabilities[index]),
        latency_ms=latency_ms,
        manifest=manifest,
    )

seed_canaries = [
    {"name": "arabic-contract", "text": "الخدمة واضحة", "language": "ar"},
    {"name": "english-contract", "text": "The service is clear", "language": "en"},
]
for case in seed_canaries:
    case["expected_label"] = service_predict(case["text"], case["language"])["prediction"]["label"]
print("CANARY_EXPECTATIONS", seed_canaries)

```

Saved output:

```text
CANARY_EXPECTATIONS [{'name': 'arabic-contract', 'text': 'الخدمة واضحة', 'language': 'ar', 'expected_label': 'LABEL_1'}, {'name': 'english-contract', 'text': 'The service is clear', 'language': 'en', 'expected_label': 'LABEL_1'}]

```

## Cell 114

```python
class ClassifyRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)
    language: Literal["ar", "en", "auto"] = "auto"

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, value):
        return validate_request_text(value, max_chars=1000)


@asynccontextmanager
async def lifespan(app):
    validate_manifest(
        manifest,
        expected_preprocessing_version=PROJECT_PREPROCESSING_VERSION,
    )
    app.state.canary_report = run_canaries(service_predict, seed_canaries)
    app.state.ready = True
    yield
    app.state.ready = False


app = FastAPI(title="Bayan Classification API", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {
        "status": "ready" if app.state.ready else "not_ready",
        "model_id": manifest.model_id,
        "model_version": manifest.model_version,
        "runtime": manifest.runtime,
        "preprocessing_version": manifest.preprocessing_version,
        "canaries": app.state.canary_report,
    }


@app.post("/v1/classify")
def classify(request: ClassifyRequest):
    return service_predict(request.text, request.language)

print("FASTAPI_APP=BUILT")

```

Saved output:

```text
FASTAPI_APP=BUILT

```

## Cell 115

```python
with TestClient(app) as client:
    health_response = client.get("/health")
    arabic_response = client.post(
        "/v1/classify", json={"text": "الخدمة واضحة", "language": "ar"}
    )
    english_response = client.post(
        "/v1/classify", json={"text": "The service is clear", "language": "en"}
    )
    empty_response = client.post(
        "/v1/classify", json={"text": "   ", "language": "auto"}
    )
    language_response = client.post(
        "/v1/classify", json={"text": "valid text", "language": "fr"}
    )

assert health_response.status_code == 200
assert health_response.json()["status"] == "ready"
assert len(health_response.json()["canaries"]) == 2
assert arabic_response.status_code == 200 and arabic_response.json()["language"] == "ar"
assert english_response.status_code == 200 and english_response.json()["language"] == "en"
assert empty_response.status_code == 422
assert language_response.status_code == 422
assert arabic_response.json()["model"]["preprocessing_version"] == PROJECT_PREPROCESSING_VERSION
service_test_summary = {
    "health": health_response.status_code,
    "arabic": arabic_response.status_code,
    "english": english_response.status_code,
    "empty_rejected": empty_response.status_code,
    "unsupported_language_rejected": language_response.status_code,
    "canaries": health_response.json()["canaries"],
}
print("FASTAPI_TESTCLIENT=PASS", service_test_summary)

```

Saved output:

```text
FASTAPI_TESTCLIENT=PASS {'health': 200, 'arabic': 200, 'english': 200, 'empty_rejected': 422, 'unsupported_language_rejected': 422, 'canaries': [{'name': 'arabic-contract', 'status': 'PASS', 'label': 'LABEL_1'}, {'name': 'english-contract', 'status': 'PASS', 'label': 'LABEL_1'}]}

```

## Cell 116

```python
def json_safe(value):
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value

environment = {
    "python": sys.version.split()[0],
    "platform": platform.platform(),
    "torch": torch.__version__,
    "onnx": onnx.__version__,
    "onnxruntime": ort.__version__,
    "device": str(device),
    "ort_provider": "CPUExecutionProvider",
}
benchmark_results = {
    "result_label": RESULT_LABEL,
    "artefact_role": ARTEFACT_ROLE,
    "warning": (
        "SYSTEMS_SMOKE proves mechanics only; replace with PROJECT_ARTIFACT for Gate D."
        if not PROJECT_MODE else None
    ),
    "environment": environment,
    "workload": {
        "rows": len(rows),
        "rows_measured_per_repetition": len(rows),
        "batch_size": BATCH_SIZE,
        "languages": sorted({row["language"] for row in rows}),
        "sha256": WORKLOAD_SHA256,
        "length": length_report,
    },
    "budget": PERFORMANCE_BUDGET,
    "budget_provenance": BUDGET_PROVENANCE,
    "measurement": {
        "warmup": WARMUP,
        "repetitions": REPETITIONS,
        "boundary": "model_only_primary_and_pytorch_end_to_end_secondary",
        "memory_method": MEMORY_METHOD,
    },
    "pytorch_fp32": {
        "model_only": baseline_model_report,
        "end_to_end": baseline_e2e_report,
        "parameter_size_mib": PYTORCH_PARAMETER_SIZE_MIB,
        "state_sha256": PYTORCH_STATE_SHA256,
        "quality_metric": quality_metric,
        "quality": baseline_quality,
    },
    "onnx_fp32": {
        "model_only": fp32_ort_report,
        "parity": fp32_parity,
        "size_mib": artifact_size_mb(FP32_ONNX),
        "sha256": sha256_file(str(FP32_ONNX)),
        "quality": fp32_quality,
        "quality_tax": fp32_quality_tax,
        "budget": fp32_budget,
        "p95_speedup_vs_pytorch": speedup(
            baseline_model_report["p95_ms"], fp32_ort_report["p95_ms"]
        ),
    },
    "onnx_dynamic_int8": {
        "status": int8_status,
        "model_only": int8_report,
        "parity": int8_parity,
        "size_mib": artifact_size_mb(INT8_ONNX) if int8_status["available"] else None,
        "sha256": sha256_file(str(INT8_ONNX)) if int8_status["available"] else None,
        "quality": int8_quality,
        "quality_tax": int8_quality_tax,
        "budget": int8_budget,
    },
    "selected_for_service": selected_name,
    "adoption_decision": adoption_decision,
    "decision_scope": ship_decision,
    "fp32_rollback": "Re-export from recorded MODEL_SOURCE; weights stay outside GitHub.",
}

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)
(reports_dir / "benchmark_results.json").write_text(
    json.dumps(json_safe(benchmark_results), ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
(reports_dir / "service_smoke.json").write_text(
    json.dumps(
        json_safe({
            "result_label": RESULT_LABEL,
            "artefact_role": ARTEFACT_ROLE,
            "manifest": manifest.to_dict(),
            "tests": service_test_summary,
        }),
        ensure_ascii=False,
        indent=2,
    ) + "\n",
    encoding="utf-8",
)

benchmarks_draft = (
    f"# BENCHMARKS draft — {ARTEFACT_ROLE}\n\n"
    f"- Result label: `{RESULT_LABEL}`\n"
    f"- Decision scope: `{ship_decision}`\n"
    f"- Workload SHA-256: `{WORKLOAD_SHA256}`\n"
    f"- Device/provider: `{device}` / `CPUExecutionProvider`\n"
    f"- Warm-up/repetitions: {WARMUP}/{REPETITIONS}\n"
    f"- Memory method: {MEMORY_METHOD}\n"
    f"- PyTorch p95: {baseline_model_report['p95_ms']:.3f} ms\n"
    f"- ONNX FP32 p95: {fp32_ort_report['p95_ms']:.3f} ms\n"
    f"- ONNX FP32 quality tax: {fp32_quality_tax:.6f}\n"
    f"- INT8 available: {int8_status['available']}\n"
    f"- Selected for service: `{selected_name}`\n\n"
    f"- Adoption decision: `{adoption_decision}`\n\n"
    "> Replace this smoke draft with the complete BENCHMARKS template "
    "and full project workload before Gate D.\n"
)
(reports_dir / "BENCHMARKS_DRAFT.md").write_text(benchmarks_draft, encoding="utf-8")
print("REPORTS_WRITTEN", [
    "reports/benchmark_results.json",
    "reports/service_smoke.json",
    "reports/BENCHMARKS_DRAFT.md",
])

```

Saved output:

```text
REPORTS_WRITTEN ['reports/benchmark_results.json', 'reports/service_smoke.json', 'reports/BENCHMARKS_DRAFT.md']

```

## Cell 117

```python
core_checks = {
    "artefact_role_disclosed": ARTEFACT_ROLE in {"SYSTEMS_SMOKE", "PROJECT_ARTIFACT"},
    "budget_written_before_candidates": bool(BUDGET_PROVENANCE),
    "warmup_and_repetitions": WARMUP >= 1 and REPETITIONS >= 30,
    "bilingual_workload": {"ar", "en"}.issubset({row["language"] for row in rows}),
    "length_audited": set(length_report) >= {"p50_tokens", "p95_tokens", "max_tokens"},
    "baseline_tail_latency": set(baseline_model_report) >= {"p50_ms", "p95_ms", "p99_ms", "throughput_items_s"},
    "onnx_checked": FP32_ONNX.is_file(),
    "onnx_numerical_parity": fp32_parity["max_abs_logits_diff"] < 1e-3,
    "onnx_prediction_parity": fp32_parity["prediction_agreement"] == 1.0,
    "int8_attempt_honest": int8_status["attempted"] and (int8_status["available"] or bool(int8_status["error"])),
    "quality_tax_explicit": isinstance(fp32_quality_tax, float),
    "fastapi_contract": all(code in {200, 422} for code in service_test_summary.values() if isinstance(code, int)),
    "startup_canaries": len(service_test_summary["canaries"]) == 2,
    "reports_written": all((reports_dir / name).is_file() for name in [
        "benchmark_results.json", "service_smoke.json", "BENCHMARKS_DRAFT.md"
    ]),
    "large_artifacts_outside_repo": str(ARTIFACT_DIR).startswith("/content/"),
}
assert all(core_checks.values()), core_checks
print(core_checks)
print("DAY4_NOTEBOOK8_CORE=PASS")
if not PROJECT_MODE:
    print("NEXT_REQUIRED_FOR_GATE_D=RERUN_WITH_PROJECT_ARTIFACT_AND_FULL_WORKLOAD")

```

Saved output:

```text
{'artefact_role_disclosed': True, 'budget_written_before_candidates': True, 'warmup_and_repetitions': True, 'bilingual_workload': True, 'length_audited': True, 'baseline_tail_latency': True, 'onnx_checked': True, 'onnx_numerical_parity': True, 'onnx_prediction_parity': True, 'int8_attempt_honest': True, 'quality_tax_explicit': True, 'fastapi_contract': True, 'startup_canaries': True, 'reports_written': True, 'large_artifacts_outside_repo': True}
DAY4_NOTEBOOK8_CORE=PASS
NEXT_REQUIRED_FOR_GATE_D=RERUN_WITH_PROJECT_ARTIFACT_AND_FULL_WORKLOAD

```

## Cell 118

```python

```

Saved output:

```text

```

## Cell 119

```python

```

Saved output:

```text

```

## Cell 120

```python

```

Saved output:

```text

```

## Cell 121

```python

```

Saved output:

```text

```

## Cell 122

```python

```

Saved output:

```text

```