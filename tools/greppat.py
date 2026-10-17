import sys, os, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=sys.argv[1]
pats=[b'noun_tag', b'noun_tag_dict', b'ln2py', b'wkvc2e', b'wwkvc2e']
for fn in sorted(os.listdir(d)):
    fp=os.path.join(d,fn)
    if not os.path.isfile(fp): continue
    if not fn.lower().endswith(('.dll','.exe')): continue
    if os.path.getsize(fp)>60*1024*1024: continue
    try: b=open(fp,'rb').read()
    except Exception as e: continue
    hits=[p.decode() for p in pats if p in b]
    if hits: print(fn, hits)