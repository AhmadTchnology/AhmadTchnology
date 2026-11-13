#!/usr/bin/env python3
"""Builds profile.svg: the whole GitHub profile as ONE animated SVG widget.

Run locally:   python scripts/build_profile.py
With real contribution data: set GH_TOKEN (the GitHub Action does this for you).
"""
import json, math, os, sys, urllib.request
from datetime import date
from xml.sax.saxutils import escape as esc

USER = os.environ.get("GH_USER", "AhmadTchnology")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT_PATH", os.path.join(HERE, "..", "profile.svg"))

BG, BG2, TRACE, TEAL, GOLD = "#0B1E2D", "#0F2F3F", "#1F6272", "#5EEAD4", "#FFC857"
TEXT, MUTED, SOFT = "#E8F1F2", "#8FB3BB", "#9CC3CB"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
W = 1000

HEADER_INNER = r"""<defs>
    <linearGradient id="board" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0B1E2D"/>
      <stop offset="1" stop-color="#0A2D38"/>
    </linearGradient>
    <pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#5EEAD4" opacity="0.10"/>
    </pattern>
    <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <path id="t1" d="M0 36 H400 L440 76 H690 L734 120 H770"/>
    <path id="t2" d="M0 268 H640 L728 180 H770"/>
    <path id="t3" d="M920 90 H960 L1000 50"/>
    <path id="t4" d="M920 180 H950 L980 210 H1000"/>
    <path id="t5" d="M560 170 H620 L640 150 H770"/>
  </defs>

  <rect width="1000" height="300" fill="url(#board)"/>
  <rect width="1000" height="300" fill="url(#dots)"/>

  <!-- copper traces -->
  <g fill="none" stroke="#1F6272" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
    <use href="#t1" xlink:href="#t1"/>
    <use href="#t2" xlink:href="#t2"/>
    <use href="#t3" xlink:href="#t3"/>
    <use href="#t4" xlink:href="#t4"/>
    <use href="#t5" xlink:href="#t5"/>
  </g>

  <!-- vias -->
  <g fill="#0B1E2D" stroke="#1F6272" stroke-width="3">
    <circle cx="560" cy="170" r="6"/>
    <circle cx="1000" cy="50" r="6"/>
    <circle cx="1000" cy="210" r="6"/>
  </g>

  <!-- chip -->
  <g>
    <g stroke="#5EEAD4" stroke-width="3" stroke-linecap="round" opacity="0.8">
      <path d="M758 90H770M758 120H770M758 150H770M758 180H770"/>
      <path d="M920 90H932M920 120H932M920 150H932M920 180H932"/>
      <path d="M800 58V70M830 58V70M860 58V70M890 58V70"/>
      <path d="M800 220V232M830 220V232M860 220V232M890 220V232"/>
    </g>
    <rect x="770" y="70" width="150" height="150" rx="12" fill="#0F2F3F" stroke="#5EEAD4" stroke-width="2.5"/>
    <rect x="786" y="86" width="118" height="118" rx="8" fill="none" stroke="#5EEAD4" stroke-width="1.5" opacity="0.45">
      <animate attributeName="opacity" values="0.2;0.8;0.2" dur="3.2s" repeatCount="indefinite"/>
    </rect>
    <text x="845" y="159" text-anchor="middle" font-family="'SFMono-Regular',Consolas,'Liberation Mono',monospace" font-size="44" font-weight="700" fill="#E8F1F2">UT</text>
    <circle cx="790" cy="90" r="3.5" fill="#FFC857">
      <animate attributeName="opacity" values="1;0.15;1" dur="1.6s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- signal pulses travelling along the traces -->
  <g filter="url(#glow)" fill="#FFC857">
    <circle r="4"><animateMotion dur="4.5s" repeatCount="indefinite" begin="0s"><mpath href="#t1" xlink:href="#t1"/></animateMotion></circle>
    <circle r="4"><animateMotion dur="4.5s" repeatCount="indefinite" begin="-2.2s"><mpath href="#t1" xlink:href="#t1"/></animateMotion></circle>
    <circle r="4"><animateMotion dur="5s" repeatCount="indefinite" begin="-1s"><mpath href="#t2" xlink:href="#t2"/></animateMotion></circle>
    <circle r="4"><animateMotion dur="5s" repeatCount="indefinite" begin="-3.5s"><mpath href="#t2" xlink:href="#t2"/></animateMotion></circle>
  </g>
  <g filter="url(#glow)" fill="#5EEAD4">
    <circle r="3.5"><animateMotion dur="2.4s" repeatCount="indefinite" begin="-0.5s"><mpath href="#t3" xlink:href="#t3"/></animateMotion></circle>
    <circle r="3.5"><animateMotion dur="2.6s" repeatCount="indefinite" begin="-1.2s"><mpath href="#t4" xlink:href="#t4"/></animateMotion></circle>
    <circle r="3.5"><animateMotion dur="3.2s" repeatCount="indefinite" begin="-0.2s"><mpath href="#t5" xlink:href="#t5"/></animateMotion></circle>
  </g>

  <!-- name block -->
  <text x="50" y="108" font-family="'SFMono-Regular',Consolas,'Liberation Mono',monospace" font-size="22" fill="#5EEAD4">
    hello, I'm
  </text>
  <text x="46" y="182" font-family="'Segoe UI','Helvetica Neue',Arial,sans-serif" font-size="88" font-weight="800" letter-spacing="-2" fill="#E8F1F2">
    Ahmed
  </text>

  <!-- rotating subtitle -->
  <g font-family="'Segoe UI','Helvetica Neue',Arial,sans-serif" font-size="24" fill="#FFC857">
    <text x="50" y="228" opacity="1">University student and full-stack developer
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.23;0.25;1" dur="14s" repeatCount="indefinite" begin="0s"/>
    </text>
    <text x="50" y="228" opacity="0">Embedded systems and AI on ESP32 and Raspberry Pi
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.25;0.27;0.48;0.50;1" dur="14s" repeatCount="indefinite" begin="0s"/>
    </text>
    <text x="50" y="228" opacity="0">Web apps, devices, and everything between
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.50;0.52;0.73;0.75;1" dur="14s" repeatCount="indefinite" begin="0s"/>
    </text>
    <text x="50" y="228" opacity="0">Learning by building
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.75;0.77;0.98;1;1" dur="14s" repeatCount="indefinite" begin="0s"/>
    </text>
  </g>"""

