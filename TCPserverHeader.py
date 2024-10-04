import socket
from struct import *
import binascii

serverIP = '127.0.0.1'
serverPort = 12345

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)

print('Server is ready to receive')

def handle_message(connection, message):
    try:
        # Unpack the message header
        msg_type, am, length = unpack('!HHI', message[:8])
        data = message[8:]
        
        # Process the message based on its type
        if msg_type == 1:
            # Process message type 1
            if am != 12345:
                return 1, 0  # AM is not consistent
            return 0, 0  # Success

        elif msg_type == 2:
            # Process message type 2
            info_type = am  # Info type is packed in 'am' field for this message
            if info_type not in (1, 2):  # Example check for valid info types
                return 2, 0  # Unknown Information Type
            return 0, 0  # Success

        elif msg_type == 3:
            # Process message type 3
            if am != 12345:
                return 1, 0  # AM is not consistent
            # Unpack and process names
            first_name_length = unpack('!H', data[:2])[0]
            first_name = data[2:2 + first_name_length].decode('utf-8')
            if not first_name:
                return 7, 0  # Both Full and Last Name not present.
            return 0, 0  # Success

        elif msg_type == 4:
            # Process message type 4
            if am != 12345:
                return 1, 0  # AM is not consistent
            phone_number = data[:12].decode('utf-8')
            if not phone_number.isdigit():
                return 3, 0  # Phone Number incorrect
            return 0, 0  # Success

        elif msg_type == 5:
            # Process message type 5
            if am != 12345:
                return 1, 0  # AM is not consistent
            tk, country_code = unpack('!HH', data[:4])
            street_length = unpack('!H', data[4:6])[0]
            street = data[6:6 + street_length].decode('utf-8')
            # Extracting other fields similarly...
            if not street:
                return 12, 0  # Postal Address missing
            return 0, 0  # Success

        elif msg_type == 6:
            # Process message type 6
            notification_type = am  # Notification type is packed in 'am' field
            return 0, 0  # Success

        else:
            return 99, 0  # Unexpected message type

    except Exception as e:
        print(f"Error processing message: {e}")
        return 99, 0  # Unexpected error

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f'Connection established with {addr}')
    while True:
        try:
            # Read the header first
            message_header = connectionSocket.recv(8)
            if not message_header:
                break

            msg_type, am, length = unpack('!HHI', message_header)
            # Read the rest of the message based on the length
            message_data = connectionSocket.recv(length - 8)

            message = message_header + message_data

            response_code, response_id = handle_message(connectionSocket, message)

            # Send the response back to the client
            response_message = pack('!HHI', msg_type, response_code, response_id)
            connectionSocket.sendall(response_message)
        except Exception as e:
            print(f"Connection error: {e}")
            break

    # Close the socket
    connectionSocket.close()
