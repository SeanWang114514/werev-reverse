import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
py=re.compile(rb'[a-z]{1,10}(?:,[a-z]{1,10}){1,9}')
words=[]
for k in range(cnt-1):
    r=d[offs[k]:offs[k+1]]
    for m in py.finditer(r):
        words.append(m.group().decode())
print('pinyin seqs', len(words))
print(words[:30])