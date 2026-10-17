import sys, struct, re, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
print('size', len(d))
print('u32[0:12]', [struct.unpack_from('<I',d,4*i)[0] for i in range(12)])
print(d[:64].hex())
runs=[]
i=0;n=len(d)
while i<n:
    if 32<=d[i]<127:
        j=i
        while j<n and 32<=d[j]<127: j+=1
        if j-i>=4: runs.append((i,d[i:j].decode()))
        i=j
    else: i+=1
print('ascii runs', len(runs))
for o,s in runs[:50]: print(hex(o), s[:70])