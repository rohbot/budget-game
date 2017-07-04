import os
import time
import serial
import sys
import redis
import pygame
import RPi.GPIO as GPIO
#import pyttsx
r = redis.Redis()
BASE_CMD = "sudo fbi -T 1 --noverbose -a "
path = "/home/pi/budget-game/assets/"

def shutdown(channel):
	logfile = open('shutdown.log', 'a')
	logfile.write(str(time.time()) + " shutting down\n")
	logfile.close()
	#os.system('flite -t "System Shutdown"')
	print 'Shutdown'
	cmd = BASE_CMD + path + 'bb.jpg'
	os.system(cmd)

	r.publish('buttons', 'x')
	pubsub.unsubscribe()
	time.sleep(1)	
	os.system('sudo shutdown -h now')
	sys.exit()
def setup():
    print "Shutdown script"
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(12, GPIO.OUT)
    GPIO.add_event_detect(14, GPIO.FALLING, callback = shutdown, bouncetime = 2000)
    GPIO.output(12, GPIO.HIGH)

setup()


strPort1 = '/dev/ttyACM0'

ser = serial.Serial(strPort1, 9600)
#ser2 = serial.Serial(strPort2, 9600)

print r.get('name')

TOPIC = 'buttons'

pubsub = r.pubsub()


WIDTH = 1920
HEIGHT = 1080

global budget, pressed, lines

images = {'start':pygame.image.load(path + "BUDRP.png"),
		'ready':pygame.image.load(path + "BUDGR.png"),
		'1':pygame.transform.scale(pygame.image.load(path + "BUD01.jpg"),(WIDTH,HEIGHT)),
		'2':pygame.transform.scale(pygame.image.load(path + "BUD02.jpg"),(WIDTH,HEIGHT)),
		'3':pygame.transform.scale(pygame.image.load(path + "BUD03.jpg"),(WIDTH,HEIGHT)),
		'cycle':pygame.transform.scale(pygame.image.load(path + "BUDCY.png"),(WIDTH,HEIGHT)),
		'logo':pygame.transform.scale(pygame.image.load(path + "bb.jpg"),(WIDTH,HEIGHT)),
		'game-bg': pygame.transform.scale(pygame.image.load(path + "BUDBG2.png"),(WIDTH,HEIGHT)),
		'ms': pygame.transform.scale(pygame.image.load(path + "BUDMS.png"),(WIDTH,HEIGHT)),
		'ta': pygame.transform.scale(pygame.image.load(path + "BUDCG.png"),(WIDTH,HEIGHT)),
		'cg': pygame.transform.scale(pygame.image.load(path + "BUDTA.png"),(WIDTH,HEIGHT)),
		'sc': pygame.transform.scale(pygame.image.load(path + "BUDSC.png"),(WIDTH,HEIGHT)),

		}


items = { 'Y':[	{'name': 'Roti Canai', 'trans': '', 'price': 'RM 3'},
				{'name': 'Thosai Masala', 'trans': '', 'price': 'RM 4'},
				{'name': 'Nasi Lemak', 'trans': '', 'price': 'RM 4'},
				{'name': 'Nasi Kerabu', 'trans': '', 'price': 'RM 5'},
				{'name': 'Sup Kambing', 'trans': '', 'price': 'RM 5'}
			],
				
		'G': [	{'name': 'Tent', 'trans': 'Khemah', 'price': 'RM 4'},
				{'name': 'Cabin', 'trans': 'Kabin', 'price': 'RM 5'},
				{'name': 'Hostel Bunk Bed', 'trans': 'Hostel Katil DUa Tingkat', 'price': 'RM 5'},
				{'name': 'Hotel', 'trans': 'Hotel', 'price': 'RM 6'},
				{'name': 'Serviced Apartment', 'trans': 'Pangsapuri Bersrvis', 'price': 'RM 7'}
			],

		'B': [	{'name': 'Swimming', 'trans': 'Berenang', 'price': 'RM 3'},
				{'name': 'Hiking', 'trans': 'Kembara', 'price': 'RM 4'},
				{'name': 'Rock Climbing', 'trans': 'Daki Tembok', 'price': 'RM 4'},
				{'name': 'Snorkeling', 'trans': 'Mensnorkel', 'price': 'RM 5'},
				{'name': 'Scuba Diving', 'trans': 'Selam Skuba', 'price': 'RM 5'}
			]
		} 

	
