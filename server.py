import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 8080

def handle_client(client_socket, client_list):
    while True:
        data = client_socket.recv(4096)
        if not data:
            client_list.remove(client_socket)
            break

        for client in client_list:
            if client != client_socket:
                client.sendall(data)

    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print("Waiting for connections...")

    client_list = []

    while True:
        client_socket, addr = server_socket.accept()
        print("Accepted connection from:", addr)
        client_list.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_list))
        client_thread.start()

if __name__ == "__main__":
    main()
