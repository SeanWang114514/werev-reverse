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

def rd_varint(b,i):
    r=0;s=0
    while i<len(b):
        c=b[i];i+=1;r|=(c&0x7f)<<s
        if not c&0x80: return r,i
        s+=7
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

def pb(b, depth=0, out=None):
    i=0
    while i < len(b):
        t,i = rd_varint(b,i)
        if t is None: break
        f=t>>3; w=t&7
        pad='  '*depth
        if w==0:
            v,i=rd_varint(b,i)
            out.append('%s%d: varint %s' % (pad,f,v))
        elif w==1:
            v=struct.unpack_from('<Q',b,i)[0]; i+=8
            out.append('%s%d: fixed64 %d' % (pad,f,v))
        elif w==5:
            v=struct.unpack_from('<I',b,i)[0]; i+=4
            out.append('%s%d: fixed32 %d' % (pad,f,v))
        elif w==2:
            ln,i=rd_varint(b,i)
            if ln is None: break
            chunk=b[i:i+ln]; i+=ln
            try:
                s=chunk.decode('utf-8')
                ok=all(31 < ord(c) for c in s)
            except Exception:
                ok=False
            sub=[]
            good=False
            if ln>0:
                try:
                    pb(chunk, depth+1, sub)
                    good = len(sub)>0 and all('Invalid' not in x for x in sub)
                except Exception:
                    good=False
            if ok and (not good or len(chunk)>12):
                out.append('%s%d: str[%d] %r' % (pad,f,ln,s[:200]))
            elif good:
                out.append('%s%d: message[%d]' % (pad,f,ln))
                out.extend(sub)
            else:
                out.append('%s%d: bytes[%d] %s' % (pad,f,ln,chunk[:40].hex()))
        else:
            out.append('%s%d: wt%d UNSUPPORTED' % (pad,f,w)); break
    return out

p=sys.argv[1]; outp=sys.argv[2]
lines=[]
for f in sorted(os.listdir(p)):
    if not f.endswith('.ldb'): continue
    for uk,payload in all_records(os.path.join(p,f)):
        key=uk.decode('utf-8','replace')
        lines.append('')
        lines.append('## %s :: %s  (%d B)' % (f, key, len(payload)))
        try:
            s=payload.decode('utf-8')
            if all(31<ord(c) for c in s):
                lines.append('  TEXT: '+s[:2000]); continue
        except Exception: pass
        try:
            o=[]; pb(payload,1,o)
            lines.extend(['  '+x if False else x for x in o])
        except Exception as e:
            lines.append('  RAW: '+payload[:80].hex()+' ('+str(e)+')')
open(outp,'w',encoding='utf-8').write(chr(10).join(lines))
print('wrote',outp,len(lines))
