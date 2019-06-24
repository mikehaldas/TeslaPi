"""
TelsaPi is a security alarm project that integrates an outdoor motion sensor with the headlights and horn of a Tesla car. 
It works with all Tesla models. The project uses a Raspberry Pi, an outdoor PIR motion detector, and the Tesla API.

TeslaPi is desctibed in more detail at:
https://videos.cctvcamerapros.com/TeslaPi

"""
import RPi.GPIO as GPIO
import teslajson
import time
import datetime
import vars

# define GPIO pins
MOTION_SENSOR = 16 # PIR motion sensor input

# setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO port for the motion sensor to pull up when sensor is normally closed (NC).
# An input GPIO will float between 0 and 1 if it's not connected to a voltage. 
# Pull-up/downs supply voltage so that the GPIO will have a defined value UNTIL overridden by a stronger force. 
# You should set a pull-down (to 0) when you expect the stronger force to pull it up to 1. 
# You should set a pull-up (to 1) when you expect the stronger force to pull it down to 0.
GPIO.setup(MOTION_SENSOR, GPIO.IN, GPIO.PUD_UP)

# Tesla API setup
print "Connecting to Tesla API...\n"
c = teslajson.Connection(vars.USERID, vars.PASS)
v = c.vehicles[0] # vehicles is an array. This assumes you only own one Tesla in your account.

# Alarm rules
ALARM_RESET_DELAY = 2 # it may take a few seconds for the motion detectors to reset
FLASH_DELAY = 1 # delay (in seconds) between headlight flashes in the alarm cycle
MONITORING_BEGIN_HOUR = 12 # hour to begin monitoring. Ex. 23 = start at 11:00pm
MONITORING_END_HOUR = 18 # hour to end monitoring. Ex. 6 = end at 6:00am
ALARM_CYCLE_TIMER = 60 # number of seconds that motion must continue for (or another event must occur in) in order to increment the alarm cycle
ACTIVATE_HORN = 0 # enable/disable horn honking. Nice to turn off when developing. 0 = off, 1 = on

# functions
def flash_headlights(num_flashes):
	for x in range(num_flashes):
		print "Flash Lights: ", x+1, " of ", num_flashes, "\n"
		r = v.command('flash_lights')
		time.sleep(FLASH_DELAY)

def honk_horn(num_honks):
	for x in range(num_honks):	
		print "Honk Horn: ", x+1, " of ", num_honks, "\n"
		if ACTIVATE_HORN:
			r = v.command('honk_horn')

def compare_time(past_time):
	#compare a date/time in the passed in with the current date/time in seconds
	current_time = datetime.datetime.now()
	diff_seconds = (current_time-past_time).total_seconds()
	return diff_seconds

# keep track of the number of times an alarm was triggered in the current cycle
# this is used to escalate the alarm level in a cycle. 
escalation_lvl = 0

# main program
try:
# setup an indefinite loop that looks for the motion detector to open the relay
	while True:

		# motion detector alarm received
		if GPIO.input(MOTION_SENSOR):
			today = datetime.date.today()
			thetime = datetime.datetime.now().time()
			print "Motion Detected on", today.strftime('%b %d %Y'), "at", thetime.strftime('%X'), "\n"

			if (thetime > datetime.time(MONITORING_BEGIN_HOUR) and thetime < datetime.time(MONITORING_END_HOUR)):
				print "In time monitoring range...\n"
				escalation_lvl += 1
				if (escalation_lvl == 1):
					first_alarm_datetime = datetime.datetime.now()
					print "First alarm cycle", first_alarm_datetime, "\n"

				print "Alarm escalation level:", escalation_lvl,  "\n" 
				print "Wake up Telsa...\n"
				v.wake_up()

				seconds_since_first_alarm = compare_time(first_alarm_datetime)
				print "Seconds since first alarm trigger:", seconds_since_first_alarm, "\n"
				if (seconds_since_first_alarm < ALARM_CYCLE_TIMER):

					# Alarm Escalation levels
					if (escalation_lvl == 1):
						flash_headlights(3)

					elif (escalation_lvl == 2):
						flash_headlights(3)

					elif (escalation_lvl == 3):
						honk_horn(1)
						flash_headlights(3)

					elif (escalation_lvl == 4):
						honk_horn(2)
						flash_headlights(3)

					elif (escalation_lvl == 5):
						honk_horn(3)
						flash_headlights(3)

						print "Resetting alarm cycle count...\n"
						escalation_lvl = 0
						
				else:
					print "More than", ALARM_CYCLE_TIMER, "seconds since first alarm. Resetting cycle.\n"
					escalation_lvl = 0
			else:
				print "Outside of monitoring time range. DO NOT send alarm.\n"

			print "Alarm Delay is ", ALARM_RESET_DELAY, " seconds...\n"
			time.sleep(ALARM_RESET_DELAY)
			# after a short delay, the motion sensor is ready again.
			print "Alarm Ready...\n"
			print "---------------------------------\n"

# ctrl-c pressed. Exit.
except KeyboardInterrupt:
	print "Exiting.\n"
	GPIO.cleanup()

finally:
	GPIO.cleanup()

# cleanup
GPIO.cleanup()