LINKS = [("LinkedIn", 190), ("Instagram", 190), ("Portfolio", 190), ("ahmadalkirsan@gmail.com", 320)]

PROJECTS = [
    ("CYD iPod", TEAL, ["An iPod-style music player on the ESP32 Cheap Yellow", "Display, with an SD card library and Bluetooth audio."], "C++, ESP32, TFT_eSPI"),
    ("uTune Jukebox", TEAL, ["Tap an RFID card that stores a YouTube link and the", "track joins the play queue."], "Python, Pygame, mpv, SQLite"),
    ("Smart Assistive Glasses", TEAL, ["Wearable device for deaf, mute, and blind users with", "sign and speech recognition on a Raspberry Pi 5."], "Python, LSTM, MediaPipe, Pi 5"),
    ("PSP YouTube Client", TEAL, ["Homebrew YouTube app for the PSP, fed by a one-click", "PC relay server that transcodes video."], "Python, yt-dlp, ffmpeg, C"),
    ("Lecture Management System", TEAL, ["A platform for universities to manage and deliver", "lectures."], "React, TypeScript, Firebase, Cloudflare R2"),
    ("More experiments", GOLD, ["Air Guitar Gloves, MeshRide, MidTune, an ESP32-S3 RFID", "storage device, and procedural Blender scenes."], "Full list at ahmedtech.engineer"),
]

