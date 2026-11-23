import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from auditor.auditor import (
    check_alt_text,
    check_non_inclusive,
    readability_grade,
    audit,
    generate_report,
)


def test_alt_text_missing():
    content = "![  ](img.png)\n![alt](img2.png)"
    issues = check_alt_text(content)
    assert len(issues) == 1
    assert "img.png" in issues[0]


def test_alt_text_ok():
    content = "![description](img.png)"
    assert check_alt_text(content) == []


def test_html_img_missing_alt():
    content = '<img src="x.png">'
    issues = check_alt_text(content)
    assert len(issues) == 1


def test_non_inclusive():
    content = "Use whitelist and blacklist"
    issues = check_non_inclusive(content)
    assert len(issues) == 2


def test_non_inclusive_ok():
    content = "Use allowlist and denylist"
    assert check_non_inclusive(content) == []


def test_readability_grade():
    text = "The cat sat on the mat. It was a good day."
    grade = readability_grade(text)
    assert isinstance(grade, float)


def test_audit():
    content = "# Hello\n![  ](img.png)\nUse whitelist"
    result = audit(content)
    assert len(result["alt_text_issues"]) == 1
    assert len(result["non_inclusive_issues"]) == 1
    assert isinstance(result["readability_grade"], float)


def test_generate_report():
    results = [audit("# Test\n![  ](img.png)")]
    report = generate_report(results)
    assert "# Inclusion Audit Report" in report
    assert "Alt-text issues" in report
