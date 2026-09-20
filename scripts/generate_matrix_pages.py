#!/usr/bin/env python3
"""
generate_matrix_pages.py — Generator deterministik untuk MkDocs thesis-review-site.

Tugas:
1. Membaca CSV SSOT:
   - DEF_matrix_batch1.csv (47 baris INCLUDE)
   - DEF_excluded_batch1.csv (10 baris EXCLUDE, untuk validasi count)
2. Menghasilkan:
   - docs/matrix/papers/<CiteKey>.md (47 berkas detail Markdown dengan YAML frontmatter lengkap)
   - docs/assets/matrix_data.json (Array 47 objek verbatim + properti turunan txt_path)
   - docs/references.bib (47 bib entry valid @misc/@inproceedings dengan key=CiteKey)
   - docs/matrix/_generated_table_snippet.md (Snippet agregasi Markdown ringkas 7 kolom)
3. Deterministik:
   - Diurutkan berdasarkan BID (B1-001 s.d. B1-142)
   - Baris baru LF ('\n') konsisten
   - UTF-8 tanpa BOM, ensure_ascii=False
   - Verifikasi rerun identik dengan flag --check (exit code 0 bila byte-identical)
"""

import argparse
import csv
import glob
import hashlib
import json
import os
import re
import sys

# Paths relatif terhadap root direktori repositori 07_review-site
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_ROOT = os.path.dirname(SCRIPT_DIR)

DEF_MATRIX_CSV = "/home/ubuntu/thesis/02_slr/extraction/DEF_matrix_batch1.csv"
DEF_EXCLUDED_CSV = "/home/ubuntu/thesis/02_slr/extraction/DEF_excluded_batch1.csv"
EXTRACTION_BASE = "/home/ubuntu/thesis/02_slr/extraction"

PAPERS_DIR = os.path.join(SITE_ROOT, "docs", "matrix", "papers")
ASSETS_DIR = os.path.join(SITE_ROOT, "docs", "assets")
MATRIX_DATA_JSON = os.path.join(ASSETS_DIR, "matrix_data.json")
REFERENCES_BIB = os.path.join(SITE_ROOT, "docs", "references.bib")
SNIPPET_MD = os.path.join(SITE_ROOT, "docs", "matrix", "_generated_table_snippet.md")


def sanitize_citekey(raw_key: str) -> str:
    """Sanitasi CiteKey untuk nama berkas [a-z0-9-]."""
    cleaned = raw_key.lower().strip()
    sanitized = re.sub(r"[^a-z0-9-]", "-", cleaned)
    return sanitized


def resolve_txt_path(bid: str, prov_tag: str, all_rel_txts: list[str]) -> str:
    """
    Menentukan path relatif berkas teks lokal dari Provenance_Tag atau pencarian disk.
    Prioritas:
    1. Path eksplisit di Provenance_Tag yang terverifikasi ada di disk.
    2. Kandidat disk berdasarkan BID (preferensi: papers/ -> txt/ -> pdf_cache/).
    3. String kosong bila tidak ditemukan (misal: abstract-only).
    """
    m = re.search(r"((?:papers|pdf_cache|txt)/[^\s;,\)]+\.txt)", prov_tag)
    prov_txt = m.group(1) if m else None
    if prov_txt and os.path.exists(os.path.join(EXTRACTION_BASE, prov_txt)):
        return prov_txt

    cands = [p for p in all_rel_txts if bid in p]
    if cands:
        papers_cands = [p for p in cands if p.startswith("papers/")]
        if papers_cands:
            return papers_cands[0]
        txt_cands = [p for p in cands if p.startswith("txt/")]
        if txt_cands:
            return txt_cands[0]
        pdf_cands = [p for p in cands if p.startswith("pdf_cache/")]
        if pdf_cands:
            return pdf_cands[0]
        return cands[0]

    return ""


def extract_year(citekey: str, authors_year: str, venue_tier: str) -> int:
    """Ekstraksi tahun publikasi 4 digit dari CiteKey atau metadata."""
    m_ck = re.search(r"(\d{4})", citekey)
    if m_ck:
        return int(m_ck.group(1))
    m_ay = re.search(r"(?:19|20)\d{2}", authors_year)
    if m_ay:
        return int(m_ay.group(0))
    m_vt = re.search(r"(?:19|20)\d{2}", venue_tier)
    if m_vt:
        return int(m_vt.group(0))
    return 2026


