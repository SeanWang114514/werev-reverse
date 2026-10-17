
import pefile, re, os, sys
p = r"D:\VibeCoding\微信输入法逆向\samples\libwxhld.dll"
pe = pefile.PE(p, fast_load=True)
pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']])
names = sorted(e.name.decode() for e in pe.DIRECTORY_ENTRY_EXPORT.symbols if e.name)
print("exports:", len(names))
import collections
pref = collections.Counter(n.split("_")[1] if n.startswith("wxime_") else ("?"+n.split("_")[0]) for n in names)
print(pref.most_common(40))
print()
for n in names:
    if n.startswith("wxime_") and re.search(r"exec|command|replay|load|json|remote|config|dict|session|input|candidate", n):
        print("  ", n)
