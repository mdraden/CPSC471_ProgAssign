
# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys

# Command line checks 
if len(sys.argv) < 2:
    print("USAGE python " + sys.argv[0] + " file.txt")
    # sys.exit(1)

# Server address
serverAddr = "localhost"

# Server port
serverPort = 21

# The name of the file
fileName = 'sendfile\\file.txt'

# Check if the file exists
if not os.path.exists(fileName):
    print(f"ERROR: {fileName} does not exist")
    sys.exit(1)

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# Open the file in binary mode
with open(fileName, "rb") as fileObj:
    # Get the file size
    fileObj.seek(0, os.SEEK_END)
    fileSize = fileObj.tell()
    fileObj.seek(0, os.SEEK_SET)

    # Prepare the size string and prepend it to the file data
    dataSizeStr = f"{fileSize:<10}".encode('utf-8')

    # Send the size of the data
    connSock.send(dataSizeStr)

    # Keep sending until all is sent
    while True:
        # Read 65536 bytes of data
        fileData = fileObj.read(65536)
        
        # If we hit EOF, break
        if not fileData:
            break

        # Send the file data
        connSock.sendall(fileData)

print("File sent successfully.")

# Close the socket
connSock.close()
