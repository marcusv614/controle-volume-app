import cv2 as cv #type:ignore
import mediapipe as mp #type:ignore

class handDetector():

	def __init__(self,mode=False,maxhands=1,
		complexModel=1,detectionCon=0.5,trackcon=0.5):
		# Método construtor

		self.mode = mode
		self.maxhands = maxhands
		self.complexModel = complexModel
		self.detectionCon = detectionCon
		self.trackcon = trackcon

		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(self.mode,self.maxhands,self.complexModel,
			self.detectionCon,self.trackcon)
		self.mpDraw = mp.solutions.drawing_utils

	def findHands(self,frame,draw=True):
		# Método para detectar as mãos

		imgRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
		self.results = self.hands.process(imgRGB)

		if self.results.multi_hand_landmarks:
			for handLms in self.results.multi_hand_landmarks:
				if draw:
					self.mpDraw.draw_landmarks(frame,handLms, self.mpHands.HAND_CONNECTIONS)
		return frame

	def findPosition(self,frame, handNo=0,draw=False,kp=0):
		# Esse método serve para armazenar as coordenadas da mão (handNo=0 é o parâmetro
		# referente a uma das mãos) em uma lista (lmList).

		lmList = []

		if self.results.multi_hand_landmarks:
			myHand = self.results.multi_hand_landmarks[handNo]

			for id, lm in enumerate(myHand.landmark):
				h,w,c = frame.shape
				cx, cy = int(lm.x * w), int(lm.y * h)
				# print(id,cx,cy)
				lmList.append([id,cx,cy])

				if draw:
					if id == kp:
						cv.circle(self.frame, (cx, cy), 5, (255, 0, 0), cv.FILLED)

		return lmList


def main():
	cap = cv.VideoCapture(0)
	detector = handDetector()

	while True:
		sucess, frame = cap.read()
		frame = detector.findHands(frame)
		lmList = detector.findPosition(frame)
		if len(lmList) != 0:
			print(lmList[4])
		# Nesse print, podemos escolher qual keyponint das mãos iremos printar.
		cv.imshow("Imagem",frame)
		if cv.waitKey(20) & 0xFF==ord("d"):
			break


	cap.release()
	cv.destroyAllWindows()

		# Nesse print, podemos escolher qual keyponint das mãos iremos printar.


if __name__ == "__main__":
    main()