import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
print('tail 160', d[-160:].hex())
print('tail ascii', d[-160:].decode('latin1'))
print('size', len(d))