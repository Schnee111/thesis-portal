# Matriks Literatur — 11 Paper (QGS-6 + Pembanding-C)

Penampil interaktif untuk 11 paper kalibrasi jalur utama:
6 QGS (penguji recall query) dan 5 pembanding-C (referensi Bab 2 / baseline RQ4).
SSOT: `02_slr/GS_quasi_gold.md`. Korpus baru (hasil screening) = OPEN, belum ada baris S-baru.

<div style="margin: 0.75rem 0 1.25rem 0; display: flex; gap: 0.5rem; flex-wrap: wrap;">
  <a href="../assets/matrix_viewer.html" target="_blank" class="md-button md-button--primary">Buka Fullscreen</a>
  <a href="../assets/matrix_data.json" download class="md-button">Unduh JSON</a>
</div>

<iframe
  src="../assets/matrix_viewer.html"
  loading="lazy"
  style="width: 100%; height: 78vh; min-height: 600px; border: 1px solid var(--md-default-fg-color--lightest, #334155); border-radius: 8px; display: block;"
  title="Penampil Matriks Literatur">
</iframe>

---

## Tabel ringkas QGS-6 (denominator recall)

| ID | Paper | Venue | Peran recall | Status v2.2 |
|:---|:---|:---|:---|:---|
| **GS02** | [ChatDev](papers/qian2024chatdev.md): Communicative Agents for Software Development | ACL 2024 Long | QGS eligible (P1+P2) | HIT Scopus (DOI eksak) |
| **GS05** | [MAGIS](papers/tao2024magis.md): LLM-Based Multi-Agent Framework for GitHub Issue Resolution | NeurIPS 2024 | QGS eligible (P1+P2) | HIT Scopus + arXiv (`2403.17927v2`) |
| **GS06** | [SGAgent](papers/zhang2026sgagent.md): Suggestion-Guided LLM-Based Multi-Agent Framework for Repository-Level Software Repair | ACM TOSEM 2026 (Q1) | QGS eligible (P1+P2) | HIT arXiv (`2602.23647v2`); MISS Scopus = lag indeks |
| **GS07** | [MapCoder](papers/islam2024mapcoder.md): Multi-Agent Code Generation for Competitive Problem Solving | ACL 2024 Long | QGS eligible (P1+P2) | HIT Scopus + arXiv (`2405.11403v1`) |
| **GS10** | [UniDebugger](papers/lee2025unidebugger.md): Hierarchical Multi-Agent Framework for Unified Software Debugging | EMNLP 2025 Main | QGS eligible (P1+P2) | HIT Scopus + arXiv (`2404.17153v3`) |
| **GS11** | [Kumar & Singh](papers/kumar2026balancing.md): Balancing autonomy and oversight through adaptive human interaction architectures | Discover AI (Springer) 2026 | QGS penutup lubang I-gate | HIT Scopus (DOI eksak); MISS arXiv = jurnal non-arXiv |

## Tabel pembanding-C (bukan denominator recall)

| ID | Paper | Venue | Peran |
|:---|:---|:---|:---|
| **GS01** | [CAMEL](papers/li2023camel.md) | NeurIPS 2023 | Fondasi role-play (Bab 2) |
| **GS03** | [SWE-agent](papers/yang2024sweagent.md) | NeurIPS 2024 | Baseline single-agent (RQ4) |
| **GS04** | [AutoCodeRover](papers/zhang2024autocoderover.md) | ISSTA 2024 | Baseline autonomous APR (RQ4) |
| **GS08** | [Reflexion](papers/shinn2023reflexion.md) | NeurIPS 2023 | Fondasi feedback-loop (Bab 2) |
| **GS09** | [TiCoder](papers/fakhoury2024ticoder.md) | IEEE TSE 2024 | Pembanding selective-gate single-interactive (Bab 2/3) |
