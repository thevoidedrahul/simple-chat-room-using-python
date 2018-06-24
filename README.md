A very simple Python chat server.
The code consists of 2 python scripts. First is the “server” and the other is the “client”.
The “server” does the following things: 
1. Accept multiple incoming connections for client.
2. Read incoming messages from each client and broadcast them to all other connected clients.

If the broadcast function fails to send message to any of the client, the client is assumed to be disconnected and the connection is closed and the socket is removed from the connection list. Or else if any of the client socket is readable, the server would read the message, and broadcast it back to all clients except the one who send the message.
The “client” does the following 2 things:
1. Listen for incoming messages from the server.
2. Check user input. If the user types in a message then send it to the server.

The client has to actually listen for server message and user input at the same time. To do this, I used the select function. The select function can monitor multiple sockets, when a message comes from the server on the connected socket, it is readable and when the user types a message and hits enter and the stdin stream is readable. The select function blocks till something happens. So after calling select, it will return only when either the server socket receives a message or the user enters a message. If nothing happens it keeps on waiting.
So the messages send by one client are seen on the consoles of other clients. 
At this point there is no client code, but the server is still usable without one. I am using MAC, all I have to do is run python path to server.py that will start the server. Then, once the server is running, I enter: telnet localhost 5000 in the command line that will connect you up to the server or if you are doing it from multiple computers, as long as you are on the same network you just have to replace localhost with the computer's IP address that you are running the server from. To start client to do run client.py that will connect client to server.


