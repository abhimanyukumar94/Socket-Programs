
#Socket programming intro

#impoting socket library

import socket

#for error handling
import sys 
#creating sockets
try:
	s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_Stream for TCP ie stream socket/SOCK_DGRAM=UDP, AF_INET = IPv4
except socket.error, msg:
	print 'Failed to create socket. Error code' + str(msg[0]) + ', Error Message' + msg[1]
	sys.exit();
	
print 'socket created'


#CONFIGURING A REMOTE SERVER
host = 'www.google.com'
port = 80
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror: #if could not resolve
	print 'hostname could not be resolved. Exiting'
	sys.exit()

print 'IP address of remote host, ' + host + 'is ' + remote_ip

#CONNECTING TO THE REMOTE HOST
s.connect((remote_ip, port))

print 'socket connected to remote host, ' + host + 'on IP ' + remote_ip

#SENDING MESSAGE TO THE SERVER

#send some data to the server
message =  "GET / HTTP/1.1\r\n\r\n"

try:
	#send the whole string
	s.sendall(message)	#sendall function of socket sends data to the connected server
except socket.error:
	#send failure
	print 'Send failed'
	sys.exit()

print 'Message sent succesfully'

#RECEIVING DATA FROM THE CONNECTED SERVER
reply = s.recv(4096)	#recv function of socket receives data from the connected server

print 'Below is the message received from the server \n'
print reply

#close the socket
s.close()
print '\n Socket closed'
