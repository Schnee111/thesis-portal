---
title: "SGAgent: Suggestion-Guided LLM-Based Multi-Agent Framework for Repository-Level Software Repair"
paper_id: GS06
bid: GS06
authors: "Zhang and others (NJU), 2026"
year: 2026
venue: "ACM TOSEM (Q1) 2026"
doi: "10.1145/3818617"
qa: "-"
role: "QGS (penguji recall P1+P2)"
extraction: "metadata-calibration"
tags:
  - qgs
  - peer-reviewed
---

# [GS06] SGAgent: Suggestion-Guided LLM-Based Multi-Agent Framework for Repository-Level Software Repair

**Kunci Stabil:** `GS06` | **Sitasi BibTeX:** [@zhang2026sgagent]

## Ringkasan Metadata

- **Penulis & Tahun:** Zhang and others (NJU), 2026
- **Venue & Tier:** ACM TOSEM (Q1) 2026
- **DOI / URL:** [10.1145/3818617](https://doi.org/10.1145/3818617)
- **Skor Kualitas (QA Score):** - (QA korpus baru OPEN, belum dinilai)
- **Peran Studi:** QGS (penguji recall P1+P2)
- **Tingkat Ekstraksi:** `metadata-calibration`
- **Cakupan (Scope):** SWE-bench Lite (300 instances) & VUL4J.

---

## 1. Masalah Utama (Core Problem)

Repository-level software repair.

## 2. Arsitektur yang Diajukan (Architecture)

Localize-suggest-fix berfase (Localizer, Suggester, Fixer) + RepoGraph KG.

## 3. Mekanisme Koordinasi & Kontrol (Coordination)

Koordinasi sekuensial suggestion-guided berbasis graf pengetahuan; otonom penuh tanpa hierarki komando dan tanpa approval gate.

## 4. Foundation Model & Infrastruktur (FM)

Claude-3.5 / Claude-4 (evaluasi).

## 5. Tolok Ukur & Dataset (Benchmark)

SWE-bench Lite + VUL4J.

## 6. Artefak & Kode Sumber (Artifact)

NJU-Seq/SGAgent.

## 7. Metrik Primer Eksak (Primary exact)

Lite 51.3% (Claude-3.5) s.d. 60.7% (Claude-4) + VUL4J 48.0% (abstrak resmi CrossRef; PDF paywalled ACM, BELUM jangkar halaman).

## 8. Metrik Sekunder (Secondary)

-

## 9. Pola Kegagalan (Failure Modes)

Gagal bila saran awal menyesatkan fixer tanpa verifikasi eksternal.

## 10. Ancaman Validitas (Threats)

0 sitasi (umur 3,5 bln); PDF paywalled ACM.

## 11. Jejak Bukti & Provenansi (Provenance)

> **Bukti Verifikasi:** EVIDENCED-FACT (GS_quasi_gold.md GS06; CrossRef resolve; arXiv 2602.23647v2 HIT; Scopus MISS = lag indeks TOSEM 2026).
