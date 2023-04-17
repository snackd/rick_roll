# coding=utf-8
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

choice = "1-4"


def playVideo():
    # from moviepy.editor import VideoFileClip
    # from moviepy.editor import AudioFileClip

    # video = VideoFileClip(config.get('info', 'video'))
    # audio = AudioFileClip(config.get('info', 'audio'))
    # output = video.set_audio(audio)

    # video.preview()
    # audio.preview()
    # output.preview()

    import cv2
    import pygame

    cap = cv2.VideoCapture(config.get('info', 'video'))

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # 初始化 Pygame
    pygame.init()

    # 載入音訊檔案
    pygame.mixer.music.load(config.get('info', 'audio'))

    # 播放音訊
    pygame.mixer.music.play()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Cannot receive frame")
            break

        cv2.imshow('Video', frame)

        # ASCII 27 = ESC keyboard
        if cv2.waitKey(25) & 0xFF == 27:
            break

    pygame.mixer.music.stop()
    pygame.quit()

    cap.release()
    cv2.destroyAllWindows()

    return


def playPicture():
    import cv2
    img = cv2.imread(config.get('info', 'picture'))
    cv2.imshow('picture', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return


def playGIF():
    from PIL import Image, ImageSequence
    import cv2
    import numpy as np

    gif = Image.open(config.get('info', 'gif'))

    img_list = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert('RGBA')
        opencv_img = np.array(frame, dtype=np.uint8)
        opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_RGBA2BGRA)
        img_list.append(opencv_img)

    loop = True
    while loop:
        for i in img_list:
            cv2.imshow('gif', i)

            if cv2.waitKey(25) & 0xFF == 27:
                loop = False
                break

    cv2.destroyAllWindows()

    return


def playAudio():
    import pyaudio
    import wave

    # 載入音訊檔案
    wf = wave.open('Rick Rolled.wav', 'rb')

    # 初始化 PyAudio
    p = pyaudio.PyAudio()

    # 設定音訊參數
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 播放音訊
    data = wf.readframes(1024)
    while data != '':
        stream.write(data)
        data = wf.readframes(1024)

    # 關閉 PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

    return


def check_input(val) -> int:
    check_pass = False

    while not val.isnumeric() or len(val) != 1 or not check_pass:

        # positive numbers
        if val.isnumeric():
            if int(val) == 0 or int(val) > 4:
                val = input("Input" + choice + ":")
            else:
                check_pass = True
        else:
            val = input("Input" + choice + ":")

    return int(val)


if __name__ == '__main__':

    val = input("Choice 1-4:")
    val = check_input(val)

    if val == 1:
        playVideo()
    elif val == 2:
        playGIF()
    elif val == 3:
        playAudio()
    else:
        playPicture()
