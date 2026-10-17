import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=r'D:\VibeCoding\微信输入法逆向\out\reports'
for f in sorted(os.listdir(d)):
    p=os.path.join(d,f)
    print('%-28s %10d' % (f, os.path.getsize(p)))