---
title: "ChatDev: Communicative Agents for Software Development"
paper_id: GS02
bid: GS02
authors: "Chen Qian and others, 2024"
year: 2024
venue: "ACL 2024 Long"
doi: "10.18653/v1/2024.acl-long.810"
qa: "-"
role: "QGS (penguji recall P1+P2)"
extraction: "metadata-calibration"
tags:
  - qgs
  - peer-reviewed
---

# [GS02] ChatDev: Communicative Agents for Software Development

**Kunci Stabil:** `GS02` | **Sitasi BibTeX:** [@qian2024chatdev]

## Ringkasan Metadata

- **Penulis & Tahun:** Chen Qian and others, 2024
- **Venue & Tier:** ACL 2024 Long
- **DOI / URL:** [10.18653/v1/2024.acl-long.810](https://doi.org/10.18653/v1/2024.acl-long.810)
- **Skor Kualitas (QA Score):** - (QA korpus baru OPEN, belum dinilai)
- **Peran Studi:** QGS (penguji recall P1+P2)
- **Tingkat Ekstraksi:** `metadata-calibration`
- **Cakupan (Scope):** SE development scope (greenfield multi-file, non-SWE-bench)

---

## 1. Masalah Utama (Core Problem)

Pengembangan perangkat lunak kolaboratif oleh agen komunikatif berbasis peran; cakupan greenfield multi-berkas skala kecil, bukan maintenance repo besar.

## 2. Arsitektur yang Diajukan (Architecture)

Waterfall role-play komunikatif (CEO, CTO, CPO, Programmer, Reviewer, Tester) via chat chain.

## 3. Mekanisme Koordinasi & Kontrol (Coordination)

Orkestrasi waterfall linier antar-peran; otonom antar-agen, tanpa supervisor dinamis dan tanpa approval gate selektif.

## 4. Foundation Model & Infrastruktur (FM)

LLM umum era 2024 (laporan facet-map subagent: durasi ~7 mnt, biaya $0.18-$0.30, code completeness di SRDD, BELUM jangkar PDF).

## 5. Tolok Ukur & Dataset (Benchmark)

SRDD (aplikasi/game creation skala kecil).

## 6. Artefak & Kode Sumber (Artifact)

OpenBMB/ChatDev.

## 7. Metrik Primer Eksak (Primary exact)

UNDOCUMENTED di SSOT jalur baru (QA/DEF korpus baru OPEN); landmark waterfall role-based.

## 8. Metrik Sekunder (Secondary)

Durasi/biaya generasi per rilis kecil (lihat naskah sumber).

## 9. Pola Kegagalan (Failure Modes)

Cascading error + halusinasi berantai tanpa gerbang pemutus.

## 10. Ancaman Validitas (Threats)

UNDOCUMENTED (QA korpus baru OPEN).

## 11. Jejak Bukti & Provenansi (Provenance)

> **Bukti Verifikasi:** EVIDENCED-FACT (GS_quasi_gold.md GS02; CrossRef DOI resolve; Scopus-769 HIT DOI eksak via micro-fix P2 v2.2).
