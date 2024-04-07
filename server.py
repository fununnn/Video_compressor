import socket
# TCPサーバーの設定
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9001

# TCPソケットの作成
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind((SERVER_IP, SERVER_PORT))
tcp_server_socket.listen(5)

print(f'TCP Server listening on {SERVER_IP}:{SERVER_PORT}')

while True:
    client_socket , addr = tcp_server_socket.accept()
    print(f'Got connection from {addr}')

    #ファイルサイズを受信
    file_size = int(client_socket.recv(32).decode().strip())
    print(f'Recieving file of size {file_size} bytes')

    #ファイルデータの受信
    mp4_dataFromClient = b''
    while len(mp4_dataFromClient) < file_size:
        fileData = client_socket.recv(1400)
        if not fileData:
            break
        mp4_dataFromClient += fileData
    
    #ファイルデータを処理
    with open("./receivedFile/received_file.mp4","wb") as file:
        print("ファイルデータを処理します")
        file.write(mp4_dataFromClient)

    #クライアントにレスポンスを送信
    responseForClient = "FIlE_RECEIVED"
    client_socket.sendall(responseForClient.encode().ljust(16))
    print("クライアントにレスポンスを送信します")

    client_socket.close()
