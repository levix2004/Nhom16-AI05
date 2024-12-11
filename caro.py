import math
import sys, os
import random
import pygame
from pygame.locals import *

DEFAULT = 325
x = 425
y = 375
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = 	(245,252,131)
PINK = (255,128,255)
GREEN_LEAF = (128,255,0)
GRAY = (182,182,182)
GRAY_FADING = (223,223,223)
GREEN_FADING = (131,254,192)
BLUE = (112,146,190)
RED = (226,55,22)	
PRUNE = (196,0,0)
MY_COLOUR=[GREEN_FADING,RED,GRAY_FADING,PRUNE,BLUE,PINK,YELLOW,GREEN_LEAF]
WIDTH = 1200
HEIGHT = 800
MIN_WIDTH = 198
MIN_HEIGHT = 99
board = ((WIDTH-MIN_WIDTH + 2)/50) * ((HEIGHT-MIN_HEIGHT)/50) 
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load("HoaTrongCamQuan.mp3") 
#os.environ['SDL_VIDEO_CENTERED'] = '1' # Center the screen 
sound = pygame.mixer.Sound('click.wav')
menu_image =pygame.image.load(os.path.join("Images","background.png"))
ingame_image = pygame.image.load(os.path.join("Images/IngameBG","1.png"))
board_image = pygame.image.load(os.path.join("Images/IngameBG","board1.png"))
redo_undo_image = pygame.image.load(os.path.join("Images","R-U.png"))
replay_image = pygame.image.load(os.path.join("Images","RE.png"))
rule1_image = pygame.image.load(os.path.join("Images/Rule","Rule1_2.png"))
rule2_image = pygame.image.load(os.path.join("Images/Rule","Rule2_2.png"))
pygame.init()
FPS = 240
# <-- DISPLAY --> #
DISPLAY= pygame.display.set_mode((WIDTH+200,HEIGHT+100),pygame.RESIZABLE)
pygame.display.set_caption("Caro Game")
Music_mode = 3
choose = 0 
player_text = pygame.font.Font(None,50)	
# <-- O images --> #
o_images = [pygame.image.load(os.path.join("Images/Balls",str(i)+".png")) for i in range (1,16) ]

# <-- X images --> #
x_images = [pygame.image.load(os.path.join("Images/X",str(i) + ".png")) for i in range(1,9) ]

# <-- Avatar --> #
Avatar = [pygame.image.load(os.path.join("Images/Avatar",str(i)+"`.png")) for i in range(1,9)]

# <-- Menu --> #
def menu(music = 0):	
	DISPLAY.blit(menu_image,(0,0))
	if music == 1:
		pygame.draw.line(DISPLAY, RED, [1340,37], [1300,90],10)


# <-- Refreshing display purpose --> #
def display():
	DISPLAY.blit(board_image,(MIN_WIDTH,MIN_HEIGHT))
	DISPLAY.blit(redo_undo_image,(1093,31))	

def invisible_player(count,color):
	if count%2 ==0:
		pygame.draw.circle(DISPLAY,color, [x,y], 19)  
	else:
		DISPLAY.blit(x_images[6],(x-17,y-17))	
		# pygame.draw.line(DISPLAY, color, [x-5,y-5], [x+5, y+5],5)
		# pygame.draw.line(DISPLAY, color, [x-5,y+5], [x+5, y-5],5)

def check_win(player,player2):
	for i in range(len(player)):  
		collums= []
		rows = []
		
		for j in range(len(player)):			
			# <-- Rows --> #
			if (player[i][1] == player[j][1]):
				rows.append(player[j][0])
				wining_holding_y[0] = player[i][1]
			# <-- Collums --> #			
			if (player[i][0] == player[j][0]):
				collums.append(player[j][1])
				wining_holding_x[0] = player [j][0]
		# <-- Primary diagonal --> #
		if [player[i][0]+50,player[i][1]+50] in player:
			if [player[i][0]+100,player[i][1]+100] in player:
				if [player[i][0]+150,player[i][1]+150] in player:
					if [player[i][0]+200,player[i][1]+200] in player:
						if rule %2 !=0:
							if [player[i][0]+250, player[i][1]+250] in player2 and [player[i][0]-50,player[i][1]-50] in player2:
								return False
						wining_diag.append([player[i][0]+50,player[i][1]+50])
						wining_diag.append([player[i][0]+100,player[i][1]+100])
						wining_diag.append([player[i][0]+150,player[i][1]+150])
						wining_diag.append([player[i][0]+200,player[i][1]+200])
						wining_diag.append([player[i][0],player[i][1]])

						return True	

		# <-- Secondary diagonal --> #
		if [player[i][0]-50,player[i][1]+50] in player:
			if [player[i][0]-100,player[i][1]+100] in player:
				if [player[i][0]-150,player[i][1]+150] in player:
					if [player[i][0]-200,player[i][1]+200] in player:								
						wining_diag.append([player[i][0]-50,player[i][1]+50])
						wining_diag.append([player[i][0]-100,player[i][1]+100])
						wining_diag.append([player[i][0]-150,player[i][1]+150])
						wining_diag.append([player[i][0]-200,player[i][1]+200])
						wining_diag.append([player[i][0],player[i][1]])
						if rule %2 !=0: # Chặn 2 đầu
							if [player[i][0]+50,player[i][1]-50] in player2 and [player[i][0]-250, player[i][1]+250] in player2:
								return False 		
						return True

		collums.sort(reverse = False)  
		rows.sort(reverse = False)
		for z in range(0,len(rows)-4):
			if rows[z] == rows[z+1] - 50 == rows[z+2] - 100 == rows[z+3] - 150 == rows[z+4] - 200:

				if [rows[z] -50 , wining_holding_y[0]] in player2 and [rows[z]+250, wining_holding_y[0]] in player2 and (rule %2 != 0):
					return False
				wining_x.append([rows[z],rows[z+1],rows[z+2],rows[z+3],rows[z+4]])
				return True
		for z in range(0,len(collums)-4):
			if collums[z] == collums[z+1] - 50 == collums[z+2] - 100 == collums[z+3] - 150 == collums[z+4] - 200:
				if [wining_holding_x[0], collums[z] - 50] in player2 and [wining_holding_x[0], collums[0]+ 250] in player2 and (rule %2 != 0):
					return False
				wining_y.append([collums[z],collums[z+1],collums[z+2],collums[z+3],collums[z+4]])
				return True
		wining_diag.clear()
	return False
