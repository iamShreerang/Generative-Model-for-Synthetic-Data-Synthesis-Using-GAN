/* ============================================================
   SynthGen — app.js
   anime.js v4 UMD: anime object exposed as window.anime
   API: anime.animate(), anime.stagger(), anime.timeline(),
        anime.createTimer(), anime.utils.*
   ============================================================ */

const API = 'http://localhost:8000';

/* ─── anime.js v4 UMD: named exports on the global `anime` object ─── */
const { animate, stagger, createTimeline, createMotionPath, createTimer, utils, random: aRandom } = anime;
const timeline = createTimeline; // alias

let selectedFiles = [];
let trainPollId   = null;
let currentPage   = 'home';

/* ════════════════════════════════════════════════════
   ENTRY POINT
   ════════════════════════════════════════════════════ */
window.addEventListener('DOMContentLoaded', () => {
  initCursorGlow();
  initParticles();
  buildNeuralNetwork();
  buildFlowSVG();
  buildCellGrid();
  animateSidebar();
  navigate('home', 0);
  checkAPI();
  setInterval(checkAPI, 8000);
  rippleAll();
});

/* ════════════════════════════════════════════════════
   CURSOR GLOW — follows mouse with anime.js spring lag
   ════════════════════════════════════════════════════ */
function initCursorGlow() {
  const el = document.getElementById('cursor-glow');
  let tx = 0, ty = 0;
  document.addEventListener('mousemove', e => {
    tx = e.clientX; ty = e.clientY;
    animate(el, {
      left: tx, top: ty,
      duration: 1200,
      ease: 'out(4)',
    });
  });
}

/* ════════════════════════════════════════════════════
   PARTICLES — individual div elements, anime.js stagger loops
   ════════════════════════════════════════════════════ */
function initParticles() {
  const wrap = document.getElementById('particles-wrap');
  const COUNT = 70;
  for (let i = 0; i < COUNT; i++) {
    const p = document.createElement('div');
    p.classList.add('particle');
    p.style.left = Math.random() * 100 + 'vw';
    p.style.top  = Math.random() * 100 + 'vh';
    wrap.appendChild(p);
  }

  // Each particle gets its own floating animation
  document.querySelectorAll('.particle').forEach((p, i) => {
    const dur  = 4000 + Math.random() * 8000;
    const dx   = (Math.random() - 0.5) * 200;
    const dy   = (Math.random() - 0.5) * 200;
    animate(p, {
      translateX: [0, dx, 0],
      translateY: [0, dy, 0],
      opacity: [0.1, 0.5, 0.1],
      scale: [0.6, 1.4, 0.6],
      duration: dur,
      delay: i * 60,
      ease: 'inOutSine',
      loop: true,
    });
  });
}

/* ════════════════════════════════════════════════════
   NEURAL NETWORK SVG — built & animated with anime.js
   Showcases: strokeDashoffset draw animation, stagger,
              looping scale pulse, anime.path() motion
   ════════════════════════════════════════════════════ */
