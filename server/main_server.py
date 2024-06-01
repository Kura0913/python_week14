from SockerServer.SocketServer import SocketServer


host = "127.0.0.1"
port = 20001

def main():
    server = SocketServer(host, port)
    server.daemon = True
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    print(f'Server start...')
    print('====================')
    while True:
        command = input()
        if command == "finish":
            break
    
    server.server_socket.close()
    print("leaving ....... ")

if __name__ == '__main__':
    main()