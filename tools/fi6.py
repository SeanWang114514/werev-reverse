# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
sizes=[offs[i+1]-offs[i] for i in range(cnt-1)]
print('max rec', max(sizes), 'min', min(sizes), 'sum', sum(sizes))
print('offsets', offs[:10], '...', offs[-3:])
print('filesize', len(d), 'last offset', offs[-1])