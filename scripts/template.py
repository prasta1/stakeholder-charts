# Stakeholder Map HTML Template
# Uses html_format() (string replacement) instead of .format()
# So CSS braces can be normal {{ }} — NOT escaped

HTML_TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{account_name} Stakeholder Map</title>
<style>
  :root {
    --bg: #050b14;
    --card: rgba(15,23,42,0.6);
    --card-border: #1f2937;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --heading: #f8fafc;
    --high: #f59e0b;
    --medium: #34d399;
    --low: #60a5fa;
    --rel-ally: #22c55e;
    --rel-warm: #f59e0b;
    --rel-neutral: #64748b;
    --rel-blocker: #ef4444;
    --rel-marketing: #a855f7;
    --group-bg: rgba(30,41,59,0.3);
  }
  * { box-sizing: border-box; }
  html,body {
    margin:0; padding:0;
    background: radial-gradient(1200px 800px at 10% -10%, #0b1d33 0%, transparent 60%),
                radial-gradient(900px 600px at 110% 10%, #0d1f2d 0%, transparent 55%),
                var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    min-height: 100vh;
  }
  .wrap {
    max-width: 1280px;
    margin: 0 auto;
    padding: 28px 24px 40px;
  }
  header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
  }
  header .dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    background: #22d3ee;
    box-shadow: 0 0 12px #22d3aa;
    animation: pulse 2.2s infinite;
  }
  @keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50% { opacity: .75; transform: scale(1.15); }
  }
  header h1 {
    margin: 0;
    font-size: 22px;
    font-weight: 600;
    letter-spacing: 0.2px;
  }
  header p {
    margin: 4px 0 0;
    color: var(--muted);
    font-size: 13px;
  }
  .controls {
    display: flex;
    gap: 12px;
    margin: 14px 0 18px;
  }
  .controls #search {
    flex: 1;
    padding: 8px 14px;
    border-radius: 8px;
    border: 1px solid var(--card-border);
    background: rgba(15,23,42,0.4);
    color: var(--text);
    font-size: 13px;
    outline: none;
  }
  .controls #search:focus {
    border-color: #22d3ee;
  }
  .controls #filter-rel {
    padding: 8px 14px;
    border-radius: 8px;
    border: 1px solid var(--card-border);
    background: rgba(15,23,42,0.4);
    color: var(--text);
    font-size: 13px;
    outline: none;
    cursor: pointer;
  }
  .legend {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin: 10px 0 18px;
    font-size: 12px;
  }
  .legend .pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    border-radius: 999px;
    background: var(--card);
    border: 1px solid var(--card-border);
  }
  .legend .swatch {
    width: 10px; height: 10px;
    border-radius: 2px;
  }
  .legend .swatch.rel {
    width: 10px; height: 10px;
    border-radius: 50%;
  }
  .stage {
    background: linear-gradient(180deg, rgba(15,23,42,0.4) 0%, rgba(15,23,42,0.2) 100%);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 18px;
    backdrop-filter: blur(4px);
  }
  .row {
    margin-bottom: 18px;
  }
  .row:last-child {
    margin-bottom: 0;
  }
  .row .label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: var(--muted);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .row .label::before {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--card-border);
  }
  .node-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }
  .node {
    background: var(--card);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 12px 14px;
    transition: all 0.2s ease;
    cursor: default;
  }
  .node:hover {
    border-color: #22d3ee;
    box-shadow: 0 0 0 2px rgba(34,211,238,0.15);
    transform: translateY(-2px);
  }
  .node-inner {
    display: flex;
    flex-direction: column;
  }
  .node .name {
    font-size: 14px;
    font-weight: 600;
    color: var(--heading);
    margin-bottom: 2px;
  }
  .node .role {
    font-size: 12px;
    color: var(--muted);
    margin-bottom: 8px;
  }
  .node .meta {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }
  .node .badge {
    padding: 3px 8px;
    border-radius: 999px;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }
  .node .badge-outline {
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--card-border);
    color: var(--muted);
  }
  .node .rel-ally { background: rgba(34,197,94,0.2); color: var(--rel-ally); }
  .node .rel-warm { background: rgba(245,158,1,0.2); color: var(--rel-warm); }
  .node .rel-neutral { background: rgba(100,116,139,0.2); color: var(--rel-neutral); }
  .node .rel-blocker { background: rgba(239,68,68,0.2); color: var(--rel-blocker); }
  .node .rel-marketing { background: rgba(168,85,247,0.2); color: var(--rel-marketing); }
  .group {
    background: var(--group-bg);
    border: 1px dashed var(--card-border);
    border-radius: 14px;
    padding: 14px;
    margin-top: 10px;
  }
  .group h4 {
    margin: 0 0 12px;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.1px;
    color: var(--muted);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .group h4::before {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--card-border);
  }
  footer {
    margin-top: 18px;
    color: var(--muted);
    font-size: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .tooltip {
    position: fixed;
    pointer-events: none;
    background: rgba(15,23,42,0.95);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 11px;
    color: var(--text);
    max-width: 240px;
    backdrop-filter: blur(8px);
    z-index: 9999;
    opacity: 0;
    transition: opacity 0.15s ease;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
  }
  .tooltip.show {
    opacity: 1;
  }
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="dot" aria-hidden="true"></div>
      <div>
        <h1>{account_name} Stakeholder Map</h1>
        <p>Customer contacts — influence, relationship, and activity snapshots</p>
      </div>
    </header>

    <div class="controls">
      <input type="text" id="search" placeholder="Search contacts by name or role…" />
      <select id="filter-rel">
        <option value="all">All Relationships</option>
        <option value="Ally">Allies</option>
        <option value="Blocker">Blockers</option>
        <option value="Warm">Warm</option>
        <option value="Marketing">Marketing</option>
        <option value="Neutral">Neutral</option>
      </select>
    </div>

    <div class="legend">
      <div class="pill"><span class="swatch" style="background:var(--high)"></span>High influence</div>
      <div class="pill"><span class="swatch" style="background:var(--medium)"></span>Medium influence</div>
      <div class="pill"><span class="swatch" style="background:var(--low)"></span>Low influence</div>
      <div class="pill"><span class="swatch rel" style="background:var(--rel-ally)"></span>Ally</div>
      <div class="pill"><span class="swatch rel" style="background:var(--rel-warm)"></span>Warm</div>
      <div class="pill"><span class="swatch rel" style="background:var(--rel-neutral)"></span>Neutral</div>
      <div class="pill"><span class="swatch rel" style="background:var(--rel-blocker)"></span>Blocker</div>
      <div class="pill"><span class="swatch rel" style="background:var(--rel-marketing)"></span>Marketing</div>
    </div>

    <div class="stage">
{rows_html}
    </div>

    <div class="tooltip" id="tooltip"></div>

    <footer>
      <span>{account_display}</span>
      <span>{contact_count} active contacts</span>
    </footer>
  </div>

  <script>
    // Client-side search + filter
    const searchInput = document.getElementById('search');
    const filterSelect = document.getElementById('filter-rel');
    const nodes = document.querySelectorAll('.node');
    const tooltip = document.getElementById('tooltip');

    function filterNodes() {
      const searchTerm = searchInput.value.toLowerCase();
      const relFilter = filterSelect.value;

      nodes.forEach(node => {
        const name = node.dataset.name.toLowerCase();
        const role = node.dataset.role.toLowerCase();
        const rel = node.dataset.rel;
        const matchesSearch = name.includes(searchTerm) || role.includes(searchTerm);
        const matchesRel = relFilter === 'all' || rel === relFilter;
        node.style.display = (matchesSearch && matchesRel) ? '' : 'none';
      });
    }

    searchInput.addEventListener('input', filterNodes);
    filterSelect.addEventListener('change', filterNodes);

    // Tooltip on hover
    document.addEventListener('mousemove', (e) => {
      const node = e.target.closest('.node');
      if (!node) { tooltip.classList.remove('show'); return; }
      const notes = node.querySelector('.name').title;
      if (!notes) { tooltip.classList.remove('show'); return; }
      tooltip.textContent = notes;
      tooltip.style.left = (e.clientX + 14) + 'px';
      tooltip.style.top = (e.clientY + 14) + 'px';
      tooltip.classList.add('show');
    });

    document.addEventListener('mouseleave', (e) => {
      if (!e.relatedTarget || !e.relatedTarget.closest('.node')) {
        tooltip.classList.remove('show');
      }
    });
  </script>
</body>
</html>'''