import socket, select

class Server(object):
    CONNECTION_LIST = []
    RECV_BUFFER = 4096  
    PORT = 5000

    def __init__(self):
        self.user_name_dict = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_up_connections()
        self.client_connect()

    def set_up_connections(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", self.PORT))
        self.server_socket.listen(10)
        self.CONNECTION_LIST.append(self.server_socket)

    def broadcast_data(self, sock, message):
        for socket in self.CONNECTION_LIST:
            if socket != self.server_socket and socket != sock:
                try:
                    socket.send(message)
                except:
                    socket.close()
                    self.CONNECTION_LIST.remove(socket)

    def send_data_to(self, sock, message):
        try:
            sock.send(message)
        except:
            socket.close()
            self.CONNECTION_LIST.remove(sock)

    def client_connect(self):
        print "Chat server started on port " + str(self.PORT)
        while 1:
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST, [], [])

            for sock in read_sockets:
                if sock == self.server_socket:
                    self.setup_connection()
                else:
                    try:
                        data = sock.recv(self.RECV_BUFFER)
                        if data:
                            if self.user_name_dict[sock].username is None:
                                self.set_client_user_name(data, sock)
                            else:
                                self.broadcast_data(sock, "\r" + '<' + self.user_name_dict[sock].username + '> ' + data)
                    except:
                        self.broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                        print "Client (%s, %s) is offline" % addr
                        sock.close()
                        self.CONNECTION_LIST.remove(sock)
                        continue

        self.server_socket.close()

    def set_client_user_name(self, data, sock):
        self.user_name_dict[sock].username = data.strip()
        self.send_data_to(sock, data.strip() + ', you entered the chat room\n')
        self.send_data_to_all_regesterd_clents(sock, data.strip() + ', has joined the chat room\n')

    def setup_connection(self):
        sockfd, addr = self.server_socket.accept()
        self.CONNECTION_LIST.append(sockfd)
        print "Client (%s, %s) connected" % addr
        self.send_data_to(sockfd, "please enter a username: ")
        self.user_name_dict.update({sockfd: Connection(addr)})

    def send_data_to_all_regesterd_clents(self, sock, message):
        for local_soc, connection in self.user_name_dict.iteritems():
            if local_soc != sock and connection.username is not None:
                self.send_data_to(local_soc, message)


class Connection(object):
    def __init__(self, address):
        self.address = address
        self.username = None


if __name__ == "__main__":
    server = Server()
