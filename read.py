#!/usr/bin/python

import sys
import csv
import kenwood

ser = kenwood.open()

cwr = csv.writer(sys.stdout)
cwr.writerow(["Channel", "Name", "Frequency", "Step", "Shift", "Reverse", "Tone", "Tone Freq", "DCS code", "Offset", "Mode", "Lockout"])

for c in kenwood.CHANNELS:
    ser.write("MR 0,"+c+"\r")
    rx = kenwood.parse_reply(kenwood.readline(ser))
    ser.write("MR 1,"+c+"\r")
    tx = kenwood.parse_reply(kenwood.readline(ser))
    ser.write("MNA "+c+"\r")
    name = kenwood.parse_reply(kenwood.readline(ser))
    if name:
        name = name[2]
    if not rx:
        rx = [None]*9
    else:
        rx = kenwood.freq.radio2human(rx[3:])

    cwr.writerow([c, name]+rx)
