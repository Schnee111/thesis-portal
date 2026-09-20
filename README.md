# Thesis Review Portal and SLR Research Artifact

> Systematic Literature Review (SLR) Knowledge Platform and Evaluation Artifact for Undergraduate Thesis in Computer Science, Universitas Pendidikan Indonesia (UPI).

[![Documentation Build](https://github.com/Schnee111/thesis-portal/actions/workflows/ci.yml/badge.svg)](https://github.com/Schnee111/thesis-portal/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MkDocs: Material](https://img.shields.io/badge/Material_for_MkDocs-9.7.7-526CFE.svg)](https://squidfunk.github.io/mkdocs-material/)
[![Cloudflare: Pages](https://img.shields.io/badge/Cloudflare_Pages-Deployment-F38020.svg)](https://thesis.schnee.web.id)

---

## Overview

This repository hosts the interactive literature review portal and evaluation artifact for the undergraduate thesis by **Muhammad Daffa Maarif (Schnee)** at the Department of Computer Science Education, Universitas Pendidikan Indonesia (UPI).

The platform serves as an open-science reproducibility companion, documenting the complete Systematic Literature Review (SLR) methodology adhering to the PRISMA 2020 protocol, research questions (RQs), inclusion/exclusion criteria, quality assessment calibration, and synthesis matrices across autonomous AI coding agents and multi-agent software engineering workflows.

---

## Architecture and Data Flow

```text
[ SLR Corpus & Extraction Matrices ]
                |
                v
[ MkDocs Material (Python 3.11) ]
        |
        +---> PRISMA 2020 Protocol & Criteria
        +---> Interactive QGS Matrix Viewer
        +---> BibTeX Citations & DOI Crossrefs
        +---> Research Gap & Synthesis
                |
                v  (Static Build: site/)
[ Cloudflare Pages Global Edge ]
        |
        v  (Custom Domain CNAME)
[ https://thesis.schnee.web.id ]
```

---

## Platform Contents

1. **Protocol and Planning (`/perencanaan`):** Complete PICOC formulation, research questions, search strings across digital libraries (ACM, IEEE, Scopus), and rigorous IC/EC criteria.
2. **PRISMA Progress (`/progres`):** Identification, screening, eligibility, and inclusion flow tracking with auditable extraction statistics.
3. **Evidence Matrix (`/matrix`):** Deep synthesis tables across Quasi-Gold Standard (QGS) calibration papers and comparative baseline studies.
4. **Gap Analysis (`/gap`):** Synthesis of unresolved challenges in multi-agent orchestration, test-driven validation, and selective human-in-the-loop governance.
5. **Audit Trail (`/audit`):** Transparent record of screening decisions, cross-reviewer validations, and versioned amendments.

---

## Quickstart

### Prerequisites

- Python 3.11+
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/Schnee111/thesis-portal.git
cd thesis-portal

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run live development server with hot-reload
mkdocs serve
```

The portal will be accessible at `http://127.0.0.1:8000/`.

### Production Build Verification

```bash
# Verify strict compilation (zero warnings or broken internal links)
mkdocs build --strict
```

The compiled static assets will be emitted to `site/`.

---

## Deployment to Cloudflare Pages

This repository is configured for edge delivery via **Cloudflare Pages**:

- **Framework Preset:** None (Static Site)
- **Build Command:** `pip install -r requirements.txt && mkdocs build --strict`
- **Build Output Directory:** `site`
- **Canonical Domain:** `https://thesis.schnee.web.id`

---

## Citation and Attribution

If you reference this literature review protocol or extraction methodology in your academic work, please cite:

```bibtex
@misc{maarif2026thesisportal,
  author = {Ma'arif, Muhammad Daffa},
  title = {Systematic Literature Review on Autonomous Multi-Agent Software Engineering},
  year = {2026},
  publisher = {Universitas Pendidikan Indonesia},
  url = {https://thesis.schnee.web.id}
}
```

---

## License

This project is licensed under the MIT License. Copyright (c) 2026 Muhammad Daffa Maarif (Schnee111).
