import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=open(sys.argv[1],'rb').read()
f=open(sys.argv[2],'w',encoding='utf-8')
n=len(d); i=0; cnt=0
while i+6<=n:
    j=i; buf=[]
    while j+1<n:
        b0=d[j]; b1=d[j+1]
        if 0x81<=b0<=0xfe and 0x40<=b1<=0xfe and b1!=0x7f:
            try: s=bytes([b0,b1]).decode('gbk')
            except: break
            if not ('\u4e00'<=s<='\u9fff'): break
            buf.append(s); j+=2
        else: break
    if len(buf)>=2:
        w=''.join(buf)
        try:
            t=w.encode('gbk').decode('utf-8')
            if all('\u4e00'<=c<='\u9fff' for c in t):
                f.write(str(i)+chr(9)+t+chr(10)); cnt+=1
        except: pass
        i=j
    else: i+=1
f.close()
print('utf8-as-gbk runs', cnt)