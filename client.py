# client chat!

import socket
import select
import sys

BUFFER = 4096

def client_chat():
    if len(sys.argv) < 3:
        print("Use: python3 client_chat.py hostname port")
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.settimeout(2)

    #connecting to server
    try:
        s.connect((host, port))
    except:
        print("Unable to connect!")
        sys.exit()

    print("Connected to server, You can start sending messages!")
    sys.stdout.write("[Me] ")
    sys.stdout.flush()

    while True:
        socket_list = [sys.stdin, s]

        ready_to_read, ready_to_write, error = select.select(socket_list, [], [])
        for sock in ready_to_read:
            if sock == s:
                data = sock.recv(BUFFER)
                if data:
                    data = data.decode('ascii')
                    sys.stdout.write(data)
                    sys.stdout.write("[Me] ")
                    sys.stdout.flush()
                else:
                    print("\nDisconnected from server chat!")
                    sys.exit()
            else:
                msg = sys.stdin.readline()
                msg = msg.encode('ascii')
                s.send(msg)
                sys.stdout.write("[Me] ")
                sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(client_chat())

