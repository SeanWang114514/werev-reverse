
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open(r"D:\werev\out\wetype_server.vtables.json",encoding='utf-8'))
want=["wetype::server::enginev2","wetype::server::handler","wetype::server::data","wetype::server::network",
      "wetype::server::clipboard","wetype::server::cross_platform","wetype::server::wechat_message",
      "wetype::server::report","wetype::server::vmode","wetype::server"]
for w in want:
    print("="*20,w)
    for b in d:
        c=b['cls']
        if c.startswith(w+"::") and c.count('::')==w.count('::')+1 and '<' not in c:
            print("  %s  %s  n=%d"%(b['addr'],c,len(b['fns'])))
