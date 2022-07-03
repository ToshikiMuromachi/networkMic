# client.py
import socket

host = 'localhost'
port = 8000
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # サーバーに接続を要求する
    s.connect((host, port))
    # データを送信する
    s.sendall(b'I sent a message.')
    # サーバーからのデータを受信
    data = s.recv(buffer_size)

    print(data.decode())