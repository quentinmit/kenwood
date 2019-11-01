#!/usr/bin/env python3

import sys

name = sys.argv[1]

out = ""
i = 0

for line in open(name, 'r'):
    if not line.strip():
        if out:
            open("%s-part%d.hex" % (name, i), "w").write(out)
            out=""
            i+=1
        continue
    out += line

if out:
    open("%s-part%d.hex" % (name, i), "w").write(out)
