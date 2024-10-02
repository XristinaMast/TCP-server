EXPLANATION OF CODE

## Client ##

 
The code starts by adding appropriate libraries and connecting communication.
 
This function sends a message to the server, prints the sent message in hex (hexadecimal) format and receives the response. But because the client sends six different types of messages to the server each time, this function is called.
 
Our exercise asks for specific variables which we declare and send to the server each time. In this example we declare the variables and then msg_length1 calculates the total length of the packet and adds 4 bits to the original data.
At message_header1 it does the `construction` to package the message type, application message and message length in binary format. The formatting string ```!HHA`'' indicates:
 ! : Network byte order (big-endian)
 H: Unsigned short (2 bytes) for msg_type1
 H: Unsigned short (2 bytes) for msg_am1
 I: Unsigned int (4 bytes) for msg_length1
Then to complete the sending process on line 36 we see that you combine the binary header with the encoded string we just did to form the final message which you send.
Finally on line 37 it goes to the function where:
 Sends the message to the server
 Prints the message sent in hexadecimal format
 Receives a response from the server
 "Opens" the reply
 Prints the received response in hexadecimal format
 Returns the response code and response ID.

The same procedure is followed for subsequent messages.

 
After sending all messages, close the connection.

 
Here we print with the appropriate codes and the corresponding response.

## Server ##
 
The code - similarly - starts by adding appropriate libraries and connecting communication.
 
 
It extracts the packets received from the header and decodes them. Depending on the memory type, appropriate codes are returned.
 
The server inserts a loop to accept the incoming connections. For each connection, it enters another loop to continuously receive messages from the client, where it reads the header it has received. It unpacks the variable header and then reads and processes it and finds the result which is sent back to the client. If it is not received or something goes wrong, it closes the connection and prints the appropriate message. 
