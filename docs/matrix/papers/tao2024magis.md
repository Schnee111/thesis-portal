---
title: "MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue Resolution"
paper_id: GS05
bid: GS05
authors: "Wei Tao and others, 2024"
year: 2024
venue: "NeurIPS 2024 (Vol 37)"
doi: "10.52202/079017-1647"
qa: "-"
role: "QGS (penguji recall P1+P2)"
extraction: "metadata-calibration"
tags:
  - qgs
  - peer-reviewed
---

# [GS05] MAGIS: LLM-Based Multi-Agent Framework for GitHub Issue Resolution

**Kunci Stabil:** `GS05` | **Sitasi BibTeX:** [@tao2024magis]

## Ringkasan Metadata

- **Penulis & Tahun:** Wei Tao and others, 2024
- **Venue & Tier:** NeurIPS 2024 (Vol 37)
- **DOI / URL:** [10.52202/079017-1647](https://doi.org/10.52202/079017-1647)
- **Skor Kualitas (QA Score):** - (QA korpus baru OPEN, belum dinilai)
- **Peran Studi:** QGS (penguji recall P1+P2)
- **Tingkat Ekstraksi:** `metadata-calibration`
- **Cakupan (Scope):** Repository-level GitHub issue resolution (SWE-bench 500 instances).

---

## 1. Masalah Utama (Core Problem)

Resolusi GitHub issue repo-level secara otonom.

## 2. Arsitektur yang Diajukan (Architecture)

Hierarki 4 agen: Manager, Custodian, Developer, QA (supervisor-worker).

## 3. Mekanisme Koordinasi & Kontrol (Coordination)

Manager membagi tugas dan mengarahkan agen lain; Custodian membatasi search space berkas; 100% otonom tanpa HITL gate.

## 4. Foundation Model & Infrastruktur (FM)

GPT-4 era.

## 5. Tolok Ukur & Dataset (Benchmark)

SWE-bench (500 issue repo-level).

## 6. Artefak & Kode Sumber (Artifact)

weitao92/MAGIS.

## 7. Metrik Primer Eksak (Primary exact)

Resolved rate 13.94% = 8x GPT-4 1.74% (PDF hal 1+7/Table 2 hal 7).

## 8. Metrik Sekunder (Secondary)

-

## 9. Pola Kegagalan (Failure Modes)

86% isu gagal terselesaikan tanpa batas eskalasi terukur.

## 10. Ancaman Validitas (Threats)

UNDOCUMENTED (QA korpus baru OPEN).

## 11. Jejak Bukti & Provenansi (Provenance)

> **Bukti Verifikasi:** EVIDENCED-FACT (GS_quasi_gold.md GS05; Scopus-769 HIT judul eksak; arXiv 2403.17927v2 HIT).
