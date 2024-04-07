import socket
import os
import sys

CLIENT_IP =  '127.0.0.1'
CLIENT_PORT = 9001

tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_socket.connect((CLIENT_IP,CLIENT_PORT))

file_path = "./uploadFile/file.mp4"
file_size = os.path.getsize(file_path)

#ファイルタイプの確認
file_extension = os.path.splitext(file_path)[1]
if file_extension != ".mp4":
    sys.exit(1)

#ファイルサイズの送信
tcp_socket.sendall(str(file_size).encode().zfill(32))

#ファイルを1400バイトづつ送信
with open(file_path,"rb") as file:
    while True:
        fileData = file.read(1400)
        if not fileData:
            break
        tcp_socket.sendall(fileData)

#サーバーからのレスポンスを受信
responseFromServer = tcp_socket.recv(16)
print("Recieved:",responseFromServer.decode())
tcp_socket.close()

