#!/usr/bin/env python3
"""Wrap GetTerms-generated raw HTML in the Setline apex design tokens."""
from pathlib import Path
import re

ROOT = Path(__file__).parent
LAST_UPDATED = "May 30, 2026"
SITE_BASE = "https://setline.tech"

PAGES = [
    ("privacy", "Privacy Policy"),
    ("terms", "Terms of Service"),
    ("cookies", "Cookie Policy"),
]

TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
    <title>{title} — Setline</title>
    <meta name="description" content="{title} for Setline ({base_host})." />
    <meta name="robots" content="index, follow" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter+Tight:wght@400;500;600&display=swap"
      rel="stylesheet"
    />
    <style>
      :root {{
        --bg: #f4f1ea;
        --sf: #faf8f2;
        --bd: #e2ddd1;
        --tx: #1a2419;
        --tm: #4d5648;
        --td: #7a7d70;
        --brand: #1f4a2c;
        --brand-deep: #142e1c;
        --brand-soft: #d9e3d9;
      }}
      * {{ box-sizing: border-box; }}
      html, body {{
        margin: 0;
        padding: 0;
        background: var(--bg);
        color: var(--tx);
        font-family: 'Inter Tight', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 15px;
        line-height: 1.65;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }}
      body {{
        min-height: 100vh;
        display: flex;
        flex-direction: column;
      }}
      header.top {{
        max-width: 740px;
        width: 100%;
        margin: 0 auto;
        padding: 36px 24px 0;
      }}
      header.top a.home {{
        font-family: 'Fraunces', Georgia, serif;
        font-weight: 500;
        font-size: 24px;
        letter-spacing: -0.02em;
        color: var(--brand);
        text-decoration: none;
      }}
      header.top a.home em {{
        color: var(--brand-deep);
        font-style: italic;
      }}
      main {{
        flex: 1;
        max-width: 740px;
        width: 100%;
        margin: 0 auto;
        padding: 28px 24px 48px;
      }}
      main h1 {{
        font-family: 'Fraunces', Georgia, serif;
        font-weight: 500;
        font-size: 38px;
        letter-spacing: -0.015em;
        color: var(--tx);
        margin: 0 0 8px;
        line-height: 1.15;
      }}
      .updated {{
        font-size: 11.5px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--td);
        margin: 0 0 32px;
      }}
      main h2 {{
        font-family: 'Fraunces', Georgia, serif;
        font-weight: 500;
        font-size: 22px;
        letter-spacing: -0.005em;
        color: var(--tx);
        margin: 40px 0 10px;
        line-height: 1.3;
      }}
      main h3 {{
        font-family: 'Inter Tight', sans-serif;
        font-weight: 600;
        font-size: 15.5px;
        color: var(--tx);
        margin: 26px 0 8px;
      }}
      main p {{
        margin: 0 0 14px;
        color: var(--tx);
      }}
      main ul, main ol {{
        padding-left: 22px;
        margin: 0 0 14px;
      }}
      main li {{
        margin-bottom: 6px;
        color: var(--tx);
      }}
      main a {{
        color: var(--brand);
        text-decoration: none;
        border-bottom: 1px solid var(--brand-soft);
      }}
      main a:hover {{
        border-bottom-color: var(--brand);
      }}
      main strong {{
        font-weight: 600;
      }}
      main em {{
        font-style: italic;
      }}
      main hr {{
        border: 0;
        border-top: 1px solid var(--bd);
        margin: 36px 0;
      }}
      main table {{
        width: 100%;
        border-collapse: collapse;
        margin: 0 0 18px;
        font-size: 14.5px;
      }}
      main th, main td {{
        text-align: left;
        padding: 8px 10px;
        border-bottom: 1px solid var(--bd);
      }}
      main th {{
        font-weight: 600;
        background: var(--sf);
      }}
      footer {{
        max-width: 740px;
        width: 100%;
        margin: 0 auto;
        padding: 24px 24px 36px;
        border-top: 1px solid var(--bd);
        display: flex;
        flex-wrap: wrap;
        gap: 18px 24px;
        align-items: baseline;
        font-size: 12.5px;
        color: var(--td);
      }}
      footer .copy {{ flex: 1; min-width: 180px; }}
      footer nav {{ display: flex; gap: 16px; flex-wrap: wrap; }}
      footer a {{
        color: var(--tm);
        text-decoration: none;
        border-bottom: 1px solid transparent;
      }}
      footer a:hover {{
        color: var(--brand);
        border-bottom-color: var(--brand-soft);
      }}
      footer a.current {{
        color: var(--brand);
      }}
      @media (max-width: 560px) {{
        main h1 {{ font-size: 30px; }}
        main h2 {{ font-size: 20px; }}
      }}
    </style>
  </head>
  <body>
    <header class="top">
      <a class="home" href="/">Setline<em>.</em></a>
    </header>
    <main>
      <h1>{title}</h1>
      <p class="updated">Last updated {last_updated}</p>
      {body}
    </main>
    <footer>
      <span class="copy">&copy; 2026 Setline</span>
      <nav>
        <a href="/">Home</a>
        <a href="/legal/privacy"{cur_privacy}>Privacy</a>
        <a href="/legal/terms"{cur_terms}>Terms</a>
        <a href="/legal/cookies"{cur_cookies}>Cookies</a>
      </nav>
    </footer>
  </body>
</html>
"""


def clean_body(raw: str) -> str:
    # Replace the domain typo
    raw = raw.replace("siteline.tech", "setline.tech")
    # Strip trailing GetTerms comment
    raw = re.sub(r"<!--\s*-->\s*$", "", raw).strip()
    # Strip any leading <h1>...</h1> since the template provides its own
    raw = re.sub(r"^\s*<h1[^>]*>.*?</h1>\s*", "", raw, count=1, flags=re.IGNORECASE | re.DOTALL)
    return raw


def main() -> None:
    for slug, title in PAGES:
        raw_path = ROOT / "legal" / slug / "raw.html"
        out_path = ROOT / "legal" / slug / "index.html"
        body = clean_body(raw_path.read_text(encoding="utf-8"))
        rendered = TEMPLATE.format(
            title=title,
            last_updated=LAST_UPDATED,
            base_host="setline.tech",
            body=body,
            cur_privacy=' class="current"' if slug == "privacy" else "",
            cur_terms=' class="current"' if slug == "terms" else "",
            cur_cookies=' class="current"' if slug == "cookies" else "",
        )
        out_path.write_text(rendered, encoding="utf-8")
        raw_path.unlink()
        print(f"wrote {out_path.relative_to(ROOT)} ({len(rendered)} bytes)")


if __name__ == "__main__":
    main()
