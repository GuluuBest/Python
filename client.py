import socket
import threading

host = '127.0.0.1'
port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

print(f"Terhubung ke server di {host}:{port}")
print("Ketik 'exit' untuk keluar dari chat.\n")

def terima_pesan():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Server menutup koneksi.")
                break
            print(f"\n{data.decode()}")
        except:
            print("Terjadi kesalahan koneksi.")
            break

threading.Thread(target=terima_pesan, daemon=True).start()

while True:
    pesan = input("")
    if pesan.lower() == 'exit':
        print("Keluar dari chat...")
        client_socket.close()
        break
    try:
        client_socket.send(pesan.encode())
    except:
        print("Koneksi ke server hilang.")
        break
