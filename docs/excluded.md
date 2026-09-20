# Studi Tereksklusi Tahap L1 (2.087 Studi)

Tahap penyaringan literatur (*screening*) L1 (Judul & Abstrak) telah diselesaikan secara penuh pada 2026-09-13 terhadap **4.643 naskah unik master**. Dari total tersebut, sebanyak **2.087 naskah (44,9%)** dieliminasi sesuai kriteria eksklusi (EC1–EC8) pada Protokol SLR §4 dan Amendment L1 No-Abstract.

Sebanyak **2.556 naskah (55,1%)** berhasil lolos (`PASS`) ke tahap penyaringan teks lengkap L2 (*full-text eligibility*).

---

## 1. Distribusi Kriteria Eksklusi L1 (PRISMA 2020)

Rincian alasan pengeluaran naskah pada penyaringan L1:

- **EC5-NonSE (1.285 studi, 61,6% dari eksklusi):** Fokus penelitian di luar ranah rekayasa perangkat lunak (*software engineering*), mencakup aplikasi seperti HVAC gedung, sistem tenaga listrik & smart grid, navigasi UAV/drone fisik, rekayasa sipil/geoteknik, kedokteran & radiologi klinis, kimia/penemuan obat, serta pertanian pintar.
- **EC3-SingleAgent (504 studi, 24,1% dari eksklusi):** Arsitektur agen tunggal, *single LLM prompt*, atau algoritma machine learning non-agentic tanpa koordinasi peran multi-agen kolaboratif maupun orkestrasi hierarkis.
- **EC2-SecondaryStudy (236 studi, 11,3% dari eksklusi):** Studi sekunder, survei literatur, *Systematic Literature Review* (SLR), dan *Systematic Mapping Studies*. Naskah-naskah ini dialihkan sebagai referensi pendukung pada Bab 2 Tinjauan Pustaka.
- **EC5-HardwareDesign (42 studi, 2,0% dari eksklusi):** Domain perancangan perangkat keras (RTL, Verilog, VHDL, FPGA/VLSI design, perbaikan bug logika sirkuit fisik).
- **EC6-ShortNonAcademic (8 studi, 0,4% dari eksklusi):** Naskah non-akademik, tulisan editorial ringkas (<4 halaman), atau naskah yang ditarik kembali (*retracted*).
- **EC8-OutOfYear (5 studi, 0,2% dari eksklusi):** Naskah preprint terbit sebelum tahun 2020 (P1472–P1476 dari arXiv).
- **EC7-LanguageMismatch (5 studi, 0,2% dari eksklusi):** Naskah lengkap dalam bahasa non-Inggris dan non-Indonesia (naskah berbahasa Mandarin/Slavia tanpa metadata bahasa Inggris).
- **EC5-GameTheory (2 studi, 0,1% dari eksklusi):** Penerapan *Multi-Agent Reinforcement Learning* (MARL) murni pada game generik (StarCraft/poker) tanpa relasi ke artefak rekayasa software.

---

## 2. Artefak dan Log Lengkap

Log lengkap keputusan per naskah beserta alasan semantik tercatat pada:
- `02_slr/screening/01_master_for_screening.csv` (15 kolom lengkap master).
- `02_slr/screening/03_screening_L1_report.md` (laporan resmi PRISMA L1).

---

## 3. Catatan Historis Scoping Batch-1

Sebagai catatan historis, sebanyak 10 studi tereksklusi dari studi penjajakan (*scoping search*) Batch-1 tersimpan pada berkas arsip `02_slr/_archive_pilot_20260911/extraction/DEF_excluded_batch1.csv` dan dialokasikan untuk satu paragraf pengantar pada Bab 3, bukan bagian dari diagram alir PRISMA korpus utama.

---

## 4. Residuum retrieval dan Tier-3/4

Penanganan residu retrieval dan prioritas Tier-3/4 pindah ke [Progres](progres.md#4-tier-3-flagship-dan-tier-4-interim-pindahan-dari-excluded-4).

