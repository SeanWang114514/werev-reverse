# -*- coding: utf-8 -*-
import sys, struct, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def varint(b, i):
    r=0; s=0
    while i < len(b):
        c=b[i]; i+=1; r |= (c & 0x7f) << s
        if not (c & 0x80): return r,i
        s+=7
        if s>63: break
    return None,i

def block_entries(block):
    if len(block)<5: return []
    nrest=struct.unpack_from('<I',block,len(block)-4)[0]
    he=len(block)-4-4*nrest
    if he<0: return []
    out=[];i=0;key=b''
    while i<he:
        sh,i=varint(block,i); ns,i=varint(block,i); vl,i=varint(block,i)
        if sh is None or ns is None or vl is None: break
        key=key[:sh]+block[i:i+ns]; i+=ns
        val=block[i:i+vl]; i+=vl
        out.append((key,val))
    return out

def all_records(p):
    d=open(p,'rb').read()
    footer=d[-48:]
    i=0
    mo,i=varint(footer,i); ms,i=varint(footer,i)
    io_,i=varint(footer,i); is_,i=varint(footer,i)
    recs=[]
    for k,v in block_entries(d[io_:io_+is_]):
        j=0; off,j=varint(v,j); sz,j=varint(v,j)
        for key,val in block_entries(d[off:off+sz]):
            uk = key[:-8] if len(key)>=8 else key
            payload = val[:-1] if len(val)>=1 else b''
            recs.append((uk,payload))
    return recs

def show(p, limit=40):
    recs=all_records(p)
    print('=== %s  recs=%d' % (p, len(recs)))
    for uk,payload in recs[:limit]:
        t=uk.decode('utf-8','replace')
        print('KEY  %s' % t[:120])
        print('  HEX %s' % payload[:160].hex())
        print('  ASC %s' % ''.join(chr(c) if 32<=c<127 else '.' for c in payload[:160]))

if __name__=='__main__':
    for a in sys.argv[1:]:
        show(a, 12)
        print('')
