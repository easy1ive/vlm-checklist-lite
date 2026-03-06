# vlm-checklist-lite

A compact, capability-oriented evaluator for vision-language model outputs.

## Motivation

Large benchmark scores often hide where a VLM fails. This project tracks performance by capabilities (object, attribute, relation, OCR, reasoning) to make model iteration more interpretable.

## Features

- JSONL-based evaluation format that is easy to version with experiments.
- Lightweight metrics: exact match + token-level F1.
- Capability-level aggregation for diagnosis.
- Optional radar plot generation for quick visual comparison.

## Data format

Each line in JSONL should contain:

```json
{
  "id": "sample-001",
  "capability": "ocr",
  "prompt": "What number is shown on the sign?",
  "reference": "42",
  "prediction": "forty two"
}
```

## Install

```bash
pip install -e .
```

## Direction

This repo is designed as a practical bridge between quick model iteration and more formal benchmark suites.
