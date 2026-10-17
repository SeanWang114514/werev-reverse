
import os, re, collections
p = r"D:\VibeCoding\微信输入法逆向\samples\runtime\context_capture\refetch_sync_legacy.log"
txt = open(p, encoding="utf-8", errors="replace").read()
blocks = txt.split("======== [REFETCH] capture ========")
print("blocks", len(blocks))
hosts=collections.Counter(); meth=collections.Counter(); src=collections.Counter(); okc=collections.Counter()
nonempty=0; samples=[]
for b in blocks[1:]:
    d={}
    for line in b.splitlines():
        if "=" in line:
            k,v=line.split("=",1); d[k.strip()]=v
    hosts[d.get("host_exe","")]+=1; meth[d.get("method","")]+=1
    src[d.get("refetch_source","")]+=1; okc[d.get("refetch_success","")]+=1
    if d.get("before_text") or d.get("after_text") or d.get("selected_text"):
        nonempty+=1
        if len(samples)<6: samples.append(d)
print("nonempty", nonempty)
print("hosts", hosts.most_common(12))
print("method", meth.most_common(8))
print("source", src.most_common(8))
print("success", okc.most_common(5))
for s in samples:
    print("---", {k:s.get(k) for k in ("time_local","host_exe","method","refetch_success","before_len","after_len","selected_len")})
    print("   before:", (s.get("before_text") or "")[:200])
    print("   sel:", (s.get("selected_text") or "")[:200])
