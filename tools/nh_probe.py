# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
head18=d[:18]
body=d[18:]
print('body', len(body))
# find next occurrence of head18 or its first 9 bytes
pat=d[0:9]
i=body.find(pat[:6])
print('6-byte pat in body at', i)
print('body head', body[:48].hex())
# try interpreting body as sequence: u32 flag, then repeat {utf8 word, 0010 00, varint freq}
pos=0
cnt=0
while pos < len(body) and cnt<20:
    # varint-ish skip: try leading u32
    v=struct.unpack_from('<I', body, pos)[0]
    print('at',hex(pos),'u32=',v)
    pos+=4; cnt+=1