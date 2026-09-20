# VERIFICATION.md — Laporan Verifikasi Gate Thesis Review Site

**Tanggal Eksekusi:** 2026-09-10 21:45 UTC (re-run pasca polish site: dark-mode toggle, perbaikan tabel, hapus emoji/em-dash, rapikan bahasa; hasil gate tak berubah, 8/8 PASS)  
**Skrip Gate:** `07_review-site/scripts/gates/gate-site.sh`  
**Hasil Akhir:** **PASS (Exit Code 0 — 8/8 checks lolos)**  
**Lingkungan:** Ubuntu Linux 6.8.0-124-generic, Python 3.11.15, MkDocs 1.6.1 (`mkdocs-material==9.7.7`, `mkdocs-bibtex==4.4.0`, `mkdocs-roamlinks-plugin==0.3.2`).

---

## 1. Ringkasan Eksekusi Gate

| No | Kriteria Evaluasi | Target | Hasil Aktual | Status | Exit Code |
|---|---|---|---|---|---|
| 1 | Generator rerun-identical | Hash 47 md, 1 json, 1 bib, 1 snippet identik | 50 berkas terverifikasi byte-identical | **PASS** | 0 |
| 2 | `matrix_data.json` valid | JSON array valid, tepat 47 entri | 47 entri valid (144.9 KB) | **PASS** | 0 |
| 3 | Berkas papers Markdown | Direktori `docs/matrix/papers/` tepat 47 `.md` | 47 berkas `.md` | **PASS** | 0 |
| 4 | Kunci BibTeX | `docs/references.bib` tepat 47 keys unik | 47 bibtex keys unik | **PASS** | 0 |
| 5 | Build MkDocs Strict | `mkdocs build --strict` tanpa peringatan fatal/error | Exit code 0 (build time: ~0.82s) | **PASS** | 0 |
| 6 | Rekonsiliasi SID & Excluded | 47 SID S01-S47 + 10 Excluded BIDs | 47 SIDs klop CSV-JSON; 10 Excluded BIDs klop | **PASS** | 0 |
| 7 | Anchor Provenance QA >= 9.0 | Semua QA >= 9.0 memiliki anchor Table/Sec/Fig | 12/12 paper QA >= 9.0 memiliki anchor | **PASS** | 0 |
| 8 | Scan Secrets & Credentials | 0 file `.env`, 0 pattern secret/API key | 0 temuan `.env` / credential pattern | **PASS** | 0 |

---

## 2. Rincian Hasil Aktual per Pemeriksaan

### Check 1: Generator Rerun-Identical
- **Perintah:** `python3 scripts/generate_matrix_pages.py --check`
- **Output:**
  ```text
  [CHECK] Memulai verifikasi deterministik TASK-1.2...
  [SUCCESS] Verifikasi deterministik sukses 100%! Semua hash identik (47 md, 1 json, 1 bib, 1 snippet).
  ```
- **Exit code:** `0`

### Check 2: Validasi `matrix_data.json`
- **File:** `07_review-site/docs/assets/matrix_data.json`
- **Ukuran:** 148,349 bytes (~144.9 KB)
- **Struktur:** Array JSON valid tingkat atas.
- **Jumlah elemen:** 47 objek (S01 hingga S47).
- **Exit code:** `0`

### Check 3: Jumlah Berkas Paper Markdown
- **Path:** `07_review-site/docs/matrix/papers/`
- **Pola file:** `*.md`
- **Total file terhitung:** 47 file
- **Sanitasi nama berkas:** Menggunakan format sanitized lowercase kebab-case `[a-z0-9-]` (sesuai CiteKey).
- **Exit code:** `0`

### Check 4: Kunci BibTeX `references.bib`
- **File:** `07_review-site/docs/references.bib`
- **Ukuran:** 16,027 bytes (~15.7 KB)
- **Total tipe entri BibTeX (misc / inproceedings):** 47
- **Total keys unik:** 47
- **Duplikasi:** 0
- **Exit code:** `0`

### Check 5: Build MkDocs Strict
- **Perintah:** `/tmp/venv_mkdocs/bin/mkdocs build --strict -f 07_review-site/mkdocs.yml`
- **Hasil build:**
  - Site directory: `07_review-site/site/`
  - Waktu build: ~0.82 detik
  - Warnings fatal: 0
  - Broken links / missing syntax: 0
- **Exit code:** `0`

