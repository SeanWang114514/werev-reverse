# -*- coding: utf-8 -*-
import sys, struct, os, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def gbk_text(b):
    return b.decode('gbk','replace')

def dump(p, maxo=0):
    d=open(p,'rb').read()
    print('FILE', p, len(d))
    print('u32[0:16]', [hex(x) for x in struct.unpack_from('<16I', d, 0)])
    print('u64[0:8] ', [hex(x) for x in struct.unpack_from('<8Q', d, 0)])
    # look for Ime trie header
    pos = d.find(b'Ime trie header')
    print('ImeTrieHeader at', pos)
    if pos >= 0:
        print('ctx', d[max(0,pos-32):pos+96].hex())
    return d

p=sys.argv[1]
d=dump(p)