STACK = [
    ("Web", ["TypeScript", "React", "Next.js", "Node.js", "JavaScript", "Tailwind CSS", "ShadCN", "Bootstrap"]),
    ("Backend and cloud", ["Firebase", "PostgreSQL", "MongoDB", "Docker", "Cloudflare"]),
    ("Embedded and systems", ["C", "C++", "Python", "Arduino", "ESP32", "Raspberry Pi", "Linux"]),
    ("Mobile, games, and 3D", ["Flutter", "Kotlin", "Android", "C#", "Unity", "Unreal Engine", "Blender"]),
]

ABOUT = ["I build practical systems that solve real problems, especially in education and",
         "university life. Most of my work sits where software meets hardware, and I learn",
         "by building. Everything ships under the Utopia Tech name."]


def fetch_contributions():
    token = os.environ.get("GH_TOKEN")
    if not token:
        return None
    query = ('query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{'
             'totalContributions weeks{contributionDays{contributionCount date}}}}}}')
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"u": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-widget"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def section(y, title):
    end = 70 + int(len(title) * 16.5) + 24
    path = f"M{end} 28 H{W-130} L{W-106} 14 H{W-74}"
    return (f'<g transform="translate(20,{y})">'
        f'<g stroke="{TEAL}" stroke-width="2" stroke-linecap="round"><path d="M4 20H10M4 36H10M46 20H52M46 36H52M18 4V10M34 4V10M18 46V52M34 46V52" opacity="0.8"/></g>'
        f'<rect x="10" y="10" width="36" height="36" rx="6" fill="{BG2}" stroke="{TEAL}" stroke-width="2"/>'
        f'<rect x="19" y="19" width="18" height="18" rx="3" fill="none" stroke="{TEAL}" stroke-width="1.5" opacity="0.5"><animate attributeName="opacity" values="0.2;0.9;0.2" dur="3.2s" repeatCount="indefinite"/></rect>'
        f'<text x="70" y="38" font-family="{SANS}" font-size="28" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
        f'<path d="{path}" fill="none" stroke="{TRACE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="{W-70}" cy="14" r="5" fill="{BG}" stroke="{TRACE}" stroke-width="3"/>'
        f'<circle r="4" fill="{GOLD}" filter="url(#g)"><animateMotion dur="4s" repeatCount="indefinite" path="{path}"/></circle></g>')


def pills(y):
    gap = 14
    total = sum(w for _, w in LINKS) + gap * (len(LINKS) - 1)
    x = (W - total) / 2
    out = ""
    for i, (label, w) in enumerate(LINKS):
        out += (f'<g transform="translate({x:.0f},{y})">'
                f'<rect x="1" y="1" width="{w-2}" height="46" rx="16" fill="{BG}" stroke="{TRACE}" stroke-width="2"/>'
                f'<circle cx="26" cy="24" r="5" fill="{TEAL}" filter="url(#g)"><animate attributeName="opacity" values="1;0.25;1" dur="{2+i*0.4}s" repeatCount="indefinite"/></circle>'
                f'<text x="44" y="30" font-family="{MONO}" font-size="16" fill="{TEXT}">{esc(label)}</text></g>')
        x += w + gap
    return out


def about(y):
    out = ""
    for i, line in enumerate(ABOUT):
        out += f'<text x="40" y="{y + 20 + i*34}" font-family="{SANS}" font-size="21" fill="{TEXT if i == 0 else "#B9CFD3"}">{esc(line)}</text>'
    return out


