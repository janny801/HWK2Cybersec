# HWK2Cybersec

## Overview
This project was developed for a cybersecurity class assignment. I was given boilerplate code and tasked with filling in the functions between the `## BEGIN` and `## END` comments to understand how encryption works in secure file transfer. The project demonstrates secure encrypted file transfer between a client and a server using Python. The objective is to ensure confidentiality by encrypting file data during transmission, preventing unauthorized access.


## Files
- **client2.py** - Encrypts and sends a file to the server.
- **server2.py** - Receives and decrypts the file from the client.
- **MyFile.txt** - A test file used to verify secure transmission.


## How It Works
1. The client encrypts `MyFile.txt` and sends it to the server using a **hybrid encryption approach** combining **RSA and AES**.
2. **RSA Encryption (Asymmetric)**
   - The client receives the **server's RSA public key**.
   - A **random 256-bit AES symmetric key** is generated.
   - The AES key is **encrypted using RSA** with the server's public key.
   - The **encrypted AES key** is sent to the server.
3. **AES Encryption (Symmetric)**
   - The client reads the file content.
   - The file is **encrypted using AES in CFB mode** with the generated AES key.
   - The **encrypted file content** is sent to the server in chunks.
4. The server decrypts the received AES key using its **RSA private key**.
5. The server then decrypts the received file using the **AES key**.
6. The transferred data should appear encrypted when analyzed with network tools like Wireshark.



## Requirements
- Python 3.x
- Required cryptographic libraries (if any)

## Usage
1. Start the server:  
   `python server2.py`
2. Run the client:  
   `python client2.py`  
   - When prompted, enter `MyFile.txt` as the file name.
3. Verify that the received file is correctly decrypted.
