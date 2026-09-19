#!/usr/bin/env python3
"""
Portfolio site generator.

Edit the PROJECTS list below (text, order, stats), then run:

    python build.py

It rewrites index.html and every projects/<slug>/index.html.
Videos and PDFs are plain files, so nothing else needs building.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent

# ---------------------------------------------------------------------------
# Personal info (shown in header/footer). Edit freely.
# ---------------------------------------------------------------------------
OWNER = {
    "name": "Mohammed Jamir Uddin",
    "title": "Full-Stack Software Developer · .NET Core & React",
    "email": "jamiruddindowlat@gmail.com",
    "phone": "+880 1715-487122",
    "location": "Chattogram, Bangladesh",
    "site_title": "Mohammed Jamir Uddin — Project Portfolio",
}

# ---------------------------------------------------------------------------
# Projects. Only facts taken from the PDFs. Order here = order on the site.
# ---------------------------------------------------------------------------
PROJECTS = [
    {
        "slug": "iums",
        "name": "Sinan International University Management System",
        "short": "IUMS",
        "tagline": "Full-stack ERP for higher-education institutions.",
        "description": (
            "A complete, full-stack Enterprise Resource Planning (ERP) platform for "
            "higher-education institutions — academics, admissions, examinations, human "
            "resources, accounting & finance, procurement, biometric attendance, and "
            "institutional communication, unified in a single secure system."
        ),
        "backend": "ASP.NET Core Web API (.NET 8) · Entity Framework Core · Microsoft SQL Server · "
                   "JWT Bearer & WebAuthn/FIDO2 Biometric Auth · BCrypt · Swagger/OpenAPI",
        "frontend": "React 18 · Vite · React Router · Recharts · React Big Calendar · jsPDF · ExcelJS · Axios",
        "stats": [("20", "Functional modules"), ("263+", "Screens documented"), ("7", "Role-based portals")],
        "pdf_pages": 124,
    },
    {
        "slug": "hms",
        "name": "Sayan Hospital Management System",
        "short": "HMS",
        "tagline": "Enterprise healthcare platform covering the entire hospital lifecycle.",
        "description": (
            "A complete, full-stack Hospital Management platform covering the entire hospital "
            "lifecycle — patient intake, doctor scheduling, appointments and admissions, medical "
            "records, nursing and ward management, pharmacy, lab and radiology, inventory, "
            "accounts and billing, HR and payroll, and management reporting, unified in a "
            "single secure system."
        ),
        "backend": "ASP.NET Core Web API (.NET 10) · Entity Framework Core · Microsoft SQL Server · "
                   "JWT Authentication · FluentValidation · Role-Based Access Control (RBAC) · Swagger/OpenAPI",
        "frontend": "React 18 · Vite · React Router · Recharts · jsPDF · ExcelJS · Axios · Bilingual (English / Bangla) UI",
        "stats": [("15+", "Functional modules"), ("50+", "Screens documented"), ("5", "Role-based portals")],
        "pdf_pages": 74,
    },
    {
        "slug": "iaps",
        "name": "Ainan International Auto Parts System",
        "short": "IAPS",
        "tagline": "Point-of-Sale & ERP platform for auto parts businesses.",
        "description": (
            "A complete, full-stack Point-of-Sale & ERP platform built for auto parts retailers, "
            "wholesalers and importers — inventory, sales, purchasing, multi-warehouse stock, "
            "customer & supplier ledgers, and full double-entry bookkeeping, unified in one system."
        ),
        "backend": "ASP.NET Core Web API (.NET 8) · Entity Framework Core · Microsoft SQL Server · "
                   "JWT Authentication · BCrypt · Swagger/OpenAPI",
        "frontend": "React 18 · Vite · React Router · Recharts · Axios",
        "modules": "POS · Inventory · Sales · Purchasing · Accounting · Multi-Warehouse · Reporting",
        "stats": [],
        "pdf_pages": 27,
    },
    {
        "slug": "ecommerce",
        "name": "Safiyan International ECommerce System (SIES)",
        "short": "SIES",
        "tagline": "Daraz-style multi-vendor e-commerce marketplace.",
        "description": (
            "A full-stack, Daraz-style multi-vendor e-commerce marketplace built with ASP.NET Core "
            "Web API, Entity Framework Core (SQL Server), and React + Vite. Features real payment "
            "gateways (SSLCommerz & Stripe), a validated order pipeline, commission engine, "
            "PDF/Excel exports, and 3 role-based portals."
        ),
        "backend": "ASP.NET Core Web API (.NET 8) · Entity Framework Core · SQL Server · "
                   "SSLCommerz (session + IPN validation) · Stripe (PaymentIntent + HMAC webhook) · "
                   "Cash on Delivery · JWT Bearer · RBAC (Admin / Vendor / Customer)",
        "frontend": "React 18 · Vite · Context API (Auth / Cart / Wishlist) · Axios",
        "stats": [("87", "Screenshots"), ("15+", "API controllers"), ("9", "Admin modules"), ("3", "Role portals")],
        "pdf_pages": 88,
    },
]

# Video durations are read at build time if ffprobe is available (optional).
def video_minutes(slug):
    import subprocess
    f = ROOT / "projects" / slug / "demo.mp4"
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
            text=True, stderr=subprocess.DEVNULL).strip()
        s = int(float(out))
        return f"{s // 60}:{s % 60:02d}"
    except Exception:
        return None


def file_mb(path):
    try:
        return f"{path.stat().st_size / 1_048_576:.1f} MB"
    except FileNotFoundError:
        return ""


# ---------------------------------------------------------------------------
# Shared HTML pieces
# ---------------------------------------------------------------------------
THEME_JS = """
<script>
(function(){
  var t = localStorage.getItem('theme');
  if (t) document.documentElement.setAttribute('data-theme', t);
})();
function toggleTheme(){
  var cur = document.documentElement.getAttribute('data-theme');
  var dark = cur ? cur === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
  var next = dark ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  try { localStorage.setItem('theme', next); } catch(e){}
}
</script>
"""


def head(title, desc, base):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<link rel="stylesheet" href="{base}assets/style.css">
{THEME_JS}
</head>
"""


