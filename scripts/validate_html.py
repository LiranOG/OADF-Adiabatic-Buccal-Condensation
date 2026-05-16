#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OADF :: HTML Structural Validator
=================================

Zero-dependency (stdlib only) structural integrity checker for the OADF web
artifacts. Verifies:

  1. File is UTF-8 decodable.
  2. <!DOCTYPE html> declaration is present.
  3. <html lang="..."> attribute exists.
  4. <meta charset="..."> declaration is present.
  5. <title>...</title> non-empty.
  6. All opened tags (excluding void elements) are properly closed
     in correct LIFO order.

Exit codes:
  0  all files passed
  1  one or more files failed validation
  2  invocation / I/O error

Usage:
  python3 scripts/validate_html.py [PATH ...]
    PATH may be a file or a directory. If a directory, all *.html files
    within (non-recursive) are validated. Defaults to `docs/web`.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Tuple

# Void elements per HTML5 spec — self-closing, no end tag expected.
VOID_ELEMENTS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
})


class StructuralValidator(HTMLParser):
    """Tracks tag-stack balance and required-element presence."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: List[Tuple[str, int]] = []
        self.errors: List[str] = []
        self.has_html_lang: bool = False
        self.has_meta_charset: bool = False
        self.has_title: bool = False
        self._in_title: bool = False
        self._title_buf: List[str] = []

    # ---- handlers ----------------------------------------------------------
    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_dict = {k.lower(): (v or "") for k, v in attrs}

        if tag == "html" and attr_dict.get("lang", "").strip():
            self.has_html_lang = True
        if tag == "meta" and attr_dict.get("charset", "").strip():
            self.has_meta_charset = True
        if tag == "title":
            self._in_title = True

        if tag not in VOID_ELEMENTS:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
            if "".join(self._title_buf).strip():
                self.has_title = True

        if tag in VOID_ELEMENTS:
            return  # void elements never produce end tags in valid markup

        if not self.stack:
            self.errors.append(
                f"L{self.getpos()[0]}: unexpected </{tag}> with empty tag stack"
            )
            return

        # Tolerate optional-end-tag elements (li, p, etc.) by popping until match.
        # If mismatch persists, record but continue.
        if self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            # Look back for a matching open tag.
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    unclosed = [t for t, _ in self.stack[i + 1:]]
                    self.errors.append(
                        f"L{self.getpos()[0]}: </{tag}> closes tag opened at "
                        f"L{self.stack[i][1]}, but inner tags {unclosed} "
                        f"are still open"
                    )
                    self.stack = self.stack[:i]
                    return
            self.errors.append(
                f"L{self.getpos()[0]}: stray </{tag}> with no matching opener"
            )

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_buf.append(data)

    # ---- finalize ----------------------------------------------------------
    def finalize(self) -> None:
        for tag, line in self.stack:
            self.errors.append(f"L{line}: <{tag}> opened but never closed")


def _validate_one(path: Path) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return False, [f"I/O error: {exc}"]

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return False, [f"not valid UTF-8: {exc}"]

    if not re.match(r"^\s*<!DOCTYPE\s+html\s*>", text, flags=re.IGNORECASE):
        errors.append("missing or malformed <!DOCTYPE html> declaration")

    parser = StructuralValidator()
    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:  # noqa: BLE001 — surface any parser-internal failure
        errors.append(f"parser exception: {exc}")
    parser.finalize()

    if not parser.has_html_lang:
        errors.append('<html> missing required `lang="..."` attribute')
    if not parser.has_meta_charset:
        errors.append('missing <meta charset="..."> declaration')
    if not parser.has_title:
        errors.append("missing or empty <title>")

    errors.extend(parser.errors)
    return (not errors), errors


def _collect_targets(args: List[str]) -> List[Path]:
    paths: List[Path] = []
    raw = args or ["docs/web"]
    for entry in raw:
        p = Path(entry)
        if p.is_dir():
            paths.extend(sorted(p.glob("*.html")))
        elif p.is_file():
            paths.append(p)
        else:
            print(f"[WARN] skipping non-existent path: {p}", file=sys.stderr)
    return paths


def main(argv: List[str]) -> int:
    targets = _collect_targets(argv[1:])
    if not targets:
        print("[FATAL] no HTML files to validate", file=sys.stderr)
        return 2

    overall_ok = True
    for path in targets:
        ok, errs = _validate_one(path)
        if ok:
            print(f"[OK]   {path}")
        else:
            overall_ok = False
            print(f"[FAIL] {path}")
            for e in errs:
                print(f"       - {e}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