function buildNeuralNetwork() {
  const svg = document.getElementById('net-svg');
  const W = 460, H = 240;

  // Layer definitions
  const layers = [
    { n: 4, x: 50,  color: '#7c3aed', label: 'z' },
    { n: 6, x: 160, color: '#6d28d9', label: 'G1' },
    { n: 6, x: 270, color: '#22d3ee', label: 'D1' },
    { n: 3, x: 380, color: '#10b981', label: 'Out' },
  ];

  // Compute node Y positions for each layer
  layers.forEach(l => {
    const spacing = (H - 40) / (l.n - 1 || 1);
    l.ys = Array.from({ length: l.n }, (_, i) => 20 + i * spacing);
  });

  // Draw edges between consecutive layers
  const edgePaths = [];
  for (let li = 0; li < layers.length - 1; li++) {
    const A = layers[li], B = layers[li + 1];
    A.ys.forEach(y1 => {
      B.ys.forEach(y2 => {
        const mx = (A.x + B.x) / 2;
        const d  = `M${A.x},${y1} C${mx},${y1} ${mx},${y2} ${B.x},${y2}`;
        const path = createSVGEl('path', {
          d, class: 'net-edge',
          'data-len': '', id: `ep-${edgePaths.length}`,
        });
        svg.appendChild(path);
        // Set dasharray for draw animation
        const len = path.getTotalLength();
        path.style.strokeDasharray  = len;
        path.style.strokeDashoffset = len;
        edgePaths.push(path);
      });
    });
  }

  // Draw nodes on top of edges
  layers.forEach((l, li) => {
    l.ys.forEach((y, ni) => {
      const cls = li === layers.length - 1 ? 'net-node out'
                : li === 2 ? 'net-node active' : 'net-node';
      const circle = createSVGEl('circle', {
        cx: l.x, cy: y, r: li === layers.length - 1 ? 9 : 6,
        class: cls,
      });
      svg.appendChild(circle);
    });
  });

  // ① DRAW edges in (strokeDashoffset) with stagger
  animate(edgePaths, {
    strokeDashoffset: (el) => [el.style.strokeDashoffset || el.getTotalLength(), 0],
    duration: 1800,
    delay: stagger(18),
    ease: 'inOutCubic',
    complete: () => {
      // ② After edges drawn, pulse nodes
      animate('.net-node', {
        r: (el) => {
          const base = parseFloat(el.getAttribute('r'));
          return [base, base * 1.7, base];
        },
        opacity: [1, 0.6, 1],
        duration: 1800,
        delay: stagger(120, { from: 'center' }),
        ease: 'inOutSine',
        loop: true,
      });

      // ③ Animate "signal" dots along edge paths using anime.path()
      animateSignals(layers, edgePaths);
    }
  });
}

function animateSignals(layers, edgePaths) {
  // Create signal circles and animate along paths
  const svg = document.getElementById('net-svg');
  const signals = [];

  // Pick a subset of edges to animate signals on (every 3rd edge)
  edgePaths.forEach((path, idx) => {
    if (idx % 4 !== 0) return;
    const dot = createSVGEl('circle', { r: 2.5, class: 'net-signal', opacity: 0 });
    svg.appendChild(dot);
    signals.push({ dot, path });
  });

  // Use anime.path() to follow each path
  signals.forEach(({ dot, path }, i) => {
    try {
      const motionPath = createMotionPath(path);
      animate(dot, {
        x: motionPath('x'),
        y: motionPath('y'),
        opacity: [0, 1, 1, 0],
        duration: 1200,
        delay: i * 180 + Math.random() * 600,
        ease: 'linear',
        loop: true,
      });
    } catch(e) {
      // motionPath not supported in this context, skip
    }
  });
}

/* ════════════════════════════════════════════════════
   FLOW SVG — training page mini-network
   ════════════════════════════════════════════════════ */
function buildFlowSVG() {
  const svg = document.getElementById('flow-svg');
  if (!svg) return;
  const nodes = [
    { x: 30, y: 40 }, { x: 90, y: 25 }, { x: 90, y: 55 },
    { x: 150, y: 40 }, { x: 210, y: 25 }, { x: 210, y: 55 },
    { x: 270, y: 40 },
  ];
  const edges = [[0,1],[0,2],[1,3],[2,3],[3,4],[3,5],[4,6],[5,6]];

  edges.forEach(([a,b]) => {
    const el = createSVGEl('line', {
      x1: nodes[a].x, y1: nodes[a].y, x2: nodes[b].x, y2: nodes[b].y,
      class: 'flow-edge',
    });
    svg.appendChild(el);
  });
  nodes.forEach(n => {
    const el = createSVGEl('circle', { cx: n.x, cy: n.y, r: 7, class: 'flow-node' });
    svg.appendChild(el);
  });

  // Animate flow nodes continuously
  animate('.flow-node', {
    opacity: [0.4, 1, 0.4],
    r: [7, 10, 7],
    duration: 1200,
    delay: stagger(140),
    ease: 'inOutSine',
    loop: true,
  });
}

/* ════════════════════════════════════════════════════
   CELL GRID — stagger ripple from center
   Showcases: anime.stagger with grid + from:'center'
   ════════════════════════════════════════════════════ */
function buildCellGrid() {
  const grid = document.getElementById('cell-grid');
  if (!grid) return;
  const COLS = 16, ROWS = 4;
  for (let i = 0; i < COLS * ROWS; i++) {
    const c = document.createElement('div');
    c.classList.add('cell');
    grid.appendChild(c);
  }
  triggerGridRipple();
  setInterval(triggerGridRipple, 6000);
}

