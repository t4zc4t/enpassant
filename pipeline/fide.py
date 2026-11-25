"""FIDE's combined rating list -> site/data/rankings.json (top lists only)."""
import io
import json
import os
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree.ElementTree import iterparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "data" / "rankings.json"
URL = "https://ratings.fide.com/download/players_list_xml.zip"
# FIDE doesn't answer GitHub's servers, so the updater goes through our Worker
RELAY = os.environ.get("FIDE_RELAY")
AGENT = "EnPassant rankings (github.com/t4zc4t/enpassant)"
TOP = 100

CONTROLS = {"standard": "rating", "rapid": "rapid_rating", "blitz": "blitz_rating"}
GAMES = {"standard": "games", "rapid": "rapid_games", "blitz": "blitz_games"}
LISTS = ["open", "women", "juniors", "girls", "india"]


def fetch():
    req = urllib.request.Request(RELAY or URL, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(req, timeout=300) as r:
        stamp = r.headers.get("Last-Modified")
        body = r.read()
    when = parsedate_to_datetime(stamp) if stamp else datetime.now(timezone.utc)
    return body, when


def players(zipped):
    """every rated, active player, one dict each"""
    with zipfile.ZipFile(io.BytesIO(zipped)) as z:
        name = next(n for n in z.namelist() if n.endswith(".xml"))
        with z.open(name) as f:
            for _, el in iterparse(f):
                if el.tag != "player":
                    continue
                p = {c.tag: (c.text or "").strip() for c in el}
                el.clear()
                if "i" in p.get("flag", ""):      # inactive players aren't ranked
                    continue
                if not any(p.get(k, "0") not in ("", "0") for k in CONTROLS.values()):
                    continue
                yield p


def display_name(raw):
    # "Carlsen, Magnus" -> "Magnus Carlsen", one-word names stay as they are
    last, _, first = raw.partition(", ")
    return f"{first} {last}".strip() if first else raw


def row(p, control):
    born = p.get("birthday") or ""
    return {
        "id": int(p["fideid"]),
        "name": display_name(p["name"]),
        "title": p.get("title") or p.get("w_title") or "",
        "fed": p.get("country", ""),
        "rating": int(p[CONTROLS[control]]),
        "games": int(p.get(GAMES[control]) or 0),
        "born": int(born) if born.isdigit() else None,
    }


def build(people, period):
    junior_from = period.year - 20       # FIDE juniors: 20 or under during the list's year
    keep = {c: {l: [] for l in LISTS} for c in CONTROLS}
    for p in people:
        woman = p.get("sex") == "F"
        born = p.get("birthday") or ""
        junior = born.isdigit() and int(born) >= junior_from
        india = p.get("country") == "IND"
        for control, field in CONTROLS.items():
            if p.get(field, "0") in ("", "0"):
                continue
            r = row(p, control)
            wanted = {"open": True, "women": woman, "juniors": junior, "girls": junior and woman, "india": india}
            for name, yes in wanted.items():
                if yes:
                    keep[control][name].append(dict(r))   # own copy, each list has its own rank
    out = {}
    for control, lists in keep.items():
        out[control] = {}
        for name, rows in lists.items():
            rows.sort(key=lambda r: (-r["rating"], r["name"]))
            top = rows[:TOP]
            rank = 0
            for i, r in enumerate(top):
                # ties share a rank
                if i == 0 or r["rating"] != top[i - 1]["rating"]:
                    rank = i + 1
                r["rank"] = rank
            out[control][name] = top
    return out


def write(data, period, previous=None):
    """keeps last period's ranks so the next list can show who moved"""
    label = period.strftime("%B %Y")
    old = previous or {}
    if old.get("period") and old["period"] != label:
        before = {c: {l: {r["id"]: r["rank"] for r in rows} for l, rows in lists.items()}
                  for c, lists in old["lists"].items()}
        prev_period = old["period"]
    else:
        before = old.get("before", {})
        prev_period = old.get("previousPeriod")
    for control, lists in data.items():
        for name, rows in lists.items():
            ranks = before.get(control, {}).get(name, {})
            for r in rows:
                was = ranks.get(r["id"]) if ranks else None
                r["was"] = was if was is not None else (None if not ranks else 0)
    out = {"period": label, "previousPeriod": prev_period, "lists": data,
           "before": before, "source": "FIDE rating list"}
    text = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists() and OUT.read_text(encoding="utf-8") == text:
        return False
    OUT.write_text(text, encoding="utf-8")
    return True


def main(path=None):
    if path:
        body = Path(path).read_bytes()
        period = datetime.now(timezone.utc)
    else:
        body, period = fetch()
    previous = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else None
    data = build(players(body), period)
    changed = write(data, period, previous)
    print("rankings changed" if changed else "rankings unchanged")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
