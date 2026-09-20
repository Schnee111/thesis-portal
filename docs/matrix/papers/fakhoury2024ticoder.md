---
title: "TiCoder: Test-Driven Interactive Code Generation"
paper_id: GS09
bid: GS09
authors: "Sarah Fakhoury and others, 2024"
year: 2024
venue: "IEEE TSE 2024 Vol 50 Issue 9"
doi: "10.1109/tse.2024.3428972"
qa: "-"
role: "pembanding-C (selective-gate Bab 2/3)"
extraction: "metadata-calibration"
tags:
  - pembanding-c
  - peer-reviewed
---

# [GS09] TiCoder: Test-Driven Interactive Code Generation

**Kunci Stabil:** `GS09` | **Sitasi BibTeX:** [@fakhoury2024ticoder]

## Ringkasan Metadata

- **Penulis & Tahun:** Sarah Fakhoury and others, 2024
- **Venue & Tier:** IEEE TSE 2024 Vol 50 Issue 9
- **DOI / URL:** [10.1109/tse.2024.3428972](https://doi.org/10.1109/tse.2024.3428972)
- **Skor Kualitas (QA Score):** - (QA korpus baru OPEN, belum dinilai)
- **Peran Studi:** pembanding-C (selective-gate Bab 2/3)
- **Tingkat Ekstraksi:** `metadata-calibration`
- **Cakupan (Scope):** Codegen test-driven + user study (gagal P1 multi-agent by-design).

---

## 1. Masalah Utama (Core Problem)

Selective interaction gate (test-driven) pada code generation single-interactive.

## 2. Arsitektur yang Diajukan (Architecture)

Single-interactive agent via LLM + test-driven gate (m=1..5).

## 3. Mekanisme Koordinasi & Kontrol (Coordination)

Gerbang interaksi selektif test-driven; bukan orkestrasi multi-agen.

## 4. Foundation Model & Infrastruktur (FM)

LLM umum era 2024.

## 5. Tolok Ukur & Dataset (Benchmark)

Codegen test-driven + user study 15 devs.

## 6. Artefak & Kode Sumber (Artifact)

- (UNDOCUMENTED).

## 7. Metrik Primer Eksak (Primary exact)

+45.97% pass@1 + user study 15 devs (TABLE IV preprint v2; BELUM jangkar halaman published).

## 8. Metrik Sekunder (Secondary)

-

## 9. Pola Kegagalan (Failure Modes)

-

## 10. Ancaman Validitas (Threats)

Single-interactive (P1 via LLM, bukan multi-agent strict).

## 11. Jejak Bukti & Provenansi (Provenance)

> **Bukti Verifikasi:** EVIDENCED-FACT (GS_quasi_gold.md GS09; pembanding-C selective-gate Bab 2/3).