# <-- Bot --> #

# <-- Attention --> #
Attack = [0,8,72,648,5832,52488,472392]
Defense =  [0,3,27,99,729,6561,59049]
# <-- Attack --> #
def AttRows(x_, y_):
	Point = 0
	Enemy = 0
	Bot = 0 
	for dem in range(1, 7):
		if x_ + dem*50 > WIDTH:
			break
		if [x_ + dem*50, y_] in player1:
			Enemy +=1
			break
		elif [x_ + dem*50, y_] in bot1:
			Bot +=1
		#Blank Space
		else:
			break
	for dem in range(1, 6):
		if x_ - dem*50 < MIN_WIDTH+2:
			break
		if [x_ - dem*50, y_] in player1:
			Enemy +=1
			break
		elif [x_ - dem*50, y_] in bot1:
			Bot +=1
		#Blank Space
		else:
			break
	if Enemy == 2:
		if rule %2 !=0:
			return 0
		if Bot <= 3:
			return 1;
	Point -= Defense[Enemy] * 3
	Point += Attack[Bot]
	return Point
def AttCollums(x_, y_):
	Point = 0
	Enemy = 0
	Bot = 0 
	for dem in range(1,7):
		if y_ +dem*50 > HEIGHT:
			break
		if [x_ , y_ + dem*50] in player1:
			Enemy += 1
			break
		elif [x_ , y_ + dem*50] in bot1:
			Bot += 1
		#Blank Space
		else:
			break
	for dem in range(1, 7):
		if y_ - dem*50 < MIN_HEIGHT+1:
			break
		if [x_, y_ - dem*50] in player1:
			Enemy +=1
			break
		elif [x_ , y_ - dem*50] in bot1:
			Bot +=1
		#Blank Space
		else:
			break
	if Enemy == 2:
		if rule %2 !=0:
			return 0
		if Bot <= 3:
			return 1;
	Point -= Defense[Enemy] * 3
	Point += Attack[Bot]
	return Point
def AttSecDiag(x_, y_):
	Point = 0
	Enemy = 0
	Bot = 0 
	for dem in range(1,7):
		if x_ + dem*50 > WIDTH or y_ - dem*50 < MIN_HEIGHT+1:
			break
		if [x_ + dem*50, y_ - dem*50] in player1:
			Enemy += 1
			break
		elif [x_ + dem*50, y_ - dem*50] in bot1:
			Bot +=1
		#Blank Space
		else:
			break

	for dem in range(1, 7):
		if x_ - dem*50 < 125 or  y_ + dem*50 > HEIGHT:
			break
		if [x_ - dem*50, y_ + dem*50] in player1:
			Enemy +=1
			break
		elif [x_ - dem*50 , y_ + dem*50] in bot1:
			Bot +=1
		#Blank Space
		else:
			break
	if Enemy == 2:
		if rule %2 !=0:
			return 0
		if Bot <= 3:
			return 1;
	Point -= Defense[Enemy] * 3
	Point += Attack[Bot]
	return Point
def AttPrDiag(x_, y_):
	Point = 0
	Enemy = 0
	Bot = 0 
	for dem in range(1,7):
		if x_ + dem*50 > WIDTH or y_ + dem*50 > HEIGHT:
			break
		if [x_ + dem*50, y_ + dem*50] in player1:
			Enemy += 1
			break
		elif [x_ + dem*50, y_ + dem*50] in bot1:
			Bot +=1
		#Blank Space
		else:
			break

	for dem in range(1, 7):
		if x_ - dem*50 < MIN_HEIGHT+1 or  y_ - dem*50 < MIN_WIDTH+2:
			break
		if [x_ - dem*50, y_ - dem*50] in player1:
			Enemy +=1
			break
		elif [x_ - dem*50 , y_ - dem*50] in bot1:
			Bot +=1
		#Blank Space
		else:
			break
	if Enemy == 2:
		if rule %2 !=0:
			return 0
		if Bot <= 3:
			return 1
	Point -= Defense[Enemy+1] * 3
	Point += Attack[Bot]
	return Point
