# -*- coding: utf-8 -*-
import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
i=d.find(bytes.fromhex('500103'))
print('at', hex(i))
print('hex', d[i:i+44].hex())
print('types', [type(x) for x in d[i:i+20]][:3])
print('len at i+2', d[i+2])