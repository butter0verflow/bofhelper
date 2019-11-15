#!/usr/bin/env python
import sys, socket

host = str(raw_input("Host: "))
port = int(raw_input("Port: "))

prefix = ''
suffix = '\nexit\n'

print "******************************"
print "Verify the prefix and suffix"
print "[+]Prefix: " + prefix
print "[+]Suffix: " + suffix
print "******************************"

buffer=["A"]
counter=100
while len(buffer) <= 30:
	buffer.append("A"*counter)
	counter=counter+200
	
for string in buffer:
	payload = prefix + string + suffix
	print "Fuzzing with %s bytes" % len(string)
	try:
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connect=s.connect((host,port))
		#s.send(string + '\n')
		#s.send('exit\r\n')
		s.send(payload)
		s.recv(1024)
		s.close()
	except:
		print('We crashed it with %s' % len(string))
		exit()
