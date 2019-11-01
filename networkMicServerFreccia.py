# coding: utf-8
import pyaudio
import socket
import threading

import numpy as np
import sys

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


class MixedSoundStreamServer(threading.Thread):
    def __init__(self, server_host, server_port):
        threading.Thread.__init__(self)
        self.SERVER_HOST = server_host
        self.SERVER_PORT = int(server_port)

    def run(self):
        audio = pyaudio.PyAudio()

        # サーバーソケット生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.bind((self.SERVER_HOST, self.SERVER_PORT))
            server_sock.listen(1)

            print("接続待機中")
            # クライアントと接続
            client_sock, _ = server_sock.accept()
            with client_sock:
                # クライアントからオーディオプロパティを受信
                settings_list = client_sock.recv(256).decode('utf-8').split(",")
                FORMAT = int(settings_list[0])
                CHANNELS = int(settings_list[1])
                RATE = int(settings_list[2])
                CHUNK = int(settings_list[3])

                # オーディオ出力ストリーム生成
                # stream = audio.open(format=FORMAT,channels=CHANNELS,rate=RATE,output=True,frames_per_buffer=CHUNK)

                # メインループ
                while True:
                    # クライアントから音データを受信
                    print("=====FORMAT:" + str(FORMAT) + "=====") # 8
                    print("=====CHANNELS:" + str(CHANNELS) + "=====") # 2　スレテオ
                    print("=====RATE:" + str(RATE) + "=====") # 44100=44.1kHz
                    print("=====CHUNK:" + str(CHUNK) + "=====") #1024 ファイル全体サイズからRIFFとWAVEのバイト数を引いた数
                    data = client_sock.recv(CHUNK)

                    ret = data
                    ret = np.frombuffer(ret, dtype="int16") / 32768
                    print(ret)
                    self.curve.setData(ret)

                    # 切断処理
                    if not data:
                        break

                    # オーディオ出力ストリームにデータ書き込み
                    # stream.write(data)
                    print(data)

        # 終了処理
        # stream.stop_stream()
        # stream.close()

        audio.terminate()


if __name__ == '__main__':
    mss_server = MixedSoundStreamServer("localhost", 5966)
    mss_server.start()
    mss_server.join()
