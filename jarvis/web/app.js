/* Glass renderer. Mirrors the layouts in panels.py -- same schema, same
   row semantics, different output medium. */

const ZONES = ["status", "main", "side", "rail"];
const grid = document.getElementById("grid");
const shell = document.getElementById("shell");
const conn = document.getElementById("conn");
const clockEl = document.getElementById("clock");

const zoneEls = {};
for (const z of ZONES) {
  const el = document.createElement("div");
  el.className = "zone";
  el.dataset.zone = z;
  grid.appendChild(el);
  zoneEls[z] = el;
}

// Last-rendered panel per zone, so an unchanged panel does not re-animate.
const rendered = {};

/* ------------------------------------------------------------- helpers -- */

const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text != null) n.textContent = text;
  return n;
};

const cell = (row, i) => (i != null && row.length > i && row[i] != null ? String(row[i]) : "");

function relTime(ts) {
  const d = Math.max(0, Math.floor(Date.now() / 1000 - (ts || 0)));
  if (d < 5) return "just now";
  if (d < 60) return `${d}s ago`;
  if (d < 3600) return `${Math.floor(d / 60)}m ago`;
  if (d < 86400) return `${Math.floor(d / 3600)}h ago`;
  return `${Math.floor(d / 86400)}d ago`;
}

/* --------------------------------------------------------------- rows -- */

// [leadIndex, midIndex, tailIndex, statusIndex] -- kept identical to panels.py
const LAYOUT = {
  agenda: [0, 1, 2, 3],
  mail: [0, 1, 2, 3],
  log: [0, 1, null, 2],
  list: [null, 0, 1, 2],
};

function rowNode(type, row) {
  const [li, ci, ri, si] = LAYOUT[type];
  const status = cell(row, si) || "ok";
  const node = el("div", `row s-${status}`);
  if (li != null && cell(row, li)) node.appendChild(el("span", "lead", cell(row, li)));
  node.appendChild(el("span", "mid", cell(row, ci)));
  if (ri != null && cell(row, ri)) node.appendChild(el("span", "tail", cell(row, ri)));
  return node;
}

function bodyNodes(panel) {
  const { type, items } = panel;

  // A working panel is deliberately blank -- the pulsing subtitle carries it.
  if (!items.length) {
    return panel.state === "working" ? [] : [el("div", "empty", "(empty)")];
  }

  if (type === "text") {
    const wrap = el("div", "text");
    for (const row of items) wrap.appendChild(el("p", null, cell(row, 0)));
    return [wrap];
  }

  if (type === "metrics") {
    const wrap = el("div", "metrics");
    for (const row of items) {
      const status = cell(row, 3) || "ok";
      const m = el("div", `metric s-${status}`);
      m.appendChild(el("div", "k", cell(row, 0)));
      const line = el("div", "row2");
      line.appendChild(el("div", "v", cell(row, 1)));
      const delta = cell(row, 2);
      if (delta) {
        const d = el("div", "d", delta);
        if (delta.trim().startsWith("-")) d.dataset.neg = "1";
        line.appendChild(d);
      }
      m.appendChild(line);
      wrap.appendChild(m);
    }
    return [wrap];
  }

  if (type === "table") {
    const table = el("table");
    const thead = el("thead");
    const htr = el("tr");
    for (const h of items[0]) htr.appendChild(el("th", null, String(h)));
    thead.appendChild(htr);
    table.appendChild(thead);
    const tbody = el("tbody");
    for (const row of items.slice(1)) {
      const tr = el("tr");
      for (let i = 0; i < items[0].length; i++) tr.appendChild(el("td", null, cell(row, i)));
      tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    return [table];
  }

  return items.map((row, i) => {
    const n = rowNode(type in LAYOUT ? type : "list", row);
    n.style.animationDelay = `${Math.min(i * 22, 220)}ms`;
    return n;
  });
}

/* -------------------------------------------------------------- panel -- */

function panelNode(panel) {
  const node = el("div", `panel ${panel.state || "ok"}`);
  node.style.setProperty("--accent", `var(--${panel.accent || "cyan"})`);

  const head = el("div", "head");
  head.appendChild(el("span", "title", panel.title || panel.type));
  head.appendChild(el("span", "sub", panel.sub || relTime(panel.ts)));
  node.appendChild(head);

  const body = el("div", "body");
  for (const n of bodyNodes(panel)) body.appendChild(n);
  node.appendChild(body);

  if (panel.note) node.appendChild(el("div", "foot", panel.note));
  return node;
}

// Drop rows that do not fit and say how many were hidden, rather than
// letting the panel scroll.
function trimOverflow(node) {
  const body = node.querySelector(".body");
  if (!body || body.scrollHeight <= body.clientHeight) return;

  const rows = [...body.querySelectorAll(".row, .metric, tbody tr")];
  if (!rows.length) return;

  const more = el("div", "row more");
  body.appendChild(more);

  let hidden = 0;
  while (body.scrollHeight > body.clientHeight && hidden < rows.length) {
    const victim = rows[rows.length - 1 - hidden];
    victim.style.display = "none";
    hidden++;
    more.textContent = `+${hidden} more`;
  }
  if (!hidden) more.remove();
}

function renderZone(zone, panel) {
  const host = zoneEls[zone];
  const key = panel ? JSON.stringify(panel) : null;
  if (rendered[zone] === key) return;
  rendered[zone] = key;

  host.replaceChildren();
  if (!panel) return;

  const node = panelNode(panel);
  host.appendChild(node);
  requestAnimationFrame(() => trimOverflow(node));
}

function render(state) {
  const zones = (state && state.zones) || {};
  for (const z of ZONES) renderZone(z, zones[z] || null);
  shell.classList.toggle("has-panels", ZONES.some((z) => zones[z]));
  // With nothing in the side column, main should span the whole width.
  grid.classList.toggle("solo", !zones.side);
}

/* ------------------------------------------------------------ transport -- */

function setConn(cls, label) {
  conn.className = `conn ${cls}`;
  conn.querySelector(".label").textContent = label;
}

let es = null;
let retry = 500;

function connect() {
  if (es) es.close();
  es = new EventSource("/events");

  es.onopen = () => {
    retry = 500;
    setConn("live", "live");
  };
  es.onmessage = (ev) => {
    try {
      render(JSON.parse(ev.data));
    } catch (err) {
      console.error("bad frame", err);
    }
  };
  es.onerror = () => {
    setConn("down", "reconnecting");
    es.close();
    // Back off to at most 10s so a stopped daemon does not spin the tab.
    setTimeout(connect, retry);
    retry = Math.min(retry * 2, 10000);
  };
}

// Repaint relative timestamps once a minute without a server round trip.
setInterval(() => {
  for (const z of ZONES) {
    const sub = zoneEls[z].querySelector(".sub");
    const key = rendered[z];
    if (!sub || !key) continue;
    const panel = JSON.parse(key);
    if (!panel.sub) sub.textContent = relTime(panel.ts);
  }
}, 60000);

function tickClock() {
  clockEl.textContent = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}
tickClock();
setInterval(tickClock, 1000);

connect();
