import sys, struct, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=open(sys.argv[1],'rb').read()
print('size', len(d))
print('u32[0:12]', [struct.unpack_from('<I',d,4*i)[0] for i in range(12)])
out=sys.argv[2]
f=open(out,'w',encoding='utf-8')
n=L=len(d)
i=0
cnt=0
while i+6<=L:
    # GBK: lead 0x81-0xFE, trail 0x40-0xFE
    j=i; buf=[]
    while j+1<L:
        b0=d[j]; b1=d[j+1]
        if 0x81<=b0<=0xfe and 0x40<=b1<=0xfe and b1!=0x7f:
            try:
                s=bytes([b0,b1]).decode('gbk')
            except: break
            if not ('\u4e00'<=s<='\u9fff'): break
            buf.append(s); j+=2
        else: break
    if len(buf)>=2:
        f.write(str(i)+chr(9)+''.join(buf)+chr(10))
        cnt+=1; i=j
    else: i+=1
f.close()
print('gbk runs', cnt)