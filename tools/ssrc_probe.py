# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
print('size', len(d))
print('head hex', d[:48].hex())
i=d.find(b'Ime trie header')
print('marker', i)
print('ctx', d[i-16:i+64].hex())