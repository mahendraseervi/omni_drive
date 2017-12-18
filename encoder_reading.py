import RPi.GPIO as GPIO
import time

en_a = 23
en_b = 24

GPIO.setmode(GPIO.BCM)

GPIO.setup(en_a, GPIO.IN)
GPIO.setup(en_b, GPIO.IN)


def destroy():
    GPIO.output(en_a,GPIO.LOW)
    GPIO.output(en_b,GPIO.LOW)
    GPIO.cleanup()                     # Release resource


def counter():
    count = 0
    last_en_a = GPIO.input(en_a)
    while(1):
        state_en_a = GPIO.input(en_a)

        if state_en_a != last_en_a:
            if GPIO.input(en_b) != state_en_a:
                count = count + 1
            else:
                count = count - 1

            print(count)

        last_en_a = state_en_a


if __name__ == '__main__':

    try:
        counter()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