# <-- Defense --> #
def DefRows(x_, y_):
	Point = 0
	Enemy = 0
	Bot = 0 
	for dem in range(1, 7):
		if x_ + dem*50 >= WIDTH:
			break
		if [x_ + dem*50, y_] in player1:
			Enemy +=1		
			
		elif [x_ + dem*50, y_] in bot1:
			Bot +=1
			break
		#Blank Space
		else:
			break
	for dem in range(1, 7):
		if x_ - dem*50 < MIN_WIDTH+2:
			break
		if [x_ - dem*50, y_] in player1:
			Enemy +=1
			
		elif [x_ - dem*50, y_] in bot1:
			Bot +=1
			break
		#Blank Space
		else:
			break
	if Bot == 2:
		return 1
	Point += Defense[Enemy]
	#print(Point)
	return Point
def DefCollums(x_, y_):
	Point = 0
	Enemy = 0
	Bot = 0 
	for dem in range(1,7):
		if y_+ dem*50 >= HEIGHT:
			break
		if [x_ , y_ + dem*50] in player1:
			Enemy += 1
			
		elif [x_ , y_ + dem*50] in bot1:
			Bot +=1
			break
		#Blank Space
		else:
			break
	for dem in range(1, 7):
		if y_ - dem*50 < MIN_HEIGHT+1:
			break
		if [x_, y_ - dem*50] in player1:
			Enemy +=1
			
		elif [x_ , y_ - dem*50] in bot1:
			Bot +=1
			break
		#Blank Space
		else:
			break
	if Bot == 2:
		return 1	 
	Point += Defense[Enemy]
	return Point
def DefSecDiag(x_, y_):
	Point = 0
	Enemy = 0
	Bot = 0 
	for dem in range(1,7):
		if x_ + dem*50 > WIDTH or y_ - dem*50 < MIN_HEIGHT+1:
		 	break
		if [x_ + dem*50, y_ - dem*50] in player1:
			Enemy += 1
			
		elif [x_ + dem*50, y_ - dem*50] in bot1:
			Bot +=1
			break
		#Blank Space
		else:
			break

	for dem in range(1, 7):
		if x_ - dem*50 < MIN_WIDTH+2 or  y_ + dem*50 >= HEIGHT:
			break
		if [x_ - dem*50, y_ + dem*50] in player1:
			Enemy +=1
			
		elif [x_ - dem*50 , y_ + dem*50] in bot1:
			Bot +=1
			break
		#Blank Space
		else:
			break
	if Bot == 2:
		return 1
	Point += Defense[Enemy]
	return Point
def DefPrDiag(x_, y_):
	Point = 0
	Enemy = 0
	Bot = 0 
	for dem in range(1,7):
		if x_ + dem*50 > WIDTH or y_ + dem*50 >= HEIGHT:
			break
		if [x_ + dem*50, y_ + dem*50] in player1:
			Enemy += 1			
		elif [x_ + dem*50, y_ + dem*50] in bot1:
			Bot +=1
			break
		#Blank Space
		else:
			break

	for dem in range(1, 7):
		if x_ - dem*50 < 125 or  y_ - dem*50 < 125:
			break
		if [x_ - dem*50, y_ - dem*50] in player1:
			Enemy +=1

		elif [x_ - dem*50 , y_ - dem*50] in bot1:
			Bot +=1
			break
		#Blank Space
		else:
			break
	if Bot == 2:
		return 1
	Point += Defense[Enemy]
	return Point
# <-- Counting points for bot --> #
def bot_ways():
	Point_max = 0
	count = 0
	result = [375,225]
	for i in range(MIN_WIDTH + 27, WIDTH, 50):
		for j in range(MIN_HEIGHT+26, HEIGHT, 50):
			if [i, j] not in player1 and [i, j] not in bot1:
				Attack_Point = AttCollums(i, j) + AttRows(i, j) + AttPrDiag(i, j) + AttSecDiag(i, j)
				Defense_Point = DefCollums(i, j) + DefRows(i, j) + DefPrDiag(i, j) + DefSecDiag(i , j)
				Temp_Point = max(Attack_Point,Defense_Point)				
				if Point_max < Temp_Point:			
					Point_max = Temp_Point
					result[0] = i
					result[1] = j
			else:
				continue

	return result
def bot():
	pos = []
	pos = bot_ways()
	bot1.append( [pos[0],pos[1]])
	replay_list.append([pos[0],pos[1]])
font = pygame.font.Font(None, 40)

# <-- Players --> #
score_1 = 0
score_2 = 0
score_bot = 0
player1= []
player2 = []
bot1 =[]
wining_x= []
wining_y= []
wining_holding_x = [0]
wining_holding_y = [0]
wining_diag = []
win = 0
count = 0
count_save = 0 
redo_save  = 0
redo_list1 = []
redo_list2 = []
replay_list = []
rule = 0
def Rule(rule):
	if rule % 2 == 0: 
		DISPLAY.blit(rule2_image,(816,20))
	else:
		DISPLAY.blit(rule1_image,(816,20))
	
def undo(count):
	undo_image = pygame.image.load(os.path.join("Images","UNDO.png"))
	DISPLAY.blit(undo_image,(1093,31))	
	pygame.display.update()							
	pygame.time.delay(50)
	global redo_save
	if count > redo_save:
		redo_save = count 
	count -= 1
	if choose == 1:
		if count%2 == 0:
			if len(player1)> 0:
				redo_list1.append(player1[len(player1)-1])
				player1.pop()
			else:
				return count + 1
		else:
			if len(player2) > 0:
				redo_list2.append(player2[len(player2)-1])
				player2.pop()
			else:
				return count + 1
		return count
	else:
		if len(player1 ) > 0:
			redo_list1.append(player1[len(player1)-1])
			redo_list2.append(bot1[len(bot1)-1])
			player1.pop()
			bot1.pop()
			return count - 1
		return count + 1

