"""Writes the html pages in site/ from one shared layout. No data needed."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BASE = "https://en-passant.pages.dev"
NAME = "EnPassant"
SEAL = "アン・パッサン"

NAV = [
    ("live", "Live"),
    ("events", "Events"),
    ("rankings", "Rankings"),
    ("players", "Players"),
    ("prodigies", "Prodigies"),
    ("compare", "Compare"),
]
MORE = [
    ("match", "Play like a GM"),
    ("upsets", "Upsets"),
    ("spirit", "Fighting spirit"),
]

# every page that isn't the homepage, in nav order
PAGES = {
    "live": {
        "title": "Live chess: top games move by move",
        "head": "Live boards",
        "desc": "Top over-the-board games as they're played, with the engine's view, both clocks and every player's rating change the moment a game ends.",
        "lede": "Every top game as it's played, with the engine's view of the position, both clocks, and each player's rating change the moment the game ends.",
        "plan": [
            "Live boards for the big events, streamed straight from Lichess broadcasts",
            "An eval bar and both clocks for every game",
            "Rating gained or lost per game, worked out with FIDE's own formula",
            "A short story of each finished game: where it turned and why",
        ],
    },
    "events": {
        "title": "Chess tournaments: standings and live odds",
        "head": "Events",
        "desc": "Standings for the top chess events, and each player's chance of winning, updated after every game.",
        "lede": "Standings for the top events, and each player's chance of winning, worked out again after every game.",
        "plan": [
            "Current and upcoming top events with their rounds",
            "Win chances from thousands of simulated finishes, based on ratings and draw rates",
            "How the chances moved round by round",
        ],
    },
    "rankings": {
        "title": "FIDE rankings: standard, rapid and blitz",
        "head": "Rankings",
        "desc": "The FIDE top lists for standard, rapid and blitz, open and women, with a live view of every Indian player in the events we follow.",
        "lede": "The FIDE top lists for standard, rapid and blitz, plus a live view of every Indian player in the events we follow.",
        "plan": [
            "Open, women and junior top lists, updated every month from FIDE",
            "Who moved up or down since last month",
            "India live: every Indian player's rating change in the events we follow, not only the top 100",
        ],
    },
    "players": {
        "title": "Top chess players: ratings, openings and clock habits",
        "head": "Players",
        "desc": "A page for every top player: rating history, peak, title, federation, opening repertoire and how they handle the clock.",
        "lede": "A page for every top player, with their rating history, peak, opening repertoire and how they handle the clock.",
        "plan": [
            "Rating history and peak in all three time controls",
            "Opening fingerprint: what they play as White and as Black, and when they try something new",
            "Clock pressure: how much time they use and how they play with little left",
        ],
    },
    "prodigies": {
        "title": "Chess prodigies: ratings compared at the same age",
        "head": "Prodigies",
        "desc": "Young players' ratings lined up by age, so any junior today can be set against where the greats were at the same age.",
        "lede": "Young players' ratings lined up by age, so any junior today can be set against where the greats were at the same age.",
        "plan": [
            "Rating by age for today's top juniors",
            "Any two players side by side at the same age",
            "Who is ahead of the pace, and by how much",
        ],
    },
    "compare": {
        "title": "Compare chess players head to head",
        "head": "Compare",
        "desc": "Put any two top players side by side: ratings over time, peaks, and their classical record against each other.",
        "lede": "Put any two top players side by side: ratings over time, peaks, and their classical record against each other.",
        "plan": [
            "Both rating lines on one chart",
            "Their results against each other in the games we have",
            "Openings they meet each other with",
        ],
    },
    "match": {
        "title": "Which grandmaster plays like you?",
        "head": "Play like a GM",
        "desc": "Type a Lichess username and see which top players your openings and style are closest to.",
        "lede": "Type a Lichess username and see which top players your openings and style are closest to. It all runs in your browser.",
        "plan": [
            "Reads your public Lichess games, nothing is stored",
            "Matches your openings and habits against the top players",
            "Shows where you're alike, and where you're not",
        ],
    },
    "upsets": {
        "title": "Biggest chess upsets by rating gap",
        "head": "Upsets",
        "desc": "The biggest wins by the lower-rated player in the events we follow, by month and by event.",
        "lede": "The biggest wins by the lower-rated player in the events we follow, by month and by event.",
        "plan": [
            "Every win where the lower-rated player was well behind",
            "Sorted by rating gap, by month and by event",
        ],
    },
    "spirit": {
        "title": "Fighting spirit: who plays for a result",
        "head": "Fighting spirit",
        "desc": "Which top players fight on in classical chess and which take quick draws, measured from their games.",
        "lede": "Which top players fight on in classical chess and which take quick draws, measured from their games.",
        "plan": [
            "Share of decisive classical games per player",
            "How long their draws last",
            "One score that puts the two together",
        ],
    },
}

FONTS = ("https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@700;800"
         "&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap")


def esc(s):
    return html.escape(str(s), quote=True)


def rankings_data():
    path = SITE / "data" / "rankings.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def rank_rows(rows, short=False):
    out = []
    for r in rows:
        title = f'<span class="ttl">{esc(r["title"])}</span>' if r["title"] else ""
        name = (f'<a class="dlink" href="https://ratings.fide.com/profile/{r["id"]}" rel="noopener" '
                f'target="_blank">{esc(r["name"])}</a>')
        cells = [f'<td class="pos mono">{r["rank"]}</td>']
        if not short:
            cells.append('<td class="mono" data-col="move" hidden></td>')
        cells.append(f'<td class="who">{title}{name}</td>')
        cells.append(f'<td class="fed mono">{esc(r["fed"])}</td>')
        cells.append(f'<td class="num mono pts">{r["rating"]}</td>')
        if not short:
            cells.append(f'<td class="num mono dim">{r["games"] or "–"}</td>')
            cells.append(f'<td class="num mono dim">{r["born"] or "–"}</td>')
        out.append("<tr>" + "".join(cells) + "</tr>")
    return "\n".join(out)


def head(title, desc, path):
    url = BASE + path
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": NAME,
                     "url": BASE + "/", "description": desc}, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0B0909">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<script src="/assets/theme.js"></script>
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(current):
    links = []
    for slug, label in NAV:
        cur = ' aria-current="page"' if slug == current else ""
        links.append(f'      <a href="/{slug}"{cur}>{label}</a>')
    more = []
    for slug, label in MORE:
        cur = ' aria-current="page"' if slug == current else ""
        more.append(f'        <a href="/{slug}"{cur}>{label}</a>')
    return f"""
