import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=open(sys.argv[1],'rb').read()
# 打印 0xf50000-0xf54000 区间的 UTF-8 中文串，长度>=3
i=0xf40000; end=min(len(d),0xf56000)
res=[]
while i<end:
    if 0xe0<=d[i]<=0xef and i+2<end and 0x80<=d[i+1]<=0xbf and 0x80<=d[i+2]<=0xbf:
        j=i; out=[]
        while j+2<end and 0xe0<=d[j]<=0xef and 0x80<=d[j+1]<=0xbf and 0x80<=d[j+2]<=0xbf:
            out.append(d[j:j+3]); j+=3
        s=b''.join(out).decode('utf-8','replace')
        if len(s)>=2: res.append((hex(i),s))
        i=j
    else: i+=1
print('runs', len(res))
for o,s in res[:120]: print(o, s)