def replay():
	DISPLAY.blit(pygame.image.load(os.path.join("Images","RE1.png")),(100,100))
	pygame.display.update()
	display()
	time = 500
	skip = font.render("SKIP",20,PRUNE)
	DISPLAY.blit(skip,(100,75))
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()
			pygame.quit()
	# <-- Player vs Player --> #
	if choose == 1:
		if count_save % 2 == 0:
			for i in range(0,len(replay_list)):
				# <-- SKIP REPLAY --> #
				for event in pygame.event.get():
					if pygame.Rect((100,75),(50, 50)).collidepoint(pygame.mouse.get_pos()):
						if event.type == pygame.MOUSEBUTTONDOWN:
							sound.play()
							time = 1
				if (i %2 == 0):
					pygame.time.wait(time)
					DISPLAY.blit(o_images[o_random],(replay_list[i][0]-21,replay_list[i][1]-21))	 	
					pygame.display.update()
				else:
					pygame.time.wait(time)
					DISPLAY.blit(x_images[x_random],(replay_list[i][0]-17,replay_list[i][1]-17))	
				pygame.display.update()
		else:
			for i in range(0,len(replay_list)):
				# <-- SKIP REPLAY --> #
				for event in pygame.event.get():
					if pygame.Rect((50,25),(50, 50)).collidepoint(pygame.mouse.get_pos()):
						if event.type == pygame.MOUSEBUTTONDOWN:
							sound.play()
							time= 0
				if (i % 2 ==  0):
					pygame.time.delay(time)
					DISPLAY.blit(x_images[x_random],(replay_list[i][0]-17,replay_list[i][1]-17))
					pygame.display.update()
				else:
					pygame.time.delay(time)
					DISPLAY.blit(o_images[o_random],(replay_list[i][0]-21,replay_list[i][1]-21))		 		
				pygame.display.update()
	# <-- Player vs Bot --> #
	else:
		for i in range(0,len(replay_list)):
				# <-- SKIP REPLAY --> #
				for event in pygame.event.get():
					if pygame.Rect((100,75),(50, 50)).collidepoint(pygame.mouse.get_pos()):
						if event.type == pygame.MOUSEBUTTONDOWN:
							sound.play()
							time = 0
				if (i %2 == 0):
					pygame.time.wait(time)
					DISPLAY.blit(o_images[o_random],(replay_list[i][0]-21,replay_list[i][1]-21))			 	
					pygame.display.update()
				else:
					pygame.time.wait(time)
					DISPLAY.blit(x_images[x_random],(replay_list[i][0]-17,replay_list[i][1]-17))			
				pygame.display.update()
	pygame.display.flip()
def save_game():
	# <-- PVP mode --> #
	if choose == 1:
		print("GAME SAVED!")
		if (os.path.isfile('./SAVE.txt')):
			os.remove("SAVE.txt")
		file = open("SAVE.txt","a+")
		for i in range(0,len(player1)):
			file.write( str(player1[i][0]) + " " + str( player1[i][1])+ " ")
		file.write("\n")
		for i in range(0,len(player2)):
			file.write( str(player2[i][0]) + " " + str( player2[i][1])+ " ")
		file.close()
		DISPLAY.fill(WHITE)
		text = font.render("GAME SAVED! GAME WILL BE CLOSED!",20,BLACK)
		DISPLAY.blit(text, (WIDTH/3,300))
		pygame.display.update()
		pygame.time.delay(1000)
		pygame.quit()
		sys.exit()
	# <-- PVB mode --> #
	else:
		print("GAME SAVED!")
		if (os.path.isfile('./SAVE_BOT.txt')): # Check if file exists
			os.remove("SAVE_BOT.txt")
		file = open("SAVE_BOT.txt","a+")
		for i in range(0,len(player1)):
			file.write( str(player1[i][0]) + " " + str( player1[i][1])+ " ")
		file.write("\n")
		for i in range(0,len(bot1)):
			file.write( str(bot1[i][0]) + " " + str( bot1[i][1])+ " ")
		file.close()
		DISPLAY.fill(WHITE)
		text = font.render("GAME SAVED! GAME WILL BE CLOSED!",20,BLACK)
		DISPLAY.blit(text, (WIDTH/3,300))
		pygame.display.update()
		pygame.time.delay(1000)
		pygame.quit()
		sys.exit()

def load_game():
	global player1,player2, bot1
	if choose == 1:
		if (os.path.isfile('./SAVE.txt')):
			f = open("SAVE.txt","r+")		
			print("SUCCEED")				
			display()
			p1 = f.readline().split()
			p2 = f.readline().split()
			player1 = [[int(p1[i]) , int(p1[i+1])] for i in range(0,len(p1)-1,2)]
			f.close()
			if (len(p1)>len(p2)):
				count = 1
		else:
			text = font.render("NO GAME SAVED FOUND!",5,PINK)
			print("Failed")
			DISPLAY.blit(text, (300,HEIGHT+20))				
			pygame.display.update()
			pygame.time.wait(100)
	if choose == 2:
		if (os.path.isfile('./SAVE_BOT.txt')) == True: # Check if file exists
			f = open("SAVE_BOT.txt","r+")	
			display()			
			p1 = f.readline().split()
			p2 = f.readline().split()
			player1 = [[int(p1[i]) , int(p1[i+1])] for i in range(0,len(p1)-1,2)]
			bot1 = [[int(p2[i]) , int(p2[i+1])] for i in range(0,len(p2)-1,2)]
			f.close()
		else:
			text = font.render("NO GAME SAVED FOUND!",5,PINK)
			DISPLAY.blit(text, (300,HEIGHT+20))				
			pygame.display.update()
			pygame.time.wait(100)
