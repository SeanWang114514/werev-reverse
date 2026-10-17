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

def scan(b):
    i=0; out=[]
    while i < len(b):
        t,i = varint(b,i)
        if t is None: break
        f=t>>3; w=t&7
        if w==0:
            v,i=varint(b,i)
            if v is None: break
            out.append(('v',f,v))
        elif w==2:
            ln,i=varint(b,i)
            if ln is None or ln<0 or i+ln>len(b): break
            out.append(('w',f,ln)); i+=ln
        elif w==1:
            if i+8>len(b): break
            out.append(('x',f,struct.unpack_from('<Q',b,i)[0])); i+=8
        elif w==5:
            if i+4>len(b): break
            out.append(('x',f,struct.unpack_from('<I',b,i)[0])); i+=4
        else: break
    return out

p=sys.argv[1]; limit=int(sys.argv[2]) if len(sys.argv)>2 else 2000
for uk,payload in all_records(p):
    key=uk.decode('utf-8','replace')
    if not key.startswith('vmodeclipboard'): continue
    fields=scan(payload)
    n=0
    for kind,f,v in fields:
        if n>=limit: break
        n+=1
        if kind=='w':
            chunk=payload[0:0]
            continue
    print('recs fields=%d' % len(fields))

def parse_clip(b, out, depth=0, maxn=[0]):
    i=0
    while i < len(b):
        t,i = varint(b,i)
        if t is None: break
        f=t>>3; w=t&7
        if w==0:
            v,i=varint(b,i)
            if v is None: break
            out.append(('  '*depth)+'f%d = %d' % (f,v))
        elif w==2:
            ln,i=varint(b,i)
            if ln is None or i+ln>len(b): break
            chunk=b[i:i+ln]; i+=ln
            ok=False; s=''
            if ln>0:
                try:
                    s=chunk.decode('utf-8'); ok=all(ord(c)>=32 or c in chr(9) for c in s)
                except Exception: ok=False
            if ok and ln>0:
                out.append(('  '*depth)+'f%d = %r' % (f, s[:300]))
            else:
                sub=[]
                try: parse_clip(chunk, sub, depth+1, maxn)
                except Exception: pass
                if sub and len(sub)<=8:
                    out.append(('  '*depth)+'f%d {' % f)
                    out.extend(sub)
                    out.append(('  '*depth)+'}')
                else:
                    out.append(('  '*depth)+'f%d = <%d B>' % (f, ln))
        elif w==1:
            i+=8
        elif w==5:
            i+=4
        else: break
    return out

print('--- parsed ---')
cnt=0
for uk,payload in all_records(p):
    key=uk.decode('utf-8','replace')
    if not key.startswith('vmodeclipboard'): continue
    cnt+=1
    out=[]; parse_clip(payload, out, 0)
    print('### vmodeclipboard #%d  (%d B)' % (cnt, len(payload)))
    for line in out[:60]: print('   '+line)
    print('   ... total lines %d' % len(out))