def projects(y):
    cw, ch, gap = 470, 160, 20
    out = ""
    for i, (name, led, desc, stack) in enumerate(PROJECTS):
        cx = 20 + (i % 2) * (cw + gap)
        cy = y + (i // 2) * (ch + 14)
        out += (f'<g transform="translate({cx},{cy})">'
                f'<rect x="1" y="1" width="{cw-2}" height="{ch-2}" rx="16" fill="{BG}" stroke="{TRACE}" stroke-width="2"/>'
                f'<circle cx="32" cy="36" r="5.5" fill="{led}" filter="url(#g)"><animate attributeName="opacity" values="1;0.25;1" dur="{1.8+0.3*i}s" repeatCount="indefinite"/></circle>'
                f'<text x="50" y="42" font-family="{MONO}" font-size="19" font-weight="700" fill="{TEXT}">{esc(name)}</text>')
        for j, line in enumerate(desc):
            out += f'<text x="30" y="{78+j*24}" font-family="{SANS}" font-size="15.5" fill="{SOFT}">{esc(line)}</text>'
        out += (f'<text x="30" y="136" font-family="{MONO}" font-size="13.5" fill="{led}">{esc(stack)}</text>'
                f'<circle r="3.5" fill="{GOLD}" filter="url(#g)"><animateMotion dur="5s" begin="-{i*0.8}s" repeatCount="indefinite" path="M20 {ch-2} H{cw-20}"/></circle></g>')
    rows = math.ceil(len(PROJECTS) / 2)
    return out, rows * ch + (rows - 1) * 14


def stack(y):
    pad_x = 50
    yy, body = 40, ""
    for label, items in STACK:
        body += f'<text x="{pad_x}" y="{yy}" font-family="{SANS}" font-size="16" font-weight="600" fill="{MUTED}">{esc(label)}</text>'
        x, cy = pad_x, yy + 14
        for it in items:
            cw = int(len(it) * 9.0 + 28)
            if x + cw > W - 50:
                x, cy = pad_x, cy + 44
            body += (f'<rect x="{x}" y="{cy}" width="{cw}" height="32" rx="8" fill="{BG2}" stroke="{TRACE}" stroke-width="1.5"/>'
                     f'<text x="{x+14}" y="{cy+21}" font-family="{MONO}" font-size="14.5" fill="{TEXT}">{esc(it)}</text>')
            x += cw + 10
        yy = cy + 32 + 34
    h = yy - 10
    out = (f'<g transform="translate(0,{y})"><rect x="21" y="1" width="{W-42}" height="{h-2}" rx="16" fill="{BG}" stroke="{TRACE}" stroke-width="2"/>{body}'
           f'<circle r="4" fill="{TEAL}" filter="url(#g)"><animateMotion dur="7s" repeatCount="indefinite" path="M40 {h-2} H{W-40}"/></circle></g>')
    return out, h


def contributions(y, cal):
    cell, gap = 13, 4
    pitch = cell + gap
    weeks = cal["weeks"] if cal else [{"contributionDays": [{"contributionCount": 0, "date": ""} for _ in range(7)]} for _ in range(53)]
    maxc = max([d["contributionCount"] for w in weeks for d in w["contributionDays"]] + [1])
    ramp = ["#10303F", "#14565F", "#1E8C88", "#3FC9B5", TEAL]
    gw = len(weeks) * pitch - gap
    x0 = (W - gw) / 2
    panel_h = 230
    out = (f'<g transform="translate(0,{y})"><rect x="21" y="1" width="{W-42}" height="{panel_h-2}" rx="16" fill="{BG}" stroke="{TRACE}" stroke-width="2"/>'
           f'<clipPath id="gridclip"><rect x="{x0-2:.0f}" y="44" width="{gw+4}" height="{7*pitch}"/></clipPath>')
    last_month = None
    for wi, wk in enumerate(weeks):
        days = wk["contributionDays"]
        if days and days[0]["date"]:
            m = int(days[0]["date"][5:7])
            if m != last_month:
                label = date(2000, m, 1).strftime("%b")
                out += f'<text x="{x0 + wi*pitch:.0f}" y="36" font-family="{SANS}" font-size="13" fill="{MUTED}">{label}</text>'
                last_month = m
        for di, d in enumerate(days):
            c = d["contributionCount"]
            lvl = 0 if c == 0 else min(4, max(1, math.ceil(4 * c / maxc)))
            out += f'<rect x="{x0 + wi*pitch:.0f}" y="{44 + di*pitch}" width="{cell}" height="{cell}" rx="3" fill="{ramp[lvl]}"/>'
    out += (f'<g clip-path="url(#gridclip)"><rect y="44" width="60" height="{7*pitch}" fill="{GOLD}" opacity="0.16">'
            f'<animate attributeName="x" values="{x0-60:.0f};{x0+gw:.0f}" dur="9s" repeatCount="indefinite"/></rect></g>')
    total = cal["totalContributions"] if cal else None
    caption = f"{total:,} contributions in the last year" if total is not None else "Contribution graph refreshes daily"
    out += f'<text x="{x0:.0f}" y="{44 + 7*pitch + 34}" font-family="{SANS}" font-size="15" fill="{SOFT}">{esc(caption)}</text>'
    lx = x0 + gw - (5 * pitch + 62)
    out += f'<text x="{lx - 34:.0f}" y="{44 + 7*pitch + 33}" font-family="{SANS}" font-size="13" fill="{MUTED}">Less</text>'
    for i, col in enumerate(ramp):
        out += f'<rect x="{lx + i*pitch:.0f}" y="{44 + 7*pitch + 21}" width="{cell}" height="{cell}" rx="3" fill="{col}"/>'
    out += f'<text x="{lx + 5*pitch + 4:.0f}" y="{44 + 7*pitch + 33}" font-family="{SANS}" font-size="13" fill="{MUTED}">More</text></g>'
    return out, panel_h


def footer(y):
    L, R = "M20 45 H200 L224 25 H270", "M980 45 H800 L776 25 H730"
    return (f'<g transform="translate(0,{y})">'
            f'<path d="{L}" fill="none" stroke="{TRACE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{R}" fill="none" stroke="{TRACE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text x="500" y="52" text-anchor="middle" font-family="{SANS}" font-size="24" font-weight="600" fill="{TEXT}">Always learning, always building.</text>'
            f'<circle r="4" fill="{GOLD}" filter="url(#g)"><animateMotion dur="4s" repeatCount="indefinite" path="{L}"/></circle>'
            f'<circle r="4" fill="{TEAL}" filter="url(#g)"><animateMotion dur="4s" begin="-2s" repeatCount="indefinite" path="{R}"/></circle></g>'), 90


def build():
    try:
        cal = fetch_contributions()
    except Exception as exc:  # keep the previous widget instead of wiping the graph
        print("Could not fetch contributions:", exc, file=sys.stderr)
        if os.path.exists(OUT):
            sys.exit(1)
        cal = None

    y = 300
    parts = []
    y += 22; parts.append(pills(y)); y += 48 + 32
    parts.append(section(y, "About")); y += 56 + 16
    parts.append(about(y)); y += 20 + 2 * 34 + 30
    parts.append(section(y, "Projects")); y += 56 + 18
    body, h = projects(y); parts.append(body); y += h + 30
    parts.append(section(y, "Tech stack")); y += 56 + 18
    body, h = stack(y); parts.append(body); y += h + 30
    parts.append(section(y, "Activity")); y += 56 + 18
    body, h = contributions(y, cal); parts.append(body); y += h + 20
    body, h = footer(y); parts.append(body); y += h
    H = y

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">'
           f'<title id="t">Ahmed, university student and full-stack developer</title>'
           f'<desc id="d">Profile widget: about, projects (CYD iPod, uTune Jukebox, Smart Assistive Glasses, PSP YouTube Client, Lecture Management System), tech stack, and contribution activity.</desc>'
           f'<defs><clipPath id="clip"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
           f'<filter id="g" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
           f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="{BG}"/>'
           f'<g>{HEADER_INNER}</g>' + "".join(parts) + '</g>'
           f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="none" stroke="{TRACE}" stroke-width="2"/></svg>')
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", os.path.abspath(OUT), f"({W}x{H})", "with live contributions" if cal else "with empty contribution grid")


if __name__ == "__main__":
    build()
