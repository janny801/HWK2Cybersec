# HWK2Cybersec

## Overview
This project was developed for a cybersecurity class assignment. It demonstrates secure encrypted file transfer between a client and a server using Python. The objective is to ensure confidentiality by encrypting file data during transmission, preventing unauthorized access.

## Files
- **client2.py** - Encrypts and sends a file to the server.
- **server2.py** - Receives and decrypts the file from the client.
- **MyFile.txt** - A test file used to verify secure transmission.

## How It Works
1. The client encrypts `MyFile.txt` and sends it to the server.
2. The server decrypts the received file.
3. The transferred data should appear encrypted when analyzed with network tools like Wireshark.

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