# <-- Text --> #
win_text1 = font.render('CLICK ANYWHEHRE TO CONINUE', 0, BLACK)
win_text2 = font.render('PRESS \'X\' TO EXIT ', 0, BLACK)
# <-- Game play --> #
while True:
		#pygame.draw.rect(DISPLAY,BLACK,(50,50, 80, 25))

# <-- Menu --> #
	
	if choose == 0:
		redo_list1.clear()
		redo_list2.clear()
		count = 0
		score_1 =0 
		score_2 = 0
		score_bot = 0
		count_save = 0
		player1.clear()
		player2.clear()
		bot1.clear()
		# <-- Images will be random --> #
		o_random = random.randint(0,len(o_images)-1)
		x_random = random.randint(0,len(x_images)-3)
		avatar_random = random.randint(1,len(Avatar)-1)
		if Music_mode % 2 == 0:
			menu()
			if pygame.mixer.get_busy() == True: 
				pygame.mixer.music.play()					
		else:
			menu(1)
			pygame.mixer.music.stop()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			# <-- Music ON/OFF --> #	
			if pygame.Rect((1290,35),(60,62)).collidepoint(pygame.mouse.get_pos()):
				if event.type == pygame.MOUSEBUTTONDOWN:
					sound.play()
					Music_mode += 1

		#pygame.draw.rect(DISPLAY,BLACK,(330,490,520,100))
		# <-- When the cursor is near multi mode --> #
			if pygame.Rect((390,565),(590, 100)).collidepoint(pygame.mouse.get_pos()):		
				if event.type == pygame.MOUSEBUTTONDOWN:
					sound.play()
					choose = 1
					print("HELLO")

		# <-- When the cursor is near single mode --> #
			if pygame.Rect((390,400),(590, 100)).collidepoint(pygame.mouse.get_pos()):	
				if event.type == pygame.MOUSEBUTTONDOWN:
					sound.play()
					choose = 2
					print("HI")

		# <-- IMAGE LOADING MUST BE OUT OF "FOR LOOPS" ABOVE. OTHEWISE, THE RESPONDING OF IMAGES WILL BE INTERRUPTED --> #
		if pygame.Rect((390,565),(590, 100)).collidepoint(pygame.mouse.get_pos()):		
			PVP = pygame.image.load(os.path.join("Images","Multiplayer.png"))
			DISPLAY.blit(PVP,(392,562))

		if pygame.Rect((390,395),(590, 100)).collidepoint(pygame.mouse.get_pos()):
			PVB = pygame.image.load(os.path.join("Images","Singleplayer.png"))
			DISPLAY.blit(PVB,(392,398))		

		if choose != 0:
			DISPLAY.blit(ingame_image,(0,0))
		clock.tick(240)
		pygame.display.flip()