def derive_tags(row: dict) -> list[str]:
    """Menghasilkan taksonomi tags terstruktur untuk YAML frontmatter."""
    tags = []
    role_lower = row.get("Role", "").lower()
    if "primary" in role_lower:
        tags.append("primary")
    elif "supporting" in role_lower:
        tags.append("supporting")

    ext_lower = row.get("Extraction_Level", "").lower()
    if "abstract-only" in ext_lower:
        tags.append("abstract-only")
    else:
        tags.append("fulltext")

    venue_lower = row.get("Venue_Tier", "").lower()
    if any(k in venue_lower for k in ["preprint", "arxiv", "ssrn", "techrxiv", "preprints.org"]):
        tags.append("preprint")
    else:
        tags.append("peer-reviewed")

    combined_text = (
        role_lower
        + " "
        + row.get("Proposed_Architecture", "").lower()
        + " "
        + row.get("Coordination_Control", "").lower()
    )
    topics = [
        ("hitl", "hitl"),
        ("langgraph", "langgraph"),
        ("metagpt", "metagpt"),
        ("tdd", "tdd"),
        ("rag", "rag"),
        ("security", "security"),
        ("exploit", "security"),
        ("observability", "observability"),
        ("coordination", "coordination"),
        ("orchestration", "orchestration"),
    ]
    for pattern, tag in topics:
        if pattern in combined_text and tag not in tags:
            tags.append(tag)

    return tags


def escape_bibtex_value(val: str) -> str:
    """
    Sanitasi string untuk nilai field BibTeX:
    - Escapes $ menjadi \\$ untuk mencegah bash parameter expansion atau error MathJaX
    - Normalisasi whitespace
    - Hindari kurung kurawal tak seimbang
    """
    v = val.strip().replace("\n", " ")
    v = re.sub(r"\s+", " ", v)
    v = v.replace("\\$", "$")  # normalisasi jika sudah ter-escape
    v = v.replace("$", r"\$")
    v = v.replace("{", "(").replace("}", ")")
    return v


def clean_bibtex_author(raw: str) -> str:
    """Membersihkan string Authors_Year untuk field author BibTeX yang valid (memakai 'and' sebagai pemisah)."""
    s = re.sub(r"\([^)]*\)", "", raw)
    s = re.sub(r",\s*(?:19|20)\d{2}$", "", s)
    s = s.strip().strip(",")
    s = re.sub(r"\s+", " ", s)
    if " et al" in s:
        base = re.sub(r"\s+et\s+al.*$", "", s).strip().strip(",")
        return escape_bibtex_value(f"{base} and others")
    parts = [p.strip() for p in s.split(",") if p.strip()]
    if len(parts) > 1:
        return escape_bibtex_value(" and ".join(parts))
    if not s:
        s = "Unknown Author"
    return escape_bibtex_value(s)


def escape_markdown(text: str) -> str:
    """
    Sanitasi karakter untuk konten Markdown.
    Meng-escape tanda dolar ($) agar tidak memicu MathJax/KaTeX di MkDocs
    serta mencegah korupsi format uang ($0.44 dsb).
    """
    if not text:
        return ""
    # Ganti $ yang tidak di-escape menjadi \$
    # Pertama ganti \$ menjadi $ dulu agar idempoten
    t = text.replace(r"\$", "$")
    t = t.replace("$", r"\$")
    return t


def generate_frontmatter_yaml(meta: dict) -> str:
    """
    Menghasilkan string YAML frontmatter secara manual & deterministik
    tanpa dependensi eksternal tak stabil.
    """
    lines = ["---"]
    # title (quote if contains special chars)
    title_escaped = meta["title"].replace('"', '\\"')
    lines.append(f'title: "{title_escaped}"')
    lines.append(f'paper_id: {meta["paper_id"]}')
    lines.append(f'bid: {meta["bid"]}')
    authors_escaped = meta["authors"].replace('"', '\\"')
    lines.append(f'authors: "{authors_escaped}"')
    lines.append(f'year: {meta["year"]}')
    venue_escaped = meta["venue"].replace('"', '\\"')
    lines.append(f'venue: "{venue_escaped}"')
    doi_escaped = meta["doi"].replace('"', '\\"')
    lines.append(f'doi: "{doi_escaped}"')
    lines.append(f'qa: {meta["qa"]}')
    role_escaped = meta["role"].replace('"', '\\"')
    lines.append(f'role: "{role_escaped}"')
    ext_escaped = meta["extraction"].replace('"', '\\"')
    lines.append(f'extraction: "{ext_escaped}"')
    lines.append("tags:")
    for t in meta["tags"]:
        lines.append(f"  - {t}")
    lines.append("---")
    return "\n".join(lines)


