#TCP Chat server

import socket, select

#Function to broadcast messages received from client to all other clients
def broadcast_msg(sock, msg):
	for socket in CONNECTION_LIST:
		if socket != server_socket and socket != sock:
			try:
				socket.send(msg)
			except:
				#for broken socket connection, maybe due to client exited
				socket.close()
				CONNECTION_LIST.remove(socket)

if __name__ == "__main__":	#like void main
	#array to keep track of number of connections
	CONNECTION_LIST = []
	recv_buffer = 4096 #advisable to keep at the power of 2
	port = 5000

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #what is the use
	server_socket.bind(("0.0.0.0", port))	
	server_socket.listen(10)

	#Add server socket to the list of connections	
	CONNECTION_LIST.append(server_socket)
	
	print "server socket connected to port " + str(port)
	
	while 1:
		#get the list of sockets ready to be read using select	
		read_socket, write_socket, error_socket = select.select(CONNECTION_LIST, [], []) #(readable sockets, writable sockets			, error sockets) the latter 2 have been left blank
		
		for sock in read_socket:
			#new connections
			if sock == server_socket:
				#when there's is a new connection received at server socket
				sockfd, addr = server_socket.accept()
				CONNECTION_LIST.append(sockfd)
				print "Client (%s, %s) connected" % addr
				
				broadcast_msg(sockfd, "[%s:%s] entered the room" % addr)

			#some incoming message from a client
			else:
				try:
					data = sock.recv(recv_buffer)
					if data:
						broadcast_msg(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
						
				except:
					broadcast_msg(sock, "Client (%s, %s) is offline" % addr)
					print "Client (%s, %s) is offline" % addr
					sock.close()
					CONNECTION_LIST.remove(sock)
					continue
	server_socket.close()
	 
