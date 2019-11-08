# coding: utf-8
import numpy as np
import wave
import pyaudio
import socket
import threading


class MixedSoundStreamClient(threading.Thread):
    def __init__(self, server_host, server_port):
        threading.Thread.__init__(self)
        self.SERVER_HOST = server_host
        self.SERVER_PORT = int(server_port)

    def run(self):
        audio = pyaudio.PyAudio()

        # 音楽ファイル読み込み
        # wav_file = wave.open(self.WAV_FILENAME, 'rb')

        # オーディオプロパティ
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024

        # マイクの入力ストリーム生成
        mic_stream = audio.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)

        # サーバに接続
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.SERVER_HOST, self.SERVER_PORT))

            # サーバにオーディオプロパティを送信
            sock.send("{},{},{},{}".format(FORMAT, CHANNELS, RATE, CHUNK).encode('utf-8', errors='ignore'))

            # メインループ
            while True:
                # マイクからデータ読み込み
                mic_data = mic_stream.read(CHUNK)

                print(mic_data)

                # デコード
                decoded_data = np.frombuffer(mic_data, np.int16).copy()
                # データサイズの不足分を0埋め
                decoded_data.resize(CHANNELS * CHUNK, refcheck=False)
                # エンコード
                sock.send(decoded_data.astype(np.int16).tobytes())

        # 終了処理
        mic_stream.stop_stream()
        mic_stream.close()

        audio.terminate()


if __name__ == '__main__':
    # mss_client = MixedSoundStreamClient("localhost", 5966)
    mss_client = MixedSoundStreamClient("localhost", 12345)
    mss_client.start()
    mss_client.join()
