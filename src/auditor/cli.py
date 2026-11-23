"""CLI for inclusion auditor."""
import argparse
import os
import sys

from .auditor import audit_file, generate_report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inclusion Auditor")
    parser.add_argument("path", help="File or directory to audit")
    parser.add_argument("--report", help="Output report file")
    args = parser.parse_args(argv)

    if os.path.isdir(args.path):
        results = []
        for root, _, files in os.walk(args.path):
            for fn in files:
                if fn.endswith(".md"):
                    results.append(audit_file(os.path.join(root, fn)))
    else:
        results = [audit_file(args.path)]

    report = generate_report(results)
    if args.report:
        with open(args.report, "w") as f:
            f.write(report)
        print(f"Report written to {args.report}")
    else:
        print(report)


if __name__ == "__main__":
    main()