def topbar(base, current=None):
    links = "".join(
        f'<a href="{base}projects/{p["slug"]}/">{escape(p["short"])}</a>' for p in PROJECTS
    )
    return f"""<header class="topbar"><div class="wrap">
  <a class="brand" href="{base}">{escape(OWNER["name"])}</a>
  <nav class="nav">{links}<button type="button" onclick="toggleTheme()" aria-label="Toggle dark mode">◐</button></nav>
</div></header>"""


def footer():
    return f"""<footer class="foot"><div class="wrap">
  <div>{escape(OWNER["name"])} · {escape(OWNER["title"])}</div>
  <div><a href="mailto:{OWNER["email"]}">{OWNER["email"]}</a> · {OWNER["phone"]} · {escape(OWNER["location"])}</div>
</div></footer>"""


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------
def card(p):
    base = "projects/" + p["slug"] + "/"
    mins = video_minutes(p["slug"])
    stats = "".join(f"<span><b>{escape(n)}</b> {escape(l.lower())}</span>" for n, l in p["stats"][:3])
    dur = f'<span class="chip" style="position:absolute;right:10px;bottom:10px;background:rgba(0,0,0,.7);color:#fff;border:0">{mins}</span>' if mins else ""
    return f"""
<article class="card" id="{p["slug"]}">
  <a class="thumb" href="{base}" aria-label="Open {escape(p["short"])} project">
    <img src="{base}poster.jpg" alt="{escape(p["name"])} video preview" loading="lazy">
    <div class="play"><span>▶</span></div>{dur}
  </a>
  <div class="body">
    <h3><a href="{base}">{escape(p["name"])}</a></h3>
    <p>{escape(p["tagline"])}</p>
    <div class="stats">{stats}</div>
    <div class="actions">
      <a class="btn primary" href="{base}#video">▶ Watch video</a>
      <a class="btn" href="{base}#pdf">📄 View PDF</a>
    </div>
  </div>
</article>"""


