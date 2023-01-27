import socket
import threading

HOST = '127.0.0.1'
PORT = 8080
USER_LIMIT = 5

def main():
	# Socket class object
	# AF_INET = Using IPv4 addresses
	# SOCK_STREAM = using TCP packets for communication
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server.bind((HOST, PORT))
		print(f"Running server on {HOST}:{PORT}")
	except:
		print(f"Unable to connect to server: {HOST} with port: {PORT}")

	# Server limit (users)
	server.listen(USER_LIMIT)

	# To listen to client connections
	while True:
		client, address = server.accept()
		print(f"Sucessfully connected to client: {address[0]} {address[1]}")

if __name__ == '__main__':
	main()