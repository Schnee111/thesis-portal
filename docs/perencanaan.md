# Perencanaan (Protokol SLR)

Verbatim `00_meta/protocol_slr.md`.

## 1. PICOC v1 (LOCKED 2026-09-09)

* **P (Population):**
  > autonomous multi-agent systems for repository-level software engineering tasks (code generation, bug fixing, automated program repair, multi-file maintenance, issue resolving, fault localization, code refactoring)
* **I (Intervention, SATU mekanisme):**
  > selective human-in-the-loop approval gate in hierarchical orchestration. Closed-loop feedback/telemetry = KANDIDAT (BELUM lock) sampai SLR membuktikan — tidak digabung diam-diam ke I.
* **C (Comparison — dibaca 3 lapis, amendment 00_meta/amendment_C3lapis_20260912.md RATIFIED 2026-09-12 ACC Schnee):**
  > L1 lower-bound single-agent/flat/manual (GS03, GS04); L2 otonom-penuh se-layer tanpa gate (GS05, GS06, GS07, GS10); L3 kriteria-selektif lain se-layer, diisi dari screening M3 (GS09, GS11 + paper selective-gate lolos IC/EC dari korpus baru). Uji utama Bab 3 = ablasi kriteria seleksi (kapan eskalasi) pada metrik sama, bukan arsitektur vs arsitektur.
* **O (Outcomes):**
  > (1) functional: task completion, resolved rate e.g. SWE-bench; (2) efficiency: token, cost per task, latency; (3) reliability: intervention rate, loop stability, drift/cascading/infinite-loop mitigation
* **C (Context):**
  > isolated containerized sandboxes, long-horizon multi-step horizons, multi-repo codebases (kondisi uji Bab 3 + kolom Scope/DEF; istilah privat tidak searchable dan dilarang masuk query)

Kueri DB hanya dari P AND I; C/O/Context jadi IC/EC + DEF; perubahan query wajib amendment baru.

## 2. Research Questions

* **RQ1 SOTA:** pendekatan arsitektur + koordinasi apa dominan kini?
* **RQ2 Mekanisme (netral):** mekanisme koordinasi, supervisi, dan umpan balik apa yang dipakai, dan bagaimana efektivitas serta limitasinya dievaluasi?
* **RQ3 Metrik:** benchmark + angka empiris apa dilaporkan?
* **RQ4 Gap (netral):** pola limitasi dan trade-off apa yang konsisten belum terselesaikan di literatur primer?

## 3. Search string

Query beku = Generic Boolean v2.2 (P1-12 + P2-11 + I-29). SSOT: `02_slr/queries/query.md`; Boolean penuh: Lampiran A.

## 4. Kriteria inklusi dan eksklusi

Satu-satunya IC/EC formal (verbatim `00_meta/protocol_slr.md` §4).

* **IC1 (Population):** Sistem berbasis multi-agent / LLM agentic architecture untuk tugas rekayasa perangkat lunak (SE).
* **IC2 (Intervention):** Mengkaji arsitektur koordinasi, komunikasi, orkestrasi hirarkis, feedback loop, atau selective approval gate.
* **IC3 (Empirical Evidence):** Menyajikan implementasi konkret atau evaluasi empiris/kuantitatif pada benchmark atau repositori.
* **IC4 (Publication Window):** Terbit antara tahun 2020 hingga 2026 (SOTA Agentic AI).
* **IC5 (Study Type & Language):** Studi penelitian primer (primary study) berbahasa Inggris atau Indonesia.
* **EC1 (No Full-Text):** Tidak tersedia teks lengkap setelah enrichment DOI (diputus di L2 per Amendment L1 No-Abstract).
* **EC2 (Secondary Study):** Studi sekunder (Survei, SLR, Systematic Mapping) — dialokasikan sebagai referensi latar belakang, bukan ekstraksi matriks DEF.
* **EC3 (Single-Agent / Architecture Mismatch):** Model tunggal tanpa koordinasi peran multi-agen / bukan sistem multi-agent.
* **EC4 (Duplicate):** Duplikat lintas basis data (telah dieliminasi pada tahap deduplikasi PRISMA).
* **EC5 (Non-SE Domain):** Penerapan di luar rekayasa perangkat lunak (seperti tenaga listrik, HVAC, robotika fisik, navigasi satelit, kedokteran, game theory MARL umum).
* **EC6 (Short / Non-Academic):** Artikel non-penelitian ringkas (<4 halaman, seperti tutorial, poster, keynote summary, editorial).
* **EC7 (Language Mismatch):** Naskah lengkap dalam bahasa selain Inggris atau Indonesia.
* **EC8 (Year Out of Range):** Terbit di luar rentang 2020–2026 (termasuk anomali preprint pra-2020).