def generate_markdown_content(row: dict, txt_rel_path: str, tags: list[str], year: int) -> str:
    """
    Menghasilkan halaman Markdown komprehensif untuk sebuah paper.
    Format: Frontmatter YAML + Body seksi lengkap (Core Problem, Architecture, dll.)
    """
    meta = {
        "title": row.get("Title", "").strip(),
        "paper_id": row.get("Paper_ID", "").strip(),
        "bid": row.get("BID", "").strip(),
        "authors": row.get("Authors_Year", "").strip(),
        "year": year,
        "venue": row.get("Venue_Tier", "").strip(),
        "doi": row.get("DOI_URL", "").strip(),
        "qa": float(row.get("QA_Score", "0.0")),
        "role": row.get("Role", "").strip(),
        "extraction": row.get("Extraction_Level", "").strip(),
        "tags": tags,
    }

    frontmatter = generate_frontmatter_yaml(meta)

    pid = row.get("Paper_ID", "").strip()
    bid = row.get("BID", "").strip()
    title = escape_markdown(row.get("Title", "").strip())
    authors = escape_markdown(row.get("Authors_Year", "").strip())
    venue = escape_markdown(row.get("Venue_Tier", "").strip())
    doi = row.get("DOI_URL", "").strip()
    qa = row.get("QA_Score", "").strip()
    role = escape_markdown(row.get("Role", "").strip())
    ext_level = escape_markdown(row.get("Extraction_Level", "").strip())
    citekey = row.get("CiteKey", "").strip()

    # Section contents
    core_problem = escape_markdown(row.get("Core_Problem", "").strip())
    scope = escape_markdown(row.get("Scope", "").strip())
    architecture = escape_markdown(row.get("Proposed_Architecture", "").strip())
    coordination = escape_markdown(row.get("Coordination_Control", "").strip())
    fm = escape_markdown(row.get("Foundation_Model", "").strip())
    benchmark = escape_markdown(row.get("Benchmark_Dataset", "").strip())
    artifact = escape_markdown(row.get("Artifact_Type", "").strip())
    primary_metrics = escape_markdown(row.get("Primary_Metrics_Exact", "").strip())
    secondary_metrics = escape_markdown(row.get("Secondary_Metrics", "").strip())
    failure_modes = escape_markdown(row.get("Failure_Modes", "").strip())
    threats = escape_markdown(row.get("Threats_Validity", "").strip())
    provenance = escape_markdown(row.get("Provenance_Tag", "").strip())

    # DOI URL link
    if doi.startswith("http://") or doi.startswith("https://"):
        doi_link = f"[{doi}]({doi})"
    elif doi:
        doi_link = f"[{doi}](https://doi.org/{doi})"
    else:
        doi_link = "Tidak tersedia"

    # Badge warna QA
    qa_val = float(qa) if qa else 0.0
    if qa_val >= 9.0:
        qa_badge = f'<span style="background-color: #2e7d32; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold;">{qa} (Tinggi)</span>'
    elif qa_val >= 7.5:
        qa_badge = f'<span style="background-color: #f57f17; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold;">{qa} (Sedang)</span>'
    else:
        qa_badge = f'<span style="background-color: #616161; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold;">{qa} (Cukup / Abstrak)</span>'

    body_parts = [
        frontmatter,
        "",
        f"# [{pid}] {title}",
        "",
        f"**Kunci Stabil (BID):** `{bid}` | **Sitasi BibTeX:** [@{citekey}]",
        "",
        "## Ringkasan Metadata",
        "",
        f"- **Penulis & Tahun:** {authors}",
        f"- **Venue & Tier:** {venue}",
        f"- **DOI / URL:** {doi_link}",
        f"- **Skor Kualitas (QA Score):** {qa_badge}",
        f"- **Peran Studi:** {role}",
        f"- **Tingkat Ekstraksi:** `{ext_level}`",
        f"- **Cakupan (Scope):** {scope}",
        f"- **Berkas Teks Lokal:** `{txt_rel_path if txt_rel_path else 'Tidak tersedia / abstract-only'}`",
        "",
        "---",
        "",
        "## 1. Masalah Utama (Core Problem)",
        "",
        core_problem if core_problem else "*Tidak dilaporkan secara eksplisit.*",
        "",
        "## 2. Arsitektur yang Diajukan (Architecture)",
        "",
        architecture if architecture else "*Tidak dilaporkan secara eksplisit.*",
        "",
        "## 3. Mekanisme Koordinasi & Kontrol (Coordination)",
        "",
        coordination if coordination else "*Tidak dilaporkan secara eksplisit.*",
        "",
        "## 4. Foundation Model & Infrastruktur (FM)",
        "",
        fm if fm else "*Tidak dilaporkan secara eksplisit.*",
        "",
        "## 5. Tolok Ukur & Dataset (Benchmark)",
        "",
        benchmark if benchmark else "*Tidak dilaporkan secara eksplisit.*",
        "",
        "## 6. Artefak & Kode Sumber (Artifact)",
        "",
        artifact if artifact else "*Tidak ada artefak publik / kode tertutup.*",
        "",
        "## 7. Metrik Primer Eksak (Primary exact)",
        "",
        primary_metrics if primary_metrics else "*Tidak ada metrik kuantitatif terlaporkan.*",
        "",
        "## 8. Metrik Sekunder (Secondary)",
        "",
        secondary_metrics if secondary_metrics else "*Tidak ada metrik sekunder terlaporkan.*",
        "",
        "## 9. Pola Kegagalan (Failure Modes)",
        "",
        failure_modes if failure_modes else "*Tidak dilaporkan.*",
        "",
        "## 10. Ancaman Validitas (Threats)",
        "",
        threats if threats else "*Tidak dilaporkan secara eksplisit.*",
        "",
        "## 11. Jejak Bukti & Provenansi (Provenance)",
        "",
        f"> **Bukti Verifikasi:** {provenance}",
        "",
    ]

    return "\n".join(body_parts)


