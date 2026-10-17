import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import ast
d=open(sys.argv[1],'rb').read()
f=open(sys.argv[2],'w',encoding='utf-8')
i=0; n=len(d); cnt=0
while i<n:
    if 0xe0<=d[i]<=0xef and i+2<n and 0x80<=d[i+1]<=0xbf and 0x80<=d[i+2]<=0xbf:
        j=i; out=[]
        while j+2<n and 0xe0<=d[j]<=0xef and 0x80<=d[j+1]<=0xbf and 0x80<=d[j+2]<=0xbf:
            out.append(d[j:j+3]); j+=3
        s=b''.join(out).decode('utf-8','replace')
        if len(s)>=2 and all('\u4e00'<=c<='\u9fff' or c.isascii() for c in s):
            f.write('%x\t%s\n'%(i,s)); cnt+=1
        i=j
    else: i+=1
f.close()
print('strings', cnt)