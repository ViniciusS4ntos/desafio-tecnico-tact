const BASE_URL = 'http://localhost:8000/api';

const ENDPOINTS = [
  { key: 'censo',     path: '/censo/',           desc: 'Todos os registros do censo' },
  { key: 'summary',  path: '/summary/',          desc: 'Resumo geral com totais e líderes' },
  { key: 'ranking',  path: '/ranking/',          desc: 'Ranking das regiões por volume' },
  { key: 'heatmap',  path: '/heatmap/',          desc: 'Matriz de calor por faixa etária e região' },
  { key: 'participacao', path: '/participacao/', desc: 'Participação percentual de cada região' },
  { key: 'dominante', path: '/dominante-regiao/',desc: 'Faixa etária dominante por região' },
  { key: 'dashboard', path: '/dashboard/',       desc: 'Consolidado completo de todos os dados' },
];

const REGION_COLORS = {
  'Norte':       'var(--nord)',
  'Nordeste':    'var(--nordeste)',
  'Sudeste':     'var(--sudeste)',
  'Sul':         'var(--sul)',
  'Centro-Oeste':'var(--co)',
};

const cache = {};
let selectedEp = null;

/* ── Fetch ── */
async function fetchEndpoint(key) {
  const ep = ENDPOINTS.find(e => e.key === key);
  setStatus(key, 'loading');
  try {
    const r = await fetch(BASE_URL + ep.path, { signal: AbortSignal.timeout(5000) });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const data = await r.json();
    cache[key] = { data, status: r.status, ok: true };
    setStatus(key, 'ok');
    return data;
  } catch (e) {
    cache[key] = { data: null, status: 0, ok: false, error: e.message };
    setStatus(key, 'err');
    return null;
  }
}

async function loadAll() {
  const btn = document.getElementById('refresh-btn');
  btn.classList.add('spinning');
  const results = await Promise.all(ENDPOINTS.map(ep => fetchEndpoint(ep.key)));
  btn.classList.remove('spinning');

  const summaryData = cache.summary?.data;
  const rankingData = cache.ranking?.data;
  const participacaoData = cache.participacao?.data;
  const heatmapData = cache.heatmap?.data;
  const dominanteData = cache.dominante?.data;

  renderMetrics(summaryData);
  renderRanking(rankingData);
  renderDonut(participacaoData);
  renderHeatmap(heatmapData);
  renderDominante(dominanteData);
  if (selectedEp) renderResponse(selectedEp);

  showToast('Dados atualizados');
}

/* ── Status dots ── */
function setStatus(key, status) {
  document.querySelectorAll(`.status-dot[data-key="${key}"]`).forEach(el => {
    el.className = 'status-dot ' + status;
  });
}

/* ── Nav ── */
function navigate(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('page-' + page).classList.add('active');
  document.querySelector(`.nav-item[data-page="${page}"]`).classList.add('active');
}

/* ── Metrics ── */
function renderMetrics(data) {
  if (!data) return;
  const total = data.totalBrasil || 0;
  const totalStr = total.toLocaleString('pt-BR');
  const totalEl = document.getElementById('m-total');
  totalEl.textContent = totalStr;
  totalEl.className = 'metric-value' + (totalStr.length > 10 ? ' medium' : '');

  const regiao = data.regiaoLider || '—';
  const regiaoEl = document.getElementById('m-regiao');
  regiaoEl.textContent = regiao;
  regiaoEl.className = 'metric-value' + (regiao.length > 10 ? ' small' : '');

  const faixa = data.faixaLider || '—';
  const el = document.getElementById('m-faixa');
  el.textContent = faixa;
  el.className = 'metric-value' + (faixa.length > 12 ? ' small' : faixa.length > 8 ? ' medium' : '');
}

