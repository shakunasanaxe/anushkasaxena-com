#!/usr/bin/env python3
"""Pre-render hook: generate listing HTML + live stats from data/*.json.

Edit data/*.json to add publications/media/quotes — everything else
(numbering, counts, homepage Latest section) updates automatically.
New entries go at the TOP of the relevant JSON array.
"""
import json
import html as H
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
INC = ROOT / "_includes"
INC.mkdir(exist_ok=True)

def load(name):
    return json.loads((DATA / f"{name}.json").read_text())

def raw(content):
    """Wrap in a pandoc raw-html block so markdown parsing never touches it."""
    return "```{=html}\n" + content + "\n```\n"

def esc(s):
    return H.escape(s or "", quote=True)

VISIBLE = 20

def pub_list(items, list_id):
    out = [f'<div class="pub-list" id="{list_id}">']
    for i, it in enumerate(items, 1):
        hid = " hidden" if i > VISIBLE else ""
        year = f'<span class="year">{it["year"]}</span>' if it.get("year") else ""
        out.append(
            f'<div class="pub-card{hid}"><div class="pub-number">{i}</div>'
            f'<div class="pub-info"><h3><a href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["title"])}</a></h3>'
            f'<div class="pub-meta">{esc(it["source"])}{year}</div></div></div>'
        )
    out.append("</div>")
    out.append('<div class="load-more-wrap"><button class="load-more" type="button">Load more</button></div>')
    return "\n".join(out)

def media_grid(items):
    out = ['<div class="media-grid" id="media-list">']
    for i, it in enumerate(items, 1):
        hid = " hidden" if i > 12 else ""
        badge = it.get("type", "video")
        thumb = ""
        if it.get("youtube_id"):
            thumb = f'<img class="thumb-img" src="https://img.youtube.com/vi/{it["youtube_id"]}/hqdefault.jpg" alt="" loading="lazy">'
        out.append(
            f'<a class="media-card{hid}" href="{esc(it["url"])}" target="_blank" rel="noopener">'
            f'<div class="media-thumb">{thumb}<div class="play-icon">&#9654;</div>'
            f'<span class="type-badge {badge}">{badge.capitalize()}</span></div>'
            f'<div class="media-body"><h3>{esc(it["title"])}</h3>'
            f'<div class="source">{esc(it["source"])}</div></div></a>'
        )
    out.append("</div>")
    out.append('<div class="load-more-wrap"><button class="load-more" type="button">Load more</button></div>')
    return "\n".join(out)

def quotes_grid(items):
    out = ['<div class="quotes-grid" id="quotes-list">']
    for i, it in enumerate(items, 1):
        hid = " hidden" if i > 12 else ""
        out.append(
            f'<a class="quote-card{hid}" href="{esc(it["url"])}" target="_blank" rel="noopener">'
            f'<h3>{esc(it["title"])}</h3><div class="source">{esc(it["source"])}</div></a>'
        )
    out.append("</div>")
    out.append('<div class="load-more-wrap"><button class="load-more" type="button">Load more</button></div>')
    return "\n".join(out)

def talks_grid(items):
    out = ['<div class="talks-grid">']
    for it in items:
        ph = " placeholder" if it.get("placeholder") else ""
        photo = ""
        if it.get("youtube_id"):
            photo = f'<img src="https://img.youtube.com/vi/{it["youtube_id"]}/hqdefault.jpg" alt="" loading="lazy">'
        elif it.get("photo"):
            photo = f'<img src="{esc(it["photo"])}" alt="" loading="lazy">'
        link_open = link_close = ""
        if it.get("url"):
            link_open = f'<a href="{esc(it["url"])}" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;">'
            link_close = "</a>"
        out.append(
            f'<article class="talk-card{ph}">{link_open}'
            f'<div class="talk-photo">{photo}<span class="talk-badge">{esc(it.get("badge","Talk"))}</span></div>'
            f'<div class="talk-body"><div class="talk-meta"><span class="talk-venue">{esc(it.get("venue",""))}</span>'
            f' &middot; <span class="talk-date">{esc(it.get("date",""))}</span></div>'
            f'<h3>{esc(it["title"])}</h3><p>{esc(it.get("description",""))}</p></div>{link_close}</article>'
        )
    out.append("</div>")
    return "\n".join(out)

def latest_band(short, long_):
    out = ['<div class="quotes-grid">']
    for it in short[:2]:
        out.append(
            f'<a class="quote-card" href="{esc(it["url"])}" target="_blank" rel="noopener">'
            f'<h3>{esc(it["title"])}</h3><div class="source">Op-ed &middot; {esc(it["source"])}</div></a>'
        )
    for it in long_[:1]:
        out.append(
            f'<a class="quote-card" href="{esc(it["url"])}" target="_blank" rel="noopener">'
            f'<h3>{esc(it["title"])}</h3><div class="source">Research &middot; {esc(it["source"])}</div></a>'
        )
    out.append("</div>")
    return "\n".join(out)

short = load("shortform")
long_ = load("longform")
media = load("media")
quotes = load("quotes")
talks = load("talks") if (DATA / "talks.json").exists() else []

(INC / "shortform.html").write_text(raw(pub_list(short, "short-form-list")))
(INC / "longform.html").write_text(raw(pub_list(long_, "long-form-list")))
(INC / "media.html").write_text(raw(media_grid(media)))
(INC / "quotes.html").write_text(raw(quotes_grid(quotes)))
(INC / "talks.html").write_text(raw(talks_grid(talks)))
(INC / "latest.html").write_text(raw(latest_band(short, long_)))

# Live stats for homepage hero
n_media = len(media) + len(quotes)
stats = (
    f'<div class="hero-stats">'
    f'<div class="stat"><b>{len(long_)}</b><span>Papers</span></div>'
    f'<div class="stat"><b>{len(short)}</b><span>Articles</span></div>'
    f'<div class="stat"><b>{n_media}</b><span>Media</span></div>'
    f'</div>'
)
(INC / "herostats.html").write_text(raw(stats))

print(f"includes built: short={len(short)} long={len(long_)} media={len(media)} quotes={len(quotes)} talks={len(talks)}")
