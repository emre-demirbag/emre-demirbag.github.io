---
layout: post
title: "Computer Science Reading List — Emre Demirbag (2026)"
date:   2025-12-30 15:25:15 +0300
categories: jekyll
---


<h1>Computer Science Reading List (2026) — Emre Demirbag</h1>

<p>
  This is Emre Demirbag’s Computer Science book list and Scientific Computing reading list (2026).
  Topics include systems, algorithms, numerical linear algebra, FEM/DG, optimization, uncertainty quantification, and ML.
  The page includes covers, Open Library links, caching, filtering, and an exportable JSON dataset.
</p>

<p class="note">
  Tip: Use the search box for quick navigation (e.g., “Knuth”, “FEM”, “Optimization”, “MPI”, “PETSc”).
</p>


<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Computer Science Reading List (2026) — Emre Demirbag",
  "description": "Curated Computer Science + Scientific Computing reading list (2026): systems, algorithms, numerics, FEM/DG, optimization, UQ, ML. Includes covers, links, caching, filtering, and JSON export.",
  "about": [
    "Computer Science",
    "Scientific Computing",
    "High Performance Computing",
    "Numerical Linear Algebra",
    "Finite Element Method",
    "Discontinuous Galerkin",
    "Optimization",
    "Uncertainty Quantification",
    "Machine Learning"
  ],
  "author": {
    "@type": "Person",
    "name": "Emre Demirbag",
    "url": "https://emre-demirbag.github.io/"
  },
  "isPartOf": {
    "@type": "WebSite",
    "name": "Emre Demirbag",
    "url": "https://emre-demirbag.github.io/"
  }
}
</script>

