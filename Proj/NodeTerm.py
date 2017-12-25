#NodeTerm.py
# Matthew Tea
#Imports
import socket
import subprocess
import re

UDP_PORT = 5007 #UDP Socket Needed
UDP_IP = ""
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Specify as UDP
try:
	sock.bind((UDP_IP, UDP_PORT)) #Connect, If fail, Force connect
except socket.error:
	temp = subprocess.Popen(['fuser','-k', str(UDP_PORT)+'/udp'])
	temp.kill()
	sock.bind((UDP_IP, UDP_PORT))
s = subprocess.Popen(['python','ProMon.py']) #initiates monitoring
while(True):
	data, addr = sock.recvfrom(1024) #listens for commands from central security
	print data
	if data == 'endcswmnode':
		s.kill()
		break
	else:
		try:
			toBeKilled = subprocess.check_output(['pidof',str(data)]).split()
			for d in toBeKilled:
				k = subprocess.Popen(['kill',d])
		except subprocess.CalledProcessError:
			if str(data).isdigit():
				toBeKilled = str(data)
				k = subprocess.Popen(['kill',toBeKilled])
			else:
				print("Process Typo or Process DNE")
				continue				

	
