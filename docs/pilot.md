# Kalibrasi L2 Pilot (50 Paper)

Kalibrasi kelaikan teks penuh (*full-text eligibility*) berbasis evaluasi silang tiga model kecerdasan buatan independen pada 50 sampel acak (seed 20260913) dari total pool 1.311 PDF [EVIDENCED-FACT].

Tiga penilai model independen:
1. **Model A:** Gemini 3.8 Flash High (Native Multimodal PDF)
2. **Model B:** Gemini 3.7 Flash High (Native Multimodal PDF)
3. **Model C:** Muse Spark 1.3 (OpenCode Agent, Teks Penuh PyMuPDF via 10 Worker Paralel)

---

### 1. Ringkasan Metrik Konsensus 3 Model

Konsensus bulat 3/3 tercapai pada **42 dari 50 paper (84,0%)** [EVIDENCED-FACT].

| Kategori | n (dari 50) | Keterangan |
|---|---|---|
| INCLUDE | 12 | Lolos IC1-IC5, termasuk 3 kontrol Quasi-Gold (P0666, P0507, P0404) |
| EXCLUDE | 30 | Gugur kriteria batas: 14 EC5, 8 EC3, 7 EC2, 1 EC6 |
| Sengketa (split 2-vs-1) | 8 (16,0%) | Di bawah ambang intervensi; perlu adjudikasi Schnee |
| Fleiss' κ | 0,7600 | Melampaui target κ > 0,75 (*Substantial Agreement*) |

Kappa adalah indeks reliabilitas antar-penilai yang terkoreksi peluang acak. STOP-rule: bila sengketa mencapai 20% maka kalibrasi dihentikan untuk adjudikasi penuh [EVIDENCED-FACT].

**Rekonsiliasi:** larangan Fleiss' kappa pada halaman [Jejak Audit](audit.md) §2 berlaku khusus untuk audit 10-pass berbagi bobot model yang sama (*shared weights*), bukan untuk kalibrasi pilot ini [SYNTHESIS-DOC]. Kalibrasi pilot memakai tiga famili model independen (Gemini 3.8 multimodal, Gemini 3.7 multimodal, Muse Spark teks) sehingga kappa lintas-model sah, dan putusan akhir atas seluruh sengketa tetap di tangan Schnee [EVIDENCED-FACT].

Delapan naskah sengketa ini berada di garis batas (*decision boundary*) dan memerlukan adjudikasi langsung oleh peninjau manusia utama (Schnee) untuk mengunci preseden interpretasi kriteria L2 [EVIDENCED-FACT].

---

### 2. Ruang Kerja Interaktif Adjudikasi

Tab **Perlu Adjudikasi (8)** aktif secara default. Gunakan tombol INCLUDE / EXCLUDE untuk menentukan keputusan akhir, lalu tekan **Salin Ringkas** untuk mengekspor rekapitulasi.

<div style="margin: 0.5rem 0 1rem 0; display: flex; gap: 0.5rem; flex-wrap: wrap;">
  <a href="../assets/pilot_app.html" target="_blank" class="md-button md-button--primary">Buka Layar Penuh (Tampilan Ponsel)</a>
  <a href="../assets/pilot_data.json" download class="md-button">Unduh Dataset JSON</a>
  <a href="../assets/pilot_l2_checklist.csv" download class="md-button">Unduh CSV Cadangan</a>
</div>

<iframe
  src="../assets/pilot_app.html"
  loading="lazy"
  style="width: 100%; height: 82vh; min-height: 680px; border: 1px solid var(--md-default-fg-color--lightest, #27272a); border-radius: 6px; display: block;"
  title="Ruang Kerja Adjudikasi L2 Pilot">
</iframe>

---

### 3. Rubrik Acuan Keputusan

**Kriteria Inklusi (Wajib Terpenuhi Semua untuk INCLUDE):**
- **IC1:** Mengusulkan atau mengkaji sistem/arsitektur Multi-Agent LLM untuk tugas Software Engineering (SE).
- **IC2:** Mengkaji koordinasi antar-agen, hierarki peran, feedback loop, komunikasi multi-agent, atau selective approval gate.
- **IC3:** Memuat evaluasi empiris kuantitatif konkret (benchmark, metrik kuantitatif, atau repository nyata).
- **IC4:** Terbit dalam rentang tahun 2020-2026.
- **IC5:** Studi primer berbahasa Inggris (EN) atau Indonesia (ID).

**Kriteria Eksklusi Utama:**
- **EC1:** Naskah tidak terbaca / teks rusak.
- **EC2:** Survei, secondary study, atau position paper murni tanpa evaluasi empiris primer.
- **EC3:** Sistem agen tunggal (single-agent) atau monolitik tanpa interaksi multi-agent.
- **EC4:** Duplikasi naskah.
- **EC5:** Di luar domain rekayasa perangkat lunak (SE).
- **EC6:** Makalah pendek (< 4 halaman) atau non-akademik.
- **EC7:** Bahasa selain Inggris atau Indonesia.
- **EC8:** Terbit di luar rentang 2020-2026.
