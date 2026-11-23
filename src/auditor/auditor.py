"""Markdown inclusion auditor."""
import re
import os

NON_INCLUSIVE_TERMS = [
    "whitelist", "blacklist", "master", "slave", "dummy", "sanity check",
    "guys", "manpower", "man-hours",
]


def check_alt_text(content: str) -> list:
    """Find images missing alt text."""
    issues = []
    # Markdown images: ![alt](url) — flag empty alt
    for m in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", content):
        alt = m.group(1).strip()
        url = m.group(2)
        if not alt:
            issues.append(f"Image missing alt text: {url}")
    # HTML img tags without alt
    for m in re.finditer(r"<img\b[^>]*>", content, re.IGNORECASE):
        tag = m.group(0)
        if "alt=" not in tag.lower():
            issues.append(f"HTML img missing alt attribute: {tag[:60]}")
    return issues


def readability_grade(content: str) -> float:
    """Approximate Flesch-Kincaid grade level."""
    # Strip markdown
    text = re.sub(r"[#*`\[\]()]", " ", content)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    words = text.split()
    if not sentences or not words:
        return 0.0
    syllables = sum(_count_syllables(w) for w in words)
    grade = 0.39 * (len(words) / len(sentences)) + 11.8 * (syllables / len(words)) - 15.59
    return round(grade, 2)


def _count_syllables(word: str) -> int:
    word = word.lower().strip(".,!?;:")
    if not word:
        return 0
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in "aeiouy"
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def check_non_inclusive(content: str) -> list:
    """Find non-inclusive terms."""
    issues = []
    lower = content.lower()
    for term in NON_INCLUSIVE_TERMS:
        if term in lower:
            issues.append(f"Non-inclusive term found: '{term}'")
    return issues


def audit(content: str) -> dict:
    return {
        "alt_text_issues": check_alt_text(content),
        "readability_grade": readability_grade(content),
        "non_inclusive_issues": check_non_inclusive(content),
    }


def audit_file(path: str) -> dict:
    with open(path) as f:
        content = f.read()
    result = audit(content)
    result["file"] = path
    return result


def generate_report(results: list) -> str:
    lines = ["# Inclusion Audit Report", ""]
    for r in results:
        lines.append(f"## {r.get('file', 'content')}")
        lines.append(f"- Readability grade: {r['readability_grade']}")
        if r["alt_text_issues"]:
            lines.append("- Alt-text issues:")
            for i in r["alt_text_issues"]:
                lines.append(f"  - {i}")
        else:
            lines.append("- Alt-text: OK")
        if r["non_inclusive_issues"]:
            lines.append("- Non-inclusive terms:")
            for i in r["non_inclusive_issues"]:
                lines.append(f"  - {i}")
        else:
            lines.append("- Inclusive language: OK")
        lines.append("")
    return "\n".join(lines)
