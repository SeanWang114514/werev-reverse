#!/usr/bin/env python3
"""Bootstrap PyPI wheels without pip (pip's vendored cachecontrol is broken)."""
import json, sys, os, io, zipfile, urllib.request, site, sysconfig

PKGS = sys.argv[1:] or ["capstone", "lief", "pyelftools"]
DEST = sysconfig.get_paths()["purelib"]
print("DEST =", DEST)

def pick(urls):
    for u in urls:
        n = u["filename"]
        if n.endswith(".whl") and ("win_amd64" in n or "none-any" in n) and "cp3" not in n.split("-")[2]:
            return u
    for u in urls:
        n = u["filename"]
        if n.endswith(".whl") and ("win_amd64" in n or "none-any" in n):
            return u
    return None

for pkg in PKGS:
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{pkg}/json", timeout=30) as r:
            meta = json.load(r)
        cand = pick(meta["urls"])
        if not cand:
            print(f"[{pkg}] no suitable wheel"); continue
        print(f"[{pkg}] -> {cand['filename']}")
        with urllib.request.urlopen(cand["url"], timeout=120) as r:
            blob = r.read()
        z = zipfile.ZipFile(io.BytesIO(blob))
        z.extractall(DEST)
        print(f"[{pkg}] installed {len(z.namelist())} entries")
    except Exception as e:
        print(f"[{pkg}] FAILED: {e}")
