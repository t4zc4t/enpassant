# EnPassant

A site for top-level chess. Live boards from the big events, FIDE rankings, each player's chance of winning a tournament after every round, and the numbers behind how the best players actually play.

I'm building it one part at a time. The base design is up in the same two looks as my other projects (Port Mafia dark, Detective Agency light), with an outline of every page. The rankings page has the FIDE top 100 in standard, rapid and blitz, for the open list, women, juniors, girls and India, and the homepage shows the world top 10.

## Running it locally

Everything is plain Python 3 with no packages to install.

```
python pipeline/fide.py               read FIDE's rating list into site/data/rankings.json
python pipeline/pages.py              write the html pages into site/
python -m unittest discover -s tests  check the pages and their links
```

The site itself is just the `site/` folder, so any static server works for a look.

## How the rankings stay up to date

FIDE publishes one combined file with every rated player, about 50 MB zipped. FIDE's server doesn't answer GitHub's machines, so a tiny Cloudflare Worker fetches the file and hands it over. A GitHub Action reads it that way once a day, keeps only active players (FIDE leaves inactive players out of its own top lists too) and writes the top 100 for each list. The rating list only changes at the start of the month, so most days the file comes out the same and nothing gets committed. When a new month's list lands, the old ranks are kept so the table can show who moved up or down.

## Data

Ratings come from FIDE's rating lists and games will come from Lichess broadcasts. Nothing is stored from Chess.com.
