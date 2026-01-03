---
layout: page
title: About
permalink: /about/
---

<style>
  :root { color-scheme: light dark; }

  .aboutwrap{
    max-width: 1100px;
    margin: 0 auto;
    padding: 22px 16px;
  }

  .term{
    border-radius: 22px;
    border: 1px solid rgba(0,0,0,.18);
    overflow: hidden;
    background: #061a10;
    box-shadow: 0 14px 40px rgba(0,0,0,.14);
  }

  .termbar{
    display:flex; align-items:center; justify-content:space-between;
    padding: 12px 14px;
    background: rgba(0,0,0,.40);
    border-bottom: 1px solid rgba(255,255,255,.10);
    color: rgba(200,255,210,.92);
    font-size: 12px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  }

  .dots{ display:flex; gap:7px; align-items:center; }
  .dot{ width:10px; height:10px; border-radius:999px; background: rgba(160,255,180,.25); }

  .title{
    font-weight: 700;
    letter-spacing: .3px;
    opacity: .95;
  }

  .clock{
    font-variant-numeric: tabular-nums;
    opacity: .92;
  }

  pre.screen{
    margin: 0;
    padding: 18px 18px 20px;
    color: #9cffb0;
    font-size: 14px;
    line-height: 1.45;
    white-space: pre;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    background:
      radial-gradient(1200px 500px at 30% 0%, rgba(156,255,176,.08), rgba(0,0,0,0)),
      #061a10;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  }

  @media (max-width: 560px){
    .aboutwrap{ padding: 16px 12px; }
    pre.screen{ font-size: 12.5px; padding: 16px; }
  }

  /* SEO-only text: visible to crawlers, hidden from users */
  .seo{
    position: absolute !important;
    width: 1px; height: 1px;
    padding: 0; margin: -1px;
    overflow: hidden;
    clip: rect(0,0,0,0);
    white-space: nowrap;
    border: 0;
  }
</style>

<!-- SEO text (no extra visible content) -->
<div class="seo">
  <h1>About Emre Demirbag</h1>
  <p>I am a software engineer with a background in Geophysics (BEng) and Computer Science (BSc).</p>
  <p>My work and interests focus on scientific computing, parallel and distributed systems, and HPC, with a systems-first perspective grounded in operating systems, compilers, and programming languages.</p>
</div>

<div class="aboutwrap">
  <div class="term" aria-label="About screen">
    <div class="termbar">
      <div class="dots" aria-hidden="true"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
      <div class="title">ABOUT</div>
      <div class="clock" id="clock">--:--:--</div>
    </div>
    <pre class="screen" id="screen"></pre>
  </div>
</div>

<script>
(function(){
  const screenEl = document.getElementById("screen");
  const clockEl  = document.getElementById("clock");

  const bioText = [
    "I am a software engineer with a background in Geophysics (BEng) and Computer Science (BSc).",
    "",
    "My work and interests focus on scientific computing, parallel and distributed systems, and HPC, with a systems-first perspective grounded in operating systems, compilers, and programming languages."
  ].join("\n");

  let cursorOn = true;

  function clamp(n, a, b){ return Math.max(a, Math.min(b, n)); }
  function padRight(s, w){ s = String(s); return s.length >= w ? s.slice(0,w) : s + " ".repeat(w - s.length); }

  function wrapText(text, width){
    const out = [];
    const paras = String(text).split("\n");
    for (const p of paras){
      if (!p.trim()){ out.push(""); continue; }
      const words = p.split(/\s+/);
      let line = "";
      for (const w of words){
        if (!line) { line = w; continue; }
        if ((line.length + 1 + w.length) <= width) line += " " + w;
        else { out.push(line); line = w; }
      }
      if (line) out.push(line);
    }
    return out;
  }

  function measureCharWidth(){
    const probe = document.createElement("span");
    probe.style.position = "absolute";
    probe.style.visibility = "hidden";
    probe.style.whiteSpace = "pre";
    probe.style.font = getComputedStyle(screenEl).font;
    probe.textContent = "M".repeat(100);
    document.body.appendChild(probe);
    const w = probe.getBoundingClientRect().width / 100;
    probe.remove();
    return w || 8;
  }

  function centerLine(s, W){
    s = String(s);
    if (s.length >= W) return s.slice(0, W);
    const L = Math.floor((W - s.length) / 2);
    return " ".repeat(L) + s + " ".repeat(W - s.length - L);
  }

  function render(){
    const charW = measureCharWidth();
    const pxW = screenEl.getBoundingClientRect().width;
    const W = clamp(Math.floor(pxW / charW) - 2, 36, 96);

    const header = "SYSTEMS / SCIENTIFIC COMPUTING";
    const innerW = W - 2;

    const wrapped = wrapText(bioText, innerW);

    // Box height: make it feel centered with generous top/bottom padding
    const bodyMin = 18;
    const bodyH = Math.max(bodyMin, wrapped.length + 10);

    const top = "┌" + "─".repeat(W) + "┐";
    const mid = "├" + "─".repeat(W) + "┤";
    const bot = "└" + "─".repeat(W) + "┘";

    const lines = [];
    lines.push(top);
    lines.push("│" + centerLine(header, W) + "│");
    lines.push(mid);

    // Build empty body
    const body = Array.from({length: bodyH}, () => " ".repeat(W));

    // Vertically center wrapped text inside body
    const startRow = Math.max(0, Math.floor((bodyH - wrapped.length) / 2) - 1);

    for (let i=0; i<wrapped.length; i++){
      const row = startRow + i;
      if (row < 0 || row >= bodyH) continue;

      // Left padding: one space, text, rest spaces
      body[row] = padRight(" " + wrapped[i], W);
    }

    // Add a blinking cursor at the end of the last non-empty line
    const lastLineIndex = Math.min(bodyH - 1, startRow + wrapped.length - 1);
    if (lastLineIndex >= 0 && lastLineIndex < bodyH){
      let line = body[lastLineIndex];
      const cur = cursorOn ? "█" : " ";
      // place cursor after last visible char (but keep inside width)
      const trimmed = line.replace(/\s+$/,"");
      const pos = clamp(trimmed.length, 0, W - 1);
      line = line.slice(0, pos) + cur + line.slice(pos + 1);
      body[lastLineIndex] = line;
    }

    for (const b of body) lines.push("│" + b + "│");
    lines.push(bot);

    screenEl.textContent = lines.join("\n");
  }

  function tickClock(){
    const d = new Date();
    const hh = String(d.getHours()).padStart(2,"0");
    const mm = String(d.getMinutes()).padStart(2,"0");
    const ss = String(d.getSeconds()).padStart(2,"0");
    clockEl.textContent = `${hh}:${mm}:${ss}`;
  }

  tickClock();
  render();

  let raf = null;
  window.addEventListener("resize", () => {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(render);
  });

  setInterval(tickClock, 1000);
  setInterval(() => { cursorOn = !cursorOn; render(); }, 520);
})();
</script>