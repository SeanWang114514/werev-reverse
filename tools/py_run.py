import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=int(sys.argv[2]) if len(sys.argv)>2 else 60
pat=re.compile(rb'(?:P\x01[\x03-\x28])|(?:[a-z]{1,9}(?:,?[a-z]{1,9}){0,3})')
# direct: find sequences of ascii letters and commas with NUL single letters
res=[]
i=0; n=len(d)
while i<n:
    j=i; buf=bytearray()
    while j<n:
        b=d[j]
        if 97<=b<=122: buf.append(b); j+=1
        elif b==44 and buf: buf.append(b); j+=1
        elif b==0 and buf: j+=1
        else: break
    if len(buf)>=4 and b',' in buf:
        res.append((i, bytes(buf).decode()))
        i=j
    else: i+=1
print('runs', len(res))
for o,s in res[:cnt]: print(hex(o), s)