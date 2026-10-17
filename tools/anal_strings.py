#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Structured analysis of extracted strings: URLs, endpoints, crypto, PDB paths, registry, paths."""
import re, sys, json, os
from pathlib import Path
from collections import Counter, OrderedDict

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"D:\VibeCoding\微信输入法逆向\out\strings")
REP = OUT.parent / "reports"; REP.mkdir(parents=True, exist_ok=True)

URL_RE = re.compile(r"(?:https?|wss?|ftp)://[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]{4,}")
DOM_RE = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+(?:com|cn|net|org|io|me|xyz|top|vip|cc|info|tv|live|app|dev|cloud|site|online|tech|pro|edu|gov)(?::\d{2,5})?\b", re.I)
PDB_RE  = re.compile(r"[A-Za-z]:\\[^\s\"']{4,200}\.(?:pdb|h|cpp|cc|c|hpp|rs|dart|proto)", re.I)
PATH_RE = re.compile(r"[A-Za-z]:\\(?:Program Files|ProgramData|Users|Windows|data|workspace|build|repo)[^\s\"'<>|]{3,180}", re.I)
HOST_RE = re.compile(r"^(?:[a-z0-9\-]+\.)+[a-z]{2,}(?::\d+)?$", re.I)

def load(name):
    p = OUT / name
    if not p.exists(): return []
    rows = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            try: off = int(parts[0])
            except: off = -1
            rows.append((off, parts[1], parts[2]))
    return rows

summary = OrderedDict()
for f in sorted(OUT.glob("*.strings.tsv")):
    binname = f.name[:-len(".strings.tsv")]
    rows = load(f.name)
    urls, doms, pdbs, paths, hosts = Counter(), Counter(), Counter(), Counter(), Counter()
    for off, enc, s in rows:
        for m in URL_RE.findall(s): urls[m] += 1
        for m in DOM_RE.findall(s): doms[m.lower()] += 1
        for m in PDB_RE.findall(s): pdbs[m] += 1
        for m in PATH_RE.findall(s): paths[m] += 1
        t = s.strip()
        if len(t) < 100 and HOST_RE.match(t): hosts[t.lower()] += 1
    summary[binname] = {"total": len(rows), "urls": len(urls), "domains": len(doms), "pdbs": len(pdbs)}

    with (REP / f"{binname}.findings.txt").open("w", encoding="utf-8") as fh:
        fh.write(f"########## {binname} ##########\n")
        fh.write(f"[URLS {len(urls)}]\n")
        for u, c in urls.most_common(400): fh.write(f"  {c:3d}  {u}\n")
        fh.write(f"\n[DOMAINS {len(doms)}]\n")
        for d, c in doms.most_common(400): fh.write(f"  {c:3d}  {d}\n")
        fh.write(f"\n[HOST-LIKE {len(hosts)}]\n")
        for d, c in hosts.most_common(300): fh.write(f"  {c:3d}  {d}\n")
        fh.write(f"\n[SOURCE/PDB PATHS {len(pdbs)}]\n")
        for d, c in pdbs.most_common(300): fh.write(f"  {c:3d}  {d}\n")
        fh.write(f"\n[FS PATHS {len(paths)}]\n")
        for d, c in paths.most_common(300): fh.write(f"  {c:3d}  {d}\n")
    print(f"{binname}: rows={len(rows)} urls={len(urls)} doms={len(doms)} pdbs={len(pdbs)}")

(REP / "_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
print("report dir:", REP)
