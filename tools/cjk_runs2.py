import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=open(sys.argv[1],'rb').read()
L=len(d)
i=0; n=0
while i<L:
    if 0xe4<=d[i]<=0xe9 and i+2<L and 0x80<=d[i+1]<=0xbf and 0x80<=d[i+2]<=0xbf:
        j=i; g=0
        while j+2<L and 0xe4<=d[j]<=0xe9 and 0x80<=d[j+1]<=0xbf and 0x80<=d[j+2]<=0xbf:
            g+=1; j+=3
        if g>=10:
            print(hex(i), g, d[i:i+3*g].decode('utf-8','replace')[:70])
            n+=1
            i=j; continue
    i+=1
print('runs', n)