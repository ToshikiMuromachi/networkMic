import socket

M_SIZE = 1024

# Serverのアドレスを用意。Serverのアドレスは確認しておく必要がある。
serv_address = ('localhost', 8890)

# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        # messageを送信する
        print('Input any messages, Type [end] to exit')
        message = input()
        if message != 'end':
            send_len = sock.sendto(message.encode('utf-8'), serv_address)
            # ※sendtoメソッドはkeyword arguments(address=serv_addressのような形式)を受け付けないので注意

            # Serverからのmessageを受付開始
            rx_meesage, addr = sock.recvfrom(M_SIZE)
            print(f"[Server]: {rx_meesage.decode(encoding='utf-8')}")

        else:
            sock.close()
            print('done')
            break

    except KeyboardInterrupt:
        sock.close()
        print('done')
        break