## 5. Sumber pencarian

10 sumber; rincian hit/export: [Progres](progres.md). Alur: Paper, Ekstraksi, Matriks DEF, Sintesis.

## 6. Penilaian kualitas

QA 9-Item Dyba-Dingsoyr, skor 0/0.5/1.0 (rincian: Lampiran B):

* High ≥7.0
* Moderate 4.5–6.5
* Exclude <4.5

### 6b. Audit 10-pass

Audit memakai 10 pass komputasional per butir DEF/QA sebagai uji konsistensi stokastik, bukan penilai independen; putusan akhir selalu manusia. Tata kelola dan log: [Jejak Audit](audit.md).

## 7. Kalibrasi query (QGS-6)

Gate 6/6 (union Scopus + arXiv) LOLOS; rincian: [Progres](progres.md).

## 8. DEF

20 kolom per studi primer (skema dan viewer: [Matriks](matrix/index.md)); tiap candidate-gap wajib diuji lawan ≥1 studi otonom.

## Lampiran A. Boolean penuh v2.2 (P AND I)

```text
("multi-agent" OR "multiagent" OR "autonomous agent*" OR "agentic workflow" OR "agentic AI" OR "compound AI system" OR "LLM agent*" OR "LLM-based agent*" OR "communicative agent*" OR "collaborative agent*" OR "software-developing agent*" OR "coding agent*") AND ("software engineering" OR "software development" OR "code generation" OR "program repair" OR "bug fix*" OR "software maintenance" OR "SWE-bench" OR "issue resolving" OR "fault localization" OR "code refactoring" OR "repository-level") AND ("hierarchical" OR "orchestration" OR "coordination" OR "collaborat*" OR "cooperat*" OR "role-play*" OR "role-based" OR "planning" OR "interactive" OR "test-driven" OR "user study" OR "user feedback" OR "intent clarification" OR "interface" OR "agent-computer" OR "human-in-the-loop" OR "HITL" OR "approval gate*" OR "selective intervention" OR "supervisor" OR "closed-loop" OR "closed loop" OR "feedback loop" OR "feedback" OR "reflect*" OR "self-repair" OR "delegation" OR "consensus" OR "telemetry")
```

Varian per-DB (Scopus, arXiv, IEEE, OpenAlex, CrossRef, SpringerLink, ScienceDirect, WoS, ACM, Scholar): SSOT `02_slr/queries/query.md`.

## Lampiran B. Instrumen QA rinci

Skor 0 / 0.5 / 1.0 per item (ACC Schnee 2026-09-12):

1. **Q1:** Tujuan penelitian jelas dan terukur.
2. **Q2:** Arsitektur dijelaskan sampai bisa direplikasi.
3. **Q3:** Baseline dan dataset pembanding transparan.
4. **Q4:** Kinerja diukur dengan metrik kuantitatif yang terdefinisi.
5. **Q5:** Ada analisis komparatif terhadap metode terdahulu.
6. **Q6:** Kesimpulan didukung bukti empiris.
7. **Q7:** Limitasi diungkap jujur.
8. **Q8:** Ada evaluasi threats to validity (internal dan eksternal).
9. **Q9:** Artefak kode/repositori tersedia dan bisa direproduksi.

Q10 novelty DIHAPUS dari instrumen QA dan dialihkan ke kolom DEF `Novel_Mechanism` serta matriks gap (QA = rigor/bias, novelty = kontribusi; gabung keduanya = construct contamination + cheap score inflation).

Ambang grid-0.5: High ≥7.0 (77.8%), Moderate 4.5–6.5, Exclude <4.5. Caps: abstract-only ≤6.0, preprint tanpa repo publik ≤7.5. Anchor ≥8.0 wajib trace Table/Sec/Fig + URL repo aktif. Footnote teoretis: batas High = ≥75% (6.75) yang pada grid 0.5 terwujud sebagai skor aktual minimum 7.0, kecuali rata-rata inter-rater. Inter-rater manusia: Cohen kappa = (Po-Pe)/(1-Pe), target >0.75.
