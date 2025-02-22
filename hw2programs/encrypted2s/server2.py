import socket
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# --- Helper Functions ---
def generate_rsa_key_pair():
    """Generate an RSA key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    """Serialize a public key to send over a socket."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_public_key(public_key_bytes):
    """Deserialize a public key received from the socket."""
    return serialization.load_pem_public_key(public_key_bytes)

def rsa_encrypt(public_key, plaintext):
    """Encrypt plaintext with an RSA public key."""
    return public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def rsa_decrypt(private_key, ciphertext):
    """Decrypt ciphertext with an RSA private key."""
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def aes_encrypt(key, plaintext):
    """Encrypt plaintext with AES using the provided key."""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv + ciphertext

def aes_decrypt(key, ciphertext):
    """Decrypt ciphertext with AES using the provided key."""
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(actual_ciphertext) + decryptor.finalize()

# --- Server Code ---
def server():
    HOST = '0.0.0.0'
    PORT = 6000
    UPLOAD_DIR = './uploads'
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate RSA key pair and call them server_private_key and
    # server_public_key
    ## BEGIN
    #
    server_private_key, server_public_key = generate_rsa_key_pair()  # Generate RSA key pair

    ## END

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT} ...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}.")

            try:
                # Send server public key to the client
                ## BEGIN
                # Serialize the public key and save it in server_public_key_bytes
                # and send it to the client
                #
                server_public_key_bytes = serialize_public_key(server_public_key)  # Serialize public key
                client_socket.sendall(server_public_key_bytes)  # Send public key to client
                #
                ## END

                # Receive encrypted symmetric key
                ## BEGIN
                # Receive up to 4096 bytes of encrypted key from client
                # and recover the symmetric_key with decryption
                encrypted_symmetric_key_size = int.from_bytes(client_socket.recv(4), 'big')  # Get key size
                encrypted_symmetric_key = client_socket.recv(encrypted_symmetric_key_size)  # Receive encrypted key
                symmetric_key = rsa_decrypt(server_private_key, encrypted_symmetric_key)  # Decrypt key
                ## END

                # Receive file metadata: first, the length of the filename (4 bytes)
                file_name_length_bytes = client_socket.recv(4)
                file_name_length = int.from_bytes(file_name_length_bytes, 'big')
                ## BEGIN
                # Receive the file name (using the length) and decode it into UTF-8
                #
                file_name_bytes = client_socket.recv(file_name_length)  # Receive filename bytes
                file_name = file_name_bytes.decode('utf-8')  # Decode filename

                ## END

                # Receive encrypted file content length (8 bytes)
                encrypted_length_bytes = client_socket.recv(8)
                encrypted_length = int.from_bytes(encrypted_length_bytes, 'big')

                # Receive the encrypted file content in chunks
                # Initialize an empty bytearray to receive the file content
                encrypted_file_content = bytearray()
                ## BEGIN
                # Use a loop to receive the encrypted content in 4096 chunk
                # Combine the chunk(s) together into encrypted_file_content.
                # Note that the size of the content may not be a multiple of 4096.
                #
                #
                #
                #
                #
                #
                received_bytes = 0
                chunk_size = 4096
                while received_bytes < encrypted_length:
                    chunk = client_socket.recv(min(chunk_size, encrypted_length - received_bytes))
                    if not chunk:
                        break
                    encrypted_file_content.extend(chunk)
                    received_bytes += len(chunk)
                ## END

                # Decrypts the encrypted_file_content using the symmetric_key and
                # assigns the resulting decrypted content to the decrypted_content variable.
                ## BEGIN
                #
                decrypted_content = aes_decrypt(symmetric_key, encrypted_file_content)

                ## END

                # Write the decrypted file
                file_path = os.path.join(UPLOAD_DIR, file_name)
                with open(file_path, 'wb') as f:
                    f.write(decrypted_content)
                    print(decrypted_content, end='\n')
                print(f"\nFile '{file_name}' received and saved.")

            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                client_socket.close()

# --- Entry Point ---
if __name__ == "__main__":
    server()
