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
	time.sleep(1)	
	os.system('sudo shutdown -h now')

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

global budget, pressed

images = {'start':pygame.image.load(path + "BUDRP.jpg"),
		'ready':pygame.image.load(path + "BUDGR.jpg"),
		'1':pygame.transform.scale(pygame.image.load(path + "BUD01.jpg"),(WIDTH,HEIGHT)),
		'2':pygame.transform.scale(pygame.image.load(path + "BUD02.jpg"),(WIDTH,HEIGHT)),
		'3':pygame.transform.scale(pygame.image.load(path + "BUD03.jpg"),(WIDTH,HEIGHT)),
		'cycle':pygame.transform.scale(pygame.image.load(path + "BUDCY.jpg"),(WIDTH,HEIGHT)),
		'logo':pygame.transform.scale(pygame.image.load(path + "bb.jpg"),(WIDTH,HEIGHT)),
		'game-bg': pygame.transform.scale(pygame.image.load(path + "BUDBG.png"),(WIDTH,HEIGHT)),
		'ms': pygame.transform.scale(pygame.image.load(path + "BUDMS.jpg"),(WIDTH,HEIGHT)),
		'cg': pygame.transform.scale(pygame.image.load(path + "BUDCG.jpg"),(WIDTH,HEIGHT)),
		'ta': pygame.transform.scale(pygame.image.load(path + "BUDTA.jpg"),(WIDTH,HEIGHT)),
		'sc': pygame.transform.scale(pygame.image.load(path + "BUDSC.jpg"),(WIDTH,HEIGHT)),
		}


# img_ready = pygame.image.load(path + "BUDGR.png")
# img_ready = pygame.transform.scale(img_ready,(WIDTH,HEIGHT))



food_val = [3,4,4,5,5]
acc_val = [4,5,5,6,7]
act_val = [3,4,4,5,6]

budget = 9

tokens = 0

pygame.init()



screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

font = pygame.font.SysFont("comicsansms", 200)

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
	show_image('game-bg')
	text = font.render("RM " + str(budget), True, (0, 0, 0))
	screen.blit(text, (WIDTH / 2 - (text.get_width() / 2) , 500))
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
			show_image('start')	

		if line[0] == 'V' and not pressed:
			validate(line)	

	except KeyboardInterrupt:
		raise
	except:
		e = sys.exc_info()[0]

		print "something messed up", e



# start_time = time.time()
# while time.time() - start_time < 1:
# 	time.sleep(0.01)
# show_image('start')

# start_time = time.time()

# while time.time() - start_time < 10:
# 	time.sleep(0.01)
# show_image('logo')
