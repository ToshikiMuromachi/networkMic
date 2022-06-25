import socket
import yaml
# import time

M_SIZE = 1024

with open('../../config/server_address.yaml', 'r') as yml:
    udp_config = yaml.safe_load(yml)
locaddr = (udp_config['host'], udp_config['port'])

# ソケットを作成する
sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)

# 自ホストで使用するIPアドレスとポート番号を指定
sock.bind(locaddr)

while True:
    try:
        # Clientからのmessageの受付開始
        message, cli_addr = sock.recvfrom(M_SIZE)
        message = message.decode(encoding='utf-8')
        print(message)

        # Clientへ受信完了messageを送信
        print('Send response to Client')
        sock.sendto('Success to receive message'.encode(
            encoding='utf-8'), cli_addr)

    except KeyboardInterrupt:
        print('\n . . .\n')
        sock.close()
        break
