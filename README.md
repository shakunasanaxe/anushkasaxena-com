# anushkasaxena.com

Personal website of Anushka Saxena, built with [Quarto](https://quarto.org).

## Updating content

All content lives in `data/*.json` (newest entries first):

- `shortform.json` — op-eds & commentary
- `longform.json` — research papers & book chapters
- `media.json` — video & podcast appearances (`youtube_id` gives the card a thumbnail)
- `quotes.json` — media quotes & mentions
- `talks.json` — talks & lectures (photo, venue, date, description)

Then render and deploy:

```sh
quarto render
quarto publish gh-pages --no-render
```

Numbering, homepage counts, and the "Recent Work" section update automatically
(`scripts/build_includes.py` runs as a pre-render hook).

The site is served by GitHub Pages from the `gh-pages` branch; `main` holds the source.
