import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
for base in [r'C:\Users\Administrator\AppData\LocalLow\Tencent\WeType\Dict', r'C:\Users\Administrator\AppData\LocalLow\Tencent\WeType\DictDir2']:
    if os.path.isdir(base):
        for r0,ds,fs in os.walk(base):
            for f in fs:
                p=os.path.join(r0,f)
                print(p, os.path.getsize(p))
    else:
        print('missing', base)