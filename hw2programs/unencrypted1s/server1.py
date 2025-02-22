import socket
import os

# --- Server Code ---
def server():
    HOST = '0.0.0.0'
    PORT = 6000
    UPLOAD_DIR = './uploads'
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server running on {HOST}:{PORT}...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            # Receive file metadata
            file_name = client_socket.recv(1024).decode()
            file_path = os.path.join(UPLOAD_DIR, file_name)
            print(f"  File_path = {file_path}.")

            # Receive file content
            with open(file_path, 'wb') as f:
                while True:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)

            print(f"File '{file_name}' received and saved.")
            client_socket.close()


# --- Entry Point ---
if __name__ == "__main__":
    server()