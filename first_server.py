import socket
import sys
from thread import * #include library to create indivisual threads for each connection

host = ''
port = 8888 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'socket created'

#bind the socket to the port

try:
	s.bind((host,port))

except socket.error, msg:
	print 'Bind, error code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'socket bind complete'

#by binding the socket, we ensure that all the traffic at the IP:port is received by the application
#this means you can't have 2 socket bind to the same port, though exceptions are there

#listening at the socket using socket_listen

s.listen(10) #argument 10 is the max number of request to be kept in waiting at he time, the 11th request is rejected

print 'Socket is listening'

#function to run threads. this function will be used to create threads
def threads(conn):
	#sending message to the client once connected
	conn.send('Welcome to the BAT server. Type anything and enter \n') #send function takes in only strings
	
	#infinite loop to receive message to the client
	while True: 
		data  = conn.recv(1094)
		reply = 'Hello bc ' + data
		if not data:
			break
		conn.sendall(reply)
	conn.close()
	 

#waiting to accept connections, indefinitly
while 1:
	conn, addr = s.accept()

	print 'socket connected to host with IP ' + addr[0] + ' at port: ' + str(addr[1])

	#using thread function to interact with the client, first argument is the thread function and other is the argument of the
	#thread function
	start_new_thread(threads, (conn,))

s.close()	