/* ── Ranking bars ── */
function renderRanking(data) {
  const el = document.getElementById('ranking-chart');
  if (!data || !data.length) { el.innerHTML = '<p style="color:var(--muted);font-size:13px;">Sem dados</p>'; return; }
  const max = Math.max(...data.map(d => d.total));
  el.innerHTML = data.map(d => {
    const pct = Math.round((d.total / max) * 100);
    const color = REGION_COLORS[d.regiao] || 'var(--accent)';
    return `<div class="bar-item">
      <div class="bar-header">
        <span class="bar-name">${d.regiao}</span>
        <span class="bar-val">${d.total.toLocaleString('pt-BR')}</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill" style="background:${color};" data-width="${pct}"></div>
      </div>
    </div>`;
  }).join('');
  requestAnimationFrame(() => {
    el.querySelectorAll('.bar-fill').forEach(b => {
      b.style.width = b.dataset.width + '%';
    });
  });
}

/* ── Donut SVG ── */
function renderDonut(data) {
  const el = document.getElementById('donut-wrap');
  if (!data || !data.length) { el.innerHTML = '<p style="color:var(--muted);font-size:13px;">Sem dados</p>'; return; }

  const size = 140, cx = 70, cy = 70, r = 52, stroke = 22;
  const circumference = 2 * Math.PI * r;
  let offset = 0;

  const slices = data.map(d => {
    const color = REGION_COLORS[d.regiao] || '#4f7cff';
    const dashLen = (d.percentual / 100) * circumference;
    const dashGap = circumference - dashLen;
    const rot = (offset / circumference) * 360 - 90;
    offset += dashLen;
    return { color, dashLen, dashGap, rot, ...d };
  });

  const svgSlices = slices.map(s =>
    `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${s.color}"
      stroke-width="${stroke}" stroke-dasharray="${s.dashLen} ${s.dashGap}"
      stroke-dashoffset="0" transform="rotate(${s.rot}, ${cx}, ${cy})"
      style="transition:stroke-dasharray 0.8s"/>`
  ).join('');

  const total = data.reduce((a, b) => a + b.percentual, 0);

  const legend = data.map(d => {
    const color = REGION_COLORS[d.regiao] || '#4f7cff';
    return `<div class="legend-item">
      <span class="legend-dot" style="background:${color}"></span>
      <span class="legend-name">${d.regiao}</span>
      <span class="legend-pct">${d.percentual}%</span>
    </div>`;
  }).join('');

  el.innerHTML = `
    <div class="donut-wrap">
      <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" style="flex-shrink:0;">
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#1a1e28" stroke-width="${stroke}"/>
        ${svgSlices}
        <text x="${cx}" y="${cy}" text-anchor="middle" dy="5" font-size="13" fill="#e8eaf0" font-family="Syne,sans-serif" font-weight="700">100%</text>
      </svg>
      <div class="donut-legend">${legend}</div>
    </div>`;
}

/* ── Heatmap ── */
function renderHeatmap(data) {
  const el = document.getElementById('heatmap-body');
  if (!data || !data.length) { el.innerHTML = '<tr><td colspan="6" style="color:var(--muted);padding:16px;">Sem dados</td></tr>'; return; }

  function pick(d, ...keys) { for (const k of keys) if (d[k] !== undefined) return d[k] || 0; return 0; }
  function getFaixa(d) { return d.faixaEtaria || d.faixa_etaria || d.grupo_idade || '—'; }

  const cols = [
    d => pick(d, 'norte'),
    d => pick(d, 'nordeste'),
    d => pick(d, 'sudeste'),
    d => pick(d, 'sul'),
    d => pick(d, 'centroOeste', 'centro_oeste'),
  ];

  const allVals = data.flatMap(d => cols.map(fn => fn(d)));
  const maxVal = Math.max(...allVals) || 1;

  function heatClass(val) {
    const p = val / maxVal;
    if (p < 0.2) return 'heat-0';
    if (p < 0.4) return 'heat-1';
    if (p < 0.6) return 'heat-2';
    if (p < 0.8) return 'heat-3';
    return 'heat-4';
  }

  el.innerHTML = data.map(d => {
    const vals = cols.map(fn => fn(d));
    return '<tr><td>' + getFaixa(d) + '</td>' +
      vals.map(v => '<td class="' + heatClass(v) + '">' + v.toLocaleString('pt-BR') + '</td>').join('') +
      '</tr>';
  }).join('');
}

