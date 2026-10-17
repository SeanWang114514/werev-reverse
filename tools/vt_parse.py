
import re, sys, collections, json
sys.stdout.reconfigure(encoding='utf-8')
f=r"D:\werev\out\wetype_server.vt.txt"
txt=open(f,encoding='utf-8',errors='replace').read().splitlines()
blocks=[]
cur=None
for ln in txt:
    if ln.startswith('### '):
        parts=ln[4:].split('\t')
        cur={'addr':parts[0],'name':parts[1] if len(parts)>1 else '','fns':[]}
        blocks.append(cur)
    elif ln.startswith('    [') and cur is not None:
        m=re.match(r'\s*\[\d+\]\s+(\S+)\s+->\s+(\S+)\s+(.*)$', ln)
        if m: cur['fns'].append((m.group(2),m.group(3).strip()))
real=[b for b in blocks if b['name'].endswith('::vftable')]
print("total blocks",len(blocks),"real vtables",len(real))
ns=collections.Counter()
for b in real:
    c=b['name'][:-9]
    parts=c.split('::')
    ns['::'.join(parts[:-1]) if len(parts)>1 else '(global)']+=1
print("\n=== namespaces by vtable count (top 40) ===")
for k,v in ns.most_common(40): print("%5d  %s"%(v,k))
json.dump([{'cls':b['name'][:-9],'addr':b['addr'],'n':len(b['fns']),'fns':b['fns']} for b in real],
          open(r"D:\werev\out\wetype_server.vtables.json",'w',encoding='utf-8'), ensure_ascii=False)
print("\nsaved vtables json")