# <-- Player VS Player -->
	if choose == 1:
		DISPLAY.blit(Avatar[avatar_random], (MIN_WIDTH-210,HEIGHT/5))
		DISPLAY.blit(Avatar[len(Avatar)-avatar_random-1], (WIDTH+25,HEIGHT/5))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			# <-- Get position of mouse --> #
			position = pygame.mouse.get_pos()

			#pygame.draw.rect(DISPLAY,RED,(50,HEIGHT+20, 220, 30))
			# <-- Music --> #
			if pygame.Rect((1330,35),(39,55)).collidepoint(pygame.mouse.get_pos()):
				if event.type == pygame.MOUSEBUTTONDOWN:
					Music_mode+=1

			# <-- Save game --> #
			if pygame.Rect((253,20),(100, 40)).collidepoint(pygame.mouse.get_pos()):
				DISPLAY.blit(pygame.image.load(os.path.join("Images","SAVE.png")),(253,20))
				pygame.display.update()
				if event.type == pygame.MOUSEBUTTONDOWN:				
					sound.play()
					save_game()
			else:	
				DISPLAY.blit(pygame.image.load(os.path.join("Images","SAVE1.png")),(253 ,20))

			# <-- Load game --> #
			if pygame.Rect((336,20),(100, 40)).collidepoint(pygame.mouse.get_pos()):
				DISPLAY.blit(pygame.image.load(os.path.join("Images","LOAD.png")),(336,20))
				if event.type == pygame.MOUSEBUTTONDOWN:
					load_game()	
			else:	
				DISPLAY.blit(pygame.image.load(os.path.join("Images","LOAD1.png")),(336,20))	

			# <-- Back to menu -->
			if pygame.Rect((12,12),(195, 65)).collidepoint(pygame.mouse.get_pos()):			
				DISPLAY.blit(pygame.image.load(os.path.join("Images","BTM1.png")),(11,13))				
				if event.type == pygame.MOUSEBUTTONUP:
					sound.play()					
					choose = 0
			else:
				DISPLAY.blit(pygame.image.load(os.path.join("Images","BTM.png")),(11,13))	

			# <-- Undo --> #
			if pygame.Rect((1093,31),(52, 60)).collidepoint(pygame.mouse.get_pos()):			
				if event.type == pygame.MOUSEBUTTONDOWN:		
					sound.play()
					count = undo(count)
					display()						
					if (count < count_save):
						count = count_save	
						
			# <-- Redo --> #
			if pygame.Rect((1150,31),(50, 60)).collidepoint(pygame.mouse.get_pos()):					
				if event.type == pygame.MOUSEBUTTONDOWN:
					sound.play()
					DISPLAY.blit(pygame.image.load(os.path.join("Images","REDO.png")),(1093,31))	
					pygame.display.update()
					pygame.time.wait(100)
					display()		
					if (redo_save  <=  count):
						redo_list1.clear()
						redo_list2.clear() 
					if count % 2 == 0:
						if (len(redo_list1) > 0):						
							player1.append(redo_list1[len(redo_list1)-1])
							redo_list1.pop()		
							count+=1
					else:
						if (len(redo_list2) > 0):
							player2.append(redo_list2[len(redo_list2)-1])
							redo_list2.pop()
							count+=1			
			pygame.display.flip()

			# <-- Rule --> #
			Rule(rule)
			if pygame.Rect((815,20),(240, 55)).collidepoint(pygame.mouse.get_pos()):
				if event.type == pygame.MOUSEBUTTONDOWN:
					sound.play()
					rule+=1

			# <-- Pre-move --> #
			if win == 0:				
				if  position[0] < MIN_WIDTH + 2 or position[1] < MIN_HEIGHT + 1 or position[0] >= WIDTH or position[1] >= HEIGHT:
					continue
				if 	[ 25* int(position[0]/25+1),25* int(position[1]/25+1)] in player1 or [ 25* int(position[0]/25+1), 25* int(position[1] /25 )] in player1 or [25* int(position[0]/25),25* int(position[1]/25+1)] in player1 or  [25* int(position[0]/25),25* int(position[1]/25)] in player1 :
					continue
				if 	[ 25* int(position[0]/25+1),25* int(position[1]/25+1)] in player2 or [ 25* int(position[0]/25+1), 25* int(position[1] /25 )] in player2 or [25* int(position[0]/25),25* int(position[1]/25+1)] in player2 or  [25* int(position[0]/25),25* int(position[1]/25)] in player2 :
					continue
				DISPLAY.blit(board_image,(MIN_WIDTH,MIN_HEIGHT))
				if (int(position[0]/25))%2 ==0:		
					x = 25* int(position[0]/25+1)
					invisible_player(count,GRAY)
				else:				
					x = 25* int(position[0]/25) 
					invisible_player(count,GRAY)
				if (int(position[1]/25))%2 ==0:			
					y = 25* int(position[1]/25+1)
					invisible_player(count,GRAY)
				else : 			
					y = 25* int((position[1] /25))
					invisible_player(count,GRAY)

			# <-- MOVE --> #
			if event.type == pygame.MOUSEBUTTONDOWN and win == 0:
				redo_save = count # When you make a new move, you can't redo what you last undo 
				sound.play()
				if [x,y] in player1 or [x,y] in player2 or x < MIN_WIDTH + 2 or y < MIN_HEIGHT+26 or x >= WIDTH or y >= HEIGHT:
					continue					
				if count %2 ==0:
					player1.append([x,y])
					replay_list.append([x,y])
				else:
					player2.append([x,y])
					replay_list.append([x,y])
				count+=1
	
			# <-- When won --> 
			if win == 1:
				if event.type == pygame.KEYDOWN:		
					if event.key == pygame.K_x:
						pygame.quit()
						sys.exit()
				# <-- Replay --> #		
				DISPLAY.blit(replay_image,(100,100))
				if pygame.Rect((100,100),(695, 78)).collidepoint(pygame.mouse.get_pos()):				
					if event.type == pygame.MOUSEBUTTONDOWN:
						replay()

				else:
					if event.type == pygame.MOUSEBUTTONDOWN:
						sound.play()
						win = 0
						replay_list.clear()
						wining_diag.clear()
						wining_x.clear()
						wining_y.clear()
						player1.clear()
						player2.clear()					
						DISPLAY.blit(ingame_image,(0,0))	
						count_save = count

		# <-- Drawing --> #
		if win == 0:
			score1 = player_text.render("%d" %score_1,10,BLACK)
			score2 = player_text.render("%d" %score_2,10,BLACK)
			DISPLAY.blit(score1,(MIN_WIDTH-52, HEIGHT/2))
			DISPLAY.blit(score2,(WIDTH + 50, HEIGHT/2))
			for i in player1:			
				DISPLAY.blit(o_images[o_random],(i[0]-21,i[1]-21))	
			for i in player2 :
				DISPLAY.blit(x_images[x_random],(i[0]-17,i[1]-17))
			pygame.display.update()

		# <-- Refill when game ended --> #
		else:
			for i in player1:
				pygame.draw.circle(DISPLAY,GRAY_FADING, i , 22)	 	
			for i in player2:					
				DISPLAY.blit(x_images[6],(i[0]-17,i[1]-17))		
			DISPLAY.blit(win_text1, (WIDTH/3+20,HEIGHT+20))
			DISPLAY.blit(win_text2, (WIDTH/3+60,HEIGHT+60))	
			pygame.display.update()
		# <-- Check win --> #
		if check_win(player1,player2) == True and win == 0:
			if len(wining_x) > 0:
				for i in wining_x[0]:
					player1.remove([i,wining_holding_y[0]])
			elif (len(wining_y) > 0):
				for i in wining_y[0]:
					player1.remove([wining_holding_x[0],i])
			else:
				for i in wining_diag:
					player1.remove(i)
			text = font.render('PLAYER 1 WON!', 10, BLACK)
			DISPLAY.blit(text, (WIDTH/2-50,50))
			win = 1 
			score_1 += 1
		if check_win(player2,player1) == True and win == 0:
			if len(wining_x) > 0:
				for i in wining_x[0]:
					player2.remove([i,wining_holding_y[0]])
			elif (len(wining_y) > 0):
				for i in wining_y[0]:
					player2.remove([wining_holding_x[0],i])
			else :
				for i in wining_diag:
					player2.remove(i)

			text = font.render('PLAYER 2 WON!', 10, BLACK)
			DISPLAY.blit(text, (WIDTH/2-50,50))		
			win = 1
			score_2 += 1
		# <-- Out of moves --> #
		if len(player1) + len(player2) >= board:
			win = 1
			text = font.render('OUT OF MOVES',10,BLACK)
			DISPLAY.blit(text, (WIDTH/2-50,50))
		# <-- When music ends --> #
		if Music_mode%2 == 0:
			DISPLAY.blit(pygame.image.load(os.path.join("Images","VO.png")),(0,0))
			if pygame.mixer.music.get_busy() == False :
				pygame.mixer.music.load("HoaTrongCamQuan.mp3")
				pygame.mixer.music.play()
		else:
			DISPLAY.blit(pygame.image.load(os.path.join("Images","VO_X.png")),(0,0))
			pygame.mixer.music.stop()
