
import os
f = r"D:\VibeCoding\微信输入法逆向\out\strings\libwxhld.dll.strings.tsv"
rows=[]
for line in open(f, encoding="utf-8", errors="replace"):
    parts=line.rstrip("\n").split("\t",2)
    if len(parts)==3:
        try: off=int(parts[0])
        except: continue
        rows.append((off,parts[1],parts[2]))
rows.sort()
idx=[i for i,(o,t,s) in enumerate(rows) if "remote_command" in s or "RemoteCommand" in s]
print("hits",len(idx))
seen=set()
for i in idx:
    lo=max(0,i-12); hi=min(len(rows),i+13)
    for j in range(lo,hi):
        if j in seen: continue
        seen.add(j)
        print("%9d %s %s"%(rows[j][0],rows[j][1],rows[j][2][:150]))
    print("  ---")
