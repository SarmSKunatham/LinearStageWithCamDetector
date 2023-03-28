from gpiozero import Button, LED, PWMLED
from time import sleep
import threading
# from rbgLight import setColor, stop_color
import warnings
warnings.filterwarnings('ignore')

# =====Declare pin names (BCM)=====
# Limit switches
LM_LEFT = 12
LM_RIGHT = 6
# Stepper Motor1 -> Slider
DIR1_PIN = 16
STEP1_PIN = 20
EN1_PIN = 21
# Stepper Motor2 -> Rotate Camera
DIR2_PIN = 13
STEP2_PIN = 19
EN2_PIN = 26

button1_pin = 24
button2_pin = 23
# RGB Colors
colors = [0xFF0000, 0x00FF00, 0x0000FF]
# =================================

# =====Initialize GPIO pins=====
# Buttons
button1 = Button(button1_pin)
button2 = Button(button2_pin)
# Limit switches
LM_Button_left = Button(LM_LEFT)
LM_Button_right = Button(LM_RIGHT)

# Stepper Motor1 -> Slider
DIR1 = LED(DIR1_PIN)
STEP1 = PWMLED(STEP1_PIN, frequency=800)
EN1 = LED(EN1_PIN)
EN1.on()
# STEP1.blink(on_time=0.001, off_time=0.001, fade_in_time=0, fade_out_time=0, n=None, background=True) # Stepper motor pwm pulse
EN1.on() # Stepper motor enable

# Stepper Motor2 -> Rotate Camera
DIR2 = LED(DIR2_PIN)
STEP2 = PWMLED(STEP2_PIN, frequency=100)
EN2 = LED(EN2_PIN)
EN2.off()
# STEP2.blink(on_time=0.01, off_time=0.01, fade_in_time=0, fade_out_time=0, n=None, background=True) # Stepper motor pwm pulse
# EN2.on() # Stepper motor enable
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
    STEP1.blink(on_time=0.001, off_time=0.001, fade_in_time=0, fade_out_time=0, n=None, background=True)
    DIR1.off()
    print('Slider moving left')
def move_slider_right():
    STEP1.blink(on_time=0.001, off_time=0.001, fade_in_time=0, fade_out_time=0, n=None, background=True)
    DIR1.on()
    print('Slider moving right')
def tilt_camera_up():
    STEP2.blink(on_time=0.05, off_time=0.05, fade_in_time=0, fade_out_time=0, n=None, background=True)
    DIR2.on()
    EN2.on()
    print('Camera tilting up')
    
def tilt_camera_down():
    STEP2.blink(on_time=0.05, off_time=0.05, fade_in_time=0, fade_out_time=0, n=None, background=True)
    DIR2.off()
    EN2.off()
    print('Camera tilting down')
    

def stop_slider():
    EN1.off()
    DIR1.off()
    STEP1.off()
    print('stop slider')
def stop_camera():
    STEP2.off()
    print('stop camera')
    

def move_slider_thread():
    try:
        while True:
            if LM_Button_right.is_pressed:
                move_slider_left()
            elif LM_Button_left.is_pressed:
#                 move_slider_right()
                stop_slider()
                sleep(1)
                move_slider_right()
            sleep(0.1)
    except:
        EN1.off()
        EN2.off()
        print('Stepper motors disabled')

def tilt_camera_thread():
    try:
        while True:
            tilt_camera_up()
            tilt_camera_down()
    except:
        EN1.off()
        EN2.off()
        print('Stepper motors disabled')
def button_print_thread():
    while True:
        if button1.is_pressed:
            print('Button 1 is pressed')
        if button2.is_pressed:
            print('Button 2 is pressed')
        sleep(0.3)

# ===============================
print('Setup complete!')


    
# if __name__ == '__main__':
#     move_slider_thread = threading.Thread(target=move_slider_thread)
#     tilt_camera_thread = threading.Thread(target=tilt_camera_thread)
#     button_print_thread = threading.Thread(target=button_print_thread)
#     move_slider_thread.start()
#     tilt_camera_thread.start()
#     button_print_thread.start()







