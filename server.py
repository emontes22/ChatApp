import socket
import threading

HOST = '127.0.0.1'
PORT = 8080
USER_LIMIT = 5
active_clients = [] # Connected users

# Listen for upcoming messages from a client
def listen_for_messages(client, username):
	# Keep listening for messages from the client
	while True:
		message = client.recv(2048).decode('utf-8')
		if message != '':
			final_msg = username + ':' + message
			send_messages(final_msg)
		else:
			print(f"Message send from client: {username} is empty")

# Send a message to one client
def send_message_to_client(client, message):
	client.sendall(message.encode())

# Send message to all clients currently connected to the server
def send_messages(message):
	
	for user in active_clients:
		send_message_to_client(user[1], message)


# Client handling
def client_handler(client):
	# Listen to client messages that contain the username
	while True:
		username = client.recv(2048).decode('utf-8')
		if username != '':
			active_clients.append((username, client))
			break
		else:
			print("Username is empty")

	threading.Thread(target=listen_for_messages, args=(client, username, )).start()

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

		threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
	main()