def generate_bibtex_entry(row: dict, year: int) -> str:
    """
    Menghasilkan 1 entri BibTeX valid (@misc atau @inproceedings).
    Key: CiteKey
    Fields: author, title, year, [booktitle], note (berisi Venue, DOI, QA)
    """
    citekey = row.get("CiteKey", "").strip()
    title = escape_bibtex_value(row.get("Title", ""))
    author = clean_bibtex_author(row.get("Authors_Year", ""))
    venue = escape_bibtex_value(row.get("Venue_Tier", ""))
    doi = escape_bibtex_value(row.get("DOI_URL", ""))
    qa = row.get("QA_Score", "").strip()

    venue_lower = venue.lower()
    is_conf = any(
        k in venue_lower
        for k in ["conference", "symposium", "workshop", "proceedings", "icse", "iclr", "fse", "satrends", "ease"]
    )
    entry_type = "inproceedings" if is_conf else "misc"

    note_parts = []
    if venue:
        note_parts.append(f"Venue: {venue}")
    if doi:
        note_parts.append(f"DOI: {doi}")
    if qa:
        note_parts.append(f"QA: {qa}")
    note_str = ", ".join(note_parts)

    lines = [f"@{entry_type}{{{citekey},"]
    lines.append(f"  author = {{{author}}},")
    lines.append(f"  title = {{{{{title}}}}},")
    lines.append(f"  year = {{{year}}},")
    if entry_type == "inproceedings":
        lines.append(f"  booktitle = {{{{{venue}}}}},")
    if note_str:
        lines.append(f"  note = {{{note_str}}}")
    else:
        lines.append("  note = {}")
    lines.append("}\n")
    return "\n".join(lines)


