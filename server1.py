# server1.py
import socket, threading

clients = []
peer_conn = None

def handle_client(conn):
    global peer_conn
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            broadcast(msg, conn)
            if peer_conn:
                peer_conn.sendall(msg.encode())
        except:
            break
    conn.close()
    if conn in clients:
        clients.remove(conn)

def broadcast(msg, sender=None):
    for c in clients:
        if c != sender:
            try:
                c.sendall(msg.encode())
            except:
                pass

def handle_peer(conn):
    global clients
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            broadcast(msg)
        except:
            break
    conn.close()

# --- setup ---
SERVER_PORT = 9000
PEER_PORT   = 9100   # where we expect Server2 to connect

# client listener
server_sock = socket.socket()
server_sock.bind(("localhost", SERVER_PORT))
server_sock.listen()

# peer listener
peer_sock = socket.socket()
peer_sock.bind(("localhost", PEER_PORT))
peer_sock.listen()

print("Server1 running...")

# accept peer (Server2 will connect here)
def accept_peer():
    global peer_conn
    conn, _ = peer_sock.accept()
    peer_conn = conn
    threading.Thread(target=handle_peer, args=(conn,), daemon=True).start()

threading.Thread(target=accept_peer, daemon=True).start()

# accept clients
while True:
    conn, _ = server_sock.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
