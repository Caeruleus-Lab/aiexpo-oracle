// ─── BOOK VARIABLES — edit these, nothing else needs to change for a new book ───
#let book-kicker   = "เขียนโดย AI เพื่อ AI"                       // top line of the cover, always
#let book-cover-art = "/images/cover-art.jpg"                // make-cover-art.sh output; AI-generated, say so in tagline + README
#let book-prompt   = "$ herdr-room in aiexpo-oracle wCC:p5 wCC:p4 --layout cols"          // the dim command line on the cover
#let book-title-1  = "ย้ายร่าง"                               // big, white
#let book-title-2  = "กลางห้อง"                              // big, accent colour
#let book-subtitle = [herdr-room ทีละคำสั่ง\ ย้าย agent จาก worktree กลับ main แล้วทำไมห้องถึงมี 3 คอลัมน์]
#let book-tagline  = [ทุกคำสั่งรันจริง ทุกภาพในเล่มคือเทอร์มินัลจริง ยกเว้นภาพปกที่ AI วาด — 2026-10-31]
#let book-author   = [AIExpo Oracle (AI, ไม่ใช่คน) กับ Nat Weerawan]
#let book-credit   = [AI oracle · Caeruleus-Lab/aiexpo-oracle · Claude]

// Page setup
#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 3cm, right: 3cm),
  numbering: "1",
)
#set text(font: "Laksaman", size: 12pt, lang: "th")
#set heading(numbering: none)
// typst >= 0.13 spaces paragraphs with par.spacing, NOT block.spacing —
// setting only block.spacing leaves Thai paragraphs as one continuous
// slab (verified by rendering pages 6 and 8, 2026-09-13)
#set par(leading: 0.95em, spacing: 1.9em, justify: false, first-line-indent: 0em)
#set block(spacing: 1.9em)

// Chapter headings — page break before
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  set text(size: 20pt, weight: "bold", fill: rgb("#1a1a2e"))
  v(2em)
  it
  v(1em)
}

// Section headings
#show heading.where(level: 2): it => {
  set text(size: 14pt, weight: "bold", fill: rgb("#2c3e50"))
  v(1em)
  it
  v(0.5em)
}

#show heading.where(level: 3): it => {
  set text(size: 12pt, weight: "bold", fill: rgb("#2c3e50"))
  v(0.8em)
  it
  v(0.4em)
}

// Code blocks — mono + background
#show raw.where(block: true): it => {
  set text(font: "Menlo", size: 9pt)
  set par(leading: 0.65em)
  block(
    fill: rgb("#f6f8fa"),
    stroke: 0.5pt + luma(200),
    inset: 14pt,
    radius: 4pt,
    width: 100%,
    it,
  )
}

// Inline code — subtle grey background + charcoal
#show raw.where(block: false): it => {
  box(
    fill: rgb("#f0f0f0"),
    inset: (x: 3pt, y: 1.5pt),
    radius: 2pt,
    text(font: "Menlo", size: 9pt, fill: rgb("#36454f"), it),
  )
}

// Bold — dark navy
#show strong: it => text(weight: "bold", fill: rgb("#1a1a2e"), it)

// Blockquotes — blue left border + light blue background
#show quote.where(block: true): it => {
  block(
    fill: rgb("#f0f4f8"),
    stroke: (left: 3pt + rgb("#3498db")),
    inset: (left: 16pt, right: 12pt, top: 10pt, bottom: 10pt),
    radius: (right: 4pt),
    it,
  )
}

// Tables — dark header + zebra stripes
#set table(
  stroke: 0.5pt + luma(180),
  fill: (_, row) => if row == 0 { rgb("#2c3e50") } else if calc.odd(row) {
    rgb("#f8f9fa")
  } else { white },
)
#show table.cell: it => {
  set text(size: 10pt)
  set align(left)
  if it.y == 0 {
    set text(fill: white, weight: "bold")
    it
  } else { it }
}

// ─── IMAGES ────────────────────────────────────────────────────────
// Every image is a terminal capture or a diagram card rendered from text by
// /ascii-diagram --png (1300-1600 px wide, no DPI). Without a width typst would
// place them at 72 dpi and overflow the page, so all images take the text width.
#set image(width: 100%)
#show figure: set block(breakable: false)
#show figure.caption: it => text(size: 9.5pt, fill: rgb("#545A51"), it)

// ─── COVER ─────────────────────────────────────────────────────────
// DEFAULT LAYOUT "C" (Nat chose it over A/B, kvmbox-oracle 2026-10-03; reused 2026-10-05):
//   kicker "เขียนโดย AI เพื่อ AI" (18pt) → the story's command (16pt) → Codex art fading into the
//   dark → title (56pt) + promise line (36pt, the ONLY accent) → rule → subtitle → tagline → author.
// Art = images/cover-art.jpg from scripts/make-cover-art.sh. It is AI-generated, NOT a photograph:
// the tagline must say so ("ยกเว้นภาพปกที่ AI วาด"). Path starts with "/" because typst runs --root .
// from build/. Terminal palette of the book's own images (#0d1117 / #79c0ff / #e6edf3).
// book-prompt is a STRING passed to text(): no markup parsing, so -- stays --, and no
// inline-code box (raw() would pick up the body's light #f0f0f0 code style on the dark cover).
#[
  #let bg = rgb("0d1117")
  #let fg = rgb("e6edf3")
  #let accent = rgb("79c0ff")
  #let dim = rgb("6e7b8b")
  #set page(paper: "a4", margin: 0pt, fill: bg, numbering: none)
  #set text(font: "Laksaman", lang: "th", fill: fg)
  #set par(leading: 0.65em, spacing: 0pt)

  #place(top + left, dx: -1mm, dy: -1mm, image(book-cover-art, width: 212mm))
  #place(top + left, dy: 62mm, rect(width: 212mm, height: 82mm, stroke: none,
    fill: gradient.linear((bg.transparentize(100%), 0%), (bg, 100%), angle: 90deg)))
  #place(top + left, dx: 24mm, dy: 18mm, text(size: 18pt, weight: "bold", fill: fg, book-kicker))
  #place(top + left, dx: 24mm, dy: 30mm, text(font: "Menlo", size: 16pt, fill: dim, book-prompt))
  #place(top + left, dx: 24mm, dy: 148mm, text(size: 56pt, weight: "bold", fill: fg, book-title-1))
  #place(top + left, dx: 24mm, dy: 172mm, text(size: 36pt, weight: "bold", fill: accent, book-title-2))
  #place(top + left, dx: 24mm, dy: 206mm, line(length: 14mm, stroke: 1pt + dim))
  #place(top + left, dx: 24mm, dy: 214mm, block(width: 160mm, text(size: 15pt, fill: fg, book-subtitle)))
  #place(top + left, dx: 24mm, dy: 238mm, block(width: 160mm, text(size: 11.5pt, fill: dim, book-tagline)))
  #place(top + left, dx: 24mm, dy: 262mm, text(size: 15pt, weight: "bold", fill: fg, book-author))
  #place(top + left, dx: 24mm, dy: 273mm, text(size: 9.5pt, fill: dim, book-credit))
]

#counter(page).update(1)

#outline(title: "สารบัญ", depth: 1)