global y_item, b_item, g_item

y_item = {'name': '', 'trans': '', 'price': ''}
g_item = {'name': '', 'trans': '', 'price': ''}
b_item = {'name': '', 'trans': '', 'price': ''}


# img_ready = pygame.image.load(path + "BUDGR.png")
# img_ready = pygame.transform.scale(img_ready,(WIDTH,HEIGHT))



food_val = [3,4,4,5,5]
acc_val = [4,5,5,6,7]
act_val = [3,4,4,5,6]

budget = 9

tokens = 0

pygame.init()



screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

FONT = "GothamMedium.ttf"

font = pygame.font.SysFont(path + FONT, 60)
ital = pygame.font.SysFont(path + FONT, 40, italic=True)
font2 = pygame.font.SysFont(path + FONT, 80)


def show_image(img):
	screen.fill((255, 255, 255))
	screen.blit(images[img], (0, 0))
	pygame.display.flip()

	# cmd = BASE_CMD + path + images[img]
	# os.system(cmd)
def showLogo():
	cmd = BASE_CMD + path + 'bb.jpg'
	os.system(cmd)

def count_down():
	show_image('ready')
	time.sleep(1)
	show_image('3')
	time.sleep(1)
	show_image('2')
	time.sleep(1)
	show_image('1')
	time.sleep(1)
	
	show_image('cycle')
	waitForFinish()
	#time.sleep(10)
	#game()

def waitForFinish():
	global budget
	finished = False
	budget = 10
	start_time = time.time()
	os.system("(sleep 70; redis-cli publish tokens F) &")
	pubsub.subscribe('tokens')
	while not finished:
		for item in pubsub.listen():
			print item
			if item['type'] == 'message':
				print item['data']
				if item['data'] == 'F':
					finished = True
					if budget < 10:
						budget = 10
					pubsub.unsubscribe()
				else:
					budget = int(item['data'])
					print 'tokens:', budget
		time.sleep(0.01)
	game()

	
def game():
	global budget
	print 'cycling'
	ser.write('F')
	updateGame()
	# show_image('game-bg')
	# text = font.render("RM " + str(budget), True, (0, 0, 0))
	# screen.blit(text, (WIDTH / 2 - (text.get_width() / 2) , 500))
	# pygame.display.flip()


def buttonPressed(colour, num):
	global y_item, b_item, g_item
	#print colour, num
	if colour == 'Y':
		y_item = items['Y'][num]
		#y_item['price'] = 'RM ' + y_item['price'] 
	if colour == 'B':
		b_item = items['B'][num]
		#b_item['price'] = 'RM ' + b_item['price']
	if colour == 'G':
		g_item = items['G'][num]
		#g_item['price'] = 'RM ' + g_item['price']
	
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



def validate(line):
	pressed = True
	tokens = line.split('\t')
	for i in tokens:
		if i == '-1':
			show_image('ms')
			pressed = False
			return
	print tokens, 'valid'
	
	food = int(tokens[1])
	acc = int(tokens[2])
	act = int(tokens[3])


	total = food_val[food] + acc_val[acc] + act_val[act]
	print food, acc, act, total

	if total <= budget:
		print 'valid'
		show_image('cg')
		time.sleep(5)
		show_image('sc')
		time.sleep(10)
		show_image('start')
		ser.write('V')
		r.publish(TOPIC, 'V')
	


	else:
		print 'invalid'
		show_image('ta')
		time.sleep(3)
		#show_image('game-bg')
		game()
		pressed = False



	

# game()
# time.sleep(10)

showLogo()

time.sleep(2)
show_image('start')
print 'starting'
pressed = False
while 1:
	try:
		line = ser.readline().strip()
		print line

		if line[0] == 'S':
			print 'Starting'
			r.publish(TOPIC, 'S')
			count_down()
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



# start_time = time.time()
# while time.time() - start_time < 1:
# 	time.sleep(0.01)
# show_image('start')

# start_time = time.time()

# while time.time() - start_time < 10:
# 	time.sleep(0.01)
# show_image('logo')
