<!--
  OADF :: Pull Request Template
  Incomplete checklists block review. Delete sections that are not
  applicable, but do NOT delete the checklist itself.
-->

## Summary

<!-- One paragraph (≤ 5 sentences). What does this PR change, and why? -->

## Type of change

<!-- Check all that apply. -->

- [ ] **paper** — LaTeX source / equations / references / figures
- [ ] **web** — `mouth_cloud_effect_*.html`
- [ ] **tools** — `Makefile` / `scripts/` / CI / `.github/`
- [ ] **docs** — `README.md` / `CONTRIBUTING.md` / `SECURITY.md`
- [ ] **chore** — dependencies / hygiene / metadata
- [ ] **fix** — resolves a tracked bug (link below)

## Linked issues

<!-- e.g. "Closes #42", "Refs #17". -->

Closes #

---

## Pre-submission Checklist

### Universal

- [ ] My branch name follows the convention in [`CONTRIBUTING.md` §3](../blob/main/CONTRIBUTING.md#3-branching--commit-conventions).
- [ ] My commits follow Conventional Commits (`feat:`, `fix:`, `docs:`, …).
- [ ] I rebased onto the latest `main` and resolved all conflicts.
- [ ] I have read and abide by the project's contribution standards.
- [ ] No secrets, tokens, or personally identifying information are introduced.

### LaTeX changes (`docs/paper/**`)

- [ ] `make paper` succeeds locally with **zero warnings** (or warnings are explained).
- [ ] All equations use `siunitx` for units and `mhchem` for chemistry.
- [ ] All cross-references use `\cref` / `\Cref` from `cleveref`.
- [ ] New bibliography entries follow the `AuthorYEAR` key convention.
- [ ] Figures are vector (PDF / TikZ) where possible; raster is justified.
- [ ] Line width is ≤ 100 columns; encoding is UTF-8.

### HTML changes (`docs/web/**`)

- [ ] `make validate` succeeds locally with exit code 0.
- [ ] `<!DOCTYPE html>`, `<html lang="…">`, `<meta charset="utf-8">`, non-empty `<title>` are all present.
- [ ] If I changed one locale (EN / HE), I made the cognate change in the other — or I explicitly justify the asymmetry.
- [ ] Accessibility: every `<img>` has `alt`, semantic landmarks used, contrast ≥ WCAG AA.
- [ ] No external CDN is required for the page to be readable offline.

### Tooling changes (`Makefile`, `scripts/`, `.github/`)

- [ ] `Makefile` targets are `.PHONY`-declared where appropriate.
- [ ] Python scripts use **stdlib only** — no new `pip` dependencies.
- [ ] CI changes have been validated with `actionlint` or equivalent.
- [ ] Action versions are pinned (major version or SHA).
- [ ] `permissions:` blocks remain minimum-scoped.

### Documentation changes

- [ ] Internal links resolve correctly on GitHub.
- [ ] Markdown is rendered-previewed; no broken tables, headers, or code fences.
- [ ] If commands changed, all examples in `README.md` were updated.

---

## How was this tested?

<!--
  Describe the validation you performed. Reproducible commands preferred.
  Example:
    make clean && make paper && make validate
    # PDF: docs/paper/OADF_academic_paper.pdf renders 24 pages, zero warnings.
    # Validator: both HTML files pass.
-->

```bash

```

## Screenshots / rendered output (if applicable)

<!-- For HTML or figure changes, attach before/after screenshots. -->

## Reviewer notes

<!--
  Anything reviewers should know that isn't obvious from the diff:
  unusual assumptions, deferred follow-ups, known limitations.
-->
