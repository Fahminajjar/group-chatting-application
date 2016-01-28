#from threading import Thread
#import multiprocessing as mp
import socket
import select

# HOST = '192.168.1.18'
HOST = '127.0.0.1'
BUFFER = 4096
PORT = 9999
socket_list = []

def broadcast(server_socket, socket, msg):
    for sock in socket_list:
        if sock != server_socket and sock != socket:
            try:
                if type(msg) is not bytes:
                    msg = msg.encode('ascii')
                sock.send(msg)
            except:
                sock.close()
                if sock in socket_list:
                    socket_list.remove(sock)
                print("Client (%s, %s) disconnected!" % sock.getpeername())


def chat_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    socket_list.append(server_socket)
    print("Chat server started on port " + str(PORT))

    while True:
        ready_to_read, ready_to_write, error = select.select(socket_list, [], [] , 0)

        for sock in ready_to_read:
            if sock == server_socket:
                client, addr = server_socket.accept()
                socket_list.append(client)
                print("Client (%s, %s) connected!" % addr)
                broadcast(server_socket, client, "[%s:%s] entered our chatting room\n" % addr)

            else:
                try:
                    data = sock.recv(BUFFER)
                    if data:
                        data = data.decode('ascii')
                        broadcast(server_socket, sock, ("\r" + '[' + str(sock.getpeername()) + ']: ' + data))

                    else:
                        if sock in socket_list:
                            socket_list.remove(sock)
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % sock.getpeername())
                        print("Client (%s, %s) disconnected!" % sock.getpeername())
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr.getpeername())
                    print("Client (%s, %s) disconnected!" % sock.getpeername())
                    continue

    server_socket.close()


if __name__ == "__main__":
    chat_server()
