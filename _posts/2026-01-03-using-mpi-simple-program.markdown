---
layout: post
title: "A First MPI Program "
date:   2026-01-03 14:09:15 +0300
categories: jekyll
---


<p class="lede">
We use the classic π-by-integration example because it’s the smallest program that still demonstrates the two MPI primitives you’ll use constantly: <span class="k">broadcast</span> and <span class="k">reduction</span>.
</p>

<!-- MathJax (so LaTeX always renders on GitHub Pages/Jekyll themes) -->
<script>
  window.MathJax = {
    tex: { inlineMath: [['\\(','\\)'], ['$', '$']] },
    options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
  };
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

<style>
  :root { color-scheme: light; }
  .wrap { max-width: 980px; margin: 0 auto; padding: 0 16px; }
  .k { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
  .lede { margin-top: 8px; font-size: 16px; line-height: 1.65; color: rgba(0,0,0,.78); }
  .card {
    border: 1px solid rgba(0,0,0,.10);
    border-radius: 18px;
    background: #fff;
    box-shadow: 0 1px 0 rgba(0,0,0,.03);
    padding: 16px;
    margin: 16px 0;
    color: #0b0b0b;
  }
  h1, h2, h3 { color:#0b0b0b; }
  h2 { margin: 0 0 10px; }
  p, li { color: rgba(0,0,0,.80); }
  .muted { color: rgba(0,0,0,.68); }

  /* Terminal-style blocks (true dark, not gray) */
  .term {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(0,0,0,.18);
    background: #040a06; /* near-black */
  }
  .termbar{
    display:flex; align-items:center; justify-content:space-between;
    padding: 10px 12px;
    background: rgba(255,255,255,.04);
    border-bottom: 1px solid rgba(255,255,255,.08);
    color: rgba(190,255,205,.92);
    font-size: 12px;
  }
  .dots { display:flex; gap:6px; align-items:center; }
  .dot { width:10px; height:10px; border-radius:999px; background: rgba(160,255,180,.25); }
  pre.termtext{
    margin: 0;
    padding: 14px 14px 16px;
    color: #9cffb0;
    font-size: 13px;
    line-height: 1.35;
    white-space: pre;
    overflow-x: auto;
  }

  .copyrow{
    display:flex; gap:10px; flex-wrap:wrap;
    align-items:center; justify-content:flex-start;
    padding: 10px 12px;
    background: rgba(255,255,255,.03);
    border-top: 1px solid rgba(255,255,255,.08);
  }
  .btn{
    appearance:none;
    border: 1px solid rgba(255,255,255,.18);
    background: rgba(255,255,255,.06);
    color: rgba(220,255,230,.95);
    border-radius: 12px;
    padding: 8px 10px;
    cursor:pointer;
    font-size: 13px;
  }
  .btn:hover{ background: rgba(255,255,255,.10); }
  .status{ font-size: 12px; color: rgba(190,255,205,.8); }

  /* Small inline diagram */
  .grid{
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    align-items:start;
  }
  .grid > *{ min-width:0; }
  @media (max-width: 900px){ .grid{ grid-template-columns: 1fr; } }

  .svgwrap{
    border: 1px solid rgba(0,0,0,.10);
    border-radius: 16px;
    overflow:hidden;
    background: #fff;
  }
  .cap { font-size: 12px; color: rgba(0,0,0,.62); margin-top: 8px; }
  code.inline { background: rgba(0,0,0,.05); padding: 2px 6px; border-radius: 8px; }
</style>

<div class="wrap">

<div class="card">
  <h2>Background</h2>
  <p class="muted">
    Parallel computing isn’t only about “speed for its own sake”: it shows up because modern workloads quickly hit limits in runtime, memory footprint,
    and the need to explore many scenarios. MPI remains a core tool because it makes cooperation explicit—processes exchange messages and combine results.
  </p>
</div>

<div class="card">
  <h2>Problem statement</h2>

  <p>
    We compute \(\pi\) using the identity:
  </p>

  <p class="k">
    \[
      \int_{0}^{1} \frac{4}{1+x^2}\,dx = \pi
    \]
  </p>

  <p class="muted">
    Let \(f(x)=\frac{4}{1+x^2}\). We approximate the integral on \([0,1]\) with the midpoint rule using \(n\) subintervals:
  </p>

  <p class="k">
    \[
      h = \frac{1}{n}, \quad x_i = \left(i+\tfrac{1}{2}\right)h,\quad
      \pi \approx h \sum_{i=0}^{n-1} f(x_i)
    \]
  </p>
</div>

<div class="card">
  <h2>Graph + MPI dataflow (kept minimal)</h2>

  <div class="grid">

    <div>
      <div class="svgwrap">
        <!-- Simple, lightweight SVG: curve + midpoint rectangles (schematic) -->
        <svg viewBox="0 0 720 420" width="100%" height="auto" role="img" aria-label="Midpoint rule rectangles under f(x)=4/(1+x^2) on [0,1]">
          <rect x="0" y="0" width="720" height="420" fill="#ffffff"/>
          <!-- axes -->
          <line x1="70" y1="350" x2="680" y2="350" stroke="rgba(0,0,0,.25)" stroke-width="2"/>
          <line x1="70" y1="60"  x2="70"  y2="350" stroke="rgba(0,0,0,.25)" stroke-width="2"/>
          <text x="38" y="80" fill="rgba(0,0,0,.55)" font-size="18" font-family="Georgia, serif">f(x)</text>

          <!-- rectangles (n=6) -->
          <!-- We'll draw schematic rectangles; heights are approximate for visual intuition -->
          <g fill="rgba(0,0,0,.06)" stroke="rgba(0,0,0,.18)" stroke-width="2">
            <rect x="70"  y="110" width="101.666" height="240"/>
            <rect x="171.666" y="120" width="101.666" height="230"/>
            <rect x="273.332" y="140" width="101.666" height="210"/>
            <rect x="374.998" y="170" width="101.666" height="180"/>
            <rect x="476.664" y="205" width="101.666" height="145"/>
            <rect x="578.33"  y="235" width="101.666" height="115"/>
          </g>

          <!-- curve (hand-drawn polyline approximation for f(x)=4/(1+x^2)) -->
          <polyline
            fill="none"
            stroke="rgba(0,0,0,.55)"
            stroke-width="5"
            points="
              70,110
              130,118
              190,130
              250,146
              310,166
              370,190
              430,215
              490,240
              550,265
              610,287
              680,305
            " />
        </svg>
      </div>
      <div class="cap">
        Schematic midpoint rectangles under \(f(x)\) on \([0,1]\). MPI parallelism is “embarrassingly simple” because the sum splits cleanly.
      </div>
    </div>

    <div>
      <div class="term">
        <div class="termbar">
          <div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
          <div class="k">MPI view: broadcast + reduce</div>
          <div class="k">dataflow</div>
        </div>
        <pre class="termtext k" id="flow_diagram">
Rank 0 (root) chooses n
        |
        |  MPI_Bcast(n)
        v
All ranks compute partial sums:
  local_sum(rank) = Σ f(x_i)  for i = rank, rank+P, rank+2P, ...

        |
        |  MPI_Reduce(local_sum -> global_sum, SUM)
        v
Rank 0 computes:
  pi_est = h * global_sum
        </pre>
        <div class="copyrow">
          <button class="btn" data-copy="#flow_diagram">Copy</button>
          <span class="status" id="status_flow">Ready.</span>
        </div>
      </div>

      <p class="muted" style="margin-top:12px;">
        The “stride” assignment \(i=\text{rank},\text{rank}+P,\dots\) is a clean first decomposition: it balances work with no extra bookkeeping.
      </p>
    </div>

  </div>
</div>

<div class="card">
  <h2>Code: MPI π approximation (C)</h2>

  <p class="muted">
    This is intentionally short and readable. Rank 0 picks <span class="k">n</span>, broadcasts it, each rank computes a partial sum over its indices,
    and Rank 0 reduces and prints the estimate.
  </p>

  <div class="term">
    <div class="termbar">
      <div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="k">pi_mpi.c</div>
      <div class="k">copy-friendly</div>
    </div>
    <pre class="termtext k" id="code_pi"><code>#include &lt;mpi.h&gt;
#include &lt;math.h&gt;
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

static inline double f(double x) {
  return 4.0 / (1.0 + x * x);
}

int main(int argc, char **argv) {
  MPI_Init(&argc, &argv);

  int rank = 0, size = 1;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  /* Rank 0 chooses n; everyone must agree on it. */
  int n = 0;
  if (rank == 0) {
    n = (argc &gt;= 2) ? atoi(argv[1]) : 10000000;
    if (n &lt;= 0) n = 10000000;
    printf("n = %d, processes = %d\n", n, size);
  }

  MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

  const double h = 1.0 / (double)n;

  double local_sum = 0.0;
  for (int i = rank; i &lt; n; i += size) {
    const double x = (i + 0.5) * h;   /* midpoint */
    local_sum += f(x);
  }

  double global_sum = 0.0;
  MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

  if (rank == 0) {
    const double pi_est = h * global_sum;
    printf("pi ≈ %.16f\n", pi_est);
    printf("error = %.16e\n", fabs(pi_est - M_PI));
  }

  MPI_Finalize();
  return 0;
}
</code></pre>
    <div class="copyrow">
      <button class="btn" data-copy="#code_pi">Copy</button>
      <span class="status" id="status_pi">Ready.</span>
    </div>
  </div>
</div>

<div class="card">
  <h2>Build + run (OpenMPI)</h2>

  <div class="term">
    <div class="termbar">
      <div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="k">commands</div>
      <div class="k">OpenMPI</div>
    </div>
    <pre class="termtext k" id="cmds">
# Compile
mpicc -O2 -std=c11 -Wall -Wextra pi_mpi.c -o pi_mpi -lm

# Run with 8 processes and n=50,000,000 intervals
mpirun -np 8 ./pi_mpi 50000000
</pre>
    <div class="copyrow">
      <button class="btn" data-copy="#cmds">Copy</button>
      <span class="status" id="status_cmds">Ready.</span>
    </div>
  </div>

  <p class="muted" style="margin-top:12px;">
    Note: increasing <span class="k">n</span> reduces discretization error (the midpoint rule converges well for smooth functions), but you’ll eventually hit
    practical limits (runtime, memory-hierarchy effects, and floating-point accumulation).
  </p>
</div>

</div> <!-- /wrap -->

<script>
  function copyFromSelector(sel) {
    const el = document.querySelector(sel);
    if (!el) return Promise.reject();
    const txt = el.innerText.replace(/\n+$/,'') + "\n";
    return navigator.clipboard.writeText(txt);
  }

  function setStatus(id, msg) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = msg;
    if (msg !== "Ready.") setTimeout(()=>{ el.textContent = "Ready."; }, 900);
  }

  document.querySelectorAll("[data-copy]").forEach(btn => {
    btn.addEventListener("click", async () => {
      const sel = btn.getAttribute("data-copy");
      const statusId =
        sel === "#flow_diagram" ? "status_flow" :
        sel === "#code_pi" ? "status_pi" :
        sel === "#cmds" ? "status_cmds" : null;

      try {
        await copyFromSelector(sel);
        if (statusId) setStatus(statusId, "Copied.");
      } catch {
        if (statusId) setStatus(statusId, "Copy failed.");
      }
    });
  });
</script>