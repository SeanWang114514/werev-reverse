import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
print('cnt',cnt,'filesize',len(d))
print('offsets', offs[:6], '...', offs[-3:])
print('header bytes 0..16', d[:16].hex())
print('u32[0:8]', [struct.unpack_from('<I',d,4*i)[0] for i in range(8)])