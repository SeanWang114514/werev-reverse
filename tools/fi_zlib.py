import sys, zlib, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
ok=0; best=[]
for k in range(cnt-1):
    r=d[offs[k]:offs[k+1]]
    for s in range(0,min(len(r),28)):
        try:
            o=zlib.decompress(r[s:])
            ok+=1; best.append((k,s,len(o),o[:80])); break
        except Exception: pass
print('zlib ok', ok)
for b in best[:5]: print(b)
print('--- whole-file zlib attempts ---')
for s in range(0,64):
    try:
        o=zlib.decompress(d[s:])
        print('ok at', s, len(o)); break
    except Exception: pass