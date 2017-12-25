#RecMon.py
# Matthew Tea
#Imports
import socket
import subprocess
import time

def logger(data, addr): #Logs Non Whitelists
	f = open('NonWLPlog','a')
	f.write("Non whitelisted process detected: " + data + " Loc: " + addr + '\n')
	f.close()

def counter(listofv): #Counter Log
	f = open('Counter','w')
	for x in listofv:
		f.write(str(x[0]) + " "+ str(x[1])+ " "+ str(x[2]) + "\n")
	f.close()

def loadlist(listofv): #loads counter into Memory
	try:
		f = open('Counter','r')
	except IOError:
		f = open ('Counter','w')
		f.close
	f = open('Counter','r')
	strlist = f.read()
	f.close
	listofv = [strlist.split()[i:i+3] for i in range (0,len(strlist.split()),3)]


UDP_IP = ""
UDP_PORT = 5005 #listens on 5005 for cpu and mem issues.
listofv = []
loadlist(listofv)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
	sock.bind((UDP_IP, UDP_PORT))
except socket.error:
	temp = subprocess.Popen(['fuser','-k', str(UDP_PORT)+'/udp'])
	time.sleep(3)
	sock.bind((UDP_IP, UDP_PORT))
	temp.kill()

while True:
	data, addr = sock.recvfrom(1024) # Recieves Data
	print "Non whitelisted process detected: ", data, " Loc: ", addr[0]
	for x in listofv:
		if data.split()[2] == x[0] and addr[0] == x[1]:
			x[2]+=1
			counter(listofv)
			break
	else:
		listofv.append([data.split()[2] ,addr[0],1])
		counter(listofv)
		
	logger(data, addr[0])
