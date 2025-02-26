# HWK2Cybersec

## Overview
This project was developed for a cybersecurity class assignment. I was given boilerplate code and tasked with filling in the functions between the `## BEGIN` and `## END` comments to understand how encryption works in secure file transfer. The project demonstrates secure encrypted file transfer between a client and a server using Python. The objective is to ensure confidentiality by encrypting file data during transmission, preventing unauthorized access.


## Installation
Before running the project, install the required dependencies:
```bash
pip install cryptography
```


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


## Viewing Encrypted Data in Wireshark

To analyze the encrypted file transfer using Wireshark, follow these steps:

### **1. Start Capturing Packets**
- Open **Wireshark**.
- Select the network interface your system is using (e.g., `Loopback` if testing locally).
- Click **Start Capture**.

### **2. Apply a Filter to View the Client-Server Communication**
Since the client (`client2.py`) and server (`server2.py`) communicate over **TCP port 6000**, apply the following filter in Wireshark:

```bash
tcp.port == 6000
```


This filter will display only the packets exchanged between the client and server.

### **3. Identify Encrypted Data**
- Look for **TCP stream data** where the file is being transferred.
- Since the file is **AES-encrypted**, the content will appear as **randomized binary data** rather than readable text.
- You can compare the encrypted file transfer data with a plain-text transfer to observe the difference.

### **4. Inspect Key Exchange**
- The **RSA-encrypted AES key** will be transferred first.
- Since RSA encryption is asymmetric, the **server's public key** is used for encryption.
- You can locate the RSA key exchange by filtering for **large outgoing packets** from the client before the actual file transfer.

### **5. Verify Encryption Effectiveness**
- Open one of the captured packets and inspect its **payload**.
- The file content should appear as **random bytes** due to AES encryption.
- If you see readable text, encryption may not be applied correctly.

### **6. Stop and Save the Capture**
- Once the file transfer is complete, stop the capture.
- Save the packet capture (`.pcapng`) file for further analysis if needed.

By following these steps, you can confirm that the **hybrid encryption (RSA for key exchange + AES for file encryption)** is working correctly.



## Requirements
- Python 3.x
- Required cryptographic libraries (if any)



## Usage
1. Navigate to the correct directory:
   ```bash
   cd encrypted2s
   ```
2.  Start the server:  
   `python server2.py`
3.  Run the client:  
   `python client2.py`  
   - When prompted, enter `MyFile.txt` as the file name.
4. Verify that the received file is correctly decrypted.



## Example Output


### **1. Running the Server (`server2.py`)**
Start the server, which listens for incoming client connections:
```bash
python server2.py
```

### **2. Output (`server2.py`)**
Server listening on 0.0.0.0:6000 ...

### **3. Running the Client (`client2.py`)**
Run the client to send an encrypted file:
```bash
python client2.py
```

### **4. Output (`client2.py`)**
Enter the file name : MyFile.txt
Sent file metadata: MyFile.txt (size: 10 bytes)
File 'MyFile.txt' sent to the server successfully.

### **5. Server Receives and Processes the File (`server2.py`)**
Connection established with ('127.0.0.1', 61584).
b'PART 2: ENCRYPTED FILE TRANSFER\nThis is a test file for Assignment 2.\nIt is used for secure encrypted file transfer.\nWireshark should capture this as encrypted data.\n'
File 'MyFile.txt' received and saved.
