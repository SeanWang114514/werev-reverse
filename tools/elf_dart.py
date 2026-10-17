#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ELF64 structure + Dart AOT snapshot section/string-pool extraction."""
import sys, json, hashlib, struct, re
from pathlib import Path
from elftools.elf.elffile import ELFFile

def main():
    p = Path(sys.argv[1]); outdir = Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
    blob = p.read_bytes()
    d = {"file": p.name, "size": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}
    with p.open("rb") as fh:
        e = ELFFile(fh)
        d["class"] = e.elfclass; d["machine"] = e["e_machine"]; d["type"] = e["e_type"]
        d["entry"] = hex(e["e_entry"])
        d["sections"] = [{"name": s.name, "type": s["sh_type"], "addr": hex(s["sh_addr"]),
                          "off": hex(s["sh_offset"]), "size": s["sh_size"],
                          "flags": s["sh_flags"]} for s in e.iter_sections()]
        syms = []
        symtab = e.get_section_by_name(".dynsym") or e.get_section_by_name(".symtab")
        if symtab:
            for s in symtab.iter_symbols():
                if s.name:
                    syms.append({"name": s.name, "value": hex(s["st_value"]), "size": s["st_size"], "shndx": s["st_shndx"]})
        d["symbols"] = syms
        if e.num_segments():
            d["segments"] = [{"type": s["p_type"], "vaddr": hex(s["p_vaddr"]), "off": hex(s["p_offset"]), "filesz": s["p_filesz"], "memsz": hex(s["p_memsz"]), "flags": s["p_flags"]} for s in e.iter_segments()]
    (outdir / (p.name + ".elf.json")).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{p.name}: sections={len(d.get('sections',[]))} syms={len(d.get('symbols',[]))} segs={len(d.get('segments',[]))}")
    for s in d.get("sections", []):
        if s["size"] > 0:
            print(f"   {s['name']:32s} {s['type']:22s} off={s['off']:>10s} size={s['size']:>10d} addr={s['addr']}")
    print("   --- notable symbols ---")
    for s in d.get("symbols", []):
        if re.search(r"[Dd]art|snapshot|Flutter|flutter|isolate|vm_", s["name"]):
            print(f"   {s['value']:>12s} size={s['size']:>10d} {s['name']}")

if __name__ == "__main__":
    main()
