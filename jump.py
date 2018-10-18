import numpy as np
import cv2
import serial
import time
import winsound
frequency = 2500  
duration = 33
prim = None
cooldown=time.time()
try:
	cap = cv2.VideoCapture(2)
	ser = serial.Serial("COM6", 38400)
	b = b'n'
	print(cap.set(3,1280))
	print(cap.set(4,720))
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		s = frame[507:587, 1051:1235]
		s = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)
		#s = cv2.GaussianBlur(s, (9, 9), 0)
		ret, s = cv2.threshold(s, 200, 255, cv2.THRESH_BINARY)
		
		#s = cv2.fastNlMeansDenoising(s)
		
		#s = cv2.GaussianBlur(s, (9, 9), 0)
		if prim != None:
			
			diffo = ((np.sum(np.abs(np.subtract(s, prim))))/1000)
			print(diffo)
			if diffo > 4.7:# or time.time() - cooldown > (36/60):
				print("\a")
				time.sleep(23.2/60)
				b = b'b'
				cooldown = time.time()
			else:
				b = b'n'
		if b != b'n':
			ser.write(b)
		# Our operations on the frame come here
		#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		cooldown += 1
		# Display the resulting frame
		cv2.imshow('frame',frame)
		cv2.imshow('score',s)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		prim = s.copy()

# When everything done, release the capture
finally:		
	print("closing up shop")
	ser.close()
	cap.release()
	cv2.destroyAllWindows()