<style>
  :root { color-scheme: light; }
  .note { font-size: 13px; color: rgba(0,0,0,.65); margin: 10px 0 14px; line-height: 1.35; }

  .controls {
    display: grid;
    grid-template-columns: 1fr 220px 200px;
    gap: 10px;
    align-items: center;
    margin: 12px 0 10px;
  }
  @media (max-width: 900px) {
    .controls { grid-template-columns: 1fr; }
  }

  input[type="search"], select {
    width: 100%;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid rgba(0,0,0,.15);
    background: white;
    outline: none;
  }

  .actions {
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    align-items:center;
    margin: 10px 0 18px;
  }
  .btn {
    padding: 9px 12px;
    border-radius: 12px;
    border: 1px solid rgba(0,0,0,.15);
    background: white;
    cursor:pointer;
    min-height: 40px;
  }
  .btn:hover { background: rgba(0,0,0,.03); }
  .status { font-size: 12px; color: rgba(0,0,0,.60); }

  table { width: 100%; border-collapse: collapse; }
  th, td { border-bottom: 1px solid rgba(0,0,0,.10); padding: 10px; vertical-align: middle; }
  th { text-align: left; font-size: 13px; color: rgba(0,0,0,.70); position: sticky; top: 0; background: white; }
  tr:hover { background: rgba(0,0,0,.02); }

  .cover { width: 56px; height: 84px; border-radius: 8px; object-fit: cover; background: rgba(0,0,0,.06); }
  .small { font-size: 13px; color: rgba(0,0,0,.68); }
  .tag { display: inline-block; padding: 2px 8px; border-radius: 999px; background: rgba(0,0,0,.06); font-size: 12px; }
  a { color: inherit; text-decoration: none; }
  a:hover { text-decoration: underline; }

  /* Mobile: turn table into cards */
  @media (max-width: 720px) {
    table { border: 0; }
    thead { display: none; }
    tbody, tr, td { display: block; width: 100%; }
    tr { border: 1px solid rgba(0,0,0,.10); border-radius: 14px; margin-bottom: 12px; overflow: hidden; }
    td { border-bottom: 1px solid rgba(0,0,0,.08); padding: 10px 12px; }
    td:last-child { border-bottom: 0; }

    td[data-label] { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
    td[data-label]::before {
      content: attr(data-label);
      font-size: 12px;
      color: rgba(0,0,0,.60);
      flex: 0 0 auto;
      min-width: 72px;
    }
    td[data-label="Cover"] { justify-content: flex-start; gap: 12px; }
    td[data-label="Cover"]::before { min-width: 72px; }
  }
</style>

<div class="note">
  Uses Open Library <code>/search.json</code> to resolve book → <code>cover_i</code> and work link. Covers load via <code>covers.openlibrary.org</code>.
  Cache lives in <code>localStorage</code>. If some covers are missing, click <strong>Reload (Resolve Missing)</strong>.
</div>

<div class="controls">
  <input id="q" type="search" placeholder="Search title/author (e.g., 'Knuth', 'FEM', 'Optimization')">
  <select id="area">
    <option value="__all__">All Areas</option>
  </select>
  <select id="sort">
    <option value="core">Sort: Core first</option>
    <option value="title">Sort: Title (A→Z)</option>
    <option value="area">Sort: Area</option>
  </select>
</div>

<div class="actions">
  <button class="btn" id="btnReload">Reload (Resolve Missing)</button>
  <button class="btn" id="btnClear">Clear Cache</button>
  <button class="btn" id="btnExport">Export Resolved JSON</button>
  <span class="status" id="status">Ready.</span>
</div>

<table>
  <thead>
    <tr>
      <th style="width:86px;">Cover</th>
      <th>Book</th>
      <th style="width:170px;">Area</th>
      <th style="width:120px;">Use</th>
    </tr>
  </thead>
  <tbody id="tbody"></tbody>
</table>

<script>
  // =========================
  // FULL SEED LIST
  // =========================
  const seedBooks = [
    // 1) Core Classics
    { title: "Structure and Interpretation of Computer Programs", author: "Abelson", area: "Programming", use: "Core" },
    { title: "The Mythical Man-Month", author: "Brooks", area: "Systems", use: "Core" },
    { title: "Gödel, Escher, Bach", author: "Hofstadter", area: "Theory", use: "Deep Dive" },
    { title: "Selected Papers on Computer Science", author: "Knuth", area: "Algorithms", use: "Reference" },
    { title: "The Sciences of the Artificial", author: "Herbert A. Simon", area: "Systems", use: "Reference" },
    { title: "The Visual Display of Quantitative Information", author: "Tufte", area: "Writing", use: "Reference" },
    { title: "The Dream Machine", author: "Waldrop", area: "Systems", use: "Reference" },
    { title: "The New Hacker’s Dictionary", author: "Raymond", area: "Systems", use: "Reference" },

    // 2) Systems, Performance, Engineering
    { title: "Computer Systems: A Programmer’s Perspective", author: "Bryant", area: "Systems", use: "Core" },
    { title: "Operating System Concepts", author: "Silberschatz", area: "Systems", use: "Core" },
    { title: "Modern Operating Systems", author: "Tanenbaum", area: "Systems", use: "Core" },
    { title: "Computer Architecture: A Quantitative Approach", author: "Hennessy", area: "Systems", use: "Deep Dive" },

    { title: "Advanced Programming in the UNIX Environment", author: "Stevens", area: "Systems", use: "Reference" },
    { title: "The Design of the UNIX Operating System", author: "Bach", area: "Systems", use: "Reference" },
    { title: "Lions’ Commentary on UNIX", author: "John Lions", area: "Systems", use: "Reference" },

    { title: "Computer Networks", author: "Tanenbaum", area: "Networks", use: "Core" },
    { title: "UNIX Network Programming, Volume 1", author: "Stevens", area: "Networks", use: "Reference" },
    { title: "UNIX Network Programming, Volume 2", author: "Stevens", area: "Networks", use: "Reference" },

    { title: "Design Patterns", author: "Gamma", area: "Systems", use: "Reference" },
    { title: "Designing Data-Intensive Applications", author: "Kleppmann", area: "Systems", use: "Deep Dive" },

    { title: "Introduction to High Performance Computing for Scientists and Engineers", author: "Hager", area: "HPC", use: "Deep Dive" },
    { title: "Using MPI", author: "Gropp", area: "HPC", use: "Reference" },
    { title: "Using OpenMP", author: "Chapman", area: "HPC", use: "Reference" },

    // 3) Algorithms, Theory, Compilers, PL
    { title: "Introduction to Algorithms", author: "Cormen", area: "Algorithms", use: "Core" },

    { title: "Introduction to the Theory of Computation", author: "Sipser", area: "Theory", use: "Deep Dive" },
    { title: "Computers and Intractability", author: "Garey", area: "Theory", use: "Reference" },

    { title: "Compilers: Principles, Techniques, and Tools", author: "Aho", area: "Compilers", use: "Reference" },
    { title: "Engineering a Compiler", author: "Cooper", area: "Compilers", use: "Reference" },
    { title: "The Little Schemer", author: "Friedman", area: "Programming", use: "Reference" },

    { title: "The C Programming Language (2nd Edition)", author: "Kernighan", area: "Programming", use: "Core" },
    { title: "The Art of Computer Programming", author: "Knuth", area: "Algorithms", use: "Reference" },

    // 4) Scientific Computing
    { title: "Iterative Methods for Sparse Linear Systems", author: "Saad", area: "Numerics", use: "Core" },
    { title: "Matrix Computations", author: "Golub", area: "Numerics", use: "Reference" },
    { title: "Accuracy and Stability of Numerical Algorithms", author: "Higham", area: "Numerics", use: "Reference" },

    { title: "The Mathematical Theory of Finite Element Methods", author: "Brenner", area: "FEM", use: "Deep Dive" },
    { title: "Finite Elements", author: "Braess", area: "FEM", use: "Reference" },
    { title: "Mixed Finite Element Methods and Applications", author: "Boffi", area: "FEM", use: "Reference" },

    { title: "Nodal Discontinuous Galerkin Methods", author: "Hesthaven", area: "DG", use: "Deep Dive" },
    { title: "Discontinuous Galerkin Methods: Theory, Computation and Applications", author: "Cockburn", area: "DG", use: "Reference" },

    { title: "Optimization with PDE Constraints", author: "Hinze", area: "Optimization", use: "Deep Dive" },
    { title: "Numerical Optimization", author: "Nocedal", area: "Optimization", use: "Reference" },

    { title: "Uncertainty Quantification: Theory, Implementation, and Applications", author: "Ralph C. Smith", area: "UQ", use: "Deep Dive" },
    { title: "Monte Carlo Statistical Methods", author: "Robert", area: "UQ", use: "Reference" },

    { title: "Discrete Inverse and State Estimation Problems", author: "Hansen", area: "Inverse", use: "Reference" },

    // Tooling/docs: direct URLs
    { title: "PETSc Documentation (KSP/PC)", author: "PETSc", area: "Tooling", use: "Reference",
      url: "https://petsc.org/release/", noLookup: true },
    { title: "TAO Documentation (Optimization)", author: "TAO", area: "Tooling", use: "Reference",
      url: "https://petsc.org/release/tao/", noLookup: true },
    { title: "petsc4py Documentation", author: "petsc4py", area: "Tooling", use: "Reference",
      url: "https://petsc4py.readthedocs.io/", noLookup: true },
    { title: "An Introduction to the Conjugate Gradient Method Without the Agonizing Pain", author: "Shewchuk", area: "Tooling", use: "Reference" },

    { title: "Automated Solution of Differential Equations by the Finite Element Method", author: "Logg", area: "FEM", use: "Reference" },
    { title: "deal.II Tutorials (step series)", author: "deal.II", area: "FEM", use: "Reference",
      url: "https://www.dealii.org/current/doxygen/deal.II/Tutorial.html", noLookup: true },

    // 5) ML / DL
    { title: "Pattern Recognition and Machine Learning", author: "Bishop", area: "ML", use: "Core" },
    { title: "Deep Learning", author: "Goodfellow", area: "ML", use: "Core" },
    { title: "Artificial Intelligence: A Modern Approach", author: "Russell", area: "ML", use: "Reference" },
    { title: "Bayesian Data Analysis", author: "Gelman", area: "ML", use: "Reference" },
    { title: "Probabilistic Machine Learning: An Introduction", author: "Murphy", area: "ML", use: "Reference" },

    // 6) Research/Writing
    { title: "You and Your Research", author: "Hamming", area: "Writing", use: "Core" },
    { title: "The Science of Scientific Writing", author: "Gopen", area: "Writing", use: "Reference" },
    { title: "Writing for Computer Science", author: "Zobel", area: "Writing", use: "Reference" },

    // 7) Fiction
    { title: "Neuromancer", author: "Gibson", area: "Fiction", use: "Optional" },
    { title: "Snow Crash", author: "Stephenson", area: "Fiction", use: "Optional" },
    { title: "The Library of Babel", author: "Borges", area: "Fiction", use: "Optional" },
  ];

  // =========================
  // Cache + Speed Settings
  // =========================
  const CACHE_KEY = "ol_cache_readinglist_v2"; // bump version when changing logic
  const MAX_CONCURRENCY = 6;
  const REQUEST_DELAY_MS = 60;
  const FIELDS = "title,author_name,cover_i,key,first_publish_year";

  const tbody = document.getElementById("tbody");
  const statusEl = document.getElementById("status");
  const btnReload = document.getElementById("btnReload");
  const btnClear  = document.getElementById("btnClear");
  const btnExport = document.getElementById("btnExport");

  const qEl = document.getElementById("q");
  const areaEl = document.getElementById("area");
  const sortEl = document.getElementById("sort");

  function esc(s) {
    return String(s ?? "").replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  function placeholderCoverDataUrl(label="no cover") {
    const svg = `
      <svg xmlns="http://www.w3.org/2000/svg" width="56" height="84">
        <rect width="100%" height="100%" fill="#e9e9e9"/>
        <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#777" font-size="10">${label}</text>
      </svg>`;
    return "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
  }

  function coverUrl(coverId) {
    if (!coverId) return placeholderCoverDataUrl();
    return `https://covers.openlibrary.org/b/id/${coverId}-M.jpg?default=false`;
  }

  function cacheLoad() {
    try { return JSON.parse(localStorage.getItem(CACHE_KEY) || "{}"); }
    catch { return {}; }
  }

  function cacheSave(obj) {
    localStorage.setItem(CACHE_KEY, JSON.stringify(obj));
  }

  function cacheKeyForBook(b) {
    return `${b.title}__${b.author || ""}`.toLowerCase();
  }

  async function olSearch(title, author) {
    const params = new URLSearchParams({ title, author, limit: "1", fields: FIELDS });
    const url = `https://openlibrary.org/search.json?${params.toString()}`;
    const r = await fetch(url);
    if (!r.ok) throw new Error(`Search failed: ${r.status}`);
    const data = await r.json();
    const doc = (data.docs && data.docs[0]) ? data.docs[0] : null;
    if (!doc) return null;

    const workUrl = doc.key ? `https://openlibrary.org${doc.key}` : null;
    const authors = Array.isArray(doc.author_name) ? doc.author_name.join(", ") : "";
    return {
      coverId: doc.cover_i || null,
      workUrl,
      authors,
      year: doc.first_publish_year || null,
      resolvedAt: new Date().toISOString()
    };
  }

  function rowHTML(b, resolved) {
    const link = b.noLookup
      ? (b.url || `https://openlibrary.org/search?q=${encodeURIComponent(b.title)}`)
      : (resolved?.workUrl || `https://openlibrary.org/search?q=${encodeURIComponent(b.title)}`);

    const authors = b.noLookup ? (b.author || "") : (resolved?.authors || b.author || "");
    const img = b.noLookup ? placeholderCoverDataUrl("doc") : coverUrl(resolved?.coverId);

    const titleLine = `<strong>"${esc(b.title)}"</strong>${resolved?.year ? ` <span class="small">(${esc(resolved.year)})</span>` : ""}`;

    return `
      <tr>
        <td data-label="Cover">
          <a href="${esc(link)}" target="_blank" rel="noopener">
            <img class="cover" loading="lazy" decoding="async"
                 src="${esc(img)}" alt="${esc(b.title)} cover"
                 onerror="this.onerror=null;this.src='${placeholderCoverDataUrl()}';">
          </a>
        </td>
        <td data-label="Book">
          <a href="${esc(link)}" target="_blank" rel="noopener">${titleLine}</a>
          <div class="small">${esc(authors)}</div>
        </td>
        <td data-label="Area"><span class="tag">${esc(b.area)}</span></td>
        <td data-label="Use"><span class="tag">${esc(b.use)}</span></td>
      </tr>
    `;
  }

  function useRank(u) {
    const s = (u || "").toLowerCase();
    if (s === "core") return 0;
    if (s === "deep dive") return 1;
    if (s === "reference") return 2;
    return 3; // optional/other
  }

  function getFilteredSorted(seed, cacheObj) {
    const q = (qEl.value || "").trim().toLowerCase();
    const area = areaEl.value;
    const sort = sortEl.value;

    let list = seed.slice();

    if (area !== "__all__") list = list.filter(b => b.area === area);

    if (q) {
      list = list.filter(b => {
        const key = cacheKeyForBook(b);
        const r = cacheObj[key];
        const resolvedAuthors = r?.authors || "";
        return (
          (b.title || "").toLowerCase().includes(q) ||
          (b.author || "").toLowerCase().includes(q) ||
          (resolvedAuthors || "").toLowerCase().includes(q) ||
          (b.area || "").toLowerCase().includes(q) ||
          (b.use || "").toLowerCase().includes(q)
        );
      });
    }

    if (sort === "core") {
      list.sort((a,b) => {
        const ra = useRank(a.use), rb = useRank(b.use);
        if (ra !== rb) return ra - rb;
        return a.title.localeCompare(b.title);
      });
    } else if (sort === "title") {
      list.sort((a,b) => a.title.localeCompare(b.title));
    } else if (sort === "area") {
      list.sort((a,b) => (a.area || "").localeCompare(b.area || "") || a.title.localeCompare(b.title));
    }

    return list;
  }

  function renderTable(seed, cacheObj) {
    const list = getFilteredSorted(seed, cacheObj);
    tbody.innerHTML = "";
    for (const b of list) {
      const key = cacheKeyForBook(b);
      const resolved = cacheObj[key] || null;
      tbody.insertAdjacentHTML("beforeend", rowHTML(b, resolved));
    }
    statusEl.textContent = `Showing ${list.length} / ${seed.length}.`;
  }

  async function resolveMissing(seed) {
    const cacheObj = cacheLoad();
    let done = 0, hit = 0, miss = 0, failed = 0;

    const tasks = seed
      .filter(b => !b.noLookup)
      .map(b => ({ b, key: cacheKeyForBook(b), has: !!cacheObj[cacheKeyForBook(b)] }));

    hit = tasks.filter(t => t.has).length;
    const toResolve = tasks.filter(t => !t.has);

    statusEl.textContent = `Cache hits: ${hit} | Resolving: ${toResolve.length} …`;
    renderTable(seed, cacheObj);

    let idx = 0;
    async function worker() {
      while (idx < toResolve.length) {
        const t = toResolve[idx++];
        try {
          const res = await olSearch(t.b.title, t.b.author || "");
          cacheObj[t.key] = res || { coverId: null, workUrl: null, authors: t.b.author || "", year: null, resolvedAt: new Date().toISOString() };
          miss++;
        } catch {
          failed++;
        }

        done++;
        if (done % 3 === 0) {
          cacheSave(cacheObj);
          renderTable(seed, cacheObj);
        }
        statusEl.textContent = `Cache hits: ${hit} | Resolved: ${done}/${toResolve.length} | fail: ${failed}`;
        await new Promise(r => setTimeout(r, REQUEST_DELAY_MS));
      }
    }

    const workers = Array.from({length: MAX_CONCURRENCY}, () => worker());
    await Promise.all(workers);

    cacheSave(cacheObj);
    renderTable(seed, cacheObj);
    statusEl.textContent = `Done. Hits: ${hit} | Newly resolved: ${miss} | failed: ${failed}`;
  }

  function exportResolvedJSON() {
    const cacheObj = cacheLoad();
    const rows = seedBooks.map(b => {
      const key = cacheKeyForBook(b);
      const r = cacheObj[key] || null;
      return {
        title: b.title,
        authors: b.noLookup ? (b.author || "") : (r?.authors || b.author || ""),
        area: b.area,
        use: b.use,
        cover_id: b.noLookup ? null : (r?.coverId || null),
        ol_url: b.noLookup ? (b.url || null) : (r?.workUrl || `https://openlibrary.org/search?q=${encodeURIComponent(b.title)}`),
        resolved_at: r?.resolvedAt || null
      };
    });

    const blob = new Blob([JSON.stringify(rows, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "books_resolved.json";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);

    statusEl.textContent = "Exported: books_resolved.json";
  }

  function clearCache() {
    localStorage.removeItem(CACHE_KEY);
    renderTable(seedBooks, {});
    statusEl.textContent = "Cache cleared.";
  }

  function initAreaDropdown() {
    const areas = Array.from(new Set(seedBooks.map(b => b.area))).sort((a,b) => a.localeCompare(b));
    for (const a of areas) {
      const opt = document.createElement("option");
      opt.value = a;
      opt.textContent = a;
      areaEl.appendChild(opt);
    }
  }

  initAreaDropdown();
  const cacheObj = cacheLoad();
  renderTable(seedBooks, cacheObj);

  btnReload.addEventListener("click", () => resolveMissing(seedBooks));
  btnClear.addEventListener("click", clearCache);
  btnExport.addEventListener("click", exportResolvedJSON);

  qEl.addEventListener("input", () => renderTable(seedBooks, cacheLoad()));
  areaEl.addEventListener("change", () => renderTable(seedBooks, cacheLoad()));
  sortEl.addEventListener("change", () => renderTable(seedBooks, cacheLoad()));
</script>