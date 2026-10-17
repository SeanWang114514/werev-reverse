#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick PE summary via lief for a single file."""
import sys, json, lief, hashlib
p = sys.argv[1]
b = open(p, "rb").read()
print("file:", p, "size:", len(b), "sha256:", hashlib.sha256(b).hexdigest())
bin_ = lief.PE.parse(list(b))
if bin_ is None:
    print("not a PE"); sys.exit(0)
print("machine:", bin_.header.machine, "is_dll:", bin_.header.characteristics & 0x2000 != 0)
print("timestamp:", bin_.header.time_date_stamps)
for e in bin_.data_directories:
    print("  dir", e.type, "rva", hex(e.rva), "size", e.size)
print("sections:")
for s in bin_.sections:
    print("  %-10s vsize=%#x raw=%#x chars=%#x" % (s.name, s.virtual_size, s.size, s.characteristics))
print("exports (%d):" % len(bin_.exported_functions))
names = []
for f in bin_.exported_functions:
    names.append(f.name)
for n in names[:200]:
    print("   ", n)
print("imports:")
for imp in bin_.imports:
    print("   ", imp.name, len(imp.entries))
