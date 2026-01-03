---
layout: post
title: "From π to a Real MPI Pattern: 2D Halo Exchange (Stencil / Jacobi) "
date:   2026-01-03 17:01:15 +0300
categories: jekyll
---

<p class="lede">
π-by-integration is great for collectives; the next “real MPI” step is the halo exchange: each rank updates a local grid, but needs boundary (“ghost”) data from its neighbors.
</p>

<!--more-->

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

  /* FIX: theme overrides <pre> background; force true terminal black */
  .term pre.termtext { background: #040a06 !important; }
  .term pre.termtext code { background: transparent !important; color: inherit; }

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

  /* Two-column layout */
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
    Many scientific kernels are <em>stencils</em>: you update each grid point using a small neighborhood (e.g., north/south/east/west).
    Parallelism is straightforward, but each rank must exchange boundary values with its neighbors every iteration.
  </p>
</div>

<div class="card">
  <h2>Problem statement</h2>

  <p class="muted">
    Consider a 2D grid \(u(i,j)\). A classic 5-point stencil (Jacobi update) is:
  </p>

  <p class="k">
    \[
      u^{(k+1)}_{i,j} = \tfrac{1}{4}\left(u^{(k)}_{i-1,j} + u^{(k)}_{i+1,j} + u^{(k)}_{i,j-1} + u^{(k)}_{i,j+1}\right)
    \]
  </p>

  <p class="muted">
    Each rank owns a local tile of the global grid, plus a 1-cell ghost layer. Before updating, it exchanges its outermost interior row/column with
    its four neighbors (north/south/east/west).
  </p>
</div>

<div class="card">
  <h2>Minimal picture + MPI dataflow</h2>

  <div class="grid">

    <div>
      <div class="svgwrap">
        <svg viewBox="0 0 720 420" width="100%" height="auto" role="img" aria-label="2D domain split into tiles; each tile exchanges halo with four neighbors">
          <rect x="0" y="0" width="720" height="420" fill="#ffffff"/>
          <text x="24" y="42" fill="rgba(0,0,0,.72)" font-size="18" font-family="Georgia, serif">Global grid split into rank tiles</text>

          <!-- tiles -->
          <g stroke="rgba(0,0,0,.22)" stroke-width="3" fill="rgba(0,0,0,.04)">
            <rect x="80"  y="80"  width="250" height="140"/>
            <rect x="360" y="80"  width="250" height="140"/>
            <rect x="80"  y="240" width="250" height="140"/>
            <rect x="360" y="240" width="250" height="140"/>
          </g>

          <!-- center tile highlight -->
          <rect x="360" y="80" width="250" height="140" fill="rgba(0,0,0,.06)" stroke="rgba(0,0,0,.35)" stroke-width="4"/>

          <!-- arrows (halo exchange) -->
          <g stroke="rgba(0,0,0,.55)" stroke-width="6" fill="none" stroke-linecap="round">
            <line x1="485" y1="80"  x2="485" y2="55"/>
            <line x1="485" y1="220" x2="485" y2="245"/>
            <line x1="360" y1="150" x2="330" y2="150"/>
            <line x1="610" y1="150" x2="640" y2="150"/>
          </g>

          <g fill="rgba(0,0,0,.60)" font-size="14" font-family="ui-monospace, Menlo, monospace">
            <text x="445" y="52">north</text>
            <text x="447" y="272">south</text>
            <text x="292" y="155">west</text>
            <text x="646" y="155">east</text>
          </g>

          <g fill="rgba(0,0,0,.72)" font-size="16" font-family="ui-monospace, Menlo, monospace">
            <text x="165" y="155">rank (0,0)</text>
            <text x="445" y="155">rank (0,1)</text>
            <text x="165" y="315">rank (1,0)</text>
            <text x="445" y="315">rank (1,1)</text>
          </g>
        </svg>
      </div>
      <div class="cap">
        Each iteration: exchange one row/column with neighbors, then compute the local stencil update.
      </div>
    </div>

    <div>
      <div class="term">
        <div class="termbar">
          <div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
          <div class="k">MPI view: halo exchange</div>
          <div class="k">dataflow</div>
        </div>
        <pre class="termtext k" id="flow_diagram">
Given a 2D process grid (px × py) and a local tile per rank:

For each iteration:
  1) Exchange ghost rows:
       send top interior row    -> north, recv ghost from north
       send bottom interior row -> south, recv ghost from south

  2) Exchange ghost columns:
       send left interior col   -> west,  recv ghost from west
       send right interior col  -> east,  recv ghost from east

  3) Update interior points with the 5-point stencil
        </pre>
        <div class="copyrow">
          <button class="btn" data-copy="#flow_diagram">Copy</button>
          <span class="status" id="status_flow">Ready.</span>
        </div>
      </div>

      <p class="muted" style="margin-top:12px;">
        This pattern shows up everywhere (PDEs, diffusion, Poisson/Laplace solvers): the “work” is local, the “MPI” is the boundary.
      </p>
    </div>

  </div>
