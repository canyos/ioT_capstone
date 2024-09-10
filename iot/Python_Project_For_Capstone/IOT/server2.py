#서버
import _thread
import socket
import os

import sys
import user_main
from os.path import exists

end = 0
global timeList

def threaded(client_socket, addr):
    print('Connected by: ', addr[0], ':', addr[1])

    with open('/home/pc/Desktop/flag_fire.txt', 'r') as f:
        try:
            str_flag = f.read(10)
        except Exception as ex:
            print(ex)

    client_socket.send(str_flag.encode('utf-8'))

    filename = client_socket.recv(1024) #클라이언트한테 파일이름(이진 바이트 스트림 형태)을 전달 받는다
    print('받은 데이터 : ', filename.decode('utf-8')) #파일 이름을 일반 문자열로 변환한다
    data_transferred = 0
    filePath = '/home/pc/Desktop/' + filename.decode('utf-8')
    if not exists(filePath):
        print("no file")
        sys.exit()
    print("파일 %s 전송 시작" %filename)
    
    with open(filePath, 'rb') as f:
        try:
            data = f.read(1024) #1024바이트 읽는다
            while data: #데이터가 없을 때까지
                data_transferred += client_socket.send(data) #1024바이트 보내고 크기 저장
                data = f.read(1024) #1024바이트 읽음
        except Exception as ex:
            print(ex)
            
    print("전송완료 %s, 전송량 %d" %(filename, data_transferred))
    client_socket.close()

def server_start():
    ip = '192.168.46.180'
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