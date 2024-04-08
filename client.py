import socket
import os
import sys
import json

CLIENT_IP =  '127.0.0.1'
CLIENT_PORT = 9001
JSON_SIZE = 16
MEDIA_TYPE_SIZE = 4
PAYLOAD_SIZE = 47
HEADER_SIZE = 64

tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_socket.connect((CLIENT_IP,CLIENT_PORT))

file_path = "./uploadFile/file.mp4"
file_size = os.path.getsize(file_path)
file_extension = os.path.splitext(file_path)[1]

#ファイルタイプの確認
if file_extension != ".mp4":
    sys.exit(1)

#ヘッダーの作成
json_data = json.dumps({"action": "process_video", "params": {"compression": "auto", "resolution": "1080p", "aspect_ratio": "16:9"}})
header = f"{len(json_data):<{JSON_SIZE}}{len(file_extension):<{MEDIA_TYPE_SIZE}}{file_size:<{PAYLOAD_SIZE}}"
header = f"{header:<{HEADER_SIZE}}"
print(len(json_data),len(file_extension))

try:
    #ヘッダー、JSONデータ、ファイルデータの送信
    tcp_socket.sendall(header.encode())
    tcp_socket.sendall(json_data.encode())
    tcp_socket.sendall(file_extension.encode())
    #ファイルを1400バイトづつ送信
    with open(file_path,"rb") as file:
        while True:
            fileData = file.read(1400)
            if not fileData:
                break
            tcp_socket.sendall(fileData)
except Exception as e:
    print("Error",e)

#サーバーからのレスポンスを受信
try:
    response_header = tcp_socket.recv(HEADER_SIZE)
    print("Recieved:",response_header.decode())
    response_json_size = int(response_header[:JSON_SIZE].decode().strip())
    response_media_type_size = int(response_header[JSON_SIZE:JSON_SIZE+MEDIA_TYPE_SIZE].decode())
    response_json_data = tcp_socket.recv(response_json_size).decode()
    response_media_type = tcp_socket.recv(response_media_type_size).decode()
    print("response_json_data:",response_json_data)
except Exception as e:
    print("Error",e)

tcp_socket.close()

