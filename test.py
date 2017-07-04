import pygame
import time
import serial
import sys
path = "/home/pi/budget-game/assets/"

WIDTH = 1920
HEIGHT = 1080

images = {'game-bg': pygame.transform.scale(pygame.image.load(path + "BUDBG2.png"),(WIDTH,HEIGHT)),
		
		}



def show_image(img):
	screen.fill((255, 255, 255))
	screen.blit(images[img], (0, 0))
	pygame.display.flip()

budget = 10

items = { 'Y':[	{'name': 'Roti Canai', 'trans': '', 'price': '3'},
				{'name': 'Thosai Masala', 'trans': '', 'price': '4'},
				{'name': 'Nasi Lemak', 'trans': '', 'price': '4'},
				{'name': 'Nasi Kerabu', 'trans': '', 'price': '5'},
				{'name': 'Sup Kambing', 'trans': '', 'price': '5'}
			],
				
		'G': [	{'name': 'Tent', 'trans': 'Khemah', 'price': '4'},
				{'name': 'Cabin', 'trans': 'Kabin', 'price': '5'},
				{'name': 'Hostel Bunk Bed', 'trans': 'Hostel Katil DUa Tingkat', 'price': '5'},
				{'name': 'Hotel', 'trans': 'Hotel', 'price': '6'},
				{'name': 'Serviced Apartment', 'trans': 'Pangsapuri Bersrvis', 'price': '7'}
			],

		'B': [	{'name': 'Swimming', 'trans': 'Berenang', 'price': '3'},
				{'name': 'Hiking', 'trans': 'Kembara', 'price': '4'},
				{'name': 'Rock Climbing', 'trans': 'Daki Tembok', 'price': '4'},
				{'name': 'Snorkeling', 'trans': 'Mensnorkel', 'price': '5'},
				{'name': 'Scuba Diving', 'trans': 'Selam Skuba', 'price': '5'}
			]
		} 

global y_item, b_item, g_item

y_item = {'name': '', 'trans': '', 'price': ''}
g_item = {'name': '', 'trans': '', 'price': ''}
b_item = {'name': '', 'trans': '', 'price': ''}


def buttonPressed(colour, num):
	global y_item, b_item, g_item
	#print colour, num
	if colour == 'Y':
		y_item = items['Y'][num]
		y_item['price'] = 'RM ' + y_item['price'] 
	if colour == 'B':
		b_item = items['B'][num]
		b_item['price'] = 'RM ' + b_item['price']
	if colour == 'G':
		g_item = items['G'][num]
		g_item['price'] = 'RM ' + g_item['price']
	
	updateGame()	

def updateGame():
	screen.blit(images['game-bg'], (0, 0))
	
	black = (0, 0, 0)
	white = (255, 255, 255)
	yellow = (205,205,0)
	green = (69,139,0)
	blue = (0,0,255)
	translate = 50
	middle = -0
	textX = 240
	rmX = 1420
	row1 = 230
	row2 = 410
	row3 = 590
	row4 = 770

	screen.blit(font.render("Available Budget", True, white), (textX , row1))
	screen.blit(ital.render("Belanjawan Sedia Ada", True, white), (textX , row1 +  translate))
	screen.blit(font2.render("RM " + str(budget), True, white ), (rmX , row1 + middle))

	screen.blit(font.render(y_item['name'], True, yellow), (textX , row2))
	screen.blit(ital.render(y_item['trans'], True, yellow), (textX , row2 +  translate))
	screen.blit(font2.render(y_item['price'], True, yellow ), (rmX , row2 + middle))


	screen.blit(font.render(g_item['name'], True, green), (textX , row3))
	screen.blit(ital.render(g_item['trans'], True, green), (textX , row3 +  translate))
	screen.blit(font2.render(g_item['price'], True, green ), (rmX , row3 + middle))

	screen.blit(font.render(b_item['name'], True, blue), (textX , row4))
	screen.blit(ital.render(b_item['trans'], True, blue), (textX , row4 +  translate))
	screen.blit(font2.render(b_item['price'], True, blue ), (rmX , row4 + middle))




	pygame.display.flip()

strPort1 = '/dev/ttyACM0'

ser = serial.Serial(strPort1, 9600)

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

FONT = "GothamMedium.ttf"

font = pygame.font.SysFont(path + FONT, 60)
ital = pygame.font.SysFont(path + FONT, 40, italic=True)
font2 = pygame.font.SysFont(path + FONT, 80)

updateGame()
while 1:
	try:
		line = ser.readline().strip()
		print line

		if line[0] == 'S':
			print 'Starting'
			#r.publish(TOPIC, 'S')
			#count_down()
			ser.write('F')
		if line[0] == 'X':
			x, colour, button = line.split('\t')

			buttonPressed(colour, int(button))	

		if line[0] == 'V' and not pressed:
			validate(line)	

	except KeyboardInterrupt:
		raise
	except:
		raise
		e = sys.exc_info()

		print "something messed up", e
