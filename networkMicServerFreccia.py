# coding: utf-8
import pyaudio
import socket
import threading

import numpy as np
import subprocess
import sys

import time


import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


class SoundStreamServer(threading.Thread):
    def __init__(self, server_host, server_port):
        threading.Thread.__init__(self)
        self.SERVER_HOST = server_host
        self.SERVER_PORT = int(server_port)

    def run(self):
        audio = pyaudio.PyAudio()

        # juliusを外部プロセスとして起動
        juliusThread = threading.Thread(target=self.julius)

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
                stream = audio.open(format=FORMAT,channels=CHANNELS,rate=RATE,output=True,frames_per_buffer=CHUNK)

                # メインループ
                while True:
                    # クライアントから音データを受信
                    print("=====FORMAT:" + str(FORMAT) + "=====")  # 8
                    print("=====CHANNELS:" + str(CHANNELS) + "=====")  # 1　モノラルに変更(julius対応)
                    print("=====RATE:" + str(RATE) + "=====")  # 44100=44.1kHz
                    print("=====CHUNK:" + str(CHUNK) + "=====")  # 1024 ファイル全体サイズからRIFFとWAVEのバイト数を引いた数
                    data = client_sock.recv(CHUNK)

                    ret = data
                    ret = np.frombuffer(ret, dtype="int16") / 32768  # 32768=2^16で割ってるのは正規化
                    print(ret)

                    # 切断処理
                    if not data:
                        break

                    # オーディオ出力ストリームにデータ書き込み
                    stream.write(data)
                    # print(data)

                    # output_string = result(data).decode()
                    # print(output_string)



        # 終了処理
        # stream.stop_stream()
        # stream.close()

        audio.terminate()

    def julius(self):
        """
            julius起動用
        """
        path = [
            './julius/run-linux.sh'
        ]
        path = ''.join(path)
        juliusProcess = subprocess.run(path, stdout=subprocess.PIPE, shell=True)

class Julius:
    def __init__(self):
        self.host = '127.0.0.1'  # localhost
        self.port = 10500  # julisuT[o[[hÌ|[g
        juliusThread = threading.Thread(target=self.main)
        juliusThread.start()

    def main(self):
        # p = subprocess.Popen(["./run-win-dnn-module.bat"], stdout=subprocess.PIPE, shell=True) # juliusN®XNvgðÀs
        # pid = str(p.stdout.read().decode('utf-8')) # juliusÌvZXIDðæ¾
        # juliusProcess = subprocess.run("run-win-dnn-module.bat", shell=True)

        time.sleep(3)  # 3bÔX[v
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))  # T[o[[hÅN®µ½juliusÉÚ±S

if __name__ == '__main__':
    # plotwin = PlotWindow()
    # winth = threading.Thread(target=PlotWindow())
    # winth.start()
    # juliusUtterance = Julius()

    mss_server = SoundStreamServer("localhost", 5966)
    mss_server.start()
    mss_server.join()

    #if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #    QtGui.QApplication.instance().exec_()