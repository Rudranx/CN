import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 12345))  # connect to server

    while True:
        msg = input("Enter message (type 'exit' to quit): ")
        if msg.lower() == "exit":
            break
        client.send(msg.encode())
        echo = client.recv(1024).decode()
        print("Echo from server:", echo)

    client.close()

if __name__ == "__main__":
    start_client()
