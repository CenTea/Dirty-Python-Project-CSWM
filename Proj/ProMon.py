#ProMon.py
# Matthew Tea
#Imports
import time
import socket
import subprocess
import re
import datetime

def proccheck(conlist): #Checks if value is in list. If not, store in another list. then return list (used for whitelist Check.)
	flist = []
	x = subprocess.check_output(['ps','-A'])
	value = re.findall(r':[0-9][0-9] ([a-zA-Z].*)\n', x)
	for i in value:
		if i not in conlist:
			flist.append(str(datetime.datetime.now()).split('.')[0]+" "+i)
	return flist

def tcheck(typecheck): #Check for Mem and CPU usage.
	x = subprocess.check_output(['ps','-eo', 'pid,cmd,%mem,%cpu'])
	value = re.findall(r'\s*([0-9]*)\s*(.*\s)\s*([0-9]+.[0-9])\s*([0-9]+.[0-9])\n', x)
	for i in value:
		if typecheck == 1 and float(i[3]) > 10:
			return(i[1].rstrip().lstrip()+' [CPU] '+i[3] + ' PID: ' + i[0])
		if typecheck == 2 and float(i[2]) > 15:
			return(i[1].rstrip().lstrip()+' [MEM] '+i[2] + ' PID: ' + i[0])

UDP_IP = "172.31.23.249" #Central IP
UDP_PORT = 5005 #Non Whitelist Usage
UDP_PORT2 = 5006 #CPU usage and Mem usage
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("", 5050))
data = "holder"
conlist = []
detectlist = []
sock.sendto("REQ", ("172.31.23.249", 5025)) #Requests Whitelist from Central on run
print "Waiting for Whitelist..."
while (data != "END"):
	if data != "END":
		data, addr = sock.recvfrom(1024)
		conlist.append(data) #constructs whitelist


while(True):
	x = tcheck(1)
	if x != None:
		sock.sendto(x, (UDP_IP, UDP_PORT2))
		print('High CPU Usage: '+ x)
	z = tcheck(2)
	if z != None:
		sock.sendto(z, (UDP_IP, UDP_PORT2))
		print('High Mem Usage: '+ x)
	p = proccheck(conlist)
	for w in range(0,len(p)):
		y = re.search(r':[0-9][0-9] (.*)', p[w])
		if y.group(1) not in detectlist:
			detectlist.append(y.group(1))
			sock.sendto(p[w], (UDP_IP, UDP_PORT))
			print('Non Whitelisted Process Detected: '+ p[w])
	time.sleep(.5)
