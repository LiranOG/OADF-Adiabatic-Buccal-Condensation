# Contributing

Procedural standards for contributions to the **Oral Adiabatic Decompression
Fog (OADF)** repository. Compliance is mandatory; non-compliant submissions
are closed without review.

---

## 1. Scope

Accepted:

- Corrections to derivations, equations, constants, or citations in
  `docs/paper/OADF_academic_paper.tex`.
- Experimental data, instrumentation protocols, or quantitative
  characterizations of OADF (schlieren imaging, transient *P(t)* / *T(t)*
  traces, droplet-size distributions, CCN counts).
- Refinements to the bio-aerosol CCN model, including treatment of organic
  surfactants and their effect on the critical supersaturation.
- Additional language versions of `docs/web/mouth_cloud_effect_*.html`.
- Improvements to `Makefile`, `scripts/validate_html.py`,
  `.github/workflows/ci.yml`.
- Repository documentation (`README.md`, `SECURITY.md`, `CITATION.cff`).

Rejected:

- Speculative content without citation to peer-reviewed literature.
- Marketing, promotional, or non-technical language.
- Renaming the phenomenon. *Oral Adiabatic Decompression Fog* is a fixed
  deliverable.
- Patches that conflate OADF with cold-breath *mixing fog* — the mechanistic
  distinction is established in §6 of the paper.

---

## 2. Issue Protocol

Before opening an issue:

1. Search open and closed issues for duplicates.
2. Select the correct template — `bug_report.yml` or `feature_request.yml`.
3. Provide a minimum reproducible example for build failures, including
   compiler version (`pdflatex --version` or `latexmk --version`) and the
   last 30 lines of the error log.
4. Use SI units, vector/scalar distinction, and citations where applicable.

Security issues follow the protocol in [`SECURITY.md`](SECURITY.md). Do not
file them as public issues.

---

## 3. Branching and Commit Conventions

### Branch names

| Prefix    | Purpose                                  |
|-----------|------------------------------------------|
| `paper/`  | LaTeX source                             |
| `web/`    | HTML articles                            |
| `tools/`  | Makefile, scripts, CI                    |
| `docs/`   | Repository documentation                 |
| `chore/`  | Hygiene, metadata, dependency bumps      |
| `fix/`    | Bug resolution (must reference an issue) |

### Commit messages

