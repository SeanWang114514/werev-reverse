import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
out=open(sys.argv[2],'w',encoding='utf-8')
L=len(d)
i=0; n=0
while i<L:
    b=d[i]
    if 0xe4<=b<=0xe9 and i+2<L and 0x80<=d[i+1]<=0xbf and 0x80<=d[i+2]<=0xbf:
        j=i; good=0
        while j+2<L and 0xe4<=d[j]<=0xe9 and 0x80<=d[j+1]<=0xbf and 0x80<=d[j+2]<=0xbf:
            good+=1; j+=3
        if good>=8:
            out.write(str(i)+chr(9)+str(good)+chr(9)+d[i:i+3*good].decode('utf-8','replace')+chr(10))
            n+=1
            i=j; continue
    i+=1
out.close()
print('runs', n)