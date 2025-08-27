import CapturaMaoModulo as cmm
import numpy as np
import cv2
import math
import subprocess

# Função para ajustar o volume do sistema via pactl
def set_volume(percent):
    percent = max(0, min(100, int(percent)))  # Limita entre 0 e 100
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{percent}%"])

# Resolução da câmera
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Detector de mãos
detector = cmm.handDetector(detectionCon=0.7)

while True:
    sucess, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)

    if len(lmList) != 0:
        # Pontos: polegar (id 4) e indicador (id 8)
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Desenho na tela
        cv2.circle(frame, (x1, y1), 8, (255, 0, 0), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 8, (255, 0, 0), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.circle(frame, (cx, cy), 8, (255, 0, 0), cv2.FILLED)

        # Calcula distância entre os dedos
        lengh = math.hypot(x2 - x1, y2 - y1)

        # Converte distância para volume (entre 30 e 200 pixels)
        volume_percent = np.interp(lengh, [30, 200], [0, 100])
        set_volume(volume_percent)

        # Feedback visual de dedo fechado
        if lengh < 50:
            cv2.circle(frame, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

        # Mostra volume na tela
        cv2.putText(frame, f'Volume: {int(volume_percent)}%', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Exibe janela
    cv2.imshow("Imagem", frame)
    if cv2.waitKey(20) & 0xFF == ord("d"):
        break

cap.release()
cv2.destroyAllWindows()
