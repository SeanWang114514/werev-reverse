
f = r"D:\VibeCoding\微信输入法逆向\out\strings\libwxhld.dll.strings.tsv"
rows=[]
for line in open(f, encoding="utf-8", errors="replace"):
    p=line.rstrip("\n").split("\t",2)
    if len(p)==3:
        try: off=int(p[0])
        except: continue
        rows.append((off,p[1],p[2]))
rows.sort()
lo,hi=14799000,14811000
for o,t,s in rows:
    if lo<=o<=hi: print("%9d %s %s"%(o,t,s[:180]))
