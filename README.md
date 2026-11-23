# EnPassant

A site for top-level chess. Live boards from the big events, FIDE rankings, each player's chance of winning a tournament after every round, and the numbers behind how the best players actually play.

I'm building it one part at a time. Right now it's the base design: the homepage and the outline of every page, in the same two looks as my other projects (Port Mafia dark, Detective Agency light). Rankings come next.

## Running it locally

Everything is plain Python 3 with no packages to install.

```
python pipeline/pages.py              write the html pages into site/
python -m unittest discover -s tests  check the pages and their links
```

The site itself is just the `site/` folder, so any static server works for a look.

## Data

Ratings come from FIDE's monthly rating lists and games from Lichess broadcasts. Nothing is stored from Chess.com.
