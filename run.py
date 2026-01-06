import argparse
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


async def main():
    p = argparse.ArgumentParser(description="Render x.html and capture a screenshot.")
    p.add_argument("--html", default="x.html", help="HTML file to render (default: x.html)")
    p.add_argument("--out", default="x_card.png", help="Output screenshot path (default: x_card.png)")
    p.add_argument("--width", type=int, default=1200, help="Viewport width (default: 1200)")
    p.add_argument("--height", type=int, default=675, help="Viewport height (default: 675)")
    p.add_argument("--wait_ms", type=int, default=300, help="Extra wait after ready signal (default: 300ms)")
    args = p.parse_args()

    html_path = (Path.cwd() / args.html).resolve()
    if not html_path.exists():
        raise SystemExit(f"HTML not found: {html_path}")

    out_path = (Path.cwd() / args.out).resolve()
    url = html_path.as_uri()

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": args.width, "height": args.height})

        # --- DEBUG HOOKS (çok kritik) ---
        page.on("console", lambda msg: print(f"[console.{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: print(f"[pageerror] {err}"))
        # --------------------------------

        # Load file (dom hazır olsun yeter)
        await page.goto(url, wait_until="domcontentloaded")

        # x.html gerçekten bizim beklediğimiz mi?
        title = await page.title()
        has_line1 = await page.locator("#line1").count()
        print(f"URL: {url}")
        print(f"Title: {title} | #line1 count: {has_line1}")

        # #line1 görünür olana kadar bekle
        await page.wait_for_selector("#line1", timeout=10_000)

        # __YG_READY varsa bekle; yoksa selector ready ile devam et
        try:
            await page.wait_for_function("() => window.__YG_READY === true", timeout=5_000)
        except Exception:
            print("WARN: __YG_READY not set; continuing after #line1 is ready.")

        # Layout stabilitesi
        await page.wait_for_timeout(args.wait_ms)

        # Screenshot (viewport kadar)
        await page.screenshot(path=str(out_path), full_page=False)

        # Log
        line1 = await page.text_content("#line1")
        print(f"OK: {line1}")
        print(f"Saved: {out_path}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())