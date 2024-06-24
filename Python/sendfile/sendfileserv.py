
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import subprocess
import os
import sys
import threading

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
	recvBuff = b''
	
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

def handle_client_control(clientSock, addr):
	print("Accepted connection from client: ", addr)


	while True:
		command = clientSock.recv(1024).decode("utf-8")
		if command.startswith("ls"):
			files = os.llistdir('.')
			files_list = '\n'.join(files)
			clientSock.send(files_list.encode())
		elif command.startswith("get"):
			_, filename = command.split()
			if os.path.exists(filename):
				send_file(clientSock, filename)
			else:
				clientSock.send(b"ERROR: File not found")
		elif command.startswith("put"):
			_, filename = command.split()
			receive_file(clientSock, filename)
		elif command.startswith("quit"):
			break

	clientSock.close()

def send_file(clientSock, filename):
	fileSize = os.path.getsize(filename)
	clientSock.send(f"{fileSize:<10}".encode())

	with open(filename, 'rb') as file:
		bytes_read = file.read(1024)
		while bytes_read:
			clientSock.send(bytes_read)
			bytes_read = file.read(1024)

def receive_file(clientSock, filename):
	header = recvAll(clientSock, 10).decode().strip()
	fileSize = int(header)

	with open(filename, 'wb') as file:
		bytes_recieved = 0
		while bytes_recieved < fileSize:
			bytes_read = clientSock.recv(1024)
			if not bytes_read:
				break
			file.write(bytes_read)
			bytes_recieved += len(bytes_read)



# Accept connections forever
while True:
	
	print("Waiting for connections...")
		
	# Accept connections
	clientSock, addr = welcomeSock.accept()
	
	handle_client_control(clientSock, addr)
	




"""
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
"""
