import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
paths=[r'C:\Program Files\Tencent\WeType\3.0.0.34\libwxhld.dll',
       r'C:\Program Files\Tencent\WeType\2.1.4.6\libwxhld.dll' ]
import os
for p in paths:
    if not os.path.exists(p): print('missing', p); continue
    b=open(p,'rb').read()
    print(p, len(b))
    for pat in [b'noun_tag', b'noun', b'cell_dict', b'large_dict', b'BuildIn', b'sepd', b'wkvc2e', b'ckvd']:
        print('  ', pat, b.find(pat))