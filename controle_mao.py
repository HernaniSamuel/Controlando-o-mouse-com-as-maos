import cv2
import mediapipe as mp
import pyautogui
from time import sleep
import speech_recognition as sr
import pygame



pygame.init()

video = cv2.VideoCapture(0)
som = pygame.mixer.Sound('smw_stomp.wav')
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils


def ouvir_microfone():
    microfone = sr.Recognizer()

    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source)
        som.play()
        audio = microfone.listen(source)
    try:
        frase = microfone.recognize_google(audio,language='pt-BR')
    except sr.UnknownValueError:
        print('Não entendi')
        frase = ''
    return(frase)

while True:
    check, img = video.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    w, h,_ = img.shape
    pontos = []
    pyautogui.FAILSAFE = False
    if handsPoints:
        for points in handsPoints:

            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                cx, cy = int((cord.x*1920-1920)*-1), int(cord.y*1080)
                pontos.append((cx, cy))

            #Quadros da tela
            if pontos[9][0] < 960 and pontos[9][1] < 540:
                xhis = 960-pontos[9][0]
                ypsolon = 540 - pontos[9][1]
                pyautogui.moveTo(pontos[9][0] - xhis, pontos[9][1] - ypsolon)

            if pontos[9][0] > 960 and pontos[9][1] < 540:
                ypsolon = 540 - pontos[9][1]
                xhis = pontos[9][0] - 960
                pyautogui.moveTo(pontos[9][0] + xhis, pontos[9][1] - ypsolon)

            if pontos[9][0] < 960 and pontos[9][1] > 540:
                xhis = 960-pontos[9][0]
                ypsolon = pontos[9][1] - 540
                pyautogui.moveTo(pontos[9][0] - xhis, pontos[9][1] + ypsolon)

            if pontos[9][0] > 960 and pontos[9][1] > 540:
                ypsolon = pontos[9][1] - 540
                xhis = pontos[9][0] - 960
                pyautogui.moveTo(pontos[9][0] + xhis, pontos[9][1] + ypsolon)

            #comandos
            if pontos[8][1] >= pontos[7][1] and pontos[20][1] <= pontos[19][1]:
                pyautogui.click()
                sleep(0.2)

            if pontos[20][1] >= pontos[19][1]:
                pyautogui.mouseDown()
            if pontos[20][1] < pontos[19][1]:
                pyautogui.mouseUp()

            if pontos[12][1] >= pontos[11][1] and pontos[20][1] <= pontos[19][1]:
                pyautogui.rightClick()
                sleep(0.2)

            if pontos[16][1] >= pontos[15][1] and pontos[20][1] <= pontos[19][1]:
                sleep(0.3)
                pyautogui.write(ouvir_microfone())
                pyautogui.press('enter')

    cv2.imshow('imagem', img)
    cv2.waitKey(1)
