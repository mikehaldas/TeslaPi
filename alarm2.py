import RPi.GPIO as GPIO
import teslajson
import time
import datetime
import vars

# define pins
ALARM_IN = 16 # motion detector input
LED = 24 # removed this line if you do not setup the LED
STROBE = 23

# setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# set GPIO port to pull up when using a PIR motion sensor that is set to normally closed
# a GPIO will float between 0 and 1 if it's not connected to a voltage. 
# pull-up/downs supply voltage so that the GPIO will have a defined value UNTIL overridden by a stronger force. 
# You should set a pull-down (to 0) when you expect the stronger force to pull it up to 1. 
# You should set a pull-up (to 1) when you expect the stronger force to pull it down to 0.
# An input gpio will float between 0 and 1 if it's not connected to a voltage. 
GPIO.setup(ALARM_IN, GPIO.IN, GPIO.PUD_UP)

# setup LED. Handy when developing & testing
GPIO.setup(LED, GPIO.OUT) # removed this line if you do not setup the LED
#GPIO.output(LED, False) # removed this line if you do not setup the LED
GPIO.output(LED, GPIO.LOW) # removed this line if you do not setup the LED

# setup alarm strobe light
GPIO.setup(STROBE, GPIO.OUT) # removed this line if you do not setup the STROBE
GPIO.output(STROBE, GPIO.HIGH) # removed this line if you do not setup the STROBE

# Tesla API setup
print "Connecting to Tesla API...\n"
c = teslajson.Connection(vars.USERID, vars.PASS)
v = c.vehicles[0] # vehicles is an array. This assumes you only have one Tesla

# general alarm rules
ALARM_RESET_DELAY = 2 # it may take a few seconds for PIR motion detectors to reset
NUM_FLASHES = 2 # number of times you want the headlights to flash per alarm cycle
FLASH_DELAY = 1 # delay (in seconds) between headlight flashes
BEGIN_HOUR = 12 # hour to begin monitoring
END_HOUR = 18 # hour to end monitoring

ALARM_CYCLE_TIMER = 60 # number of seconds that motion must continue for (or another event must occur in) in order to increment the alarm cycle
ACTIVATE_HORN = 0 # enable horn honking in WARNING and PANIC alarms
WARNING_HORN_ALARM_THRESHOLD = 3 # number of alarm cycles to trigger warning horn alarm
PANIC_HORN_ALARM_THRESHOLD = 5 # number of alarm cycles to trigger panic horn alarm
WARNING_HONKS = 1 # numner of time to honk horn during warning alarm
PANIC_HONKS = 3 # number of times to honk horn during panic alarm

# functions
def flash_headlights():
	for x in range(NUM_FLASHES):
		print "Flash Lights: ", x+1, " of ", NUM_FLASHES, "\n"
		r = v.command('flash_lights')
		time.sleep(FLASH_DELAY)

def honk_horn(num_honks):
	for x in range(num_honks):	
		print "Honk Horn: ", x+1, " of ", num_honks, "\n"
		if ACTIVATE_HORN:
			r = v.command('honk_horn')

def compare_time(past_time):
	#compare the date passed in with the current date in seconds
	current_time = datetime.datetime.now()
	diff_seconds = (current_time-past_time).total_seconds()
	return diff_seconds


# number of time an alarm was triggered in the current cycle
alarm_cycle_count = 0

# main program
try:
# setup an indefinite loop that looks for the motion detector to open the relay
	while True:

		# motion detector alarm received
		if GPIO.input(ALARM_IN):
			GPIO.output(LED, GPIO.HIGH) # turn LED on
			GPIO.output(STROBE, GPIO.LOW) # turn STROBE on
			today = datetime.date.today()
			thetime = datetime.datetime.now().time()
			print "Motion Detected on", today.strftime('%b %d %Y'), "at", thetime.strftime('%X'), "\n"

			if (thetime > datetime.time(BEGIN_HOUR) and thetime < datetime.time(END_HOUR)):
				print "In time monitoring range...\n"
				alarm_cycle_count += 1
				if (alarm_cycle_count == 1):
					first_alarm_datetime = datetime.datetime.now()
					print "First alarm cycle", first_alarm_datetime, "\n"

				print "Alarm cycle count:", alarm_cycle_count,  "\n" 
				print "Wake up Telsa...\n"
				v.wake_up()

				seconds_since_first_alarm = compare_time(first_alarm_datetime)
				print "Seconds since first alarm trigger:", seconds_since_first_alarm, "\n"
				if (seconds_since_first_alarm < ALARM_CYCLE_TIMER):

					# if we have reached WARNING or PANIC thresholds, take action!
					if (alarm_cycle_count >= PANIC_HORN_ALARM_THRESHOLD):
						print "Send Panic Horn Alarm to Tesla...\n"
						honk_horn(PANIC_HONKS)
						print "Resetting alarm cycle count...\n"
						alarm_cycle_count = 0
					elif (alarm_cycle_count >= WARNING_HORN_ALARM_THRESHOLD):
						print "Send Warning Horn Alarm to Tesla...\n"
						honk_horn(WARNING_HONKS)

					# always flash headlights regardless of alarm_cycle_count
					print "Sending Headlight Alarm to Tesla...\n"
					flash_headlights()
				else:
					print "More than", ALARM_CYCLE_TIMER, "seconds since first alarm. Resetting cycle.\n"
					alarm_cycle_count = 0
			else:
				print "Outside of monitoring time range. DO NOT send alarm.\n"

			print "Alarm Delay is ", ALARM_RESET_DELAY, " seconds...\n"
			time.sleep(ALARM_RESET_DELAY)
			GPIO.output(LED, GPIO.LOW) # turn LED off
			GPIO.output(STROBE, GPIO.HIGH) # turn STROBE off
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
