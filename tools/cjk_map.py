import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
# find region where utf8 3-byte CJK sequences cluster
cjk=[]
i=0
while i<n-2:
    b=d[i]
    if 0xe4<=b<=0xe9:
        try:
            s=d[i:i+3].decode('utf-8')
            if '\u4e00'<=s<='\u9fff':
                cjk.append(i); i+=3; continue
        except Exception: pass
    i+=1
print('cjk count', len(cjk))
if cjk:
    print('first', hex(cjk[0]), 'last', hex(cjk[-1]))
    # density by 64KB bucket
    from collections import Counter
    c=Counter(x//65536 for x in cjk)
    print(sorted(c.items())[:20])