[Conventional Commits](https://www.conventionalcommits.org/) syntax:
`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `ci:`, `style:`.
Subject line ≤ 72 characters, imperative mood, no trailing period. Provide
a body explaining *what* changed and *why* for any non-trivial change.

---

## 4. LaTeX Source Standards (`docs/paper/`)

- **Encoding:** UTF-8.
- **Line length:** ≤ 100 columns. One sentence per line is preferred.
- **Indentation:** 2 spaces; no tabs.
- **Dimensional quantities:** `siunitx` macros (`\SI`, `\si`, `\num`)
  exclusively.
- **Chemical formulae:** `mhchem` (`\ce{...}`) exclusively.
- **Vectors:** `\mathbf` (text/inline), `\vec` (display only).
- **Equation labels:** `eq:short-descriptive-handle`.
- **Cross-references:** explicit `Sec.~\ref{...}`, `Eq.~\ref{...}`, and
  `Table~\ref{...}` forms are accepted; a future style-only pass may migrate
  to `cleveref`.
- **Bibliography keys:** `AuthorYEAR` (e.g., `Wilson1911`, `Koehler1936`).
- **Floats:** placed near first reference. `[H]` requires justification.
- **Deprecated commands prohibited:** `\bf`, `\it`, `\rm`.

`make paper` must produce a **zero-warning compile** before submission.

---

## 5. HTML Standards (`docs/web/`)

- `<!DOCTYPE html>` on line 1.
- `<html lang="...">` with correct ISO 639-1 code; `dir="rtl"` for Hebrew.
- `<meta charset="utf-8">` as the first `<meta>` element.
- Non-empty `<title>`, ≤ 60 characters.
- Accessibility: semantic landmarks, `alt` on every `<img>`, WCAG AA
  contrast minimum.
- `make validate` must exit `0`.
- Locale parity: a change to one locale requires the cognate change to the
  other, or explicit justification of the asymmetry.

---

## 6. Python Script Standards (`scripts/`)

- **Stdlib only.** No third-party runtime dependencies.
- PEP 8 compliance.
- Type hints on all public functions.
- Docstrings (Google or NumPy style).
- Exit codes: `0` success; `1` validation failure; `2` invocation error.

---

## 7. Pull Request Workflow

1. Fork; clone fork; create feature branch per §3.
2. Make focused, logically atomic commits.
3. Run the full local pipeline:
   ```bash
   make clean
   make paper
   make validate
   ```
4. Push; open a PR against `main`.
5. Complete every applicable section of the PR template.
6. Ensure CI is green.
7. Respond to review comments within 30 days.

---

## 8. Review Criteria

| Axis              | Question                                                  |
|-------------------|-----------------------------------------------------------|
| Correctness       | Does the change agree with cited literature / observation? |
| Reproducibility   | Does `make paper && make validate` succeed on a clean clone? |
| Style compliance  | Does the change adhere to §4–§6?                          |
| Atomicity         | Single logical concern per PR?                            |
| Documentation     | Equations labeled, references current, comments clear?    |
| Locale parity     | HTML changes cover all locales or justify asymmetry?      |

---

## 9. Maintainer

Liran Schwartz · GitHub: [`@LiranOG`](https://github.com/LiranOG) ·
ORCID: [0009-0008-8035-1308](https://orcid.org/0009-0008-8035-1308) ·
Contact: `scliran9@gmail.com`.

---

## 10. Contribution Licensing (Inbound License Terms)

By submitting a pull request, issue comment, patch, dataset, translation,
figure, equation, derivation, or any other contribution to this repository
(each a "**Contribution**"), the contributor irrevocably accepts the
following terms. These terms are non-negotiable and form a condition
precedent to acceptance of any merge.

### 10.1 Inbound = Outbound

Every Contribution is licensed to the project under the license that
governs the file or content class it modifies, as defined by the
[`LICENSE`](LICENSE) file at the root of this repository (the
"Dual-Licensing Architecture"). The applicable inbound license is
determined by the Contribution's target as follows.

### 10.2 Software-Layer Contributions → MIT License

Any Contribution to the **Software Layer** is automatically and
irrevocably licensed under the **MIT License**
(SPDX identifier: `MIT`), identical in terms to the MIT text in
[`LICENSE`](LICENSE) Section 5. The Software Layer includes:

- `Makefile`
- `scripts/**` (including `validate_html.py`)
- `.github/workflows/**` (CI/CD configuration)
- `.github/ISSUE_TEMPLATE/**` and `.github/PULL_REQUEST_TEMPLATE.md`
- `.gitignore`
- Repository documentation: `README.md`, `CONTRIBUTING.md`, `SECURITY.md`,
  `LICENSE`, `CITATION.cff`
- The structural HTML / CSS / JavaScript scaffolding of
  `docs/web/*.html` (the *shell*, not the embedded scientific content —
  see §10.3 and `LICENSE` Section 3 for the intra-file split).

### 10.3 Academic-Layer Contributions → Creative Commons Attribution 4.0 International

Any Contribution to the **Academic Layer** is automatically and
irrevocably licensed under the **Creative Commons Attribution 4.0
International License** (SPDX identifier: `CC-BY-4.0`), canonically hosted
at https://creativecommons.org/licenses/by/4.0/legalcode. The Academic
Layer includes:

- `docs/paper/OADF_academic_paper.tex`
- `docs/paper/OADF_academic_paper.pdf`
- All scientific prose, equations, derivations, figures, tables, and
  thermodynamic / aerosol-physics model exposition embedded within
  `docs/web/*.html`
- Any direct quotation of the above appearing in any other repository
  document.

This category includes — without limitation — physics-model refinements,
new derivations, additional figures, experimental datasets, translations
of the popular-science HTML articles, and any pedagogical reformulation
of the OADF four-phase decomposition.

### 10.4 Mixed-Content Contributions

A Contribution that modifies both layers (e.g., editing both the DOM
scaffolding and the scientific paragraph within a single HTML file) is
split at the granularity of the change: the lines, fragments, or commits
affecting the Software Layer are inbound under MIT; the lines, fragments,
or commits affecting the Academic Layer are inbound under CC BY 4.0.
Contributors should — when practicable — separate such changes into
distinct commits to preserve provenance.

### 10.5 Primary Copyright Holder; Attribution Stack

For the avoidance of doubt:

- The **primary copyright holder** of the OADF project, including the
  scholarly content of the paper and the OADF model itself, is
  **Liran Schwartz** (ORCID
  [0009-0008-8035-1308](https://orcid.org/0009-0008-8035-1308)).
- Contributors retain copyright in their individual Contributions but
  irrevocably grant the project the licenses defined in §10.2–§10.4
  above.
- Attribution to contributors is preserved through the repository's
  Git history. Substantive academic contributions may, at the
  maintainer's discretion, be acknowledged in the manuscript's
  Acknowledgments section in a future revision.

### 10.6 Contributor Representations

By submitting a Contribution, the contributor represents and warrants
that:

1. The Contribution is the contributor's original work, or the
   contributor holds the necessary rights to license it under the terms
   above.
2. The Contribution does not knowingly infringe the copyright,
   trademark, patent, or trade-secret rights of any third party.
3. The contributor has the legal capacity and authority to enter into
   this agreement.
4. If the contributor's employer or affiliated institution holds rights
   in the Contribution, the contributor has secured authorization to
   submit the Contribution under the terms above.

### 10.7 No Warranty; No Obligation to Merge

Contributions are accepted "AS IS" without warranty of any kind, express
or implied. The maintainer is under no obligation to accept, review, or
incorporate any Contribution, and may reject or revert any Contribution
for any reason consistent with the project's stated scope (§1) and
review criteria (§8).

### 10.8 Severability

If any provision of §10 is held by a court of competent jurisdiction to
be unenforceable, the remaining provisions remain in full force and
effect.
