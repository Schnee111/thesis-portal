---
title: "UniDebugger: Hierarchical Multi-Agent Framework for Unified Software Debugging"
paper_id: GS10
bid: GS10
authors: "Cheryl Lee and others (CUHK & UIUC), 2025"
year: 2025
venue: "EMNLP 2025 Main"
doi: "10.18653/v1/2025.emnlp-main.921"
qa: "-"
role: "QGS (penguji recall P1+P2)"
extraction: "metadata-calibration"
tags:
  - qgs
  - peer-reviewed
---

# [GS10] UniDebugger: Hierarchical Multi-Agent Framework for Unified Software Debugging

**Kunci Stabil:** `GS10` | **Sitasi BibTeX:** [@lee2025unidebugger]

## Ringkasan Metadata

- **Penulis & Tahun:** Cheryl Lee and others (CUHK & UIUC), 2025
- **Venue & Tier:** EMNLP 2025 Main
- **DOI / URL:** [10.18653/v1/2025.emnlp-main.921](https://doi.org/10.18653/v1/2025.emnlp-main.921)
- **Skor Kualitas (QA Score):** - (QA korpus baru OPEN, belum dinilai)
- **Peran Studi:** QGS (penguji recall P1+P2)
- **Tingkat Ekstraksi:** `metadata-calibration`
- **Cakupan (Scope):** APR multi-berkas Defects4J v1.2 & v2.0 (bukan open-ended issue resolving).

---

## 1. Masalah Utama (Core Problem)

Unified software debugging multi-berkas.

## 2. Arsitektur yang Diajukan (Architecture)

Hierarki adaptif 3 level (L1 simple, L2 single-file, L3 cross-file MAS).

## 3. Mekanisme Koordinasi & Kontrol (Coordination)

Eskalasi penugasan L1-L2-L3 sesuai kesulitan bug; 100% otonom tanpa gate manusia.

## 4. Foundation Model & Infrastruktur (FM)

LLM umum era 2025.

## 5. Tolok Ukur & Dataset (Benchmark)

Defects4J (197 correct / 286 plausible).

## 6. Artefak & Kode Sumber (Artifact)

Cheryl-Lee/UniDebugger.

## 7. Metrik Primer Eksak (Primary exact)

197 correct / 286 plausible = +25.48% vs ChatRepair + 42 unik (Figure 5 hal 7).

## 8. Metrik Sekunder (Secondary)

-

## 9. Pola Kegagalan (Failure Modes)

Patch plausible-but-incorrect lolos tanpa verifikasi manusia.

## 10. Ancaman Validitas (Threats)

Sitasi 2 (prosiding baru).

## 11. Jejak Bukti & Provenansi (Provenance)

> **Bukti Verifikasi:** EVIDENCED-FACT (GS_quasi_gold.md GS10; Scopus-769 HIT DOI eksak; arXiv 2404.17153v3 HIT).
