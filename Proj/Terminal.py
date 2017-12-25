#Terminal.py
# Matthew Tea
#Imports
import subprocess
import re
import string
import socket
import signal

def append(conlist, string): #Appends to whitelist Function
	conlist.append(string)
	f = open('safe','w')
	for i in range(len(conlist)):
		f.write(conlist[i]+'\n')
	f.close()

def remove(conlist, rstr): #Removes from whitelist function
	conlist.remove(rstr)
	f = open('safe','w')
	for i in range(len(conlist)):
		f.write(conlist[i]+'\n')
	f.close()

def load(): #Reads Whitelist Function
	f = open('safe','r')
	strlist = f.read()
	f.close
	conlist = re.findall(r'([a-zA-Z].*)\n',strlist)
	return conlist

UDP_PORT = 5007 #uses 5007 to send remote commands
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conlist = load()
x = subprocess.Popen(['python','RecMon2.py']) #Init Subprocesses
y = subprocess.Popen(['python','RecMon.py'])
z = subprocess.Popen(['python','RecMon3.py'])
xpause = False
ypause = False

while (True): #terminal for commands
	command = raw_input('CSWM Terminal\n Commands:\n  Append <ProcessName>\n  Remove <ProcessName>\n  Kill <ProcessName> <IP>\n  Kill PID <PID> <IP>\n  Pause \'CPU\' or \'NW\'\n  Help\n  Exit\n')
	command = str(command).upper()
	if command == 'EXIT':
		x.kill()
		y.kill()
		z.kill()
		print('Exiting CSWM Terminal... Killing subprocesses.')
		break
	elif command.startswith('PRINT'):
		print(conlist)
	elif command.startswith('APPEND'):
		append(conlist,command.split('APPEND ',1)[1].lower())
	elif command.startswith('REMOVE'):
		try:
			remove(conlist,command.split('REMOVE ',1)[1].lower())
		except ValueError:
			print("Typo or that process does not exist in the whitelist.")
	elif command.startswith('KILL'):
		try:
			command, process, IP = command.split(' ')
		except ValueError:
			command, subcommand, process, IP = command.split(' ')
				
		sock.sendto(process.lower(), (IP, UDP_PORT))
	elif command.startswith('HELP'):
		print('\nAppend will add a process to the whitelist and update it.\nRemove will remove a process name from the whitelist.\nKill will kill a process on the specified Node by IP. \n(Typing endcswmnode instead of process name will end monitoring)\nPause will halt/resume output of detections\nUsing Pause \'status\' will display streaming status\nExit will exit this program.\n')
	elif command.startswith('PAUSE'):
		try:
			if command.split()[1].lower() == "cpu" and xpause==False:
				x.send_signal(signal.SIGSTOP)
				xpause = True
			elif command.split()[1].lower() == "cpu":
				x.send_signal(signal.SIGCONT)
				xpause = False
			elif command.split()[1].lower() == "nw" and ypause==False:
				y.send_signal(signal.SIGSTOP)
				ypause = True
			elif command.split()[1].lower() == "nw":
				y.send_signal(signal.SIGCONT)
				ypause = False
			elif command.split()[1].lower() == "status":
				print('\nCPU/MEM status paused: ' + str(xpause))
				print('NW status paused: ' + str(ypause)+'\n')
		except IndexError:
			print('Please use parameters cpu, nw or staus')
			continue
