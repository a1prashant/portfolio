# Prashant Prabodh — Portfolio

Static portfolio website for **Prashant Prabodh**
(Senior Technology Executive | Software Architect | Consultant | Coder).

## Architecture

| Layer | Where |
|---|---|
| **Single source of truth** | This GitHub repository (`a1prashant/portfolio`, `master`) |
| **Public website** | GitHub Pages — https://a1prashant.github.io/portfolio |
| **Videos** | Hosted on YouTube (https://www.youtube.com/@TechPrashantPrabodh); links/embeds are integrated into the relevant pages here |
| **Legacy source** | Google Sites (https://sites.google.com/view/techprashantprabodh) — content migrated from here, **not** part of the final architecture |

## Site structure

- `index.html` — Home: Technical Bits, Articles, Projects, Quotes
- `aboutme.html` — Personal life + full professional bio / skills / career journey
- `profile.html` — Resume (embedded PDF in `dox/`)
- `videos.html` — YouTube video embeds
- `quotes.html` — Favorite quotes
- `social.html` — Social Responsibility (Helping Hands India, PEWS)
- `techbit-*.html` — Technical Bits reference pages
- `article-*.html` — Long-form articles (e.g. Self-aware SDLC)
- `library.md` — Markdown Library index (rendered by Jekyll)
- `md/` — Markdown notes/references; **rendered directly by Jekyll** on GitHub Pages (no manual build step)
- `_layouts/`, `_includes/`, `_data/` — Jekyll layouts, partials, and navigation data

## Local preview

Open `index.html` in a browser (nav/footer are injected via `script/local.js`).
The main site is static HTML styled by `css/style.css`.

### Preview markdown pages with Jekyll

- install ruby + bundler (`gem install bundler jekyll`)
- `bundle exec jekyll serve` (or `jekyll serve`)
- open `http://localhost:4000/portfolio/`

Jekyll is **not** required to preview the static pages — it is only needed to
render the `md/` notes and `library.md` exactly as GitHub Pages will.

## Diagrams (Mermaid)

Markdown notes use [Mermaid](https://mermaid.js.org) ` ```mermaid ` fenced
blocks for flowcharts/diagrams. GitHub Pages (Jekyll) does **not** render
Mermaid server-side, so markdown pages include a small client-side script
(`_includes/mermaid.html`) that loads Mermaid from a CDN and renders every
`language-mermaid` code block into an SVG when the page loads.

## Contributing / workflow

- Edit content directly in this repository (single source of truth).
- Commit to `master`; GitHub Pages runs Jekyll and serves the static files.
- Add markdown notes under `md/` — they appear automatically in the
  [Markdown Library](library.html).
- Keep videos on YouTube; only embed links here.