function triggerGridRipple() {
  const cells = document.querySelectorAll('.cell');
  if (!cells.length) return;
  animate(cells, {
    backgroundColor: [
      'rgba(255,255,255,0.025)',
      'rgba(124,58,237,0.45)',
      'rgba(34,211,238,0.2)',
      'rgba(255,255,255,0.025)',
    ],
    borderColor: [
      'rgba(255,255,255,0.03)',
      'rgba(124,58,237,0.7)',
      'rgba(34,211,238,0.3)',
      'rgba(255,255,255,0.03)',
    ],
    duration: 1400,
    delay: stagger(55, { grid: [16, 4], from: 'center' }),
    ease: 'out(3)',
  });
}

/* ════════════════════════════════════════════════════
   SIDEBAR ENTRANCE
   Showcases: timeline() with chained animations
   ════════════════════════════════════════════════════ */
function animateSidebar() {
  const tl = timeline({ defaults: { ease: 'out(3)' } });
  tl.add('.sidebar', { translateX: [-30, 0], opacity: [0, 1], duration: 500 })
    .add('.logo-wrap', { opacity: [0, 1], translateY: [-10, 0], duration: 300 }, '-=200')
    .add('.nav-item', { opacity: [0, 1], translateX: [-16, 0], duration: 280, delay: stagger(55) }, '-=100');
}

/* ════════════════════════════════════════════════════
   NAVIGATION
   Showcases: spring easing for sidebar indicator,
              timeline for page transition
   ════════════════════════════════════════════════════ */
function navigate(page, idx) {
  if (page === currentPage && document.getElementById(`page-${page}`).classList.contains('active')) {
    // still run page-specific init
  }
  currentPage = page;

  // Update nav items
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  const navEl = document.querySelector(`[data-page="${page}"]`);
  if (navEl) navEl.classList.add('active');

  // Slide sidebar indicator with spring physics
  const indicatorTop = 92 + (idx || 0) * 46;
  animate('#sidebar-indicator', {
    top: indicatorTop,
    duration: 500,
    ease: 'spring(1, 100, 12, 0)',
  });

  // Hide all pages
  document.querySelectorAll('.page').forEach(p => {
    p.classList.remove('active');
    p.style.display = 'none';
  });

  const target = document.getElementById(`page-${page}`);
  target.style.display = 'block';
  target.classList.add('active');

  // Page transition timeline
  const tl = createTimeline({ defaults: { ease: 'out(3)' } });
  tl.add(target, { opacity: [0, 1], translateY: [24, 0], duration: 350 })
    .add(`#page-${page} .card`, {
      opacity: [0, 1], translateY: [18, 0],
      duration: 320, delay: stagger(70),
    }, '-=180');

  // Page-specific initialisation
  if (page === 'home') initHomePage();
  if (page === 'dataset') loadDatasets();
  if (page === 'training') { pollTraining(); buildFlowSVG(); }
  if (page === 'generate') loadModels();
  if (page === 'evaluation') animateEvalRings();
}
window.navigate = navigate;

/* ════════════════════════════════════════════════════
   HOME PAGE INIT
   ════════════════════════════════════════════════════ */
function initHomePage() {
  animateHeroTitle();
  updateHomeStats();
  // Entrance animation for stats bar
  animate('#stats-bar', { opacity: [0, 1], translateY: [16, 0], duration: 500, ease: 'out(3)', delay: 400 });
}

/* Hero title — character-by-character with stagger
   Showcases: splitting text + stagger per character */
function animateHeroTitle() {
  const title = document.getElementById('hero-title');
  const text  = 'Synthetic\nIntelligence';
  title.innerHTML = '';
  text.split('').forEach(ch => {
    if (ch === '\n') { title.appendChild(document.createElement('br')); return; }
    const span = document.createElement('span');
    span.classList.add('char');
    if (ch === ' ') span.classList.add('space');
    span.textContent = ch;
    title.appendChild(span);
  });
  animate('.char', {
    opacity: [0, 1],
    translateY: [30, 0],
    rotateX: [-90, 0],
    duration: 700,
    delay: stagger(35, { start: 300 }),
    ease: 'out(4)',
  });
}