<header class="top">
  <div class="wrap top-row">
    <a class="brand" href="/">
      <span class="brand-name">EN PASSANT</span>
      <span class="brand-jp" lang="ja">{SEAL}</span>
    </a>
    <nav aria-label="Main">
{chr(10).join(links)}
      <details class="nav-more"><summary>More</summary><div class="nav-menu">
{chr(10).join(more)}
      </div></details>
    </nav>
  </div>
</header>
"""


FOOTER_TOP = """
<footer>
  <div class="wrap foot-row">
    <span>An independent, non-commercial fan project. Not associated with FIDE, Lichess or Chess.com.</span>
    <span>Data from FIDE and Lichess</span>
  </div>
</footer>
"""


def footer(*scripts):
    tags = "".join(f'<script src="/assets/{s}"></script>\n' for s in scripts)
    return FOOTER_TOP + tags + "</body>\n</html>\n"


FOOTER = footer()

# the pawn, drawn on a 45 x 45 square
PAWN = ('<circle cx="22.5" cy="12" r="6"/>'
        '<path d="M16.5 20h12l-2 3.5c3 3.5 4.5 8 4.5 12h-17c0-4 1.5-8.5 4.5-12z"/>'
        '<rect x="10" y="35" width="25" height="5" rx="1.5"/>')


def board():
    """the en passant capture: White's e5 pawn takes the d5 pawn that just came from d7"""
    pieces = {
        "a2": "w", "b2": "w", "c3": "w", "f2": "w", "g3": "w", "h2": "w", "e5": "w",
        "a7": "b", "b6": "b", "c7": "b", "d5": "b", "f7": "b", "g7": "b", "h6": "b",
    }
    marks = {"e5": "from", "d6": "to", "d5": "gone"}
    cells = []
    for rank in range(8, 0, -1):
        for f, file in enumerate("abcdefgh"):
            sq = f"{file}{rank}"
            dark = (f + rank) % 2 == 1
            cls = "sq" + (" dk" if dark else "") + (f" {marks[sq]}" if sq in marks else "")
            inner = ""
            if sq in pieces:
                inner = f'<svg viewBox="0 0 45 45" aria-hidden="true"><g class="pawn-{pieces[sq]}">{PAWN}</g></svg>'
            elif sq == "d7":
                inner = f'<svg viewBox="0 0 45 45" aria-hidden="true"><g class="pawn-ghost">{PAWN}</g></svg>'
            cells.append(f'<span class="{cls}">{inner}</span>')
    ranks = "".join(f"<span>{r}</span>" for r in range(8, 0, -1))
    files = "".join(f"<span>{f}</span>" for f in "abcdefgh")
    # arrow from e5 to d6, laid over the 64 squares
    arrow = ('<svg class="board-arrow" viewBox="0 0 8 8" aria-hidden="true">'
             '<defs><marker id="tip" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto">'
             '<path class="arrow-tip" d="M0 0L10 5L0 10z"/></marker></defs>'
             '<line x1="4.5" y1="3.5" x2="3.78" y2="2.78" class="arrow-line" marker-end="url(#tip)"/>'
             '</svg>')
    return f"""<figure class="board-card" aria-label="An en passant capture on the board">
        <div class="board-wrap">
          <div class="board">
            <div class="ranks">{ranks}</div>
            <div class="squares">{''.join(cells)}{arrow}</div>
            <span></span>
            <div class="files">{files}</div>
          </div>
        </div>
        <figcaption class="board-cap">Black plays <b>d7–d5</b>, and White's pawn on e5 takes it <b>en passant</b>, landing on d6.</figcaption>
      </figure>"""


