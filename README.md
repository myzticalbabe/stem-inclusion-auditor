# stem-inclusion-auditor

Inclusion auditor MVP: alt-text, readability grade, non-inclusive terms, markdown report.

## Usage

```bash
python -m auditor.cli <file-or-dir> [--report report.md]
```

## Sample Report

Running on a file with missing alt text and non-inclusive terms produces a markdown report listing issues.

## Tests

```bash
pytest
```
