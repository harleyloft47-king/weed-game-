#!/usr/bin/env python3
"""Builds the phone app (docs/) from strain-packs.html.

Run this after changing strain-packs.html:  python3 build-app.py
It writes docs/index.html and bumps the cache version in docs/sw.js so phones pick up the new version.
"""
import hashlib, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
game = open(os.path.join(HERE, "strain-packs.html"), encoding="utf-8").read()
game = game.replace("<title>Strain Packs</title>", "", 1)

head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Strain Packs</title>
<meta name="description" content="Open strain packs, grow, trim and sell in your bunker.">
<meta name="theme-color" content="#0c0e11">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Strain Packs">
<style>html,body{margin:0;background:#0c0e11}[hidden]{display:none!important}</style>
</head>
<body>
"""
tail = """
<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => { navigator.serviceWorker.register("sw.js").catch(() => {}); });
}
</script>
</body>
</html>
"""
html = head + game + tail
os.makedirs(os.path.join(HERE, "docs"), exist_ok=True)
open(os.path.join(HERE, "docs", "index.html"), "w", encoding="utf-8").write(html)

version = hashlib.sha1(html.encode("utf-8")).hexdigest()[:10]
sw_path = os.path.join(HERE, "docs", "sw.js")
sw = open(sw_path, encoding="utf-8").read()
sw = re.sub(r'const VERSION = "[^"]*";', f'const VERSION = "{version}";', sw, count=1)
open(sw_path, "w", encoding="utf-8").write(sw)
print("Built docs/index.html, version", version)
