# Security Policy

This repository ships a LaTeX manuscript, two static HTML documents, build
automation (`Makefile`, GitHub Actions), and a stdlib-only Python validator.
It exposes no runtime service, no network listener, and no executable
binary. Supply-chain and tooling vulnerabilities nevertheless apply. This
document defines the disclosure protocol.

## Maintainer

| Role          | Identity                                                  |
|---------------|-----------------------------------------------------------|
| Maintainer    | Liran Schwartz (GitHub: [`@LiranOG`](https://github.com/LiranOG)) |
| ORCID         | [0009-0008-8035-1308](https://orcid.org/0009-0008-8035-1308) |
| Security email | `scliran9@gmail.com`                                     |

## Supported Versions

Security fixes are applied only to the current `main` branch and the most
recent release tag.

| Version       | Supported          |
|---------------|--------------------|
| `main` (HEAD) | yes                |
| Latest tag    | yes                |
| Older tags    | no                 |

## Threat Model — In Scope

1. **Build-system injection.** Payloads in the LaTeX source, `Makefile`, or
   `scripts/validate_html.py` that execute during local build (`make paper`,
   `make validate`), including `--shell-escape` abuse.
2. **CI/CD compromise.** Vulnerabilities in `.github/workflows/ci.yml`:
   unpinned third-party actions, token leakage, over-scoped `permissions:`.
3. **HTML asset exploitation.** XSS, clickjacking, or credential-harvest
   vectors in `docs/web/*.html`.
4. **Dependency CVEs.** Known issues in pinned GitHub Actions or in the
   TeX Live image consumed by CI.
5. **Repository metadata.** Secrets, tokens, or private keys accidentally
   committed.

## Threat Model — Out of Scope

- Scientific correctness of the physical model — open a regular issue using
  the `feature_request` template.
- Stylistic disagreements with the manuscript.
- Upstream TeX Live vulnerabilities — report directly to upstream.

## Reporting Procedure

**Do not open a public Issue, Pull Request, or Discussion for a security
report.** Public disclosure prior to fix availability creates risk for
downstream consumers.

Preferred channels, in order:

1. **GitHub Private Vulnerability Reporting** — *Security → Report a
   vulnerability* on this repository. Produces a private advisory visible
   only to the maintainer.
2. **Encrypted email** — `scliran9@gmail.com`. Subject line:
   `[OADF SECURITY] <short title>`. PGP key available on request.

### Required Contents

- Description of the issue and the threat-model item it falls under.
- Affected files and line ranges, or affected workflow step.
- Minimum reproducible example or exploit scenario.
- Commit SHA or tag where the issue was observed.
- Suggested remediation, if any.
- Whether attribution is desired in the resulting advisory.

### Response Targets

| Stage                                  | Target SLA       |
|----------------------------------------|------------------|
| Initial acknowledgement                | ≤ 72 hours       |
| Triage decision (accepted / rejected)  | ≤ 7 days         |
| Fix merged for high-severity finding   | ≤ 30 days        |
| Public advisory (after fix)            | coordinated      |

Default coordinated-disclosure window: **90 days**. The window is
accelerated upon evidence of active exploitation and extended when fix
delivery depends on an upstream patch (coordinated with the reporter).

## Hardening Currently in Place

- `pdflatex` / `latexmk` invoked **without** `--shell-escape` in both
  `Makefile` and CI.
- GitHub Actions are pinned to immutable commit SHAs where available, or to
  explicit release tags when the upstream action release is the compatibility
  boundary.
- CI `permissions:` reduced to `contents: read`.
- Python validator is stdlib-only — no `pip install` step.
- `.gitignore` excludes common secret-bearing files (`.env`, `*.pem`,
  `*.key`, `*.p12`, `*.pfx`).
