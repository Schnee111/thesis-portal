#!/usr/bin/env bash
# ==============================================================================
# gate-site.sh — Gate verifikasi penuh untuk 07_review-site (LANE5, SSOT 11)
#
# SSOT: 02_slr/GS_quasi_gold.md — 11 paper kalibrasi jalur utama
#   (QGS-6 eligible GS02/05/06/07/10/11 + pembanding-C GS01/03/04/08/09)
# Era-47 (DEF_matrix_batch1.csv S01-S47 + DEF_excluded_batch1.csv) DIARSIPKAN di
#   07_review-site/_archive_pilot_batch1/ — DILARANG jadi acuan gate.
#
# Memverifikasi 6 kriteria penerimaan secara deterministik:
# 1. matrix_data.json valid JSON dengan tepat 11 entri
# 2. Direktori docs/matrix/papers berisi tepat 11 file .md
# 3. docs/references.bib berisi tepat 11 bibtex keys unik
# 4. Klop CiteKey vs GS_quasi_gold.md (Paper_ID/BID = GS01-GS11;
#    CiteKey JSON = keys bib = basename papers; anti-regresi S01-S47/B1-xxx)
# 5. mkdocs build --strict exit code 0
# 6. Tidak ada secrets (.env / pola API key / private key) di 07_review-site
#
# Output: Status per check [PASS]/[FAIL], ringkasan exit code 0 bila semua lolos.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
THESIS_DIR="$(cd "${SITE_DIR}/.." && pwd)"

# ANSI Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "================================================================================"
echo "GATE: 07_review-site verification (LANE5, SSOT 11 paper GS_quasi_gold.md)"
echo "Site root   : ${SITE_DIR}"
echo "Thesis root : ${THESIS_DIR}"
echo "Timestamp   : $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "================================================================================"

TOTAL_CHECKS=6
FAILED_CHECKS=0

fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
}

pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# ------------------------------------------------------------------------------
# Check 1/6: matrix_data.json tepat 11 entri valid
# ------------------------------------------------------------------------------
echo ""
echo "--- Check 1/6: matrix_data.json 11 valid ---"
JSON_FILE="${SITE_DIR}/docs/assets/matrix_data.json"
if [[ ! -f "${JSON_FILE}" ]]; then
    fail "matrix_data.json tidak ditemukan di ${JSON_FILE}"
