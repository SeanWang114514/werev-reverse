# -*- coding: utf-8 -*-
import sys, struct, os, json
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

p=sys.argv[1]
outp=sys.argv[2]
lines=[]
for f in sorted(os.listdir(p)):
    if not f.endswith('.ldb'): continue
    fp=os.path.join(p,f)
    try: recs=all_records(fp)
    except Exception as e:
        lines.append('## %s ERROR %s' % (f,e)); continue
    lines.append('## %s  recs=%d' % (f,len(recs)))
    for uk,payload in recs:
        k=uk.decode('utf-8','replace')
        lines.append(k)
        try:
            s=payload.decode('utf-8')
            lines.append('  V: '+s.replace(chr(10),' ')[:3000])
        except Exception:
            lines.append('  H: '+payload[:96].hex())
open(outp,'w',encoding='utf-8').write(chr(10).join(lines))
print('wrote', outp, len(lines))
