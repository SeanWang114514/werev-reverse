import sys, struct, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=open(sys.argv[1],'rb').read()
c=collections.Counter()
n=len(d)
for i in range(0,n-3,2):
    v1=struct.unpack_from('<H',d,i)[0]
    v2=struct.unpack_from('<H',d,i+2)[0]
    if 0x4e00<=v1<=0x9fff and 0x4e00<=v2<=0x9fff:
        c[chr(v1)+chr(v2)]+=1
print('distinct pairs', len(c))
print([(k,v) for k,v in c.most_common(20)])