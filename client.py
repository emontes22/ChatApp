import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 8080

BLACK = '#000000'
NAVY = '#030c1c'
WHITE = '#FFFFFF'
FONT = ('Verdana', 15)
MEDIUM_FONT = ('Verdana', 12)
SMALL_FONT = ('Verdana', 10)

# Socket class object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
	message_box.config(state=tk.NORMAL)
	message_box.insert(tk.END, message + "\n")
	message_box.config(state=tk.DISABLED)

def connect():
	# Connect to server
	try:
		client.connect((HOST, PORT))
		add_message("[SERVER]: Sucessfully connected to the server!")
	except:
		messagebox.showerror("Unable to connect to server.", f"Unable to connect to server: {HOST}:{PORT}")

	username = username_textbox.get()
	if username != '':
		client.sendall(username.encode())
	else:
		messagebox.showerror("Invalid username", "Username cannot be empty")

	threading.Thread(target=listen_for_messages, args=(client, )).start()

	username_textbox.config(state=tk.DISABLED)
	username_button.config(state=tk.DISABLED)

def send_message():
	message = message_textbox.get()
	if message != '':
		client.sendall(message.encode())
		message_textbox.delete(0, len(message))
	else:
		messagebox.showerror("Message is empty", "Message cannot be empty")

root = tk.Tk()
root.geometry("500x500")
root.title("Chat Application")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=3)
root.grid_rowconfigure(2, weight=1)

top = tk.Frame(root, width=500, height=80, bg=BLACK)
top.grid(row = 0, column = 0, sticky = tk.NSEW)

mid = tk.Frame(root, width=500, height=340, bg=NAVY)
mid.grid(row = 1, column = 0, sticky = tk.NSEW)

bot = tk.Frame(root, width=500, height=80, bg=BLACK)
bot.grid(row = 2, column = 0, sticky = tk.NSEW)

username_label = tk.Label(top, text="Enter username: ", font=FONT, bg=BLACK, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=3)

username_textbox = tk.Entry(top, font=FONT, bg=BLACK, fg=WHITE, width=18)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top, text="Join", font=MEDIUM_FONT, bg=BLACK, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bot, font=FONT, bg=BLACK, fg=WHITE, width=30)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bot, text="Send", font=MEDIUM_FONT, bg=BLACK, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(mid, font=SMALL_FONT, bg= NAVY, fg=WHITE, width=62, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

def listen_for_messages(client):
	while True:
		message = client.recv(2048).decode('utf-8')
		if message != '':
			username = message.split(":")[0]
			content = message.split(":")[1]

			add_message(f"[{username}] {content}")
		else:
			messagebox.showerror("Error", "Message received is empty")

def main():

	root.mainloop()

if __name__ == '__main__':
	main()