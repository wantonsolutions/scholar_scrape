#import RPi.GPIO as GPIO
import scholar

citation_log_file = "citation.log"

dir_path = scholar.parse_args()
citation_log_file=dir_path+"/"+citation_log_file
blinks = scholar.get_daily_diff(citation_log_file)

print("BLINKING #", blinks, " Times")