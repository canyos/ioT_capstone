import socket

def ipcheck():
	return socket.gethostbyname(socket.getfqdn())

print(ipcheck())