FEATURES = [
    ("live", "Live", "Live boards", "Top games as they happen, with the engine's view, both clocks and rating changes the moment a game ends.", "Planned"),
    ("events", "Odds", "Tournament odds", "Each player's chance of winning an event, simulated again after every game.", "Planned"),
    ("rankings", "FIDE", "Rankings", "The FIDE top 100 in standard, rapid and blitz: open, women, juniors, girls and the India list.", "New"),
    ("players", "Players", "Player pages", "Rating history, peak, opening fingerprint and how each player handles the clock.", "Planned"),
    ("prodigies", "Juniors", "Prodigy tracker", "Today's juniors against the greats, rating by rating at the same age.", "Planned"),
    ("compare", "H2H", "Head to head", "Two players side by side: ratings, peaks and their record against each other.", "Planned"),
    ("match", "You", "Play like a GM", "Type a Lichess username to see which top player your openings are closest to.", "Planned"),
    ("upsets", "Upsets", "Upset tracker", "The biggest wins by the lower-rated player, by month and by event.", "Planned"),
    ("spirit", "Spirit", "Fighting spirit", "Who fights on in classical chess, and who takes the quick draw.", "Planned"),
]


def top_ten(data):
    if not data:
        return ""
    return f"""  <section class="wrap block" aria-labelledby="top-ten">
    <div class="block-head"><h2 id="top-ten">World top 10</h2><a class="text-link" href="/rankings">Full rankings</a></div>
    <p class="label intro">Standard, FIDE rating list, {esc(data['period'])}</p>
    <div class="table-box">
      <table class="short">
        <thead><tr><th scope="col">#</th><th scope="col">Player</th><th scope="col">Fed</th><th scope="col" class="num">Rating</th></tr></thead>
        <tbody>
{rank_rows(data['lists']['standard']['open'][:10], short=True)}
        </tbody>
      </table>
    </div>
  </section>
"""


def home(data=None):
    desc = ("Live top chess games with the engine's view and both clocks, FIDE rankings, tournament odds "
            "updated after every game, player pages and a prodigy tracker.")
    cards = []
    for slug, kind, name, text, status in FEATURES:
        pill = "pill pill-next" if status in ("Next", "New") else "pill"
        cards.append(f"""      <a class="fcard" href="/{slug}">
        <div class="fcard-top"><span class="fcard-kind">{kind.upper()}</span><span class="{pill}">{status}</span></div>
        <span class="fcard-name">{name}</span>
        <p class="fcard-text">{text}</p>
      </a>""")
    body = f"""
<main id="main" tabindex="-1">
  <section class="wrap hero">
    <div class="hero-copy">
      <p class="label">Top-level chess, followed move by move</p>
      <h1 class="hero-title">Every game, every clock, every rating point.</h1>
      <p class="lede">Live boards from the big events, FIDE rankings, each player's chance of winning a tournament after every round, and the numbers behind how the best players actually play.</p>
      <div class="cta">
        <a class="btn btn-solid" href="/rankings">See the rankings</a>
        <a class="btn btn-quiet" href="/live">Live boards</a>
      </div>
    </div>
    {board()}
  </section>

{top_ten(data)}
  <section class="wrap block" aria-labelledby="whats-here">
    <div class="block-head"><h2 id="whats-here">What's here</h2></div>
    <p class="label intro">The site is being built one part at a time. Rankings are up, the rest follows.</p>
    <div class="features">
{chr(10).join(cards)}
    </div>
  </section>
</main>
"""
    return head(f"{NAME} · Live chess, FIDE rankings and tournament odds", desc, "/") + header(None) + body + FOOTER


