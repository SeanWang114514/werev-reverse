import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
print('size', n)
print('u32[0:8]', [struct.unpack_from('<I',d,4*i)[0] for i in range(8)])
# scan for utf-8 cjk with context
res=[]
i=0
while i<n-3:
    b=d[i]
    if 0xe4<=b<=0xe9:
        try:
            s=d[i:i+3].decode('utf-8')
            if '\u4e00'<=s<='\u9fff': res.append(i); i+=3; continue
        except Exception: pass
    i+=1
print('cjk chars', len(res))
if res:
    print('first offsets', [hex(x) for x in res[:10]])
    o=res[0]
    print('ctx hex', d[max(0,o-32):o+64].hex())
    print('ctx txt', d[max(0,o-32):o+64].decode('utf-8','replace'))