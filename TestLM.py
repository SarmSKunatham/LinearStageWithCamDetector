from gpiozero import Button
import time
right_button = Button(6)
left_button = Button(12)

print(left_button.is_pressed)
print(right_button.is_pressed)
print(right_button.is_pressed)
print(right_button.is_pressed)
print(right_button.is_pressed)
# time.sleep(3)
print(right_button.is_pressed)


while True:
    if right_button.is_pressed:
        print('right is pressed')
    elif left_button.is_pressed:
        print('left is pressed')
    time.sleep(0.3)
    