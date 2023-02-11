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


largura, altura = pyautogui.size()
metade_largura = int(largura/2)
metade_altura = int(altura/2)


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
    return (frase)


while True:
    check, img = video.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    w, h, _ = img.shape
    pontos = []
    pyautogui.FAILSAFE = False
    if handsPoints:
        for points in handsPoints:
            mpDraw.draw_landmarks(img, points, hand.HAND_CONNECTIONS)
            for id, cord in enumerate(points.landmark):
                cx, cy = int((cord.x*largura-largura)*-1), int(cord.y*altura)
                pontos.append((cx, cy))

            # Quadros da tela (Divide a tela em quatro quadros para amplificar o movimento do cursor)
            # superior esquerdo
            if pontos[9][0] < metade_largura and pontos[9][1] < metade_altura:
                horizontal = metade_largura - pontos[9][0]
                vertical = metade_altura - pontos[9][1]
                pyautogui.moveTo(pontos[9][0] - horizontal, pontos[9][1] - vertical)

            # superior direito
            if pontos[9][0] > metade_largura and pontos[9][1] < metade_altura:
                vertical = metade_altura - pontos[9][1]
                horizontal = pontos[9][0] - metade_largura
                pyautogui.moveTo(pontos[9][0] + horizontal, pontos[9][1] - vertical)

            # inferior esquerdo
            if pontos[9][0] < metade_largura and pontos[9][1] > metade_altura:
                horizontal = metade_largura - pontos[9][0]
                vertical = pontos[9][1] - metade_altura
                pyautogui.moveTo(pontos[9][0] - horizontal, pontos[9][1] + vertical)

            # inferior direito
            if pontos[9][0] > metade_largura and pontos[9][1] > metade_altura:
                vertical = pontos[9][1] - metade_altura
                horizontal = pontos[9][0] - metade_largura
                pyautogui.moveTo(pontos[9][0] + horizontal, pontos[9][1] + vertical)

            # comandos

            # Clique
            if pontos[8][1] >= pontos[7][1] and pontos[20][1] <= pontos[19][1]:
                pyautogui.click()
                sleep(0.2)

            # Segurar e arrastar
            if pontos[20][1] >= pontos[19][1]:
                pyautogui.mouseDown()

            # Soltar
            if pontos[20][1] < pontos[19][1]:
                pyautogui.mouseUp()

            # Clique com o botão direito
            if pontos[12][1] >= pontos[11][1] and pontos[20][1] <= pontos[19][1]:
                pyautogui.rightClick()
                sleep(0.2)

            # Pesquisa por voz
            if pontos[16][1] >= pontos[15][1] and pontos[20][1] <= pontos[19][1]:
                sleep(0.3)
                pyautogui.write(ouvir_microfone())
                pyautogui.press('enter')

    cv2.imshow('imagem', img)
    cv2.waitKey(1)
