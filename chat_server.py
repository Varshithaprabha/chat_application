import socket
import threading
import sqlite3
from datetime import datetime

# SQLite database for user authentication and message history
def init_db():
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (username TEXT, message TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def handle_client(client_socket, client_address):
    print(f"Connection from {client_address} has been established.")
    
    while True:
        msg = client_socket.recv(1024).decode('utf-8')
        if msg == 'exit':
            break
        username, message = msg.split(': ', 1)
        print(f"[{username}] {message}")
        save_message(username, message)
        broadcast(msg, client_socket)

    client_socket.close()

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message.encode('utf-8'))

def save_message(username, message):
    conn = sqlite3.connect('chat_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)",
              (username, message, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def start_server():
    init_db()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)
    
    print("Server is listening...")
    
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

clients = []
start_server()
