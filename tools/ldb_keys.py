# -*- coding: utf-8 -*-
import sys, struct, os, collections
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

if __name__=='__main__':
    p=sys.argv[1]
    recs=all_records(p)
    print('# %s records=%d' % (os.path.basename(p), len(recs)))
    buckets=collections.Counter()
    samples=collections.defaultdict(list)
    for uk,payload in recs:
        s=uk.decode('utf-8','replace')
        parts=s.split('!')
        tag='!'.join(parts[:3]) if s.startswith('!') else (parts[0] if parts else '')
        buckets[tag]+=1
        if len(samples[tag])<6:
            samples[tag].append((s,payload.hex()[:64]))
    for tag,cnt in buckets.most_common(60):
        print('')
        print('### %-50s x%d' % (tag, cnt))
        for s,h in samples[tag]:
            print('    %-70s %s' % (s[:70], h))
