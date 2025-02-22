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
    # The purpose of serialize_public_key() is to covert the
    # public key from its internal representation, such as
    # an object or a data structure, into a string or byte array.
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_public_key(public_key_bytes):
    """Deserialize a public key received from the socket."""
    # It takes a serialized public key (like a string or byte
    # array) and converts it back into its original data
    # structure or object representation.
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

# --- Client Code ---
def client():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 6000
    file_path = input("Enter the file name : ").strip()
    # file_path should really be called file_name, but it has been used

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        # Receive server public key (up to 4096 bytes) and deserialize it
        ## BEGIN
        # Use 'server_public_key_bytes' to receive the key from the socket
        server_public_key_bytes = client_socket.recv(4096)  # Receive public key
        # deserialize the key and store it in 'server_public_key'
        server_public_key = deserialize_public_key(server_public_key_bytes)  # Deserialize key
        ## END

        # Generate and send encrypted symmetric key
        symmetric_key = os.urandom(32)  # AES-256 key
        ## BEGIN
        # Encrypt the RSA symmetric_key with the public key from the server
        # save the encrypted key in encrypted_symmetric_key and send it to
        # the server through the socket
        encrypted_symmetric_key = rsa_encrypt(server_public_key, symmetric_key)  # Encrypt AES key
        client_socket.sendall(len(encrypted_symmetric_key).to_bytes(4, 'big'))  # Send key size
        client_socket.sendall(encrypted_symmetric_key)  # Send encrypted AES key

        #
        #
        ## END

        # Send file metadata: filename length and filename
        file_name = os.path.basename(file_path)
        file_name_bytes = file_name.encode()
        file_name_length = len(file_name_bytes)
        client_socket.sendall(file_name_length.to_bytes(4, 'big'))
        client_socket.sendall(file_name_bytes)
        ## BEGIN
        # Print messages indicating what has been sent to the server
        #
        print(f"Sent file metadata: {file_name} (size: {file_name_length} bytes)")
        #
        ## END

        # Read and encrypt file content
        with open(file_path, 'rb') as f:
            file_content = f.read()
        ## BEGIN
        # Encrypt the file_content using AES and save
        # the result in 'encrypted_content'.
        #
        encrypted_content = aes_encrypt(symmetric_key, file_content)  # Encrypt file content

        ## END

        # Send the length of the encrypted file content (8 bytes)
        encrypted_length = len(encrypted_content)
        client_socket.sendall(encrypted_length.to_bytes(8, 'big'))

        # Send the encrypted file content in chunks
        chunk_size = 4096
        ## BEGIN
        # Send the encrypted file content in chunk_size to the server
        # through the socket
        sent_bytes = 0
        while sent_bytes < encrypted_length:
            chunk = encrypted_content[sent_bytes:sent_bytes + chunk_size]
            client_socket.sendall(chunk)
            sent_bytes += len(chunk)
        #
        #
        ## END
        print(f"File '{file_name}' sent to the server successfully.")


# --- Entry Point ---
if __name__ == "__main__":
    client()