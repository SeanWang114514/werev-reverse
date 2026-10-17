
import os, re, glob
pat = re.compile(r"log_crypt|xlogger|begin of mmap|mmap3|xlog|LogCrypt|zstd|Zstd", re.I)
for f in glob.glob(r"D:\VibeCoding\微信输入法逆向\out\strings\*.strings.tsv"):
    n=os.path.basename(f)
    for line in open(f, encoding="utf-8", errors="replace"):
        if pat.search(line):
            print(n+"\t"+line.rstrip()[:200])
