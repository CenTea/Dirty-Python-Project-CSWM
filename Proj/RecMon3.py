#RecMon3.py
# Matthew Tea
#Imports
import socket
import subprocess
import re

def load(): #Loads Whitelist
	f = open('safe','r')
	strlist = f.read()
	f.close
	conlist = re.findall(r'([a-zA-Z].*)\n',strlist)
	return conlist

UDP_IP = ""
UDP_PORT = 5025 #listens on port 5025

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP

try: #Bind, If taken Kill and take
	sock.bind((UDP_IP, UDP_PORT))
except socket.error:
	temp = subprocess.Popen(['fuser','-k', str(UDP_PORT)+'/udp'])
	time.sleep(3)
	sock.bind((UDP_IP, UDP_PORT))
	temp.kill()
	
conlist = load() #Loads Whitelist.

while True:
	data, addr = sock.recvfrom(1024) # Waits for Request
	for x in conlist: #When request is recieved, Send Whitelist
		sock.sendto(x, (addr[0],5050))
	sock.sendto("END", (addr[0],5050))
