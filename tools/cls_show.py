#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re
from pathlib import Path
p = Path(sys.argv[1]); want = sys.argv[2:]
txt = p.read_text(encoding="utf-8").splitlines()
cur = None
for l in txt:
    if l.startswith("### "):
        cur = l[4:].split("  (")[0]
        if any(cur == w or cur.startswith(w + "::") for w in want):
            print(l)
        continue
    if cur and any(cur == w or cur.startswith(w + "::") for w in want):
        print(l)
