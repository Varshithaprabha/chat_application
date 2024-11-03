import socket
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
import base64

def connect_to_server(username, password):
    try:
        client_socket.connect(('127.0.0.1', 5555))
        client_socket.send(f"{username}: {password}".encode('utf-8'))
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to server: {e}")
        return False

def send_message():
    message = message_entry.get()
    if message:
        client_socket.send(f"{username}: {message}".encode('utf-8'))
        message_entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, msg + "\n")
            chat_area.config(state=tk.DISABLED)
            chat_area.see(tk.END)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def upload_image():
    file_path = filedialog.askopenfilename()
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    client_socket.send(f"{username}: [IMAGE:{encoded_image}]".encode('utf-8'))

# Setup GUI
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root = tk.Tk()
root.title("Chat Application")

frame = tk.Frame(root)
frame.pack(pady=20)

chat_area = tk.Text(frame, width=50, height=20, state=tk.DISABLED)
chat_area.pack()

message_entry = tk.Entry(frame, width=40)
message_entry.pack(side=tk.LEFT, padx=10)

send_button = tk.Button(frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

upload_button = tk.Button(frame, text="Upload Image", command=upload_image)
upload_button.pack(side=tk.LEFT)

username = "user"  # Replace this with your username
password = "pass"  # Replace this with your password

if connect_to_server(username, password):
    threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
