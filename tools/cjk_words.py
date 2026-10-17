import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
res=[]
i=0
while i<n-24:
    b=d[i]
    if 0xe4<=b<=0xe9:
        try:
            s=d[i:i+3].decode('utf-8')
            if '\u4e00'<=s<='\u9fff':
                # extend forward
                j=i+3; out=[s]
                while j<n-2:
                    try:
                        t=d[j:j+3].decode('utf-8')
                        if '\u4e00'<=t<='\u9fff': out.append(t); j+=3; continue
                    except Exception: pass
                    break
                word=''.join(out)
                if len(word)>=2: res.append((i,word))
                i=j; continue
        except Exception: pass
    i+=1
print('words', len(res))
seen=set(); u=[]
for o,w in res:
    if w not in seen: seen.add(w); u.append((o,w))
print('unique', len(u))
for o,w in u[:80]: print(hex(o), w)