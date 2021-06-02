import RPi.GPIO as GPIO
import scholar
import time
from scholar import Scholar
from scholar import LogEntry

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17,GPIO.OUT)

def blink_times(times,duration):
    for i in range(times):
        GPIO.output(17,GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(17,GPIO.LOW)
        time.sleep(duration)

citation_log_file = "citation.log"

dir_path = scholar.parse_args()
citation_log_file=dir_path+"/"+citation_log_file
blinks = scholar.get_daily_diff(citation_log_file)

print("BLINKING #", blinks, " Times")

init()
blink_times(blinks, 0.5)




