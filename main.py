from gpiozero import Button, LED, PWMLED
from time import sleep
import threading
from rbgLight import setColor, stop_color
import warnings
warnings.filterwarnings('ignore')

# =====Declare pin names (BCM)=====
# Limit switches
LM_LEFT = 6
LM_RIGHT = 12
# Stepper Motor1 -> Slider
DIR1_PIN = 16
STEP1_PIN = 20
EN1_PIN = 21
# Stepper Motor2 -> Rotate Camera
DIR2_PIN = 13
STEP2_PIN = 19
EN2_PIN = 26
# RGB Colors
colors = [0xFF0000, 0x00FF00, 0x0000FF]
# =================================

# =====Initialize GPIO pins=====
# Limit switches
LM_Button_left = Button(LM_LEFT)
LM_Button_right = Button(LM_RIGHT)
# Stepper Motor1 -> Slider
DIR1 = LED(DIR1_PIN)
STEP1 = PWMLED(STEP1_PIN, frequency=100)
EN1 = LED(EN1_PIN)
STEP1.blink(on_time=1, off_time=1, fade_in_time=0, fade_out_time=0, n=None, background=True) # Stepper motor pwm pulse
EN1.on() # Stepper motor enable
# Stepper Motor2 -> Rotate Camera
DIR2 = LED(DIR2_PIN)
STEP2 = PWMLED(STEP2_PIN, frequency=100)
EN2 = LED(EN2_PIN)
STEP2.blink(on_time=1, off_time=1, fade_in_time=0, fade_out_time=0, n=None, background=True) # Stepper motor pwm pulse
EN2.off() # Stepper motor enable
# ===============================

# =====Initialize Functions=====
def LM_left_pressed():
    if LM_Button_left.is_pressed:
        print('LM left is pressed!')
        return True
    return False
def LM_right_pressed():
    if LM_Button_right.is_pressed:
        print('LM right is pressed!')
        return True
    return False
def move_slider_left():
    DIR1.off()
    print('Slider moving left')
def move_slider_right():
    DIR1.on()
    print('Slider moving right')
def tilt_camera_up():
    EN2.on()
    DIR2.on()
    print('Camera tilting up')
    sleep(3)
    EN2.off()
def tilt_camera_down():
    EN2.on()
    DIR2.off()
    print('Camera tilting down')
    sleep(3)
    EN2.off()
def move_slider_thread():
    try:
        while True:
            if LM_left_pressed():
                move_slider_left()
            if LM_right_pressed():
                move_slider_right()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        EN1.off()
        EN2.off()
        print('Stepper motors disabled')
def tilt_camera_thread():
    try:
        while True:
            tilt_camera_up()
            tilt_camera_down()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        EN1.off()
        EN2.off()
        print('Stepper motors disabled')
def change_color_thread():
    try:
        while True:
            for color in colors:
                setColor(color)
                sleep(3)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        stop_color()
        print('RGB LED turned off')
# ===============================
print('Setup complete!')

if __name__ == '__main__':
    move_slider_thread = threading.Thread(target=move_slider_thread)
    tilt_camera_thread = threading.Thread(target=tilt_camera_thread)
    change_color_thread = threading.Thread(target=change_color_thread)
    move_slider_thread.start()
    tilt_camera_thread.start()
    change_color_thread.start()






