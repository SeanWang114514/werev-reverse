
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open(r"D:\werev\out\wetype_server.vtables.json",encoding='utf-8'))
first={}
for b in d:
    c=b['cls']
    if c not in first or int(b['addr'],16)<int(first[c]['addr'],16): first[c]=b
want=["wetype::server::enginev2::ImeEngine","wetype::server::enginev2::WximeImpl",
      "wetype::server::network::Network","wetype::server::clipboard::ClipboardDataManager",
      "wetype::server::ImeIpcServer","wetype::server::cross_platform::CrossPlatformManager",
      "wetype::server::handler::InputProcessor","wetype::server::vmode::VmodeDataManager",
      "wetype::server::report::ImeReport","wetype::server::handler::DictUpdater"]
CAP=10
lines=[]
for c in want:
    b=first.get(c); seen=0
    for i,(tgt,fn) in enumerate(b['fns']):
        if fn=='(no function)' or seen>=CAP: break
        lines.append("%s  %s#s%d"%(tgt,c.replace('::','_'),i)); seen+=1
open(r"D:\werev\out\addrs.txt",'w').write("\n".join(lines))
print("addrs:",len(lines))
