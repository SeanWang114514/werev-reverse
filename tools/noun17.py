import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
print('cnt', cnt)
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
# find real data start: first offset
data_start=offs[0]
print('data_start', hex(data_start))
# The records are: t u32, then 4*(t+? )? derive by parsing from data_start sequentially
pos=data_start
rec=0
while pos<len(d) and rec<8:
    t=struct.unpack_from('<I',d,pos)[0]
    print('rec',rec,'pos',hex(pos),'t',t)
    # try: after t u32, there are t u32 hash values (4 bytes each!)
    cand=pos+4+4*t
    print('  next pos cand', hex(cand), d[pos+4:pos+4+4*t].hex()[:60])
    rec+=1
    pos=cand