/* ── Dominante ── */
function renderDominante(data) {
  const el = document.getElementById('dominante-grid');
  if (!data || !data.length) { el.innerHTML = '<p style="color:var(--muted);font-size:13px;">Sem dados</p>'; return; }
  el.innerHTML = data.map(d => {
    const color = REGION_COLORS[d.regiao] || 'var(--accent)';
    return `<div class="dom-card">
      <div class="dom-regiao">${d.regiao}</div>
      <div class="dom-faixa">${d.faixaDominante || '—'}</div>
      <div class="dom-total">${(d.totalPosses || 0).toLocaleString('pt-BR')} pessoas</div>
      <div class="dom-accent" style="background:${color}"></div>
    </div>`;
  }).join('');
}

/* ── Endpoints page ── */
function buildEndpointsList() {
  const el = document.getElementById('ep-list');
  el.innerHTML = ENDPOINTS.map(ep => `
    <div class="ep-row" data-key="${ep.key}" onclick="selectEndpoint('${ep.key}')">
      <span class="ep-method">GET</span>
      <span class="ep-path">/api${ep.path}</span>
      <span class="ep-desc">${ep.desc}</span>
      <span class="ep-status">
        <span class="status-dot" data-key="${ep.key}"></span>
        <span id="ep-code-${ep.key}" style="font-size:11px;color:var(--muted);font-family:'DM Mono',monospace;">—</span>
      </span>
    </div>
  `).join('');
}

function selectEndpoint(key) {
  selectedEp = key;
  document.querySelectorAll('.ep-row').forEach(r => r.classList.remove('selected'));
  const row = document.querySelector(`.ep-row[data-key="${key}"]`);
  if (row) row.classList.add('selected');
  if (cache[key]) renderResponse(key);
}

function renderResponse(key) {
  const cached = cache[key];
  const panel = document.getElementById('response-panel');
  panel.style.display = 'block';

  const statusEl = document.getElementById('resp-status');
  const bodyEl = document.getElementById('resp-body');
  const epCode = document.getElementById('ep-code-' + key);

  if (!cached) {
    statusEl.textContent = '—';
    bodyEl.textContent = 'Clique em ↺ Atualizar para buscar os dados.';
    return;
  }

  if (!cached.ok) {
    statusEl.style.color = 'var(--red)';
    statusEl.textContent = 'ERRO — ' + cached.error;
    bodyEl.textContent = 'Não foi possível conectar à API.\n\nVerifique se o servidor Django está rodando:\n  python manage.py runserver';
    if (epCode) { epCode.textContent = 'ERR'; epCode.style.color = 'var(--red)'; }
    return;
  }

  statusEl.style.color = 'var(--green)';
  statusEl.textContent = '200 OK';
  if (epCode) { epCode.textContent = '200'; epCode.style.color = 'var(--green)'; }

  const raw = JSON.stringify(cached.data, null, 2);
  bodyEl.innerHTML = syntaxHighlight(raw.slice(0, 2000) + (raw.length > 2000 ? '\n\n}' : ''));
}

function syntaxHighlight(json) {
  return json
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, match => {
      if (/^"/.test(match)) {
        if (/:$/.test(match)) return `<span class="json-key">${match}</span>`;
        return `<span class="json-str">${match}</span>`;
      }
      return `<span class="json-num">${match}</span>`;
    });
}

/* ── Toast ── */
function showToast(msg) {
  const t = document.getElementById('toast');
  t.querySelector('.toast-msg').textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2800);
}

/* ── Init ── */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-item').forEach(n => {
    n.addEventListener('click', () => navigate(n.dataset.page));
  });
  buildEndpointsList();
  loadAll();
});
