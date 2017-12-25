#RecMon2.py
# Matthew Tea
#Imports
import socket
import subprocess
import time

def logger(data, addr): #Logs CPU and Mem issues
	f = open('CPU-MEMlog','a+')
	f.write("High Usage: " + data + " Loc: " + addr + '\n')
	f.close()

UDP_IP = ""
UDP_PORT = 5006 #listens on port 5006 for CPU and Mem Issues

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try: #Bind, If something is there, Kill it and take over.
	sock.bind((UDP_IP, UDP_PORT))
except socket.error:
	temp = subprocess.Popen(['fuser','-k', str(UDP_PORT)+'/udp'])
	time.sleep(3)
	sock.bind((UDP_IP, UDP_PORT))
	temp.kill()

while True:
	data, addr = sock.recvfrom(1024) # Wait for Data
	print "High Usage: ", data, "Loc:", addr[0]
	logger(data, addr[0])
