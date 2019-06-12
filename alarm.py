import RPi.GPIO as GPIO
import teslajson
import time
import datetime
import vars

# GPIO setup
ALARM_IN = 16 # motion detector input
LED = 24 # removed this line if you do not setup the LED

#setup GPIO using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# set GPIO port to normally closed position
GPIO.setup(ALARM_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#setup LED. This is handy when developing
GPIO.setup(LED, GPIO.OUT) # removed this line if you do not setup the LED
GPIO.output(LED, False) # removed this line if you do not setup the LED

#tesla setup
print "Connecting to Tesla API...\n"
c = teslajson.Connection(vars.USERID, vars.PASS)
v = c.vehicles[0]

#alarm rules
ALARM_RESET_DELAY = 5
NUM_OF_FLASHES = 2
FLASH_DELAY = 1
BEGIN_HOUR = 12
END_HOUR = 18
WARNING_HORN_ALARM_THRESHOLD = 3
PANIC_HORN_ALARM_THRESHOLD = 5
PANIC_TIMER = 10


def flash_headlights():
	for x in range(NUM_OF_FLASHES):
		print "Flash Lights: ", x+1, " of ", NUM_OF_FLASHES, "\n"
		r = v.command('flash_lights')
		time.sleep(FLASH_DELAY)

def honk_horn(num_honks):
	for x in range(num_honks):	
		r = v.command('honk_horn')

def compare_time(past_time):
	#compare the date passed in with the current date in seconds
	current_time = datetime.datetime.now()
	diff_seconds = (current_time-past_time).total_seconds()
	return diff_seconds


#number of time an alarm was triggered in the current cycle
alarm_cycle_count = 0

try:
# setup an indefinite loop that looks for the motion detector to open it's relay
	while True:

		# DVR Alarm received
		GPIO.wait_for_edge(ALARM_IN, GPIO.RISING)
		GPIO.output(LED, True) # removed this line if you do not setup the LED
		today = datetime.date.today()
		thetime = datetime.datetime.now().time()
		print "Motion Detected on", today.strftime('%b %d %Y'), "at", thetime.strftime('%X'), ".\n"

		if (thetime > datetime.time(BEGIN_HOUR) and thetime < datetime.time(END_HOUR)):
			alarm_cycle_count += 1
			if (alarm_cycle_count == 1):
				first_alarm_datetime = datetime.datetime.now()
				print "First alarm cycle", first_alarm_datetime, "\n\n"

			print "Alarm cycle count:", alarm_cycle_count,  "\n" 
			print "In time monitoring range...\n"
			print "Waking up Telsa...\n"
			v.wake_up()

			seconds_since_first_alarm = compare_time(first_alarm_datetime)
			print "Seconds since first alarm trigger:", seconds_since_first_alarm
			if (seconds_since_first_alarm < PANIC_TIMER):

				if (alarm_cycle_count >= PANIC_HORN_ALARM_THRESHOLD):
					print "Send Panic Horn Alarm to Tesla...\n"
					honk_horn(3)
					print "Resetting alarm cycle count...\n"
					alarm_cycle_count = 0
				elif (alarm_cycle_count >= WARNING_HORN_ALARM_THRESHOLD):
					print "Send Warning Horn Alarm to Tesla...\n"
					honk_horn(1)

				print "Sending Headlight Alarm to Tesla...\n"
				flash_headlights()
			else:
				print "More than", PANIC_TIMER, "seconds since first alarm. Resetting cycle.\n"
				alarm_cycle_count = 0
		else:
			print "Outside of monitoring time. DO NOT send alarm.\n"

		print "Alarm Delay is ", ALARM_RESET_DELAY, " seconds...\n"
		time.sleep(ALARM_RESET_DELAY)
		GPIO.output(LED, False)
		print "Alarm Ready...\n"

except KeyboardInterrupt:
	print "Exiting.\n"
	#GPIO.cleanup()

finally:
	GPIO.cleanup()

# cleanup
GPIO.cleanup()
