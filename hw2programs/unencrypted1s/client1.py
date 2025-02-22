import socket
import os

# --- Client Code ---
def client():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 6000
    file_path = input("Enter the path to the file: ").strip()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        # Send file metadata
        file_name = os.path.basename(file_path)
        client_socket.sendall(file_name.encode())

        # Send file content
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                client_socket.sendall(chunk)

        print(f"File '{file_name}' uploaded successfully.")


# --- Entry Point ---
if __name__ == "__main__":
    client()