def page(slug):
    p = PAGES[slug]
    plan = "\n".join(f"          <li>{esc(x)}</li>" for x in p["plan"])
    body = f"""
<main id="main" tabindex="-1">
  <section class="wrap page-head">
    <h1 class="page-title">{esc(p['head'])}</h1>
    <p class="lede">{esc(p['lede'])}</p>
  </section>
  <section class="wrap block">
    <div class="soon">
      <div class="panel">
        <h2 class="panel-title">What this page will show</h2>
        <ul class="plan">
{plan}
        </ul>
      </div>
      <div class="panel">
        <h2 class="panel-title">Where it's at</h2>
        <p class="panel-note">This page is still being built. It fills in as its data comes online, so it's worth checking back.</p>
        <div class="cta back-row"><a class="btn btn-quiet" href="/">Back to the homepage</a></div>
      </div>
    </div>
  </section>
</main>
"""
    return head(f"{p['title']} · {NAME}", p["desc"], f"/{slug}") + header(slug) + body + FOOTER


def rankings(data):
    p = PAGES["rankings"]
    if not data:
        return page("rankings")
    controls = "".join(
        f'<button type="button" class="seg-btn{" on" if c == "standard" else ""}" aria-pressed="{str(c == "standard").lower()}" data-tc="{c}">{c.title()}</button>'
        for c in ("standard", "rapid", "blitz"))
    lists = "".join(
        f'<button type="button" class="chip{" on" if l == "open" else ""}" aria-pressed="{str(l == "open").lower()}" data-list="{l}">{n}</button>'
        for l, n in (("open", "Open"), ("women", "Women"), ("juniors", "Juniors"), ("girls", "Girls"), ("india", "India")))
    body = f"""
<main id="main" tabindex="-1">
  <section class="wrap page-head">
    <h1 class="page-title">{esc(p['head'])}</h1>
    <p class="lede">The FIDE top 100 in standard, rapid and blitz, for the open list, women, juniors, girls and India. Only active players are ranked, the same as FIDE's own lists.</p>
  </section>
  <section class="wrap block">
    <div class="rank-bar">
      <div class="seg" role="group" aria-label="Time control">{controls}</div>
      <div class="chips" role="group" aria-label="Which list">{lists}</div>
    </div>
    <p class="label rank-note" id="rank-note">Standard · Open · FIDE rating list, {esc(data['period'])} · active players only</p>
    <div class="table-box">
      <table class="rank">
        <thead><tr><th scope="col">#</th><th scope="col" data-col="move" hidden>Move</th><th scope="col">Player</th><th scope="col">Fed</th><th scope="col" class="num">Rating</th><th scope="col" class="num">Games</th><th scope="col" class="num">Born</th></tr></thead>
        <tbody id="rank-body">
{rank_rows(data['lists']['standard']['open'])}
        </tbody>
      </table>
    </div>
    <p class="label fine">Games is the number of rated games in the last rating period. Juniors are players turning 20 or younger this year. Who moved up or down shows from the next monthly list on.</p>
  </section>
</main>
"""
    return head(f"{p['title']} · {NAME}", p["desc"], "/rankings") + header("rankings") + body + footer("rankings.js")


def not_found():
    body = """
<main id="main" tabindex="-1">
  <section class="wrap page-head lost">
    <h1 class="page-title">Illegal move.</h1>
    <p class="lede">This page isn't on the board. The homepage has everything the site covers so far.</p>
    <div class="cta"><a class="btn btn-solid" href="/">Back to the homepage</a></div>
  </section>
</main>
"""
    return head(f"Not found · {NAME}", "Live chess, FIDE rankings and tournament odds.", "/404") + header(None) + body + FOOTER


def write():
    data = rankings_data()
    files = {"index.html": home(data), "404.html": not_found()}
    files.update({f"{slug}.html": page(slug) for slug in PAGES})
    files["rankings.html"] = rankings(data)
    for name, text in files.items():
        (SITE / name).write_text(text, encoding="utf-8", newline="\n")
    return sorted(files)


if __name__ == "__main__":
    for name in write():
        print(name)