def build_home():
    cards = "".join(card(p) for p in PROJECTS)
    desc = f"Project portfolio of {OWNER['name']} — {OWNER['title']}."
    html = head(OWNER["site_title"], desc, "") + f"""<body>
{topbar("")}
<main class="wrap">
  <section class="hero">
    <h1>{escape(OWNER["name"])}</h1>
    <p>{escape(OWNER["title"])}. Four complete, solo-built enterprise systems — each with a walkthrough video and a full documentation PDF.</p>
    <div class="chips">
      <span class="chip">ASP.NET Core</span><span class="chip">Entity Framework Core</span>
      <span class="chip">SQL Server</span><span class="chip">React</span><span class="chip">Vite</span>
      <span class="chip">JWT / RBAC</span>
    </div>
  </section>

  <div class="toolbar">
    <h2>Projects</h2>
    <div class="seg" role="group" aria-label="Layout">
      <button type="button" id="v-grid" aria-pressed="true">Grid</button>
      <button type="button" id="v-list" aria-pressed="false">Show all</button>
    </div>
  </div>

  <section class="grid" id="grid">{cards}
  </section>
</main>
{footer()}
<script>
(function(){{
  var body = document.body, g = document.getElementById('v-grid'), l = document.getElementById('v-list');
  function set(mode){{
    body.classList.toggle('all-mode', mode === 'list');
    g.setAttribute('aria-pressed', mode !== 'list');
    l.setAttribute('aria-pressed', mode === 'list');
  }}
  g.onclick = function(){{ set('grid'); }};
  l.onclick = function(){{ set('list'); }};
  if (location.hash === '#all') set('list');
}})();
</script>
</body></html>"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# Project page
# ---------------------------------------------------------------------------
def build_project(i, p):
    base = "../../"
    prev_p = PROJECTS[i - 1] if i > 0 else None
    next_p = PROJECTS[i + 1] if i < len(PROJECTS) - 1 else None
    mins = video_minutes(p["slug"])
    d = ROOT / "projects" / p["slug"]
    pdf_size = file_mb(d / "overview.pdf")
    vid_size = file_mb(d / "demo.mp4")

    boxes = "".join(
        f'<div class="box"><small>{escape(l)}</small><div>{escape(n)}</div></div>' for n, l in p["stats"]
    )
    boxes += f'<div class="box"><small>Documentation</small><div>{p["pdf_pages"]} pages (PDF)</div></div>'
    if mins:
        boxes += f'<div class="box"><small>Walkthrough video</small><div>{mins} min</div></div>'

    modules_row = f'<div class="box" style="grid-column:1/-1"><small>Modules</small><div style="font-weight:500">{escape(p["modules"])}</div></div>' if p.get("modules") else ""

    pager = '<div class="pager">'
    pager += (f'<a class="btn" href="{base}projects/{prev_p["slug"]}/">← {escape(prev_p["short"])}</a>' if prev_p else "<span></span>")
    pager += f'<a class="btn" href="{base}#all">All projects</a>'
    pager += (f'<a class="btn" href="{base}projects/{next_p["slug"]}/">{escape(next_p["short"])} →</a>' if next_p else "<span></span>")
    pager += "</div>"

    html = head(f'{p["name"]} — {OWNER["name"]}', p["tagline"] + " " + p["description"][:140], base) + f"""<body>
{topbar(base)}
<main class="wrap">
  <div class="crumb"><a href="{base}">Portfolio</a> / {escape(p["short"])}</div>
  <h1 class="ptitle">{escape(p["name"])}</h1>
  <p class="plead">{escape(p["description"])}</p>

  <div class="tabs" role="tablist">
    <button type="button" role="tab" id="t-video" aria-selected="true"  aria-controls="video">▶ Video</button>
    <button type="button" role="tab" id="t-pdf"   aria-selected="false" aria-controls="pdf">📄 PDF</button>
    <button type="button" role="tab" id="t-both"  aria-selected="false" aria-controls="both">Show both</button>
  </div>

  <section class="panel" id="video" role="tabpanel">
    <div class="stage">
      <video id="vid" controls preload="metadata" poster="poster.jpg" playsinline>
        <source src="demo.mp4" type="video/mp4">
        Your browser does not support video. <a href="demo.mp4">Download the video</a>.
      </video>
    </div>
    <p class="pdfnote"><a href="demo.mp4" download>Download video</a> ({vid_size})</p>
  </section>

  <section class="panel" id="pdf" role="tabpanel" hidden>
    <iframe class="pdfframe" id="pdfframe" title="{escape(p["short"])} documentation PDF" data-src="overview.pdf#view=FitH"></iframe>
    <div class="pdfcard" id="pdfcard">
      <div class="pdfcard-icon">📄</div>
      <h3>{escape(p["short"])} documentation</h3>
      <p>{p["pdf_pages"]} pages &middot; {pdf_size}. Opens in your phone's PDF viewer with full scrolling, zoom and download.</p>
      <a class="btn primary big" href="overview.pdf" target="_blank" rel="noopener">Open full PDF</a>
    </div>
    <p class="pdfnote pdfnote-desk">PDF not showing? <a href="overview.pdf" target="_blank" rel="noopener">Open it in a new tab</a> &middot; <a href="overview.pdf" download="{escape(p["short"])}-documentation.pdf">Download</a> ({pdf_size})</p>
  </section>

  <section class="panel" id="both" role="tabpanel" hidden></section>

  <div class="meta">
    <div class="box" style="grid-column:1/-1"><small>Backend</small><div style="font-weight:500">{escape(p["backend"])}</div></div>
    <div class="box" style="grid-column:1/-1"><small>Frontend</small><div style="font-weight:500">{escape(p["frontend"])}</div></div>
    {modules_row}
    {boxes}
  </div>

  {pager}
