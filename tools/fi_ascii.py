import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
# 提取 ASCII 段（>=4）以及 GBK/UTF8 中文
f=open(sys.argv[2],'w',encoding='utf-8')
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    i=0
    while i < len(r):
        b=r[i]
        if 32<=b<127:
            j=i
            while j<len(r) and 32<=r[j]<127: j+=1
            if j-i>=4: f.write('%d\tA\t%s\n' % (k, r[i:j].decode('ascii')))
            i=j
        else: i+=1
f.close()
print('done')