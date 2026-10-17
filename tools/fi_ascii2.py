import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=open(sys.argv[1],'rb').read()
f=open(sys.argv[2],'w',encoding='utf-8')
i=0; n=len(d)
while i<n:
    if 32<=d[i]<127:
        j=i
        while j<n and 32<=d[j]<127: j+=1
        if j-i>=5: f.write('%x\t%s\n' % (i, d[i:j].decode('ascii')))
        i=j
    else: i+=1
f.close()
print('ok')