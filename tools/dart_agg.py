#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aggregate app.so Dart strings: domains, urls, channel names, storage keys."""
import re, json, sys
from pathlib import Path
from collections import Counter

d = Path(sys.argv[1])
lines = (d / "app_iso_strings.txt").read_text(encoding="utf-8", errors="replace").splitlines()
toks = []
for ln in lines:
    if "\t" in ln:
        toks.append(ln.split("\t", 1)[1])
print("tokens:", len(toks))

dom = Counter()
for t in toks:
    for m in re.finditer(r"\b((?:[a-z0-9][a-z0-9-]*\.)+(?:com|cn|net|org|io|qq\.com|weixin\.qq\.com|woa\.com|myqcloud\.com|tencent\.com|qq\.com)\b)", t):
        dom[m.group(1)] += 1
print("\n=== DOMAINS (top 60) ===")
for k, v in dom.most_common(60):
    print(f"{v:4d}  {k}")

print("\n=== URLs ===")
urls = sorted({m.group(0) for t in toks for m in re.finditer(r"https?://[^\s\"'<>\\]+", t)})
for u in urls:
    print(" ", u)

print("\n=== channel-like names ===")
chan = sorted({t for t in toks if re.match(r"^[a-z][a-zA-Z0-9_]*(Channel|channel)$", t) or re.match(r"^(com|cn)\.[a-z0-9.]+$", t)})
for c in chan:
    print(" ", c)

print("\n=== KV / storage keys (dotted or snake, len>=6) ===")
kv = sorted({t for t in toks if re.match(r"^[a-zA-Z][a-zA-Z0-9_.]{5,60}$", t) and ("." in t or "_" in t) and not t.startswith("package:") and not t.startswith("dart:") and "/" not in t})
print("count:", len(kv))
Path(sys.argv[2]).write_text("\n".join(kv), encoding="utf-8")

print("\n=== event/ipc names ===")
ev = sorted({t for t in toks if re.match(r"^[a-z][a-z0-9_]{3,40}$", t) and ("_" in t)})
Path(sys.argv[3]).write_text("\n".join(ev), encoding="utf-8")
print("snake ids:", len(ev))
