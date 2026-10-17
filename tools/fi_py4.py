# -*- coding: utf-8 -*-
import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
# pattern: 'P' 0x01 <n> <ascii pinyin, groups separated by 0x00>
pat=re.compile(rb'P\x01(?P<n>[\x03-\x28])(?P<body>[\x20-\x7e\x00]{3,40})')
out=[]
for m in pat.finditer(d):
    n=m.group('n')[0]
    body=m.group('body')[:n]
    if len(body)<n: continue
    s=body.decode('ascii','replace')
    s=s.replace('\x00',',')
    if re.fullmatch(r'[a-z]+(,[a-z]+)*', s):
        out.append((m.start(), s))
print('valid pinyin records', len(out))
for off,s in out[:20]: print(hex(off), s)
print('...')
for off,s in out[-10:]: print(hex(off), s)