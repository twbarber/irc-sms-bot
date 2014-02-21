import socket

server = 'harperslittleroom.org'
port = 6667
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect_to_server():
	irc.connect(server, port)
	print(irc.recv(4096))
	irc.send ( 'NICK smsbot\r\n' )
	irc.send ( 'JOIN #nerds\r\n' )
	#irc.send ( 'PRIVMSG #Paul :Hello World.\r\n' )

def main():
	connect_to_server()
	while True:
		data = irc.recv(4096)
		if data.find ( 'PING' ) != -1:
			irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
