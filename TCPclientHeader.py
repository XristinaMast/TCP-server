from struct import *
import socket 
import binascii
import ctypes

serverIP = '127.0.0.1'
serverPort = 54541

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))

# Function to create and send a message, then receive and process the response
def send_and_receive_message(message):
    clientSocket.sendall(message)
    print(f'Sent message: {binascii.hexlify(message)}')
    response = clientSocket.recv(8)
    msg_type, response_code, response_id = unpack('!HHI', response)
    print(f'Received response: {binascii.hexlify(response)}')
    return response_code, response_id

#     0                   1                   2                   3
#     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2
#     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#     |        Message Type           |              AM               |
#     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#     |                            Length                             |
#     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Message 1: Simple message with type, AM, and some data
msg_type1 = 1  # Example message type
msg_am1 = 12345  # Example AM
msg_data1 = "Hello, this is a test message."
msg_length1 = 8 + len(msg_data1)  # 4 bytes for initial data + length of the message data

message_header1 = pack('!HHI', msg_type1, msg_am1, msg_length1)
message1 = message_header1 + msg_data1.encode('utf-8')
send_and_receive_message(message1)


#     0                   1                   2                   3
#     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2
#     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#     |        Message Type           |      Information Type         |
#     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#     |                            Length                             |
#     +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+.

# Message 2: Simple message with type, information type, and some data
msg_type2 = 2  # Example message type
info_type = 2  # Example information type
msg_data2 = "Test information message."
msg_length2 = 8 + len(msg_data2)  # Length of the data part

message_header2 = pack('!HHI', msg_type2, info_type, msg_length2)
message2 = message_header2 + msg_data2.encode('utf-8')
send_and_receive_message(message2)

# 0                   1                   2                   33
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |        Message Type           |              AM               |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                            Length                             |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |        First Name Length      |          First Name           |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                         ..........                            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |             First Name                        |   Padding1    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |         Last Name Length      |           Last Name           |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                         ..........                            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |              Last Name                        |   Padding2    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |       Father's Name Length    |         Father's Name         |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                         ..........                            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |              Last Name                        |   Padding3    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Message 3: Complex message with multiple fields including names
msg_type3 = 3  # Example message type
msg_am3 = 12345  # Example AM
first_name = "John"
last_name = "Doe"
fathers_name = "Michael"

first_name_length = len(first_name)
first_name_padding = (4 - (first_name_length % 4)) % 4
last_name_length = len(last_name)
last_name_padding = (4 - (last_name_length % 4)) % 4
fathers_name_length = len(fathers_name)
fathers_name_padding = (4 - (fathers_name_length % 4)) % 4

msg_length3 = (8 + 
              2 + first_name_length + first_name_padding + 
              2 + last_name_length + last_name_padding + 
              2 + fathers_name_length + fathers_name_padding)

message_header3 = pack('!HHI', msg_type3, msg_am3, msg_length3)
first_name_packed = pack('!H', first_name_length) + first_name.encode('utf-8') + b'\x00' * first_name_padding
last_name_packed = pack('!H', last_name_length) + last_name.encode('utf-8') + b'\x00' * last_name_padding
fathers_name_packed = pack('!H', fathers_name_length) + fathers_name.encode('utf-8') + b'\x00' * fathers_name_padding

message3 = message_header3 + first_name_packed + last_name_packed + fathers_name_packed
send_and_receive_message(message3)


# 0                   1                   2                   3
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |        Message Type           |              AM               |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                            Length                             |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                          Phone Number                         |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                          Phone Number                         |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |        Phone Number           |      Padding (2 bytes)        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Message 4: Phone number message
msg_type4 = 4  # Example message type
msg_am4 = 12345  # Example AM
phone_number = "123456789012"  # Example phone number (12 digits)

msg_length4 = 8 + 12  # Header length + phone number length

message_header4 = pack('!HHI', msg_type4, msg_am4, msg_length4)
phone_number_packed = pack('!12s', phone_number.encode('utf-8'))
message4 = message_header4 + phone_number_packed
send_and_receive_message(message4)

# 0                   1                   2                   3
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |        Message Type           |              AM               |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                            Length                             |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |             TK                |          Country Code         |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |        Street Length          |             Street            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                         ..........                            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                  Street                       |   Padding2    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |           City Length         |              City             |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                         ..........                            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                   City                        |   Padding3    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Message 5: Postal address message
msg_type5 = 5  # Example message type
msg_am5 = 12345  # Example AM
tk = 678  # Example TK
country_code = 44  # Example Country Code
street = "Main Street"
city = "New York"

street_length = len(street)
street_padding = (4 - (street_length % 4)) % 4
city_length = len(city)
city_padding = (4 - (city_length % 4)) % 4

msg_length5 = (8 + 
              2 + 2 + 
              2 + street_length + street_padding + 
              2 + city_length + city_padding)

message_header5 = pack('!HHI', msg_type5, msg_am5, msg_length5)
tk_country_code_packed = pack('!HH', tk, country_code)
street_packed = pack('!H', street_length) + street.encode('utf-8') + b'\x00' * street_padding
city_packed = pack('!H', city_length) + city.encode('utf-8') + b'\x00' * city_padding

message5 = message_header5 + tk_country_code_packed + street_packed + city_packed
send_and_receive_message(message5)

# 0                   1                   2                   3
# 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |        Message Type           |      Notification Type        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                            Length                             |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Message 6: Notification message
msg_type6 = 6  # Example message type
notification_type = 2  # Example notification type
msg_length6 = 8  # Length of the header (8 bytes)

message6 = pack('!HHI', msg_type6, notification_type, msg_length6)
send_and_receive_message(message6)


# Close the socket
clientSocket.close()

msg_response_code = -1  # Example value, replace with the actual value
if(msg_response_code==0):
    print("All went well, the connection is to be terminated. This notification is sent by the Server if everything is ok.")   
elif(msg_response_code==1):
    print("AM is not consistent.")
elif(msg_response_code==2):
    print("Unknown Information Type.")
elif(msg_response_code==3):
    print("Phone Number incorrect.")
elif(msg_response_code==4):
    print("Full Name not present.")
elif(msg_response_code==5):
    print("Last Name not present.")
elif(msg_response_code==6):
    print("Father's Name not present.")
elif(msg_response_code==7):
    print("Both Full and Last Name not present.")
elif(msg_response_code==8):
    print("Both Full and Father's Name not present.")
elif(msg_response_code==9):
    print("Both Last and Father's Name not present.")
elif(msg_response_code==10):
    print("All names not present.")
elif(msg_response_code==11):
    print("Postal Code missing.")
elif(msg_response_code==12):
    print("Postal Address missing.")
elif(msg_response_code==13):
    print("Postal Country missing.")
elif(msg_response_code==14):
    print("Postal Code and Address missing.")
elif(msg_response_code == 15):
    print("Postal Code and Country missing.")
elif(msg_response_code == 16):
    print("All fields from Postal data is missing.")
else:
    print("Unexpected error.")    
