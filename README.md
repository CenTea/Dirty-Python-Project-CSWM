# CSWM - Central Security Whitelist Model

A project I had for cloud computing.

Intended to be a process checking system for Linux between different computers/VMs.

It was tried on AWS and attempted to manage multiple EC2 Ubuntu systems.

There are better ways to go around this, but unfortunately there was a time factor to deal with.

Contents:

  Two "Terminal" based python files that "manage" the other pyhton sub processes.
  
  2 files for the monitored node
  
    NodeTerm.py
    ProMon.py
    
  4 files for the Central Security Node
  
    Terminal.Py
    RecMon.py
    RecMon2.py   
    RecMon3.py 
    
Notable Issues:

	Uses UDP inefficiently
	The way Sockets were used
	The way Subprocesses were managed and used.
 	Vulnerable to attacks

Tested and made on xUbuntu 14.04:

	May not work with new versions of xUbuntu.
