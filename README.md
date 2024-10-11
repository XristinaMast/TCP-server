# TCP Server

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Project Structure](#project-structure)
5. [Prerequisites](#prerequisites)
6. [How to Run the Server](#how-to-run-the-server)
7. [Client Interaction](#client-interaction)
8. [Usage Examples](#usage-examples)

## Introduction

The **TCP Server** project implements a simple and efficient TCP server in Python. This server is designed to handle multiple client connections concurrently using threading, enabling it to process client requests in real-time. The server can be extended or modified to meet various application needs, such as file transfer, messaging, or remote procedure calls.

## Features

- **Multi-threaded Support**: Handles multiple clients simultaneously.
- **Flexible Communication**: Supports sending and receiving custom messages between clients and the server.
- **Robust Error Handling**: Gracefully handles connection errors and client disconnections.
- **Configurable**: Easily adjustable settings for server parameters like host and port.

## Technologies Used

- **Python 3.x**: The programming language used to build the server.
- **Socket Library**: Utilized for network communication via TCP/IP.
- **Threading Module**: Enables handling multiple clients concurrently.

## Project Structure

```
TCP-server/
│
├── server.py             # Main server application file
├── README.md             # This README file
└── requirements.txt       # Required Python packages (if any)
```

## Prerequisites

Before running the server, ensure you have the following installed:

- **Python 3.6+**: The latest version of Python.
  
### Optional

- If your project has specific dependencies, you can install them using:

```bash
pip install -r requirements.txt
```

## How to Run the Server

1. **Clone the Repository**

   First, clone the repository to your local machine:

   ```bash
   git clone https://github.com/XristinaMast/TCP-server.git
   cd TCP-server
   ```

2. **Run the Server**

   Execute the following command to start the TCP server:

   ```bash
   python server.py
   ```

   The server will start listening for incoming client connections on the specified host and port (default is `localhost:8080`).

## Client Interaction

### Connecting to the Server

To interact with the server, you will need a TCP client. You can use any TCP client application (such as **telnet**, **netcat**, or even another Python script) to connect to the server.

### Example Client (Python)

Here’s a simple example of a TCP client in Python that can connect to the server:

```python
import socket

def tcp_client():
    host = 'localhost'  # Server address
    port = 8080         # Server port

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((host, port))
        
        # Send a message
        s.sendall(b'Hello, Server!')
        
        # Receive a response
        data = s.recv(1024)
        
        print('Received from server:', data.decode())

if __name__ == "__main__":
    tcp_client()
```

## Usage Examples

1. **Start the Server**: Run `python server.py` in the terminal. You should see a message indicating that the server is running and waiting for connections.

2. **Connect a Client**: Open another terminal or command prompt and run the client script provided above or use a tool like `telnet`:

   ```bash
   telnet localhost 8080
   ```

3. **Send a Message**: Type a message into the client and hit enter. The server will receive and process the message.

4. **View Server Output**: Check the terminal where the server is running to see incoming messages and client connections.