async function updateHomeStats() {
  try {
    const ds = await apiGet('/datasets/');
    countUp('sb-datasets', ds.datasets.length);
  } catch {}
  try {
    const ms = await apiGet('/models/');
    countUp('sb-models', ms.models.length);
  } catch {}
}

/* Count-up using anime.js — showcases object property animation */
function countUp(id, target) {
  const el = document.getElementById(id);
  const obj = { val: 0 };
  animate(obj, {
    val: target,
    duration: 1200,
    ease: 'out(3)',
    onUpdate: () => { el.textContent = Math.round(obj.val); },
  });
}

/* ════════════════════════════════════════════════════
   API STATUS
   ════════════════════════════════════════════════════ */
async function checkAPI() {
  const dot  = document.getElementById('api-dot');
  const text = document.getElementById('api-text');
  const sb   = document.getElementById('sb-api');
  try {
    await apiGet('/');
    dot.className  = 'api-dot online';
    text.textContent = 'API Online';
    if (sb) sb.textContent = 'Online';
  } catch {
    dot.className  = 'api-dot offline';
    text.textContent = 'API Offline';
    if (sb) sb.textContent = 'Offline';
  }
}

/* ════════════════════════════════════════════════════
   DATASET PAGE
   ════════════════════════════════════════════════════ */
window.handleDragOver  = e => { e.preventDefault(); e.currentTarget.classList.add('over'); };
window.handleDragLeave = e => e.currentTarget.classList.remove('over');
window.handleDrop = e => {
  e.preventDefault();
  e.currentTarget.classList.remove('over');
  addFiles(Array.from(e.dataTransfer.files).filter(f => /\.(jpg|jpeg|png)$/i.test(f.name)));
};
window.handleFileSelect = e => addFiles(Array.from(e.target.files));

function addFiles(files) {
  selectedFiles = [...selectedFiles, ...files];
  renderChips();
}

function renderChips() {
  const row = document.getElementById('file-chips');
  row.innerHTML = selectedFiles.map(f => `<span class="chip">${f.name}</span>`).join('');
  animate('.chip', { opacity: [0,1], scale: [0.7,1], duration: 260, delay: stagger(25), ease: 'out(4)' });
}

async function uploadDataset() {
  const name = document.getElementById('ds-name').value.trim();
  const btn  = document.getElementById('upload-btn');
  if (!name) { toast('Enter a dataset name', 'err'); return; }
  if (!selectedFiles.length) { toast('Select files first', 'err'); return; }
  btn.disabled = true;
  showMsg('upload-msg', 'Uploading…', 'info');
  const fd = new FormData();
  selectedFiles.forEach(f => fd.append('files', f));
  try {
    const res = await apiPost(`/upload-dataset/?dataset_name=${encodeURIComponent(name)}`, fd, true);
    showMsg('upload-msg', `✓ ${res.message}`, 'ok');
    toast(`Uploaded ${selectedFiles.length} images`, 'ok');
    selectedFiles = [];
    renderChips();
    loadDatasets();
  } catch(e) {
    showMsg('upload-msg', `Error: ${e.message}`, 'err');
    toast('Upload failed', 'err');
  } finally { btn.disabled = false; }
}
window.uploadDataset = uploadDataset;

async function loadDatasets() {
  const el = document.getElementById('ds-list');
  el.innerHTML = '<div style="height:60px" class="loading-shimmer"></div>';
  try {
    const data = await apiGet('/datasets/');
    if (!data.datasets.length) {
      el.innerHTML = '<div class="empty-s"><span>◈</span><p>No datasets yet</p></div>';
      return;
    }
    el.innerHTML = data.datasets.map(ds => `
      <div class="ds-item">
        <div><div class="ds-name">${ds.name}</div><div class="ds-meta">${ds.image_count} images</div></div>
        <span class="ds-badge">${ds.image_count}</span>
      </div>`).join('');
    animate('.ds-item', { opacity:[0,1], translateX:[-14,0], duration:300, delay:stagger(60), ease:'out(3)' });
  } catch {
    el.innerHTML = '<div class="empty-s"><span>⚠</span><p>Cannot reach API</p></div>';
  }
}
window.loadDatasets = loadDatasets;

