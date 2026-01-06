import argparse
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright


async def main():
    p = argparse.ArgumentParser(description="Render x.html and capture a screenshot + write meta JSON.")
    p.add_argument("--html", default="x.html", help="HTML file to render (default: x.html)")
    p.add_argument("--out", default="x_card.png", help="Output screenshot path (default: x_card.png)")
    p.add_argument("--meta", default="x_out.json", help="Output meta JSON path (default: x_out.json)")
    p.add_argument("--width", type=int, default=1200, help="Viewport width (default: 1200)")
    p.add_argument("--height", type=int, default=675, help="Viewport height (default: 675)")
    p.add_argument("--wait_ms", type=int, default=300, help="Extra wait after ready signal (default: 300ms)")
    args = p.parse_args()

    html_path = (Path.cwd() / args.html).resolve()
    if not html_path.exists():
        raise SystemExit(f"HTML not found: {html_path}")

    out_path = (Path.cwd() / args.out).resolve()
    meta_path = (Path.cwd() / args.meta).resolve()
    url = html_path.as_uri()

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": args.width, "height": args.height})

        await page.goto(url, wait_until="load")

        # Prefer explicit ready flag if your x.html sets it
        ready_ok = True
        try:
            await page.wait_for_function("() => window.__YG_READY === true", timeout=10_000)
        except Exception:
            ready_ok = False

        # Fallback: wait for line1 to exist
        await page.wait_for_selector("#line1", timeout=10_000)
        await page.wait_for_timeout(args.wait_ms)

        await page.screenshot(path=str(out_path), full_page=False)

        # Extract text from DOM
        line1 = (await page.text_content("#line1")) or ""
        line2 = (await page.text_content("#line2")) or ""
        utc = (await page.text_content("#utc")) or ""
        pct = (await page.text_content("#pct")) or ""

        # Normalize
        line1 = line1.strip()
        line2 = line2.strip()
        utc = utc.strip()
        pct = pct.strip()

        meta = {
            "tweet_text": line1,     # e.g. "2026 is 1.52% complete."
            "line1": line1,
            "line2": line2,
            "pct": pct,              # e.g. "1.52%"
            "utc": utc,              # e.g. "UTC 2026-01-06 12:54"
            "ready_flag": ready_ok,
            "html": str(html_path),
            "image": str(out_path),
            "url": url,
        }
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"URL: {url}")
        print(f"OK: {line1}")
        print(f"Saved: {out_path}")
        print(f"Meta: {meta_path}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())