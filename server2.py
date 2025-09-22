# server2.py
import socket, threading, time

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
SERVER_PORT = 9001
PEER_HOST   = "localhost"
PEER_PORT   = 9100   # connects to Server1’s peer port

# client listener
server_sock = socket.socket()
server_sock.bind(("localhost", SERVER_PORT))
server_sock.listen()

# connect to peer (retry until success)
while True:
    try:
        s = socket.socket()
        s.connect((PEER_HOST, PEER_PORT))
        peer_conn = s
        threading.Thread(target=handle_peer, args=(s,), daemon=True).start()
        break
    except:
        time.sleep(1)

print("Server2 running...")

# accept clients
while True:
    conn, _ = server_sock.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
