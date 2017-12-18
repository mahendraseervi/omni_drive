import RPi.GPIO as GPIO
import time

en_a = 23
en_b = 24
Motor_R1 = 16
Motor_R2 = 12
Motor_pwm = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(en_a, GPIO.IN)
GPIO.setup(en_b, GPIO.IN)
GPIO.setup(Motor_R1, GPIO.OUT)
GPIO.setup(Motor_R2, GPIO.OUT)
GPIO.setup(Motor_pwm, GPIO.OUT)

p = GPIO.PWM(Motor_pwm, 50)
p.start(0)


def destroy():
    GPIO.output(Motor_R1,GPIO.LOW)
    GPIO.output(Motor_R2,GPIO.LOW)
    GPIO.cleanup()  # Release resource

def stop_pos():          # used to stop the motor
    GPIO.output(Motor_R1,GPIO.LOW)
    GPIO.output(Motor_R2,GPIO.LOW)

def deg_to_count(degree):        # used to convert degree to count values
    cnt = ((1536 * degree)/360)
    return cnt


def counter():
    count = 0
    last_en_a = GPIO.input(en_a)

    while(1):

        print ('Enter the degree value : ')
        degree = raw_input()
        in_value = deg_to_count(int(degree))

        # in_value = 1536    # set count value
        cle = 2    # extra clearence value
        cnt = 0
        while(1):

            if count > in_value + cle:
                p.ChangeDutyCycle(100)
                GPIO.output(Motor_R1,GPIO.HIGH)
                GPIO.output(Motor_R2,GPIO.LOW)

            elif count < in_value - cle:
                p.ChangeDutyCycle(100)
                GPIO.output(Motor_R1,GPIO.LOW)
                GPIO.output(Motor_R2,GPIO.HIGH)

            elif count >= (in_value-cle) or count <= (in_value+cle):
                stop_pos()
                cnt = cnt + 1

                if cnt > 30:
                    print('break')
                    break


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