# <-- Player VS Bot -->
	if choose == 2:
		DISPLAY.blit(Avatar[avatar_random], (MIN_WIDTH-200,HEIGHT/5))
		DISPLAY.blit(Avatar[len(Avatar) - avatar_random], (WIDTH+25,HEIGHT/5))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# <-- Music --> #
			if pygame.Rect((1330,35),(39,55)).collidepoint(pygame.mouse.get_pos()):
				if event.type == pygame.MOUSEBUTTONDOWN:
					Music_mode+=1
			# <-- Save game --> #
			if pygame.Rect((253,20),(100, 40)).collidepoint(pygame.mouse.get_pos()):
				DISPLAY.blit(pygame.image.load(os.path.join("Images","SAVE.png")),(253,20))
				pygame.display.update()
				if event.type == pygame.MOUSEBUTTONDOWN:				
					sound.play()
					save_game()
			else:	
				DISPLAY.blit(pygame.image.load(os.path.join("Images","SAVE1.png")),(253 ,20))
			# <-- Load game --> #
			if pygame.Rect((336,20),(100, 40)).collidepoint(pygame.mouse.get_pos()):
				DISPLAY.blit(pygame.image.load(os.path.join("Images","LOAD.png")),(336,20))
				if event.type == pygame.MOUSEBUTTONDOWN:
					load_game()	
			else:	
				DISPLAY.blit(pygame.image.load(os.path.join("Images","LOAD1.png")),(336,20))	

			# <-- Back to menu -->
			if pygame.Rect((12,12),(195, 65)).collidepoint(pygame.mouse.get_pos()):			
				DISPLAY.blit(pygame.image.load(os.path.join("Images","BTM1.png")),(11,13))				
				if event.type == pygame.MOUSEBUTTONUP:
					sound.play()					
					choose = 0
			else:
				DISPLAY.blit(pygame.image.load(os.path.join("Images","BTM.png")),(11,13))	

			# <-- Undo -->
			if pygame.Rect((1093,31),(52, 60)).collidepoint(pygame.mouse.get_pos()):	
				if event.type == pygame.MOUSEBUTTONUP:
					sound.play()
					count = undo(count)
					display()

			# <-- Redo --> #
			if pygame.Rect((1150,31),(50, 60)).collidepoint(pygame.mouse.get_pos()):					
				if event.type == pygame.MOUSEBUTTONDOWN:
					sound.play()
					DISPLAY.blit(pygame.image.load(os.path.join("Images","REDO.png")),(1093,31))	
					pygame.display.update()
					pygame.time.wait(100)
					display()		
					if (redo_save  <=  count):
						redo_list1.clear()
						redo_list2.clear() 
					if (len(redo_list1) > 0):						
						player1.append(redo_list1[len(redo_list1)-1])
						redo_list1.pop()								
						bot1.append(redo_list2[len(redo_list2)-1])
						redo_list2.pop()
						count+=2
			# <-- Rule --> #
			Rule(rule)
			if pygame.Rect((815,20),(240, 55)).collidepoint(pygame.mouse.get_pos()):
				if event.type == pygame.MOUSEBUTTONDOWN:
					sound.play()
					rule+=1
			# <-- Get position of mouse --> #
			position = pygame.mouse.get_pos()
			# <-- Pre-move --> #
			if win == 0:
				DISPLAY.blit(board_image,(MIN_WIDTH,MIN_HEIGHT))
				if  position[0] < MIN_WIDTH + 2 or position[1] < MIN_HEIGHT + 1 or position[0] >= WIDTH or position[1] >= HEIGHT:
					continue				
				if 	[ 25* int(position[0]/25+1),25* int(position[1]/25+1)] in player1 or [ 25* int(position[0]/25+1), 25* int(position[1] /25 )] in player1 or [25* int(position[0]/25),25* int(position[1]/25+1)] in player1 or  [25* int(position[0]/25),25* int(position[1]/25)] in player1 :
					continue
				if 	[ 25* int(position[0]/25+1),25* int(position[1]/25+1)] in bot1 or [ 25* int(position[0]/25+1), 25* int(position[1] /25 )] in bot1 or [25* int(position[0]/25),25* int(position[1]/25+1)] in bot1 or  [25* int(position[0]/25),25* int(position[1]/25)] in bot1 :
					continue
				if (int(position[0]/25))%2 ==0:
					x = 25* int(position[0]/25+1)
					invisible_player(0,GRAY)
				else:
					x = 25* int(position[0]/25) 
					invisible_player(0,GRAY)
				if (int(position[1]/25))%2 ==0:
					y = 25* int(position[1]/25+1)
					invisible_player(0,GRAY)
				else : 
					y = 25* int((position[1] /25 ))
					invisible_player(0,GRAY)

			# <-- MOVE --> #
			if event.type == pygame.MOUSEBUTTONDOWN and win == 0:			
				if [x,y] in player1 or [x,y] in bot1 or x < MIN_WIDTH + 2 or y < MIN_HEIGHT + 1 or x > WIDTH or y > HEIGHT:
					continue	
				sound.play()
				player1.append([x,y])
				replay_list.append([x,y])	
				if check_win(player1,bot1) == True and win == 0:
					pass
				else:		
					bot()
				count +=  2
				redo_save = 0
			# <-- When wins --> 
			if win == 1:
				if event.type == pygame.KEYDOWN and win == 1:		
					if event.key == pygame.K_x:
						pygame.quit()
						sys.exit()
				# <-- Replay --> #		
				DISPLAY.blit(replay_image,(100,100))
				if pygame.Rect((100,100),(695, 78)).collidepoint(pygame.mouse.get_pos()):				
					if event.type == pygame.MOUSEBUTTONDOWN:
						replay()
				else:
					if event.type == pygame.MOUSEBUTTONDOWN and win == 1:
						sound.play()
						win = 0
						wining_diag.clear()
						replay_list.clear()
						wining_x.clear()
						wining_y.clear()
						player1.clear()
						bot1.clear()
						DISPLAY.blit(ingame_image,(0,0))		

		# <-- Drawing --> #
		if win == 0:
			score1 = player_text.render("%d" %score_1,10,BLACK)
			score2 = player_text.render("%d" %score_bot,10,BLACK)
			DISPLAY.blit(score1,(MIN_WIDTH-52, HEIGHT/2))
			DISPLAY.blit(score2,(WIDTH + 50, HEIGHT/2))
			for i in player1:
				DISPLAY.blit(o_images[o_random],(i[0]-21,i[1]-21))	
			for i in bot1:
				DISPLAY.blit(x_images[x_random],(i[0]-17,i[1]-17))
			if len(bot1) > 0:
				DISPLAY.blit(x_images[7],[bot1[len(bot1)-1][0]-17,bot1[len(bot1)-1][1]-17])
		else:
			for i in player1:
				pygame.draw.circle(DISPLAY,GRAY,i ,22)	
			for i in bot1:
				DISPLAY.blit(x_images[6],(i[0]-17,i[1]-17))	
			DISPLAY.blit(win_text1, (WIDTH/3+20,HEIGHT+20))
			DISPLAY.blit(win_text2, (WIDTH/3+20,HEIGHT+60))	
		# <-- Check win --> #
		if check_win(player1,bot1) == True and win == 0:
			if len(wining_x) > 0:
				for i in wining_x[0]:
					player1.remove([i,wining_holding_y[0]])
			elif (len(wining_y) > 0):
				for i in wining_y[0]:
					player1.remove([wining_holding_x[0],i])
			else:
				print(wining_diag)
				print(player1)
				for i in wining_diag:
					player1.remove(i)
			score_1 +=1
			text = font.render('YOU WON!', 10, BLACK)
			DISPLAY.blit(text, (WIDTH/2-50,50))
			win = 1 
		if check_win(bot1,player1) == True and win == 0:
			if len(wining_x) > 0:
				for i in wining_x[0]:
					bot1.remove([i,wining_holding_y[0]])
			elif (len(wining_y) > 0):
				for i in wining_y[0]:
					bot1.remove([wining_holding_x[0],i])
			else:
				for i in wining_diag:
					bot1.remove(i)
			text = font.render('YOU LOSE!', 10, BLACK)
			score_bot +=1
			DISPLAY.blit(text, (WIDTH/2-50,50))
			win = 1
		# <-- Out of moves --> #
		if len(player1) + len(bot1) >= board:
			win =1
			text = font.render('OUT OF MOVES',10,BLACK)
			DISPLAY.blit(text, (WIDTH/2-50,50))

		# <-- When music ends --> #
		if Music_mode%2 == 0:
			DISPLAY.blit(pygame.image.load(os.path.join("Images","VO.png")),(0,0))
			if pygame.mixer.music.get_busy() == False :
				pygame.mixer.music.load("HoaTrongCamQuan.mp3")
				pygame.mixer.music.play()
		else:
			DISPLAY.blit(pygame.image.load(os.path.join("Images","VO_X.png")),(0,0))
			pygame.mixer.music.stop()
	clock.tick(FPS)
	pygame.display.flip()


# 4:50 PM - 10/03/2019 #
# --Chưa:
# Làm game Mới
# Đổi ký tự người chơi
# Fix save/load position

# -- Mới:
# Resolution
# Nothing new
# Fixing resolution
# Nước cờ X
# Fix các nút