def generate_table_snippet(rows: list[dict]) -> str:
    """
    Menghasilkan snippet tabel Markdown 7-kolom untuk agregasi:
    | Paper ID | BID | Judul & Sitasi | Arsitektur | QA | Peran | Detail |
    """
    lines = [
        "<!-- Auto-generated by scripts/generate_matrix_pages.py. DO NOT EDIT DIRECTLY. -->",
        "",
        "| ID | BID | Judul Studi | Arsitektur | QA | Peran | Tautan |",
        "|:---|:---|:---|:---|:---:|:---|:---:|",
    ]

    for r in rows:
        pid = r.get("Paper_ID", "").strip()
        bid = r.get("BID", "").strip()
        raw_title = r.get("Title", "").strip()
        # Ringkas judul jika terlalu panjang untuk tampilan tabel
        title = raw_title if len(raw_title) <= 75 else raw_title[:72] + "..."
        citekey = r.get("CiteKey", "").strip()
        sanitized_ck = sanitize_citekey(citekey)
        arch = r.get("Proposed_Architecture", "").strip()
        arch_short = arch if len(arch) <= 80 else arch[:77] + "..."
        qa = r.get("QA_Score", "").strip()
        role = r.get("Role", "").strip()
        role_short = role if len(role) <= 40 else role[:37] + "..."

        # Escape pipe symbols in markdown table cells
        title_cell = escape_markdown(title).replace("|", "\\|")
        arch_cell = escape_markdown(arch_short).replace("|", "\\|")
        role_cell = escape_markdown(role_short).replace("|", "\\|")

        link_detail = f"[Buka Detail](papers/{sanitized_ck}.md)"

        lines.append(f"| **{pid}** | `{bid}` | {title_cell} | {arch_cell} | **{qa}** | {role_cell} | {link_detail} |")

    lines.append("")
    return "\n".join(lines)


