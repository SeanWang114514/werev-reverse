import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
out=[]
i=0
while i<n:
    j=i; buf=bytearray()
    while j<n:
        b=d[j]
        if 97<=b<=122: buf.append(b); j+=1
        elif b==44 and buf: buf.append(b); j+=1
        elif b==0 and buf: j+=1
        else: break
    if len(buf)>=2:
        s=bytes(buf).decode()
        out.append((i,s)); i=j
    else: i+=1
print('items', len(out), 'unique', len(set(s for _,s in out)))
for o,s in out[:40]: print(hex(o), s)