else
    set +e
    JSON_RESULT=$(python3 -c "
import json, sys
try:
    with open('${JSON_FILE}', 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, list):
        print('Bukan JSON array', file=sys.stderr)
        sys.exit(1)
    count = len(data)
    print(count)
    if count != 11:
        sys.exit(2)
except Exception as e:
    print(f'Error parsing JSON: {e}', file=sys.stderr)
    sys.exit(3)
" 2>&1)
    JSON_EXIT=$?
    set -e
    if [[ ${JSON_EXIT} -eq 0 && "${JSON_RESULT}" -eq 11 ]]; then
        pass "matrix_data.json valid JSON dengan tepat 11 entri"
    else
        fail "matrix_data.json tidak valid atau count != 11 (exit: ${JSON_EXIT}, output: ${JSON_RESULT})"
    fi
fi

# ------------------------------------------------------------------------------
# Check 2/6: papers tepat 11 files
# ------------------------------------------------------------------------------
echo ""
echo "--- Check 2/6: papers 11 files ---"
PAPERS_DIR="${SITE_DIR}/docs/matrix/papers"
if [[ ! -d "${PAPERS_DIR}" ]]; then
    fail "Direktori papers tidak ditemukan di ${PAPERS_DIR}"
else
    PAPERS_COUNT=$(find "${PAPERS_DIR}" -maxdepth 1 -name "*.md" | wc -l)
    if [[ "${PAPERS_COUNT}" -eq 11 ]]; then
        pass "docs/matrix/papers/ berisi tepat 11 file .md"
    else
        fail "docs/matrix/papers/ berisi ${PAPERS_COUNT} file .md (harus tepat 11)"
    fi
fi

# ------------------------------------------------------------------------------
# Check 3/6: bib tepat 11 keys unik
# ------------------------------------------------------------------------------
echo ""
echo "--- Check 3/6: bib 11 keys unik ---"
BIB_FILE="${SITE_DIR}/docs/references.bib"
if [[ ! -f "${BIB_FILE}" ]]; then
    fail "references.bib tidak ditemukan di ${BIB_FILE}"
else
    set +e
    BIB_RESULT=$(python3 -c "
import re, sys
with open('${BIB_FILE}', 'r', encoding='utf-8') as f:
    content = f.read()
keys = re.findall(r'@\w+\s*\{\s*([^,\s]+),', content)
unique_keys = set(keys)
if len(keys) != 11:
    print(f'Count {len(keys)} != 11', file=sys.stderr)
    sys.exit(1)
if len(unique_keys) != 11:
    print(f'Duplicate keys found: {len(unique_keys)} unik dari {len(keys)}', file=sys.stderr)
    sys.exit(2)
print(len(unique_keys))
" 2>&1)
    BIB_EXIT=$?
    set -e
    if [[ ${BIB_EXIT} -eq 0 && "${BIB_RESULT}" -eq 11 ]]; then
        pass "references.bib berisi tepat 11 bibtex keys unik"
    else
        fail "references.bib tidak memiliki 11 keys unik (exit: ${BIB_EXIT}, output: ${BIB_RESULT})"
    fi
fi

# ------------------------------------------------------------------------------
# Check 4/6: klop CiteKey vs GS_quasi_gold.md (GS01-GS11, anti S01-S47/B1-xxx)
# ------------------------------------------------------------------------------
echo ""
echo "--- Check 4/6: klop CiteKey vs GS_quasi_gold.md ---"
GS_FILE="${THESIS_DIR}/02_slr/GS_quasi_gold.md"

if [[ ! -f "${GS_FILE}" ]]; then
    fail "SSOT GS_quasi_gold.md tidak ditemukan: ${GS_FILE}"
elif [[ ! -f "${JSON_FILE}" || ! -f "${BIB_FILE}" || ! -d "${PAPERS_DIR}" ]]; then
    fail "Artefak JSON/bib/papers belum lengkap, klop CiteKey tidak bisa dicek"
else
    set +e
    KLOP_RESULT=$(python3 -c "
import json, os, re, sys

with open('${GS_FILE}', 'r', encoding='utf-8') as f:
    gs = f.read()
gs_ids = sorted(set(re.findall(r'^\|\s*(GS\d{2})\s*\|', gs, re.M)))
expected = ['GS%02d' % i for i in range(1, 12)]
if gs_ids != expected:
    print('GS ids di GS_quasi_gold.md != GS01-GS11: %s' % gs_ids, file=sys.stderr)
    sys.exit(1)

with open('${JSON_FILE}', 'r', encoding='utf-8') as f:
    data = json.load(f)
pids = sorted([r.get('Paper_ID', '') for r in data])
bids = sorted([r.get('BID', '') for r in data])
citekeys = sorted([r.get('CiteKey', '') for r in data])
if pids != expected:
    print('JSON Paper_ID tidak klop GS01-GS11: %s' % pids, file=sys.stderr)
    sys.exit(2)
if bids != expected:
    print('JSON BID tidak klop GS01-GS11: %s' % bids, file=sys.stderr)
    sys.exit(3)

with open('${BIB_FILE}', 'r', encoding='utf-8') as f:
    bib = f.read()
bib_keys = sorted(set(re.findall(r'@\w+\s*\{\s*([^,\s]+),', bib)))
if bib_keys != citekeys:
    print('Keys bib != CiteKey JSON: %s vs %s' % (bib_keys, citekeys), file=sys.stderr)
    sys.exit(4)

paper_files = sorted([fn[:-3] for fn in os.listdir('${PAPERS_DIR}') if fn.endswith('.md')])
if paper_files != citekeys:
    print('Basename papers != CiteKey JSON: %s vs %s' % (paper_files, citekeys), file=sys.stderr)
    sys.exit(5)

legacy_pids = [p for p in pids if re.fullmatch(r'S\d{2}', p)]
legacy_bids = [b for b in bids if re.fullmatch(r'B1-\d+', b)]
if legacy_pids or legacy_bids:
    print('Regresi era-47 terdeteksi (S01-S47/B1-xxx): %s %s' % (legacy_pids, legacy_bids), file=sys.stderr)
    sys.exit(6)

print('11 GS ids (GS01-GS11) klop JSON/bib/papers; 0 regresi S01-S47/B1-xxx')
" 2>&1)
    KLOP_EXIT=$?
    set -e
    if [[ ${KLOP_EXIT} -eq 0 ]]; then
        pass "Klop CiteKey vs GS_quasi_gold.md: ${KLOP_RESULT}"
    else
        fail "CiteKey tidak klop GS_quasi_gold.md (exit: ${KLOP_EXIT}, output: ${KLOP_RESULT})"
    fi
fi

# ------------------------------------------------------------------------------
# Check 5/6: mkdocs build --strict exit 0
# ------------------------------------------------------------------------------
echo ""
echo "--- Check 5/6: mkdocs build --strict exit 0 ---"
MKDOCS_BIN=""
if command -v mkdocs >/dev/null 2>&1; then
    MKDOCS_BIN="mkdocs"
elif [[ -x "/tmp/venv_mkdocs/bin/mkdocs" ]]; then
    MKDOCS_BIN="/tmp/venv_mkdocs/bin/mkdocs"
elif [[ -x "/home/ubuntu/.hermes/hermes-agent/venv/bin/mkdocs" ]]; then
    MKDOCS_BIN="/home/ubuntu/.hermes/hermes-agent/venv/bin/mkdocs"
fi

if [[ -z "${MKDOCS_BIN}" ]]; then
    fail "mkdocs executable tidak ditemukan di PATH maupun /tmp/venv_mkdocs/bin"
else
    set +e
    MKDOCS_OUTPUT=$("${MKDOCS_BIN}" build --strict -f "${SITE_DIR}/mkdocs.yml" 2>&1)
    MKDOCS_EXIT=$?
    set -e
    if [[ ${MKDOCS_EXIT} -eq 0 ]]; then
        pass "mkdocs build --strict berhasil dengan exit code 0"
    else
        fail "mkdocs build --strict gagal (exit code: ${MKDOCS_EXIT}):\n${MKDOCS_OUTPUT}"
    fi
fi

# ------------------------------------------------------------------------------
# Check 6/6: Grep no secrets (.env / API key pola)
# ------------------------------------------------------------------------------
echo ""
echo "--- Check 6/6: Grep no secrets (.env / API key patterns) ---"
SECRETS_FOUND=0

# 6a: Cek file .env di 07_review-site
ENV_FILES=$(find "${SITE_DIR}" -name ".env*" 2>/dev/null || true)
if [[ -n "${ENV_FILES}" ]]; then
    fail "Ditemukan file .env di 07_review-site:\n${ENV_FILES}"
    SECRETS_FOUND=1
fi

# 6b: Scan file (exclude scripts/gates/gate-site.sh sendiri agar tidak false-positive pada definisi pola)
SECRET_PATTERN='sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|BEGIN PRIVATE KEY|AKIA[0-9A-Z]{16}'
SECRET_MATCHES=$(grep -rnI -E "${SECRET_PATTERN}" --exclude="gate-site.sh" "${SITE_DIR}" 2>/dev/null || true)
if [[ -n "${SECRET_MATCHES}" ]]; then
    fail "Ditemukan pattern credentials/secret di file:\n${SECRET_MATCHES}"
    SECRETS_FOUND=1
fi

if [[ ${SECRETS_FOUND} -eq 0 ]]; then
    pass "Tidak ditemukan file .env maupun pattern API key/credentials di 07_review-site"
fi

# ------------------------------------------------------------------------------
# Ringkasan Akhir
# ------------------------------------------------------------------------------
echo ""
echo "================================================================================"
if [[ ${FAILED_CHECKS} -eq 0 ]]; then
    echo -e "${GREEN}SUCCESS: Semua ${TOTAL_CHECKS}/${TOTAL_CHECKS} checks lolos!${NC}"
    echo "================================================================================"
    exit 0
else
    echo -e "${RED}FAILURE: ${FAILED_CHECKS}/${TOTAL_CHECKS} checks gagal!${NC}"
    echo "================================================================================"
    exit 1
fi