/* ════════════════════════════════════════════════════
   TRAINING PAGE
   Showcases: training ring spin (CSS + anime.js class toggle),
              smooth progress-bar anime
   ════════════════════════════════════════════════════ */
window.setToggle = (btn, fieldId, val) => {
  const parent = btn.closest('.fg');
  parent.querySelectorAll('.tog').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(fieldId).value = val;
};

async function startTraining() {
  const btn = document.getElementById('tr-btn');
  btn.disabled = true;
  showMsg('tr-msg', 'Starting training…', 'info');
  const config = {
    dataset_name: document.getElementById('tr-dataset').value.trim(),
    epochs:       parseInt(document.getElementById('tr-epochs').value),
    batch_size:   parseInt(document.getElementById('tr-batch').value),
    learning_rate:parseFloat(document.getElementById('tr-lr').value),
    image_size:   parseInt(document.getElementById('tr-size').value),
  };
  try {
    await apiPost('/train/', config);
    showMsg('tr-msg', '✓ Training started!', 'ok');
    toast('Training started!', 'ok');
    pollTraining();
  } catch(e) {
    showMsg('tr-msg', `Error: ${e.message}`, 'err');
    toast(e.message, 'err');
  } finally { btn.disabled = false; }
}
window.startTraining = startTraining;

async function pollTraining() {
  if (trainPollId) clearTimeout(trainPollId);
  try {
    const s   = await apiGet('/training-status/');
    const ring = document.getElementById('tr-ring');
    const txt  = document.getElementById('tr-state-txt');
    if (s.is_training) {
      ring.classList.add('spin');
      txt.textContent = 'Training in progress…';
      txt.style.color = '#a78bfa';
    } else {
      ring.classList.remove('spin');
      txt.textContent = 'Idle — waiting to train';
      txt.style.color = '';
    }
    document.getElementById('m-ep').textContent = `${s.current_epoch}/${s.total_epochs}`;
    document.getElementById('m-gl').textContent = s.gen_loss.toFixed(4);
    document.getElementById('m-dl').textContent = s.disc_loss.toFixed(4);
    const pct = s.total_epochs > 0 ? (s.current_epoch / s.total_epochs) * 100 : 0;
    document.getElementById('prog-fill').style.width  = `${pct}%`;
    document.getElementById('prog-label').textContent = `${Math.round(pct)}%`;
    if (s.is_training) trainPollId = setTimeout(pollTraining, 2000);
  } catch {}
}

/* ════════════════════════════════════════════════════
   GENERATE PAGE
   ════════════════════════════════════════════════════ */
async function loadModels() {
  const sel = document.getElementById('model-sel');
  sel.innerHTML = '<option>Loading…</option>';
  try {
    const data = await apiGet('/models/');
    if (!data.models.length) {
      sel.innerHTML = '<option value="">No trained models</option>';
    } else {
      sel.innerHTML = data.models.map(m => `<option value="${m.path}">${m.name}</option>`).join('');
    }
  } catch { sel.innerHTML = '<option value="">Cannot reach API</option>'; }
}
window.loadModels = loadModels;

async function generateImages() {
  const btn  = document.getElementById('gen-btn');
  const path = document.getElementById('model-sel').value;
  const n    = parseInt(document.getElementById('num-samples').value);
  if (!path) { toast('Select a model first', 'err'); return; }
  btn.disabled = true;
  showMsg('gen-msg', 'Generating images…', 'info');
  try {
    const res = await apiPost('/generate/', { num_samples: n, model_path: path });
    showMsg('gen-msg', `✓ ${res.message}`, 'ok');
    toast('Images generated!', 'ok');
    showGalleryPlaceholders(n);
  } catch(e) {
    showMsg('gen-msg', `Error: ${e.message}`, 'err');
    toast(e.message, 'err');
  } finally { btn.disabled = false; }
}
window.generateImages = generateImages;

function showGalleryPlaceholders(n) {
  const g = document.getElementById('gallery');
  g.innerHTML = Array.from({ length: Math.min(n, 16) }).map(() =>
    `<div class="gal-img" style="background:linear-gradient(135deg,rgba(124,58,237,.15),rgba(34,211,238,.1));"></div>`
  ).join('');
  // Stagger entrance with spring from center
  animate('.gal-img', {
    opacity: [0, 1], scale: [0.5, 1],
    duration: 500,
    delay: stagger(40, { from: 'center' }),
    ease: 'spring(1, 80, 12, 0)',
  });
}

