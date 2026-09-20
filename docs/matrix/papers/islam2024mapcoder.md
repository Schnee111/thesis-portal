---
title: "MapCoder: Multi-Agent Code Generation for Competitive Problem Solving"
paper_id: GS07
bid: GS07
authors: "Md Ashraful Islam and others (BUET & Rochester), 2024"
year: 2024
venue: "ACL 2024 Long"
doi: "10.18653/v1/2024.acl-long.269"
qa: "-"
role: "QGS (penguji recall P1+P2)"
extraction: "metadata-calibration"
tags:
  - qgs
  - peer-reviewed
---

# [GS07] MapCoder: Multi-Agent Code Generation for Competitive Problem Solving

**Kunci Stabil:** `GS07` | **Sitasi BibTeX:** [@islam2024mapcoder]

## Ringkasan Metadata

- **Penulis & Tahun:** Md Ashraful Islam and others (BUET & Rochester), 2024
- **Venue & Tier:** ACL 2024 Long
- **DOI / URL:** [10.18653/v1/2024.acl-long.269](https://doi.org/10.18653/v1/2024.acl-long.269)
- **Skor Kualitas (QA Score):** - (QA korpus baru OPEN, belum dinilai)
- **Peran Studi:** QGS (penguji recall P1+P2)
- **Tingkat Ekstraksi:** `metadata-calibration`
- **Cakupan (Scope):** Competitive problem solving (HumanEval, MBPP, APPS, CodeContests), function-level, bukan repo.

---

## 1. Masalah Utama (Core Problem)

Generasi kode problem-solving kompetitif via multi-agen.

## 2. Arsitektur yang Diajukan (Architecture)

4 agen (Retrieval, Planning, Coding, Debugging); siklus plan-code-debug retrieval-augmented.

## 3. Mekanisme Koordinasi & Kontrol (Coordination)

Siklik retrieval-planning; otonom penuh tanpa hierarki formal dan tanpa gate.

## 4. Foundation Model & Infrastruktur (FM)

LLM umum era 2024.

## 5. Tolok Ukur & Dataset (Benchmark)

HumanEval, MBPP, APPS, CodeContests.

## 6. Artefak & Kode Sumber (Artifact)

ideis/MapCoder.

## 7. Metrik Primer Eksak (Primary exact)

UNDOCUMENTED di SSOT jalur baru (QA/DEF korpus baru OPEN).

## 8. Metrik Sekunder (Secondary)

-

## 9. Pola Kegagalan (Failure Modes)

Generalisasi ke repo skala besar belum terbukti.

## 10. Ancaman Validitas (Threats)

UNDOCUMENTED (QA korpus baru OPEN).

## 11. Jejak Bukti & Provenansi (Provenance)

> **Bukti Verifikasi:** EVIDENCED-FACT (GS_quasi_gold.md GS07; Scopus-769 HIT DOI eksak; arXiv 2405.11403v1 HIT).
