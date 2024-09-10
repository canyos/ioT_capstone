import _thread
import socket

end = 0
print("안녕하세요")


def threaded(client_socket, addr):
    print('Connected by: ', addr[0], ':', addr[1])

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('Disconnected by ' + addr[0], ':', addr[1])
                break

            print('Received from ' + addr[0], ':', addr[1], data.decode())

            client_socket.send(data)
        except ConnectionResetError as e:
            print("Disconnected by", addr[0], ':', addr[1])
            print(f"e: {e}")
            end = 1

ip = '127.0.0.1'
port = 9998

# 소켓 초기화
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓 에러처리
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((ip, port))

server_socket.listen()

print('server start')

while True:
    print("wait")
    cs, addr = server_socket.accept()
    _thread.start_new_thread(threaded, (cs, addr))
    if end == 1:
        break
