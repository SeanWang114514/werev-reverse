import sys, struct, zlib, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
tails=collections.Counter()
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    tails[r[-3:].hex()]+=1
print('tail patterns top', tails.most_common(12))
# try zlib on region
big=max(range(cnt), key=lambda k: ends[k]-offs[k])
print('biggest rec', big, ends[big]-offs[big])
r=d[offs[big]:ends[big]]
head=r[:32].hex()
print('head', head)
for off in range(0,20):
    try:
        o=zlib.decompressobj()
        out=o.decompress(r[off:])
        if len(out)>40: print('zlib ok at', off, len(out), out[:60])
    except Exception as e: pass