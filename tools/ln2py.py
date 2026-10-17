import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
print('size', len(d))
print('u32', [struct.unpack_from('<I',d,4*i)[0] for i in range(8)])
print('u64', [struct.unpack_from('<Q',d,8*i)[0] for i in range(4)])
# marker
for mk in [b'Ime trie header']:
    i=d.find(mk)
    print('marker', mk, hex(i) if i>=0 else -1)
# ascii runs
runs=[]
i=0;n=len(d)
while i<n:
    if 32<=d[i]<127:
        j=i
        while j<n and 32<=d[j]<127: j+=1
        if j-i>=3: runs.append((i,d[i:j].decode()))
        i=j
    else: i+=1
print('ascii runs', len(runs))
for o,s in runs[:60]: print(hex(o), s[:60])