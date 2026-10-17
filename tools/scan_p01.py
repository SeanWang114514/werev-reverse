import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
print('size', n)
idx=[i for i in range(0,n-5) if d[i]==0x50 and d[i+1]==0x01 and 3<=d[i+2]<=40]
print('P01 candidates', len(idx))
good=0
ex=[]
for i in idx:
    ln=d[i+2]
    body=d[i+3:i+3+ln]
    if len(body)<ln: continue
    try:
        s=body.decode('gbk')
    except Exception:
        continue
    if all('\u4e00'<=c<='\u9fff' for c in s):
        good+=1
        if len(ex)<25: ex.append((hex(i), s))
print('gbk cjk bodies', good)
for e in ex: print(e)