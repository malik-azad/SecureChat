import socket
import threading

def receive_messages(connection):
    while True:
        try:
            message = connection.recv(1024).decode()
            if message:
                print("\nReceived:", message)
            else:
                break
        except ConnectionResetError:
            print("\nConnection closed by the server.")
            break

def send_messages(connection):
    while True:
        message = input("Enter message: ")
        connection.send(message.encode())

def start_server():
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 5555

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server listening on port", port)

    connection, address = server_socket.accept()
    print("Connected to", address)

    receive_thread = threading.Thread(target=receive_messages, args=(connection,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(connection,))
    send_thread.start()

def start_client(server_ip):
    host = server_ip
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server at", host)

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    role = input("Run as (s)erver or (c)lient ? ")

    if role.lower() == 's':
        start_server()
    elif role.lower() == 'c':
        server_ip = input("Enter server IP address: ")
        start_client(server_ip)
    else:
        print("Invalid choice. Please enter 's' for server or 'c' for client.")
