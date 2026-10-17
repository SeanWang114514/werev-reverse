#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dart AOT snapshot (app.so) string-pool / pattern extraction."""
import sys, re, json, struct
from pathlib import Path
from collections import Counter, defaultdict

def read_snapshot_header(blob, off):
    magic, length, kind = struct.unpack_from("<III", blob, off)
    return {"magic": hex(magic), "length": length, "kind": kind,
            "magic_ok": magic == 0xdcdcf5f5}

def strings_in(blob, start, end, minlen=4):
    """Extract printable ASCII runs."""
    out = []
    cur = bytearray()
    for i in range(start, end):
        b = blob[i]
        if 32 <= b < 127:
            cur.append(b)
        else:
            if len(cur) >= minlen:
                out.append((i - len(cur), cur.decode("ascii", "replace")))
            cur = bytearray()
    if len(cur) >= minlen:
        out.append((end - len(cur), cur.decode("ascii", "replace")))
    return out

def main():
    p = Path(sys.argv[1]); outdir = Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
    blob = p.read_bytes()
    rep = {}

    # snapshot data regions per ELF symbol table facts (fixed for this build, recompute anyway)
    syms = {"vm_data": (0x200, 0x200 + 35344),
            "iso_data": (0x8c40, 0x8c40 + 6078688)}
    rep["headers"] = {k: read_snapshot_header(blob, o) for k, (o, e) in syms.items()}

    s = strings_in(blob, syms["iso_data"][0], syms["iso_data"][1], 5)
    (outdir / "app_iso_strings.txt").write_text(
        "\n".join(f"{o:#x}\t{t}" for o, t in s), encoding="utf-8")
    rep["iso_string_count"] = len(s)
    rep["iso_string_bytes"] = sum(len(t) for _, t in s)

    s2 = strings_in(blob, syms["vm_data"][0], syms["vm_data"][1], 5)
    (outdir / "app_vm_strings.txt").write_text(
        "\n".join(f"{o:#x}\t{t}" for o, t in s2), encoding="utf-8")

    allt = [t for _, t in s]
    pats = {
        "package_uris": r"^package:[A-Za-z0-9_./-]+$",
        "dart_uris": r"^dart:[A-Za-z0-9_./-]+$",
        "file_uris": r"^file:///.*",
        "dotted_paths": r"^[a-z][a-zA-Z0-9_]*(?:\.[a-z][a-zA-Z0-9_]*){2,}$",
        "lib_paths": r"^(lib|assets|src)/[A-Za-z0-9_./-]+\.dart$",
        "urls": r"https?://[^\s\"']+",
        "snake_case_ids": r"^[a-z][a-z0-9]*(?:_[a-z0-9]+){1,}$",
    }
    buckets = defaultdict(list)
    for t in allt:
        for name, rx in pats.items():
            if re.match(rx, t) if name != "urls" else re.search(rx, t):
                buckets[name].append(t)
    rep["pattern_counts"] = {k: len(v) for k, v in buckets.items()}
    for k, v in buckets.items():
        uniq = sorted(set(v))
        (outdir / f"app_{k}.txt").write_text("\n".join(uniq), encoding="utf-8")

    # Dart class-name-like tokens: CamelCase, len>=4, appears standalone
    camel = sorted({t for t in allt if re.match(r"^[A-Z][A-Za-z0-9]{3,}$", t)})
    (outdir / "app_camel_tokens.txt").write_text("\n".join(camel), encoding="utf-8")
    rep["camel_count"] = len(camel)

    (outdir / "app_dart_report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(rep, indent=1, ensure_ascii=False))
    print("\n--- package uris (first 60) ---")
    print("\n".join(sorted(set(buckets["package_uris"]))[:60]))
    print("\n--- urls (first 40) ---")
    print("\n".join(sorted(set(buckets["urls"]))[:40]))

if __name__ == "__main__":
    main()