</div>

<div class="card">
  <h2>Code: 2D halo exchange + Jacobi update (C + OpenMPI)</h2>

  <p class="muted">
    Assumptions (kept deliberately simple): global sizes <span class="k">NX</span> and <span class="k">NY</span> are divisible by the MPI process grid.
    Each rank holds a local <span class="k">nx × ny</span> tile plus a 1-cell ghost layer on all sides.
  </p>

  <div class="term">
    <div class="termbar">
      <div class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="k">stencil_halo.c</div>
      <div class="k">copy-friendly</div>
    </div>
    <pre class="termtext k" id="code_c"><code>#include &lt;mpi.h&gt;
#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

static inline int idx(int i, int j, int pitch) { return i * pitch + j; }

int main(int argc, char **argv) {
  MPI_Init(&argc, &argv);

  int world_rank = 0, world_size = 1;
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);

  /* Global grid size + iterations */
  int NX = (argc &gt;= 2) ? atoi(argv[1]) : 256;
  int NY = (argc &gt;= 3) ? atoi(argv[2]) : 256;
  int iters = (argc &gt;= 4) ? atoi(argv[3]) : 100;
  if (NX &lt;= 0) NX = 256;
  if (NY &lt;= 0) NY = 256;
  if (iters &lt;= 0) iters = 100;

  /* Build a 2D process grid */
  int dims[2] = {0, 0};
  MPI_Dims_create(world_size, 2, dims);   /* dims[0] * dims[1] = world_size */
  int periods[2] = {0, 0};               /* non-periodic */
  MPI_Comm cart = MPI_COMM_NULL;
  MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, 1, &cart);

  int rank = 0;
  MPI_Comm_rank(cart, &rank);

  int coords[2] = {0, 0};
  MPI_Cart_coords(cart, rank, 2, coords);

  /* Require divisibility to keep the example minimal */
  if ((NX % dims[0]) != 0 || (NY % dims[1]) != 0) {
    if (rank == 0) {
      fprintf(stderr, "NX,NY must be divisible by process grid dims (%d x %d). Got NX=%d NY=%d\n",
              dims[0], dims[1], NX, NY);
    }
    MPI_Finalize();
    return 1;
  }

  const int nx = NX / dims[0];
  const int ny = NY / dims[1];

  /* Local arrays include ghost layers: (nx+2) x (ny+2) */
  const int pitch = (ny + 2);
  const int rows  = (nx + 2);
  double *u  = (double*)calloc((size_t)rows * pitch, sizeof(double));
  double *un = (double*)calloc((size_t)rows * pitch, sizeof(double));
  if (!u || !un) {
    fprintf(stderr, "Allocation failed\n");
    MPI_Abort(cart, 2);
  }

  /* Initialize interior to 1.0 (toy); boundaries remain 0.0 */
  for (int i = 1; i &lt;= nx; i++) {
    for (int j = 1; j &lt;= ny; j++) {
      u[idx(i, j, pitch)] = 1.0;
    }
  }

  /* Neighbor ranks (N/S in dim 0, W/E in dim 1) */
  int north, south, west, east;
  MPI_Cart_shift(cart, 0, 1, &north, &south);
  MPI_Cart_shift(cart, 1, 1, &west,  &east);

  /* Datatype for one interior column (nx elements, stride = pitch) */
  MPI_Datatype col_t;
  MPI_Type_vector(nx, 1, pitch, MPI_DOUBLE, &col_t);
  MPI_Type_commit(&col_t);

  for (int k = 0; k &lt; iters; k++) {
    /* 1) Exchange rows (contiguous) */
    MPI_Sendrecv(
      /* sendbuf */ &u[idx(1, 1, pitch)], ny, MPI_DOUBLE, north, 10,
      /* recvbuf */ &u[idx(0, 1, pitch)], ny, MPI_DOUBLE, north, 11,
      cart, MPI_STATUS_IGNORE
    );
    MPI_Sendrecv(
      &u[idx(nx, 1, pitch)], ny, MPI_DOUBLE, south, 11,
      &u[idx(nx+1, 1, pitch)], ny, MPI_DOUBLE, south, 10,
      cart, MPI_STATUS_IGNORE
    );

    /* 2) Exchange columns (vector type) */
    MPI_Sendrecv(
      &u[idx(1, 1, pitch)], 1, col_t, west, 20,
      &u[idx(1, 0, pitch)], 1, col_t, west, 21,
      cart, MPI_STATUS_IGNORE
    );
    MPI_Sendrecv(
      &u[idx(1, ny, pitch)], 1, col_t, east, 21,
      &u[idx(1, ny+1, pitch)], 1, col_t, east, 20,
      cart, MPI_STATUS_IGNORE
    );

    /* 3) Jacobi update on interior */
    for (int i = 1; i &lt;= nx; i++) {
      for (int j = 1; j &lt;= ny; j++) {
        un[idx(i, j, pitch)] = 0.25 * (
          u[idx(i-1, j, pitch)] + u[idx(i+1, j, pitch)] +
          u[idx(i, j-1, pitch)] + u[idx(i, j+1, pitch)]
        );
      }
    }

    /* swap u & un pointers */
    double *tmp = u; u = un; un = tmp;
  }

  /* Small checksum: sum all interior values to rank 0 */
  double local_sum = 0.0;
  for (int i = 1; i &lt;= nx; i++)
    for (int j = 1; j &lt;= ny; j++)
      local_sum += u[idx(i, j, pitch)];

  double global_sum = 0.0;
  MPI_Reduce(&local_sum, &global_sum, 1, MPI_DOUBLE, MPI_SUM, 0, cart);

  if (rank == 0) {
    printf("NX=%d NY=%d iters=%d | procgrid=%dx%d | checksum(sum)=%0.6f\n",
           NX, NY, iters, dims[0], dims[1], global_sum);
  }

  MPI_Type_free(&col_t);
  free(u);
  free(un);

  MPI_Comm_free(&cart);
  MPI_Finalize();
  return 0;
}
</code></pre>
    <div class="copyrow">
      <button class="btn" data-copy="#code_c">Copy</button>
      <span class="status" id="status_c">Ready.</span>
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
# Compile (minimal)
mpicc -O2 -std=c11 stencil_halo.c -o stencil_halo

# Run (example: 2x2 ranks, global 256x256, 200 iterations)
mpirun -np 4 ./stencil_halo 256 256 200

# Try 8 ranks (dims picked automatically by MPI_Dims_create)
mpirun -np 8 ./stencil_halo 512 512 100
</pre>
    <div class="copyrow">
      <button class="btn" data-copy="#cmds">Copy</button>
      <span class="status" id="status_cmds">Ready.</span>
    </div>
  </div>

  <p class="muted" style="margin-top:12px;">
    Tip: if you want extra compiler diagnostics, add <span class="k">-Wall -Wextra</span>. They’re common GCC/Clang warning flags, not MPI-specific.
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
        sel === "#code_c" ? "status_c" :
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