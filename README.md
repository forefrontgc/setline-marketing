# setline-marketing

Apex placeholder for **setline.tech** — the public-facing landing page until a
real marketing site lands.

This repo is intentionally minimal: one static `index.html` rendered as-is by
Vercel's static deploy. No build step, no framework, no dependencies.

## What lives here

- `index.html` — the "Coming soon" page (Setline wordmark, value-prop, contact)
- `vercel.json` — single redirect rule (none today; reserved for future)
- That's it.

## What does NOT live here

- The Setline workspace app — that's `forefrontgc/forefront-portal`. Subdomains
  like `forefront.setline.tech` route there.
- The super-admin app — that's `/admin` inside forefront-portal, served at
  `admin.setline.tech` via middleware rewrite.
- Real legal pages — `/legal/{privacy,terms,cookies}` links currently 404.
  The GetTerms-licensed pages will be added to this repo at Phase 12.

## Deploy

Vercel auto-deploys on push to `main`. Domain config: apex `setline.tech` →
this project.

## Brand

Matches the workspace app's Fernway palette (cream `#f4f1ea` / forest `#1f4a2c`).
Fonts: Fraunces (display) + Inter Tight (body), same `<link>` URL the workspace
uses so the cache entry is shared when visitors traverse setline.tech → a
tenant subdomain.
