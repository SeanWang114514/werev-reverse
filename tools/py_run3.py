import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
letters=bytes(range(97,123))+b','
i=0
items=[]
while i<n:
    if d[i] in letters:
        j=i
        lat=0; nul=0
        while j<n and d[j] in letters+b'\x00':
            if 97<=d[j]<=122: lat+=1
            elif d[j]==0: nul+=1
            j+=1
        if lat>=6:
            seg=d[i:j]
            # reconstruct: letters and commas, dropping single NULs between letters
            s=seg.decode('latin1').replace('\x00','')
            s=re.sub(r',+', ',', s)
            items.append((i,s))
        i=j
    else: i+=1
print('items', len(items))
for o,s in items[:30]: print(hex(o), s[:80])