import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
out=0; tot=0
ex=[]
i=0x2c000
while i < n:
    b=d[i]
    if 32<=b<127 and d[i-1]==0:
        j=i; s=bytearray()
        while j<n and 32<=d[j]<127: s.append(d[j]); j+=1
        txt=s.decode()
        if re.fullmatch(r'[a-z]{1,9}(,[a-z]{1,9}){1,9}', txt):
            tot+=1
            if len(ex)<40: ex.append((hex(i),txt))
        i=j
    else: i+=1
print('pinyin seqs', tot)
for o,s in ex: print(o,s)