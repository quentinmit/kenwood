#!/usr/bin/env python3

import sys

class Decryptor(object):
    decrypting = True
    key = 39
    key_incr = 39

    def decrypt(self, input):
        if not self.decrypting:
            return input
        if not input:
            return ""
        output = ""
        if input[0] == "$":
            for i in range(1, (len(input)-1)//2 + 1):
                offset = (i-1) * 2 + 1
                n = int(input[offset:offset+2], 16)
                n = n ^ ((i & 1) * 255)
                n = (n - self.key) & 255
                output += chr(n)
                self.key = (self.key + self.key_incr) & 255
        else:
            output += ":"
            for i in range(1, (len(input)-1)//2 + 1):
                offset = (i-1) * 2 + 1
                n = int(input[offset:offset+2], 16)
                n = n ^ ((i & 1) * 255)
                n = (n - self.key) & 255
                output += "%02X" % n
                self.key = (self.key + self.key_incr) & 255
        return output
d = Decryptor()

for line in sys.stdin:
    print(d.decrypt(line.strip()))
