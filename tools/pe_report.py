#!/usr/bin/env python3
"""PE structure report: headers, sections, imports, exports, resources, debug/PDB, rich header."""
import sys, json, struct, hashlib
from pathlib import Path
try:
    import pefile
except ImportError:
    print("pefile missing"); sys.exit(1)

def main():
    p = Path(sys.argv[1])
    pe = pefile.PE(str(p), fast_load=True)
    pe.parse_data_directories()
    d = {"file": p.name, "size": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
    d["machine"] = hex(pe.FILE_HEADER.Machine)
    d["timestamp"] = pe.FILE_HEADER.TimeDateStamp
    import datetime
    try: d["timestamp_iso"] = datetime.datetime.utcfromtimestamp(pe.FILE_HEADER.TimeDateStamp).isoformat()+"Z"
    except Exception: d["timestamp_iso"] = None
    d["characteristics"] = hex(pe.FILE_HEADER.Characteristics)
    d["subsystem"] = pe.OPTIONAL_HEADER.Subsystem
    d["dll"] = bool(pe.FILE_HEADER.Characteristics & 0x2000)
    d["entrypoint"] = hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    d["imagebase"] = hex(pe.OPTIONAL_HEADER.ImageBase)
    d["dllchar"] = hex(getattr(pe.OPTIONAL_HEADER,"DllCharacteristics",0))
    d["sections"] = [{"name": s.Name.rstrip(b"\x00").decode("ascii","replace"),
                      "va": hex(s.VirtualAddress), "vsize": s.Misc_VirtualSize,
                      "raw": hex(s.PointerToRawData), "rawsize": s.SizeOfRawData,
                      "entropy": round(s.get_entropy(),3),
                      "chars": hex(s.Characteristics)} for s in pe.sections]
    imps = []
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for e in pe.DIRECTORY_ENTRY_IMPORT:
            fns = []
            for imp in e.imports:
                if imp.name: fns.append(imp.name.decode("ascii","replace"))
                else: fns.append("ord#%s" % imp.ordinal)
            imps.append({"dll": e.dll.decode("ascii","replace"), "count": len(fns), "funcs": fns})
    d["imports"] = imps
    exps = []
    if hasattr(pe, "DIRECTORY_ENTRY_EXPORT"):
        for e in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            exps.append({"ord": e.ordinal, "name": (e.name or b"").decode("ascii","replace"), "addr": hex(e.address)})
    d["exports"] = exps
    dbg = []
    if hasattr(pe, "DIRECTORY_ENTRY_DEBUG"):
        for e in pe.DIRECTORY_ENTRY_DEBUG:
            try:
                if e.struct.Type == 2 and e.entry is not None:
                    dbg.append({"type":"CODEVIEW","pdb": getattr(e.entry,"PdbFileName",b"").decode("ascii","replace") if isinstance(getattr(e.entry,"PdbFileName",b""),bytes) else str(getattr(e.entry,"PdbFileName","")), "guid": str(getattr(e.entry,"Signature_Data1","")), "age": getattr(e.entry,"Age",None)})
                else:
                    dbg.append({"type": e.struct.Type})
            except Exception as ex: dbg.append({"err": str(ex)})
    d["debug"] = dbg
    res = []
    if hasattr(pe, "DIRECTORY_ENTRY_RESOURCE"):
        for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            res.append({"type": str(t.name) if t.name else pefile.RESOURCE_TYPE.get(t.struct.Id, t.struct.Id), "id": t.struct.Id})
    d["resources"] = res
    print(json.dumps(d, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
