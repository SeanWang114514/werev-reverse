import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
root=r'D:\VibeCoding\微信输入法逆向'
bi=r'C:\Program Files\Tencent\WeType\3.0.0.34\BuildIn'
idx=json.load(open(os.path.join(bi,'index.json'),encoding='utf-8'))
rows=[]
for it in idx:
    p=os.path.join(bi,it['name'])
    sz=os.path.getsize(p) if os.path.exists(p) else -1
    head=open(p,'rb').read(32) if sz>0 else b''
    rows.append((it['name'],sz,it['type'],it['dict_type'],it['uniqueID'],it['version'],head[:16].hex()))
out=open(os.path.join(root,'out','reports','buildin_catalog.tsv'),'w',encoding='utf-8')
out.write('name\tsize\ttype\tdict_type\tuniqueID\tversion\thead16\n')
for r in rows: out.write('\t'.join(str(x) for x in r)+'\n')
out.close()
print('rows', len(rows))