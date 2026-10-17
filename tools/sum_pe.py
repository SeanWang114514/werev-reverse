
import json, glob, os
for p in sorted(glob.glob(r"D:\VibeCoding\微信输入法逆向\out\pe\*.json")):
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print(os.path.basename(p), "PARSE-ERR", e); continue
    if "file" not in d: print(os.path.basename(p), "EMPTY"); continue
    print("="*70)
    print(f"{d['file']}  size={d['size']}  machine={d['machine']}  dll={d['dll']}  subsystem={d['subsystem']}")
    print(f"  ts={d['timestamp']} ({d.get('timestamp_iso')})  dllchar={d.get('dllchar')}  imagebase={d.get('imagebase')}")
    print(f"  sections: " + ", ".join(f"{s['name']}({s['vsize']//1024}K,e={s['entropy']})" for s in d.get("sections",[])))
    dbg = d.get("debug") or []
    for b in dbg:
        if b.get("pdb"): print(f"  PDB: {b['pdb']}  age={b.get('age')}")
    imps = d.get("imports") or []
    print(f"  imports: {len(imps)} dlls, {sum(i['count'] for i in imps)} funcs")
    print("    " + ", ".join(i['dll'] for i in imps))
    exps = d.get("exports") or []
    if exps:
        named = [e for e in exps if e['name']]
        print(f"  exports: {len(exps)} ({len(named)} named)")
        print("    " + ", ".join(e['name'] for e in named[:40]))
