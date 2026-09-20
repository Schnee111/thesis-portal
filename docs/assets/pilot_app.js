// pilot_app.js - Minimalist, Utilitarian Review Workspace for Pilot L2
(function() {
  const STORAGE_KEY = 'schnee_pilot_l2_answers_v3';
  let papers = [];
  let userAnswers = {};
  let activeFilter = 'disagree';
  let searchQuery = '';

  const EC_OPTIONS = [
    { code: '', label: 'Pilih EC (jika N)...' },
    { code: 'EC1', label: 'EC1: Corrupt / Unreadable' },
    { code: 'EC2', label: 'EC2: Secondary / Survey / Position' },
    { code: 'EC3', label: 'EC3: Single-Agent / Non Multi-Agent' },
    { code: 'EC4', label: 'EC4: Duplication' },
    { code: 'EC5', label: 'EC5: Out of Software Engineering Domain' },
    { code: 'EC6', label: 'EC6: Short Paper (<4 pages)' },
    { code: 'EC7', label: 'EC7: Non-English / Non-Indonesian' },
    { code: 'EC8', label: 'EC8: Year out of 2020-2026' }
  ];

  function showToast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2000);
  }

  function loadSavedAnswers() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) userAnswers = JSON.parse(raw);
    } catch (e) {
      userAnswers = {};
    }
  }

  function persistAnswers() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(userAnswers));
    } catch (e) {}
    updateStats();
  }

  async function init() {
    loadSavedAnswers();
    try {
      const res = await fetch('./pilot_data.json?v=' + Date.now());
      if (!res.ok) throw new Error('HTTP ' + res.status);
      papers = await res.json();
    } catch (e) {
      document.getElementById('cards-list').innerHTML =
        '<div style="color:var(--exc-text);padding:30px;text-align:center;">Gagal memuat dataset: ' + e.message + '</div>';
      return;
    }

    // Auto-populate unanimous decisions
    let autoCount = 0;
    papers.forEach(p => {
      if (!userAnswers[p.paper_id] && p.unanimous && p.modelA) {
        const dec = p.modelA.decision === 'INCLUDE' ? 'Y' : 'N';
        const ec = (dec === 'N') ? (p.modelA.ec !== '-' ? p.modelA.ec : '') : '';
        userAnswers[p.paper_id] = {
          decision: dec,
          ec: ec,
          note: 'Auto: Konsensus 3/3 Model AI'
        };
        autoCount++;
      }
    });
    if (autoCount > 0) persistAnswers();

    setupEventListeners();
    updateStats();
    renderCards();
  }

  function setupEventListeners() {
    const searchBox = document.getElementById('search-box');
    searchBox.addEventListener('input', (e) => {
      searchQuery = e.target.value.toLowerCase().trim();
      renderCards();
    });

    const filterBtns = document.querySelectorAll('.segmented-btn');
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => {
          b.classList.remove('active');
          b.classList.remove('active-warning');
        });
        activeFilter = btn.getAttribute('data-filter');
        if (activeFilter === 'disagree') {
          btn.classList.add('active-warning');
        } else {
          btn.classList.add('active');
        }
        renderCards();
      });
    });

    document.getElementById('btn-copy-summary').addEventListener('click', copySummary);
    document.getElementById('btn-download-csv').addEventListener('click', downloadCSV);
    document.getElementById('btn-download-json').addEventListener('click', downloadJSON);
  }

  function updateStats() {
    let countY = 0;
    let countN = 0;
    let answered = 0;

    papers.forEach(p => {
      const ans = userAnswers[p.paper_id];
      if (ans && (ans.decision === 'Y' || ans.decision === 'N')) {
        answered++;
        if (ans.decision === 'Y') countY++;
        if (ans.decision === 'N') countN++;
      }
    });

    const total = papers.length || 50;
    const pct = Math.round((answered / total) * 100);

    const txt = document.getElementById('progress-text');
    if (txt) {
      txt.textContent = `${answered} / ${total} (${pct}%) · INC: ${countY} · EXC: ${countN}`;
    }
    const fill = document.getElementById('progress-fill');
    if (fill) fill.style.width = pct + '%';
  }

  function renderCards() {
    const list = document.getElementById('cards-list');
    if (!list) return;

    const filtered = papers.filter(p => {
      if (activeFilter === 'disagree') {
        if (!p.is_disagreement) return false;
      } else if (activeFilter === 'agree-include') {
        if (p.is_disagreement || (p.majority_decision !== 'INCLUDE')) return false;
      } else if (activeFilter === 'agree-exclude') {
        if (p.is_disagreement || (p.majority_decision !== 'EXCLUDE')) return false;
      } else if (activeFilter === 'unanswered') {
        const ans = userAnswers[p.paper_id];
        if (ans && (ans.decision === 'Y' || ans.decision === 'N')) return false;
      }

      if (searchQuery) {
        const hay = [
          p.paper_id,
          p.title,
          p.venue,
          p.doi,
          p.abstract_short || ''
        ].join(' ').toLowerCase();
        if (!hay.includes(searchQuery)) return false;
      }
      return true;
    });

    if (filtered.length === 0) {
      list.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-faint);">Tidak ada paper yang cocok dengan filter.</div>';
      return;
    }

    list.innerHTML = '';
    filtered.forEach(p => {
      list.appendChild(createCardElement(p));
    });
  }

  function createCardElement(p) {
    const ans = userAnswers[p.paper_id] || { decision: '', ec: '', note: '' };
    const card = document.createElement('article');
    card.className = 'paper-card';
    card.id = 'card-' + p.paper_id;

    if (p.is_disagreement) card.classList.add('is-split');
    if (ans.decision === 'Y') card.classList.add('answered-inc');
    else if (ans.decision === 'N') card.classList.add('answered-exc');

    // Card Top Row
    const topRow = document.createElement('div');
    topRow.className = 'card-top';

    const tagsLeft = document.createElement('div');
    tagsLeft.className = 'card-tags';

    const pid = document.createElement('span');
    pid.className = 'tag-mono';
    pid.textContent = `#${p.no} ${p.paper_id}`;
    tagsLeft.appendChild(pid);

    if (p.is_control) {
      const ctrlTag = document.createElement('span');
      ctrlTag.className = 'tag tag-control';
      ctrlTag.textContent = 'QGS CONTROL';
      tagsLeft.appendChild(ctrlTag);
    }

    if (p.is_disagreement) {
      const splitTag = document.createElement('span');
      splitTag.className = 'tag tag-split';
      splitTag.textContent = `SPLIT 2 vs 1 (Mayoritas: ${p.majority_decision})`;
      tagsLeft.appendChild(splitTag);
    } else {
      const agTag = document.createElement('span');
      agTag.className = 'tag';
      agTag.textContent = `BULAT 3/3: ${p.majority_decision}`;
      tagsLeft.appendChild(agTag);
    }

    const yr = document.createElement('span');
    yr.className = 'tag';
    yr.textContent = p.year || '-';
    tagsLeft.appendChild(yr);

    topRow.appendChild(tagsLeft);
    card.appendChild(topRow);

    // Title
    const titleEl = document.createElement('h2');
    titleEl.className = 'card-title';
    titleEl.textContent = p.title;
    card.appendChild(titleEl);

    // Meta row
    const meta = document.createElement('div');
    meta.className = 'card-meta';
    let metaHtml = `<span><strong>Venue:</strong> ${escapeHtml(p.venue || '-')}</span>`;
    if (p.doi) {
      metaHtml += `<span><strong>DOI:</strong> <a href="https://doi.org/${encodeURIComponent(p.doi)}" target="_blank">${escapeHtml(p.doi)}</a></span>`;
    }
    metaHtml += `<a href="./pilot_pdfs/${encodeURIComponent(p.paper_id)}.pdf" target="_blank" class="btn-pdf">PDF ↗</a>`;
    meta.innerHTML = metaHtml;
    card.appendChild(meta);

    // Model Breakdown Table (Minimalist Table)
    const table = document.createElement('table');
    table.className = 'model-table';
    let tbodyHtml = '';

    const models = [
      { name: 'Gemini 3.8', data: p.modelA },
      { name: 'Gemini 3.7', data: p.modelB },
      { name: 'Muse 1.3', data: p.modelC }
    ];

    models.forEach(m => {
      if (!m.data) return;
      const dec = m.data.decision || 'EXCLUDE';
      const ec = (m.data.ec && m.data.ec !== '-') ? ` ${m.data.ec}` : '';
      const bClass = dec === 'INCLUDE' ? 'badge-inc' : 'badge-exc';
      tbodyHtml += `
        <tr>
          <td class="col-model">${m.name}</td>
          <td class="col-dec"><span class="badge-dec ${bClass}">${dec}${ec}</span></td>
          <td class="col-rat">${escapeHtml(m.data.rationale || '')}</td>
        </tr>
      `;
    });
    table.innerHTML = tbodyHtml;
    card.appendChild(table);

    // Controls Strip
    const ctrlStrip = document.createElement('div');
    ctrlStrip.className = 'controls-strip';

    const btnInc = document.createElement('button');
    btnInc.className = 'btn btn-choice ' + (ans.decision === 'Y' ? 'active-inc' : '');
    btnInc.textContent = 'INCLUDE';
    btnInc.addEventListener('click', () => setDecision(p.paper_id, 'Y'));

    const btnExc = document.createElement('button');
    btnExc.className = 'btn btn-choice ' + (ans.decision === 'N' ? 'active-exc' : '');
    btnExc.textContent = 'EXCLUDE';
    btnExc.addEventListener('click', () => setDecision(p.paper_id, 'N'));

    ctrlStrip.appendChild(btnInc);
    ctrlStrip.appendChild(btnExc);

    const selEC = document.createElement('select');
    selEC.className = 'select-ec';
    EC_OPTIONS.forEach(opt => {
      const elOpt = document.createElement('option');
      elOpt.value = opt.code;
      elOpt.textContent = opt.label;
      if (ans.ec === opt.code) elOpt.selected = true;
      selEC.appendChild(elOpt);
    });
    selEC.addEventListener('change', (e) => setEC(p.paper_id, e.target.value));
    ctrlStrip.appendChild(selEC);

    const noteInp = document.createElement('input');
    noteInp.type = 'text';
    noteInp.className = 'input-note';
    noteInp.placeholder = 'Catatan pertimbangan (opsional)...';
    noteInp.value = ans.note || '';
    noteInp.addEventListener('input', (e) => setNote(p.paper_id, e.target.value));
    ctrlStrip.appendChild(noteInp);

    card.appendChild(ctrlStrip);
    return card;
  }

  function setDecision(paperId, dec) {
    if (!userAnswers[paperId]) userAnswers[paperId] = { decision: '', ec: '', note: '' };
    userAnswers[paperId].decision = dec;
    if (dec === 'Y') userAnswers[paperId].ec = '';
    persistAnswers();
    renderCards();
    showToast(`${paperId}: ${dec}`);
  }

  function setEC(paperId, ec) {
    if (!userAnswers[paperId]) userAnswers[paperId] = { decision: 'N', ec: '', note: '' };
    userAnswers[paperId].ec = ec;
    if (ec && userAnswers[paperId].decision !== 'N') userAnswers[paperId].decision = 'N';
    persistAnswers();
    renderCards();
    showToast(`${paperId} EC: ${ec}`);
  }

  function setNote(paperId, note) {
    if (!userAnswers[paperId]) userAnswers[paperId] = { decision: '', ec: '', note: '' };
    userAnswers[paperId].note = note;
    persistAnswers();
  }

  function copySummary() {
    let lines = [];
    papers.forEach(p => {
      const ans = userAnswers[p.paper_id] || { decision: '-', ec: '-', note: '' };
      const d = ans.decision || '-';
      const ec = ans.ec || '-';
      const n = ans.note ? ' - ' + ans.note : '';
      lines.push(`${p.paper_id} ${d} ${ec}${n}`);
    });
    const txt = lines.join('\n');
    navigator.clipboard.writeText(txt).then(() => {
      showToast(`Rekap ${papers.length} paper disalin!`);
    }).catch(err => {
      prompt('Salin teks rekap berikut:', txt);
    });
  }

  function downloadCSV() {
    let rows = ['No,Paper_ID,Title,Year,Venue,DOI,Decision,EC,Note'];
    papers.forEach(p => {
      const ans = userAnswers[p.paper_id] || { decision: '', ec: '', note: '' };
      const row = [
        p.no,
        p.paper_id,
        escapeCsv(p.title),
        p.year,
        escapeCsv(p.venue),
        escapeCsv(p.doi),
        ans.decision,
        ans.ec,
        escapeCsv(ans.note)
      ];
      rows.push(row.join(','));
    });
    const blob = new Blob([rows.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'L2_pilot_50_adjudication_Schnee.csv';
    a.click();
    URL.revokeObjectURL(url);
    showToast('CSV diunduh');
  }

  function downloadJSON() {
    const payload = {
      adjudicator: 'Schnee',
      timestamp: new Date().toISOString(),
      total_papers: papers.length,
      answers: userAnswers
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'L2_pilot_50_adjudication_Schnee.json';
    a.click();
    URL.revokeObjectURL(url);
    showToast('JSON diunduh');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function escapeCsv(str) {
    if (!str) return '""';
    return `"${String(str).replace(/"/g, '""')}"`;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