### Check 6: Klop SID 47 + Excluded 10 BIDs
- **Sumber Data (SSOT):**
  - Included: `/home/ubuntu/thesis/02_slr/extraction/DEF_matrix_batch1.csv` (47 baris)
  - Excluded: `/home/ubuntu/thesis/02_slr/extraction/DEF_excluded_batch1.csv` (10 baris)
  - Generated: `07_review-site/docs/assets/matrix_data.json` (47 baris)
- **Validasi SID:**
  - Rentang terverifikasi: `S01` s.d. `S47` (47 unik berurutan, klop 100% antara CSV dan JSON).
- **Validasi BIDs Excluded (10/10 terverifikasi):**
  - `B1-046` (EC1)
  - `B1-047` (EC1)
  - `B1-051` (EC1)
  - `B1-056` (EC1)
  - `B1-066` (EC1)
  - `B1-074` (EC1)
  - `B1-076` (EC1)
  - `B1-081` (EC1)
  - `B1-083` (EC1)
  - `B1-140` (EC2)
- **Exit code:** `0`

### Check 7: Anchor Provenance QA >= 9.0
- **Kriteria:** Setiap entri dengan `QA_Score >= 9.0` wajib mencantumkan lokasi data konkret (`Table`, `Tab`, `Sec`, `Section`, `Fig`, `Figure`) pada `Provenance_Tag`.
- **Total paper dengan QA >= 9.0:** 12 paper.
- **Rincian Anchor Faktual:**
  1. `S01` (`B1-001`, QA 9.5): `Table 4` (`papers/B1-001.txt Table 4: 91.2%/8.4%/F1 0.913, CI [0.872,0.945]`)
  2. `S04` (`B1-052`, QA 9.5): `Sec 4.1-4.2` (`papers/B1-052.txt Sec 4.1-4.2: HumanEval 85.9%, MBPP 87.7%`)
  3. `S11` (`B1-070`, QA 9.5): `Table 1-2` (`pdf_cache/B1-070.txt Table 1-2`)
  4. `S16` (`B1-093`, QA 9.0): `Tab5`, `Tab6`, `Tab7`, `Tab8`, `Tab10`, `Sec6.7.1` (`pdf_cache/B1-093.txt`)
  5. `S18` (`B1-095`, QA 9.0): `Tab3`, `Tab4` (`pdf_cache/B1-095.txt p6 Tab3, p7 Tab4`)
  6. `S31` (`B1-116`, QA 9.0): `Table 1`, `Sec4` (`txt/B1-116.txt Table 1 Sec4`)
  7. `S34` (`B1-120`, QA 9.0): `Table 1-2`, `Sec5` (`txt/B1-120.txt Table 1-2 Sec5`)
  8. `S39` (`B1-128`, QA 9.5): `Table 1`, `Sec4-5` (`txt/B1-128.txt Table 1 Sec4-5 CA/SR/P5-CA/CVaR0.1`)
  9. `S42` (`B1-134`, QA 9.5): `Sec3-4` (`txt/B1-134.txt Sec3-4: PlayEval 43 repos, Play (at) k`)
  10. `S44` (`B1-136`, QA 9.0): `Table 1-7`, `Sec3-5`, `Fig1-6` (`txt/B1-136.txt`)
  11. `S45` (`B1-139`, QA 9.0): `Fig1/3-5` (`txt/B1-139.txt Fig1/3-5 SWE-bench 59/80 + Terminal-Bench 42.5%`)
  12. `S47` (`B1-142`, QA 9.5): `Tables1-3/6`, `Sec4-5` (`txt/B1-142.txt pp6-10 Tables1-3/6 Sec4-5`)
- **Missing anchors:** 0
- **Exit code:** `0`

### Check 8: Pemeriksaan Secrets & Keamanan
- **Pemeriksaan File `.env*`:**
  - `find 07_review-site -name ".env*"` -> 0 file ditemukan.
- **Pemeriksaan Pola API Key / Private Key:**
  - Jenis pola dicek: OpenAI sk-key, GitHub token ghp, Private Key header, AWS AKIA key.
  - Target: Seluruh file di `07_review-site/` (kecuali file gate test itu sendiri).
  - Temuan: 0 matches.
- **Exit code:** `0`

---

## 3. Kesimpulan Verifikasi
Situs review skripsi (`07_review-site`) telah memenuhi seluruh kriteria penerimaan TASK-3.1. Build dokumentasi MkDocs bersifat deterministik, bebas dari kebocoran kredensial, memiliki integritas referensi dan data ekstraksi yang sepenuhnya konsisten terhadap CSV SSOT (47 Include + 10 Exclude).
