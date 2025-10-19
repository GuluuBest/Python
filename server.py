import socket
import threading

host = '127.0.0.1'
port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen()

print(f"Server berjalan di {host}:{port}, menunggu koneksi...")

clients = []

def broadcast(pesan, pengirim=None):
    for client in clients:
        if client != pengirim:
            try:
                client.send(pesan)
            except:
                clients.remove(client)
                client.close()

def handle_client(conn, addr):
    print(f"Terhubung dengan client dari {addr}")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} terputus.")
                break
            pesan = data.decode()
            print(f"Pesan dari {addr}: {pesan}")
            kirim = f"({addr[0]}): {pesan}"
            broadcast(kirim.encode(), pengirim=conn)
    except ConnectionResetError:
        print(f"Client {addr} memutus koneksi.")
    finally:
        if conn in clients:
            clients.remove(conn)
        conn.close()
        print(f"Koneksi dari {addr} ditutup.")
try:
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
except KeyboardInterrupt:
    print("\n🛑 Server dihentikan secara manual.")

server_socket.close()
print("Server berhenti.")
