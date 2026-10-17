import sys, struct, re, math, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=193344
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(0, min(cnt,4000))]
print('first offs', [hex(o) for o in offs[:8]])
a=offs[0]; b=offs[1]
print('rec0 region', hex(a), hex(b), b-a)
print(d[a:b].hex())
print(d[a:b].decode('utf-8','replace'))