</main>
{footer()}
<script>
(function(){{
  var tabs = {{ video: 't-video', pdf: 't-pdf', both: 't-both' }};
  var frame = document.getElementById('pdfframe');
  var vid = document.getElementById('vid');
  var stageV = document.querySelector('#video .stage');
  var noteV  = document.querySelector('#video .pdfnote');
  var panelV = document.getElementById('video');
  var panelP = document.getElementById('pdf');
  var panelB = document.getElementById('both');
  var gap = document.createElement('div'); gap.style.height = '18px'; gap.className = 'gap';

  var isMobile = /Android|iPhone|iPad|iPod|Mobile|Silk/i.test(navigator.userAgent) || (navigator.maxTouchPoints > 1 && window.innerWidth < 900);
  var card = document.getElementById('pdfcard');
  document.documentElement.classList.toggle('is-mobile', isMobile);
  function loadPdf(){{
    if (isMobile) return;  // phones: use the "Open full PDF" button instead of an iframe
    if (!frame.getAttribute('src')) frame.setAttribute('src', frame.getAttribute('data-src'));
  }}

  function show(name){{
    Object.keys(tabs).forEach(function(k){{
      document.getElementById(tabs[k]).setAttribute('aria-selected', k === name);
    }});
    // reset: put video/pdf children back in their own panels
    if (panelB.contains(stageV)) {{ panelV.insertBefore(stageV, panelV.firstChild); panelV.appendChild(noteV); }}
    if (panelB.contains(frame))  {{ panelP.insertBefore(frame, panelP.firstChild); }}
    if (panelB.contains(card))   {{ panelP.insertBefore(card, panelP.firstChild); }}
    panelV.hidden = name !== 'video';
    panelP.hidden = name !== 'pdf';
    panelB.hidden = name !== 'both';
    if (name !== 'video') {{ try {{ vid.pause(); }} catch(e){{}} }}
    if (name === 'pdf') loadPdf();
    if (name === 'both') {{
      loadPdf();
      panelB.appendChild(stageV);
      panelB.appendChild(gap);
      panelB.appendChild(isMobile ? card : frame);
    }}
    try {{
      if (history.replaceState) history.replaceState(null, '', name === 'video' ? location.pathname : '#' + name);
    }} catch(e) {{ /* file:// in some browsers: URL just won't update, everything else works */ }}
  }}
  Object.keys(tabs).forEach(function(k){{
    document.getElementById(tabs[k]).onclick = function(){{ show(k); }};
  }});
  var h = (location.hash || '').replace('#','');
  show(tabs[h] ? h : 'video');
}})();
</script>
</body></html>"""
    (d / "index.html").write_text(html, encoding="utf-8")


def main():
    build_home()
    for i, p in enumerate(PROJECTS):
        build_project(i, p)
    print("Built index.html +", len(PROJECTS), "project pages")


if __name__ == "__main__":
    main()
