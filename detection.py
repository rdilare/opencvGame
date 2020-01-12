#! /usr/bin/env python3

import cv2
import numpy as np
import threading, sys


def get_mask(img,color,inRange=[5,50,50]):

	"""
	return the binary mask based on the given color \
	as HSV values.
	"""
	frame = img.copy()
	hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	l_color=np.array([i-j for i,j in zip(color,inRange)])
	u_color=np.array([i+j for i,j in zip(color,inRange)])
	mask=cv2.inRange(hsv, l_color, u_color)
	blur_mask=cv2.blur(mask, (5,5))
	ret,thresh_mask = cv2.threshold(blur_mask,200,255,cv2.THRESH_BINARY)


	return thresh_mask

def get_center(mask_img):
	"""
	return center(x,y) of detected object in \
	binary mask_img.
	"""
	contours, hierarchy = cv2.findContours(mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	if len(contours)!=0:
		cnt = contours[0]

		(x,y),radius=cv2.minEnclosingCircle(cnt)
	else :
		x,y = 0,0

	return int(x),int(y)



def circle(img,x,y,r,color):
	return cv2.circle(img,(x,y),r,color)



class OpenCV:
	def __init__(self):
		self.camera = cv2.VideoCapture(0)

		self.pos = (0,0)
		self.isrunning = True

		self.t = threading.Thread(target = self.start)
		self.t.start()
		# self.t.join()

	def start(self):
		i = 0
		while self.isrunning:

			# bg = (np.array(range(400*600))*0).reshape(400,600)
			# bg = np.ones((400,600,3),dtype = np.uint8)
			rt,bg = self.camera.read()
			bg = cv2.flip(bg,1)
			bg_mask = get_mask(bg, color=[63,150,150],inRange=[10,100,100])
			x,y = get_center(bg_mask)


			if x!=0 and y!=0:
				self.pos = (x,y)

			c = circle(bg,x,y,50,(0,5*i,255))

			# print(bg[1][1])
			if i<100:
				i+=1
			else:
				i=0


			# cv2.imshow('result',c)
			# key=cv2.waitKey(int(1000/200))
			# if key==ord('x') or key == 27: # 27 for Escape key
			# 	break

	def get_pos(self):
		return self.pos
		

	def stop(self):
		# pass
		print("------------closed----------")
		self.isrunning=False
		# self.t.join()
		sys.exit()





# i = 0

# while 1:

# 	bg = (np.array(range(400*600))*0).reshape(400,600)
# 	bg = np.ones((400,600,3),dtype = np.uint8)
# 	rt,bg = camera.read()

# 	bg_mask = get_mask(bg, color=[63,150,150],inRange=[10,100,100])
# 	x,y = get_center(bg_mask)

# 	c = circle(bg,x,y,50,(0,5*i,255))

# 	# print(bg[1][1])
# 	if i<100:
# 		i+=1
# 	else:
# 		i=0


# 	cv2.imshow('result',c)
# 	key=cv2.waitKey(int(1000/200))
# 	if key==ord('x') or key == 27: # 27 for Escape key
# 		break


# cv2.destroyAllWindows()