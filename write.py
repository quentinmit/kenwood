#!/usr/bin/python

import sys
import csv
import kenwood

ser = kenwood.open()

cr = csv.reader(sys.stdin)
print "Got headers", cr.next()

header = ""
while not header:
    ser.write("ID\r")
    header = kenwood.readline(ser)
    print "Got header:", header

for l in cr:
    channel = l[0]
    try:
        channel = "%03d" % int(channel)
    except:
        pass
    name = l[1]
    data = l[2:]
    if data[0]: # There's a frequency specified
        data = kenwood.freq.human2radio(data)
        print "For channel", channel, " ("+name+") setting data", data
        command = "MW 0,"+channel+","+",".join(data)+"\r"
        print command
        ser.write(command)
        print kenwood.parse_reply(kenwood.readline(ser))
        if name:
            ser.write("MNA "+channel+","+name+"\r")
            print kenwood.parse_reply(kenwood.readline(ser))