def run_generator(dry_run: bool = False) -> dict[str, str]:
    """
    Mengeksekusi pembacaan SSOT dan menghasilkan seluruh artefak.
    Mengembalikan dictionary: {file_path: file_content_str}.
    """
    if not os.path.exists(DEF_MATRIX_CSV):
        raise FileNotFoundError(f"SSOT Matrix CSV tidak ditemukan: {DEF_MATRIX_CSV}")

    # 1. Validasi count excluded CSV
    if os.path.exists(DEF_EXCLUDED_CSV):
        with open(DEF_EXCLUDED_CSV, mode="r", encoding="utf-8") as f_ex:
            excluded_rows = list(csv.DictReader(f_ex))
            if len(excluded_rows) != 10:
                print(f"[WARNING] Jumlah excluded rows ({len(excluded_rows)}) != 10 yang diharapkan.")
    else:
        print(f"[WARNING] SSOT Excluded CSV tidak ditemukan: {DEF_EXCLUDED_CSV}")

    # 2. Baca DEF_matrix_batch1.csv
    with open(DEF_MATRIX_CSV, mode="r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        rows = list(reader)

    if len(rows) != 47:
        raise ValueError(f"Jumlah baris matrix {len(rows)} != 47 yang diharapkan.")

    # Sort deterministik berdasarkan BID
    rows.sort(key=lambda r: r["BID"].strip())

    # Cari daftar berkas teks lokal di extraction base
    all_txt = glob.glob(os.path.join(EXTRACTION_BASE, "**", "*.txt"), recursive=True)
    all_rel_txts = [os.path.relpath(p, EXTRACTION_BASE) for p in all_txt]

    generated_files = {}

    # 3. Bentuk data JSON dan berkas papers/*.md
    json_array = []
    bib_entries = []
    seen_citekeys = set()

    for r in rows:
        bid = r.get("BID", "").strip()
        citekey = r.get("CiteKey", "").strip()
        sanitized_ck = sanitize_citekey(citekey)

        if sanitized_ck in seen_citekeys:
            raise ValueError(f"CiteKey tidak unik setelah sanitasi: {sanitized_ck}")
        seen_citekeys.add(sanitized_ck)

        prov_tag = r.get("Provenance_Tag", "").strip()
        txt_rel_path = resolve_txt_path(bid, prov_tag, all_rel_txts)
        year = extract_year(citekey, r.get("Authors_Year", ""), r.get("Venue_Tier", ""))
        tags = derive_tags(r)

        # Siapkan objek JSON (semua kolom CSV verbatim + txt_path turunan)
        row_json = dict(r)
        row_json["txt_path"] = txt_rel_path
        row_json["year_derived"] = year
        row_json["tags_derived"] = tags
        json_array.append(row_json)

        # Siapkan Markdown paper
        md_content = generate_markdown_content(r, txt_rel_path, tags, year)
        md_path = os.path.join(PAPERS_DIR, f"{sanitized_ck}.md")
        generated_files[md_path] = md_content

        # Siapkan BibTeX entry
        bib_entry = generate_bibtex_entry(r, year)
        bib_entries.append(bib_entry)

    # JSON output string
    json_str = json.dumps(json_array, ensure_ascii=False, indent=2) + "\n"
    generated_files[MATRIX_DATA_JSON] = json_str

    # BibTeX output string
    bib_str = "% References BibTeX stub generated by generate_matrix_pages.py\n% Total entries: 47\n\n" + "\n".join(bib_entries)
    generated_files[REFERENCES_BIB] = bib_str

    # Snippet Markdown output string
    snippet_str = generate_table_snippet(rows)
    generated_files[SNIPPET_MD] = snippet_str

    if not dry_run:
        os.makedirs(PAPERS_DIR, exist_ok=True)
        os.makedirs(ASSETS_DIR, exist_ok=True)

        for path, content in generated_files.items():
            with open(path, mode="w", encoding="utf-8", newline="\n") as out_f:
                out_f.write(content)

    return generated_files


def calculate_hashes(files_dict: dict[str, str]) -> dict[str, str]:
    """Menghitung hash SHA256 dari konten setiap berkas."""
    hashes = {}
    for path, content in sorted(files_dict.items()):
        h = hashlib.sha256(content.encode("utf-8")).hexdigest()
        hashes[path] = h
    return hashes


def main():
    parser = argparse.ArgumentParser(description="Generator halaman matriks studi tesis.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verifikasi determinisme: jalankan generasi 2x dan pastikan hash berkas identik serta sesuai disk.",
    )
    args = parser.parse_args()

    if args.check:
        print("[CHECK] Memulai verifikasi deterministik TASK-1.2...")
        # Run 1: generate dan tulis ke disk
        files1 = run_generator(dry_run=False)
        hashes1 = calculate_hashes(files1)

        # Run 2: generate kembali (dry run)
        files2 = run_generator(dry_run=True)
        hashes2 = calculate_hashes(files2)

        # Bandingkan run 1 vs run 2
        mismatches = []
        for path in hashes1:
            if hashes1[path] != hashes2.get(path):
                mismatches.append(path)

        if mismatches:
            print(f"[FAIL] Ditemukan ketidakcocokan hash antara Run 1 dan Run 2 pada {len(mismatches)} berkas:")
            for m in mismatches:
                print(f"  - {m}")
            sys.exit(1)

        # Verifikasi terhadap apa yang tertulis di disk
        disk_mismatches = []
        for path, content in files1.items():
            if not os.path.exists(path):
                disk_mismatches.append(f"{path} (berkas tidak ada di disk)")
                continue
            with open(path, mode="r", encoding="utf-8") as df:
                disk_content = df.read()
            disk_h = hashlib.sha256(disk_content.encode("utf-8")).hexdigest()
            if disk_h != hashes1[path]:
                disk_mismatches.append(f"{path} (hash disk berbeda dari hash generator)")

        if disk_mismatches:
            print(f"[FAIL] Ketidakcocokan dengan disk:")
            for dm in disk_mismatches:
                print(f"  - {dm}")
            sys.exit(1)

        # Verifikasi counts
        paper_files = [p for p in files1.keys() if p.startswith(PAPERS_DIR)]
        if len(paper_files) != 47:
            print(f"[FAIL] Jumlah paper markdown {len(paper_files)} != 47")
            sys.exit(1)

        # Verifikasi json load
        with open(MATRIX_DATA_JSON, mode="r", encoding="utf-8") as jf:
            data = json.load(jf)
            if len(data) != 47:
                print(f"[FAIL] JSON data length {len(data)} != 47")
                sys.exit(1)

        print("[SUCCESS] Verifikasi deterministik sukses 100%! Semua hash identik (47 md, 1 json, 1 bib, 1 snippet).")
        sys.exit(0)
    else:
        print("[GENERATE] Menjalankan generator halaman matriks...")
        files = run_generator(dry_run=False)
        print(f"[SUCCESS] Berhasil menghasilkan {len(files)} berkas:")
        print(f"  - {len([p for p in files if p.startswith(PAPERS_DIR)])} berkas di docs/matrix/papers/")
        print(f"  - docs/assets/matrix_data.json ({os.path.getsize(MATRIX_DATA_JSON)} bytes)")
        print(f"  - docs/references.bib ({os.path.getsize(REFERENCES_BIB)} bytes)")
        print(f"  - docs/matrix/_generated_table_snippet.md ({os.path.getsize(SNIPPET_MD)} bytes)")


if __name__ == "__main__":
    main()