/* ════════════════════════════════════════════════════
   EVALUATION PAGE
   Showcases: SVG strokeDashoffset ring animation
              triggered on page enter
   ════════════════════════════════════════════════════ */
function animateEvalRings() {
  const circumference = 2 * Math.PI * 24; // r=24
  // Animate rings decoratively
  ['er-fid','er-ssim','er-psnr'].forEach((id, i) => {
    const el = document.getElementById(id);
    if (!el) return;
    animate(el, {
      strokeDashoffset: [circumference, circumference * 0.3],
      duration: 1400,
      delay: i * 200,
      ease: 'out(3)',
    });
  });
  // Animate eval card entrance
  animate('.eval-card', {
    opacity: [0, 1], translateY: [30, 0], scale: [0.92, 1],
    duration: 500, delay: stagger(120, { from: 'center' }), ease: 'out(4)',
  });
}

async function calcMetrics() {
  const btn = document.getElementById('ev-btn');
  btn.disabled = true;
  showMsg('ev-msg', 'Metrics require a /evaluate/ API endpoint. Add it to FastAPI to enable full evaluation.', 'info');
  // Demo: animate some fake values to showcase number animation
  animateMetricVal('ev-fid',  '—', '47.3');
  animateMetricVal('ev-ssim', '—', '0.81');
  animateMetricVal('ev-psnr', '—', '22.6');
  btn.disabled = false;
}
window.calcMetrics = calcMetrics;

function animateMetricVal(id, from, to) {
  const el = document.getElementById(id);
  const obj = { v: 0 };
  const target = parseFloat(to);
  animate(obj, {
    v: target, duration: 1600, ease: 'out(3)',
    onUpdate: () => { el.textContent = obj.v.toFixed(2); },
  });
}

/* ════════════════════════════════════════════════════
   RIPPLE EFFECT on buttons
   Showcases: scale from click position with anime.js
   ════════════════════════════════════════════════════ */
function rippleAll() {
  document.addEventListener('click', e => {
    const btn = e.target.closest('.ripple-btn');
    if (!btn) return;
    const rect = btn.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height) * 2;
    const x    = e.clientX - rect.left - size / 2;
    const y    = e.clientY - rect.top  - size / 2;
    const el   = document.createElement('div');
    el.classList.add('ripple-circle');
    el.style.cssText = `width:${size}px;height:${size}px;left:${x}px;top:${y}px;`;
    btn.appendChild(el);
    animate(el, {
      scale: [0, 1], opacity: [0.35, 0],
      duration: 600, ease: 'out(2)',
      complete: () => el.remove(),
    });
  });
}

/* ════════════════════════════════════════════════════
   TOAST NOTIFICATIONS
   ════════════════════════════════════════════════════ */
let toastTimer = null;
function toast(msg, type = 'info') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = `toast ${type} show`;
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.classList.remove('show'); }, 3200);
}

/* ════════════════════════════════════════════════════
   MESSAGES
   ════════════════════════════════════════════════════ */
function showMsg(containerId, text, type) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `<div class="msg ${type}">${text}</div>`;
  animate(el.firstChild, { opacity:[0,1], translateY:[6,0], duration:280, ease:'out(3)' });
}

/* ════════════════════════════════════════════════════
   API HELPERS
   ════════════════════════════════════════════════════ */
async function apiGet(path) {
  const r = await fetch(`${API}${path}`);
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}
async function apiPost(path, body, isForm = false) {
  const opts = { method: 'POST' };
  if (isForm) { opts.body = body; }
  else { opts.headers = { 'Content-Type': 'application/json' }; opts.body = JSON.stringify(body); }
  const r = await fetch(`${API}${path}`, opts);
  const d = await r.json();
  if (!r.ok) throw new Error(d.detail || `HTTP ${r.status}`);
  return d;
}

/* ════════════════════════════════════════════════════
   SVG HELPER
   ════════════════════════════════════════════════════ */
function createSVGEl(tag, attrs = {}) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
  return el;
}
