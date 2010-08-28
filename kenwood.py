#!/usr/bin/python

import serial
import sys
import os
import time
import csv

STEP_SIZES = {
    '0': '5.0 kHz',
    '1': '6.25 kHz',
    '2': '8.33 kHz',
    '3': '9.0 kHz',
    '4': '10.0 kHz',
    '5': '12.5 kHz',
    '6': '15.0 kHz',
    '7': '20.0 kHz',
    '8': '25.0 kHz',
    '9': '30.0 kHz',
    'a': '50.0 kHz',
    'b': '100.0 kHz',
    }
SHIFT = {
    '0': '',
    '1': '+',
    '2': '-',
    }
TONE_FREQ = {
    '00': '67.0', 
    '01': '69.3', 
    '02': '71.9', 
    '03': '74.4', 
    '04': '77.0', 
    '05': '79.7', 
    '06': '82.5', 
    '07': '85.4', 
    '08': '88.5', 
    '09': '91.5', 
    '10': '94.8', 
    '11': '97.4', 
    '12': '100.0',
    '13': '103.5',
    '14': '107.2',
    '15': '110.9',
    '16': '114.8',
    '17': '118.8',
    '18': '123.0',
    '19': '127.3',
    '20': '131.8',
    '21': '136.5',
    '22': '141.3',
    '23': '146.2',
    '24': '151.4',
    '25': '156.7',
    '26': '162.2',
    '27': '167.9',
    '28': '173.8',
    '29': '179.9',
    '30': '186.2',
    '31': '192.8',
    '32': '203.5',
    '33': '206.5',
    '34': '210.7',
    '35': '218.1',
    '36': '225.7',
    '37': '229.1',
    '38': '233.6',
    '39': '241.8',
    '40': '250.3',
    '41': '254.1',
    }

DCS_CODE = {
    '000': '023',
    '001': '025',
    '002': '026',
    '003': '031',
    '004': '032',
    '005': '036',
    '006': '043',
    '007': '047',
    '008': '051',
    '009': '053',
    '010': '054',
    '011': '065',
    '012': '071',
    '013': '072',
    '014': '073',
    '015': '074',
    '016': '114',
    '017': '115',
    '018': '116',
    '019': '122',
    '020': '125',
    '021': '131',
    '022': '132',
    '023': '134',
    '024': '143',
    '025': '145',
    '026': '152',
    '027': '155',
    '028': '156',
    '029': '162',
    '030': '165',
    '031': '172',
    '032': '174',
    '033': '205',
    '034': '212',
    '035': '223',
    '036': '225',
    '037': '226',
    '038': '243',
    '039': '244',
    '040': '245',
    '041': '246',
    '042': '251',
    '043': '252',
    '044': '255',
    '045': '261',
    '046': '263',
    '047': '265',
    '048': '266',
    '049': '271',
    '050': '274',
    '051': '306',
    '052': '311',
    '053': '315',
    '054': '325',
    '055': '331',
    '056': '332',
    '057': '343',
    '058': '346',
    '059': '351',
    '060': '356',
    '061': '364',
    '062': '365',
    '063': '371',
    '064': '411',
    '065': '412',
    '066': '413',
    '067': '423',
    '068': '431',
    '069': '432',
    '070': '445',
    '071': '446',
    '072': '452',
    '073': '454',
    '074': '455',
    '075': '462',
    '076': '464',
    '077': '465',
    '078': '466',
    '079': '503',
    '080': '506',
    '081': '516',
    '082': '523',
    '083': '526',
    '084': '532',
    '085': '546',
    '086': '565',
    '087': '606',
    '088': '612',
    '089': '624',
    '090': '627',
    '091': '631',
    '092': '632',
    '093': '654',
    '094': '662',
    '095': '664',
    '096': '703',
    '097': '712',
    '098': '723',
    '099': '731',
    '100': '732',
    '101': '734',
    '102': '743',
    '103': '754',
    }

MODE = {
    '0': 'FM',
    '1': 'WFM',
    '2': 'AM',
    '3': 'LSB',
    '4': 'USB',
    '5': 'CW',
    }

def readline(ser, limit=-1):
    res = ""
    while limit < 0 or len(res) < limit:
        b = ser.read(1)
        if not b:
            break
        if b == ("\r"):
            break
        res += b
    return res
def slowwrite(ser, data, delay=1):
    for b in data:
        print "Writing", b
        ser.write(b)
        time.sleep(delay)

def parse_reply(reply):
    if reply == "N":
        return None
    command,args = reply.split(" ", 2)
    args = args.split(",")
    return [command]+args

ser = serial.Serial()
ser.port = "/dev/cu.usbserial"
#ser.port = "/dev/cu.PL2303-0000101D"
ser.baudrate = 9600
ser.parity = 'N'
ser.rtscts = False
ser.xonxoff = False
ser.timeout = 2
ser.interCharTimeout = 1

try:
    ser.open()
except serial.SerialException, e:
    sys.stderr.write("Could not open serial port %s: %s\n" % (ser.portstr, e))
    sys.exit(1)

ser.write("ID\r")
print >>sys.stderr, readline(ser)

channels = ["%03d" % i for i in range(0,399)] + [i+str(j) for i in ("L", "U", "I-") for j in range(0,9)] + ["PR1", "PR2"]

cwr = csv.writer(sys.stdout)
cwr.writerow(["Channel", "Name", "Frequency", "Step", "Shift", "Reverse", "Tone", "Tone Freq", "DCS code", "Offset", "Mode", "Lockout"])

for c in channels:
    ser.write("MR 0,"+c+"\r")
    rx = parse_reply(readline(ser))
    ser.write("MR 1,"+c+"\r")
    tx = parse_reply(readline(ser))
    ser.write("MNA "+c+"\r")
    name = parse_reply(readline(ser))
    if name:
        name = name[2]
    if not rx:
        rx = [None]*9
    else:
        freq, step, shift, rev, tone, ctcss, dcs, tone_freq, ctcss_freq, dcs_code, offset, mode, lockout = rx[3:]
        if len(freq) == 11:
            freq = freq[:5]+"."+freq[5:]
        step = STEP_SIZES.get(step, step)
        shift = SHIFT.get(shift, shift)
        if int(dcs):
            tone = "D"
        elif int(ctcss):
            tone = "C"
        elif int(tone):
            tone = "T"
        if tone == "C":
            tone_freq = TONE_FREQ.get(ctcss_freq, ctcss_freq)
        else:
            tone_freq = TONE_FREQ.get(tone_freq, tone_freq)
        dcs_code = DCS_CODE.get(dcs_code, dcs_code)
        mode = MODE.get(mode, mode)
        offset = offset[:3]+"."+offset[3:]
        rx = [freq,step,shift,rev,tone, tone_freq, dcs_code, offset, mode, lockout]
    
    cwr.writerow([c, name]+rx)
