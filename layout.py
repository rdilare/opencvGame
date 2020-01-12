
import pygame


class Button:
	def __init__(self,pos,size,text,text_size,action = None):
		self.pos = pos
		self.size = size
		# font = pygame.font.SysFont("comicsansms",20)
		font = pygame.font.SysFont("poppins",text_size)
		self.text = font.render(text, True, (0,0,0))
		self.color = (50,200,50)
		self.action = action

		self.textrect =self.text.get_rect()
		self.textrect.center = (self.pos[0]+self.size[0]//2, self.pos[1]+self.size[1]//2)


	def draw(self,surf):
		pygame.draw.rect(surf, self.color, pygame.Rect(self.pos, self.size))
		surf.blit(self.text,self.textrect)

	def checkEvents(self):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		x,y = self.pos
		w,h = self.size

		if x < mouse[0] < x+w and y < mouse[1] < y+h:
			self.color = (180,230,50)
			
			if click[0]==1 and self.action != None:
				self.action()
		else:
			self.color = (50,200,50)


class Menu:

	def __init__(self,pos,buttonSize,text_size,labels,action=None):
		self.labels = labels
		self.action = action
		self.pos = pos
		self.buttonSize = buttonSize

		if not self.action:
			self.action  = [None for i in range(len(self.labels))]

		x,y = self.pos
		w,h = self.buttonSize
		self.items = [Button((x,y+(i*(h+1))),(w,h),text, text_size, self.action[i]) for i,text in enumerate(self.labels)]
		
	def draw(self,surf):
		for b in self.items:
			b.draw(surf)

	def checkEvents(self):
		for b in self.items:
			b.checkEvents()


def printText(surf,pos,text,text_size):
    font = pygame.font.SysFont("comicsansms", text_size)
    text = font.render(str(text), True, (10,10,10))
    surf.blit(text,pos)








# def button(bg,msg,x,y,w,h,ic,ac,action=None):
# 	global current_window
# 	screen = pygame.display.get_surface()
# 	mouse = pygame.mouse.get_pos()
# 	click = pygame.mouse.get_pressed()

# 	menuScreen  = bg
	

# 	if x+w > mouse[0] > x and y+h > mouse[1] > y:
# 		pygame.draw.rect(menuScreen, ac,(x,y,w,h))
# 		if click[0] == 1 and action != None:
# 			current_window = action         
# 	else:
# 		pygame.draw.rect(menuScreen, ic,(x,y,w,h))

# 	smallText = pygame.font.SysFont("comicsansms",20)
# 	textSurf, textRect = text_objects(msg, smallText)
# 	textRect.center = ( (x+(w/2)), (y+(h/2)) )
# 	menuScreen.blit(textSurf, textRect)

# 	screen.blit(menuScreen,(0,0))