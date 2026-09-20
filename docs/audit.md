# Jejak Audit Data

Audit testing recall query v2.2 FROZEN dan hunting final 7 pangkalan data terhadap Quasi-Gold Standard (QGS-6).
Detail baseline tersimpan di `02_slr/raw_exports/*_BASELINE.md`, `02_slr/screening/DEDUPLICATION_REPORT.md`, dan `02_slr/screening/03_screening_L1_report.md`.

---

## 1. Ringkasan Audit Pangkalan Data & Seleksi

| Pangkalan data | Skor QGS-6 | Sebab MISS |
|---|---|---|
| Scopus | 5/6 | GS06 MISS: lag indeks Scopus untuk TOSEM 2026, bukan cacat query |
| arXiv | 4/6 | GS02 MISS: tanpa record arXiv judul-eksak; GS11 MISS: artikel jurnal non-arXiv |
| OpenAlex | 6/6 | Nihil (HIT penuh GS02, GS05, GS06, GS07, GS10, GS11) |
| CrossRef | 1/6 | MISS struktural tanpa abstrak; GS06 HIT by DOI; membawa 293 DOI baru di luar Scopus |
| IEEE Xplore | 0/6 | Seluruh QGS-6 terbit di luar IEEE; TiCoder pembanding-C tepat tersaring (single-agent) |
| SpringerLink | 1/6 | Hanya GS11 Kumar & Singh HIT (baris 1006, Discover AI) |
| ScienceDirect | 0/6 | Seluruh QGS-6 terbit di luar Elsevier |
| Union 7 pangkalan data | **6/6 (100%) LOLOS** | Sintaksis Boolean v2.2 menangkap seluruh acuan tanpa kehilangan sensitivitas |
* **Koreksi audit 1 (false hit ditolak):** hit "UA-ChatDev" (`2607.02186v1`) adalah paper lain, bukan GS02 ChatDev. GS02 tercatat MISS di arXiv.
* **Koreksi audit 2 (HIT diperbaiki):** record eksak MapCoder (`2405.11403v1`) ADA di arXiv-824 (bukan hanya varian MapCoder-Lite).
* **Identifikasi GS02 di Scopus:** via DOI eksak `10.18653/v1/2024.acl-long.810`, lolos berkat penambahan istilah faset "software development" di P2 v2.2.
* **Arsip audit pilot:** audit 47 studi Batch-1 tersimpan di `02_slr/_archive_pilot_20260911/` (dialokasikan untuk 1 paragraf latar belakang Bab 3, bukan SSOT utama).

---

## 2. Tata Kelola Audit Ekstraksi (10-Pass LLM-Assisted Audit)

Mengacu pada `00_meta/protocol_slr.md` §6b dan `00_meta/rules_ai_assisted.md` §3 (ACC Schnee 2026-09-12),
verifikasi mutu matriks ekstraksi (DEF) dan penilaian kualitas (QA) korpus baru diatur secara transparan dan akuntabel.

### Ketentuan Metodologis §6b

* **Definisi & Batasan Epistemik:**
    * Audit menggunakan 10 pass komputasional per butir ekstraksi DEF dan skor QA.
    * Seluruh pass berbagi bobot model (*shared model weights*) dan representasi laten serupa,
      sehingga **BUKAN penilai manusia independen** (*independent human peer reviewers*).
    * Fungsinya murni sebagai instrumen uji konsistensi stokastik (*consistency check*) dan penyaring anomali teks.
* **Empat Syarat Konteks Wajib:**
    * *Isolated context window:* tiap pass berjalan pada jendela konteks mandiri tanpa riwayat pass lain.
    * *First-pass blind:* evaluasi awal buta tanpa riwayat adjudikasi terdahulu maupun nilai awal matriks.
    * *Identical rubric & evidence anchor:* seluruh pass memakai instruksi identik serta wajib mencantumkan bukti kutipan halaman, seksi, atau tabel naskah primer.
    * *Human escalation on disagreement:* jika ditemukan perbedaan luaran (variansi $\ge 1$ pass), status ditetapkan sebagai `DISAGREEMENT` dan wajib dieskalasi ke penelaah manusia.
* **Larangan Voting Mayoritas LLM:**
    * Dilarang konsensus otomatis berbasis suara terbanyak antar-pass LLM.
    * Voting otomatis berisiko memperkuat halusinasi berkorelasi (*correlated errors*) serta meniadakan akuntabilitas akademik.
    * Putusan akhir terhadap seluruh butir disagreement selalu berada di tangan penelaah manusia (`Schnee`).
* **Metrik Kesepakatan (Raw Agreement):**
    * Statistik Fleiss' kappa tidak digunakan karena asumsi independensi gugur pada shared weights serta rentan terhadap paradoks *high-agreement low-kappa*.
    * Tingkat kesepakatan diukur menggunakan persentase kesepakatan mentah (*raw agreement percentage*) disertai pengungkapan penuh (*full disclosure*) seluruh log audit.
* **Rekonsiliasi:** larangan Fleiss' kappa di atas berlaku khusus untuk audit 10-pass berbagi bobot model yang sama (*shared weights*), bukan untuk kalibrasi pilot [SYNTHESIS-DOC]. Kalibrasi pilot memakai tiga famili model independen (Gemini 3.8 multimodal, Gemini 3.7 multimodal, Muse Spark teks) sehingga kappa lintas-model sah, dan putusan akhir atas seluruh sengketa tetap di tangan Schnee [EVIDENCED-FACT].
* **Eskalasi Adjudikasi Manusia:**
    * Seluruh butir ketidaksepakatan dieskalasi satu pintu kepada penelaah manusia (`Schnee`).
    * Format log memuat 9 kolom formal: `paper_BID`, `claim_id`, `pass_verdicts`, `type` (*factual/interpretive/scope*),
      `adjudicator` (wajib `Schnee`), `final` (*ACCEPT/REVISE/REJECT*), `rationale`, `evidence_anchor`, dan `date`.
    * Spesifikasi lengkap terdokumentasi pada `02_slr/audit/disagreement_log_SCHEMA.md` (lihat juga subseksi §6b pada halaman [Perencanaan](perencanaan.md)).

### Template dan Status Log Disagreement

* **Template Log Disagreement:**
    * Berkas format baku pelaporan ketidaksepakatan tersedia pada `02_slr/audit/disagreement_log_TEMPLATE.csv`.
* **Status Log Riil Korpus Baru:**
    * Berstatus **OPEN** (menunggu pelaksanaan penapisan/screening dan ekstraksi korpus baru pasca-pencarian final v2.2).
    * Belum ada baris ketidaksepakatan riil dari studi primer baru yang dicatat.
* **Integritas Data & Larangan Rekonstruksi Fiktif:**
    * Berkas template saat ini hanya memuat contoh sintetis berlabel eksplisit `CONTOH-FORMAT-BUKAN-DATA-SYNTH-01` dan `CONTOH-FORMAT-BUKAN-DATA-SYNTH-02`.
    * Dilarang keras mempublikasikan fabrikasi atau rekonstruksi fiktif atas riwayat audit masa lalu demi pemenuhan kelengkapan semu (*anti-fabrication rule*).
    * Seluruh log korpus baru nantinya wajib bersumber murni dari data eksekusi nyata yang diadjudikasi langsung oleh penelaah manusia (`Schnee`).
