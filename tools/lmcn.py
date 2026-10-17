import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
# find all offsets where prefix 0x80000001 shard table style appears
lens=sorted(set([4,8,16,32,64]))
best=None
for start in [0]:
    pass
# strategy: scan for increasing u32 arrays anchored at 0x10
def read_off(base):
    cnt=struct.unpack_from('<I',d,base-4)[0]
    print('cnt at', hex(base-4), cnt)
    if cnt>200000: return
    offs=[struct.unpack_from('<I',d,base+4*i)[0] for i in range(min(cnt,20))]
    print('offs', [hex(o) for o in offs])
read_off(0x10)
# dump region 0x00..0x200 bytes
print(d[:512].hex())