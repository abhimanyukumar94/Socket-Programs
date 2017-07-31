#TCP client application

import sys, socket, select, string

def prompt():
	sys.stdout.write('<You>')
	sys.stdout.flush()

#main function
if __name__ == "__main__":

	if (len(sys.argv) < 3):
		print 'Usage: python client_TCP_chat.py hostname port'
		sys.exit()

	host = sys.argv[1]
	port = int(sys.argv[2])

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	s.settimeout(10)

	#connect to a remote host
	try:
		s.connect((host, port))
	except:
		print 'Unable to connect'
		sys.exit()

	print 'Connect to remote host. Send message...'
	prompt()
	
	while 1:
		socket_list = [sys.stdin, s]
		
		#GET readable sockets
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		
		for sock in socket_list:
			#for incoming messages from a remote server
			if sock == s:
				data = s.recv(4096)
				if not data:
					print '\nDisconnted from the chat server'
					sys.exit()
				else:
					#print data
					sys.stdin.write(data)
					prompt()
			
			#for user generated message
			else:
				msg = sys.stdin.readline()
				s.send(msg)
				prompt()
