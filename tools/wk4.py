import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=open(sys.argv[1],'rb').read()
# find P01 markers and dump surrounding context in readable form
cnt=0
i=0
n=len(d)
res=[]
while i<n-6:
    if d[i]==0x50 and d[i+1]==0x01 and d[i+2] in (2,3,4,5):
        ln=d[i+2]
        seg=d[i+3:i+3+ln]
        ctx=d[max(0,i-6):i+3+ln+10]
        res.append((i,ln,seg,ctx))
        cnt+=1
        i+=3+ln
    else: i+=1
print('markers', cnt)
# The 2-byte ASCII tokens look like a custom alphabet. Show bytes as-is:
for off,ln,seg,ctx in res[:20]:
    print(hex(off), ln, seg.hex(), 'ctx', ctx.hex())