# client.py
import socket, threading

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break

name = input("Enter your name: ")
choice = input("Connect to Server1 or Server2? (1/2): ")

if choice == "1":
    port = 9000
    server_name = "Server1"
else:
    port = 9001
    server_name = "Server2"

sock = socket.socket()
sock.connect(("localhost", port))

threading.Thread(target=receive, args=(sock,), daemon=True).start()

print(f"Connected to {server_name}. Type messages, 'quit' to exit.")
while True:
    msg = input()
    if msg.lower() == "quit":
        break
    sock.sendall(f"{name}: {msg}".encode())
sock.close()
