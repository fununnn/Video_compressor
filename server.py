import socket
import os
import json

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9001
HEADER_SIZE = 64
JSON_SIZE = 16
MEDIA_TYPE_SIZE = 4
PAYLOAD_SIZE = 47


tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind((SERVER_IP, SERVER_PORT))
tcp_server_socket.listen(5)

print(f'TCP Server listening on {SERVER_IP}:{SERVER_PORT}')

def process_media(json_obj,media_type):
    return json.dumps({"status": "success", "message": "Media processed successfully"})


while True:
    client_socket , addr = tcp_server_socket.accept()
    print(f'Got connection from {addr}')
    try:
        #ヘッダーの受信
        header = client_socket.recv(HEADER_SIZE)
        json_size = int(header[:JSON_SIZE].decode().strip())
        media_type_size = int(header[JSON_SIZE:JSON_SIZE + MEDIA_TYPE_SIZE].decode().strip())
        payload_size = int(header[JSON_SIZE + MEDIA_TYPE_SIZE:HEADER_SIZE].decode().strip())
        #JSONデータの受信
        json_data = client_socket.recv(json_size).decode()
        json_obj = json.loads(json_data)
        #メディアデータを受信
        media_type = client_socket.recv(media_type_size).decode()
        payload = client_socket.recv(payload_size)

        #メディアデータの保存
        with open(f"./receivedFile/received_file.{media_type}","wb") as file:
            file.write(payload)
        #メディアデータの処理
        response_json = process_media(json_obj,media_type)

        #レスポンスをクライアントに送信
        response_header = f"{len(response_json):<{JSON_SIZE}}{len(media_type):<{MEDIA_TYPE_SIZE}}{0:<{PAYLOAD_SIZE}}"
        client_socket.sendall(response_header.encode())
        client_socket.sendall(response_json.encode())
        client_socket.sendall(media_type.encode())
    except Exception as e:
        print("Error",e)
    finally:
        client_socket.close()