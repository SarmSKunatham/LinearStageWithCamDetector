from gpiozero import PWMLED, LED
from time import sleep
DIR1_PIN = 16
STEP1_PIN = 20
EN1_PIN = 21
# Stepper Motor2 -> Rotate Camera
DIR2_PIN = 13
STEP2_PIN = 19
EN2_PIN = 26

DIR1 = LED(DIR1_PIN)
STEP1 = PWMLED(STEP1_PIN, frequency = 2500)
EN1 = LED(EN1_PIN)
DIR1.on()
EN1.off()

DIR2 = LED(DIR2_PIN)
STEP2 = PWMLED(STEP2_PIN, frequency = 1500)
EN2 = LED(EN2_PIN)
DIR2.on()
EN2.off()

STEP1.blink(on_time=0.001, off_time=0.001, fade_in_time=0, fade_out_time=0, n=None, background=True) # Stepper motor pwm pulse
STEP2.blink(on_time=0.001, off_time=0.001, fade_in_time=0, fade_out_time=0, n=None, background=True) # Stepper motor pwm pulse 

EN1.on() # Stepper motor enable
EN2.on()
print('Start')

while True:
    DIR1.on()
    DIR2.on()
    print('move 1')
    sleep(2)
    DIR1.off()
    DIR2.off()
    print('move 2')
    sleep(2)