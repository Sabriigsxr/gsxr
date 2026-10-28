# GSXR LAUNCHCTRL — Brand & Marketing Kit

**A complete pre-launch marketing package for GSXR LAUNCHCTRL** — an AI coding-agent
CLI with an automotive/motorsport aesthetic, built for developers who push limits.

> **Status:** IN DEVELOPMENT — All assets are pre-launch deliverables. No code in `src/`
> was modified. This package delivers brand identity, campaign assets, and a landing site.

---

## Quick Start

```bash
# Preview the landing page locally
cd gsxr-launchctrl/website
python3 -m http.server 8000
# → Open http://localhost:8000/index.html
```

---

## Package Contents

| Folder | Contents | Description |
|--------|----------|-------------|
| `brand/guidelines/` | 4 markdown files | Full brand identity: personality, logo rules, colors, motion |
| `brand/design-tokens/` | 4 files | Color/typography/spacing JSON + CSS tokens |
| `brand/logo/` | 6 SVG files | All logo variations + animated reveal |
| `campaign/photos/` | 4 files | 10 production-ready image generation prompts |
| `campaign/video/` | 1 file | 3 complete video storyboards with shot lists |
| `campaign/coming-soon/` | 1 file | Poster design brief with layout instructions |
| `website/` | 7 files | Complete responsive landing page (HTML + CSS + JS) |
| `social/` | 3 files | Style guide, 4-week content calendar, asset inventory |

---

## Brand Identity Highlights

- **Tagline:** "LAUNCH SMARTER. EXECUTE HARDER."
- **Secondary:** "Power Under Control."
- **Campaign:** "Same Passion. New Frontier."
- **Colors:** Obsidian Black, Racing Blue, Electric Cyan, Redline Red
- **Fonts:** Space Grotesk (display), Inter (body), IBM Plex Mono (terminal)

## Landing Page Sections

- **A. Hero** — Brand name, tagline, status, CTA
- **B. Mission** — Brand positioning statement
- **C. Product Vision** — 6-feature grid (Planning, Models, Agents, Integration, Terminal, Workflows)
- **D. Terminal Showcase** — Concept terminal with typing animation
- **E. Engineering Philosophy** — 4 principles (Plan → Select → Coordinate → Execute)
- **F. Coming Soon** — Call-to-action
- **G. Footer** — Status indicator, nav links, copyright

## Image Generation

Photography prompts are ready for Midjourney/DALL·E/Stable Diffusion. Each JSON file
contains the exact prompt, negative prompt, aspect ratio, and expected filename for 10
total assets covering social posts, hero images, and vertical stories.

## Development Notes

This package was created as a **branding/marketing deliverable**. The underlying
TypeScript source code in `/home/gsxr/src/` was read for context but **not modified**.
All new files live under `/home/gsxr/gsxr-launchctrl/`.

---

*See `social/asset-inventory.md` for a complete file listing with creation dates.*
