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
    GPIO.output(Motor_pwm,GPIO.LOW)
    GPIO.cleanup()  # Release resource

def stop_pos():          # used to stop the motor
    GPIO.output(Motor_R1,GPIO.LOW)
    GPIO.output(Motor_R2,GPIO.LOW)
    # GPIO.output(Motor_pwm,GPIO.LOW)


def deg_to_count(degree):        # used to convert degree to count values
    cnt = ((1536 * degree)/360)
    return cnt


def counter():
    absolute_count = 0
    count = 0
    last_en_a = GPIO.input(en_a)
    last_degree_value = 0

    while(1):
        absolute_count = absolute_count + count
        breaker = False
        print(absolute_count,count)
        print ('Enter the degree value : ')
        degree = raw_input()
        in_value = deg_to_count(int(degree))
        in_value = in_value-absolute_count

        # in_value = 1536    # set count value
        cle = 0    # extra clearence value
        cnt = 0
        count = 0
        if last_degree_value != degree:
            ramp_up = int((in_value * 0.2))
            ramp_middle = int((in_value * 0.8))
            ramp_down = int((in_value * 1))
            print(ramp_up,ramp_middle,ramp_down,count,absolute_count)

            last_degree_value = degree

        else:
            breaker = True



        while(1):
            if breaker == True:
                break

        ################# clock wise rotation(with ramp up down) #####################

            elif ((count < in_value - cle) and cnt < 1):

                if (count <= ramp_up):
                    if count == 0:
                        p.ChangeDutyCycle(10)
                        GPIO.output(Motor_R1,GPIO.LOW)
                        GPIO.output(Motor_R2,GPIO.HIGH)

                    # print('first loop')
                    temp_up = count
                    # print(temp_up)
                    temp_up = (abs((temp_up * (100.0/ramp_up))/2))
                    p.ChangeDutyCycle(temp_up)
                    GPIO.output(Motor_R1,GPIO.LOW)
                    GPIO.output(Motor_R2,GPIO.HIGH)

                elif ((count <= ramp_middle) and (count > ramp_up)):
                    # print('second loop')
                    p.ChangeDutyCycle(100)
                    GPIO.output(Motor_R1,GPIO.LOW)
                    GPIO.output(Motor_R2,GPIO.HIGH)

                elif ((count <= ramp_down) and (count > ramp_middle)):
                    # print('third loop')
                    temp_down = count - ramp_middle
                    temp_down = abs((temp_down * (100.0/(ramp_down-ramp_middle)))/2)
                    p.ChangeDutyCycle(50 - temp_down)
                    GPIO.output(Motor_R1,GPIO.LOW)
                    GPIO.output(Motor_R2,GPIO.HIGH)

        ################### Anti clock wise rotation(with ramp up down) ######################

            elif ((count > in_value + cle) and cnt < 1):

                if (count >= ramp_up):
                    if count == 0:
                        p.ChangeDutyCycle(10)
                        GPIO.output(Motor_R1,GPIO.HIGH)
                        GPIO.output(Motor_R2,GPIO.LOW)

                    # print('first loop')
                    temp_up = count
                    temp_up = abs((temp_up * (100.0/ramp_up))/2)
                    p.ChangeDutyCycle(temp_up)
                    GPIO.output(Motor_R1,GPIO.HIGH)
                    GPIO.output(Motor_R2,GPIO.LOW)

                elif ((count >= ramp_middle) and (count < ramp_up)):
                    # print('second loop')
                    p.ChangeDutyCycle(100)
                    GPIO.output(Motor_R1,GPIO.HIGH)
                    GPIO.output(Motor_R2,GPIO.LOW)

                elif ((count >= ramp_down) and (count < ramp_middle)):
                    # print('third loop')
                    temp_down = count - ramp_middle
                    temp_down = abs((temp_down * (100.0/(ramp_down-ramp_middle)))/2)
                    p.ChangeDutyCycle(50 - temp_down)
                    GPIO.output(Motor_R1,GPIO.HIGH)
                    GPIO.output(Motor_R2,GPIO.LOW)

        ########################## To stop the motor ##############################

            elif (count >= (in_value-cle) and count <= (in_value+cle)):
                # print('stop')
                stop_pos()
                cnt = cnt + 1
                # print(cnt)

                if cnt == 50:
                    break


        ####################### For stability #############################

            elif ((count < in_value - cle) and cnt > 1):
                print('first')
                p.ChangeDutyCycle(20)
                GPIO.output(Motor_R1,GPIO.LOW)
                GPIO.output(Motor_R2,GPIO.HIGH)

            elif ((count > in_value + cle) and cnt > 1):
                print('second')
                p.ChangeDutyCycle(20)
                GPIO.output(Motor_R1,GPIO.HIGH)
                GPIO.output(Motor_R2,GPIO.LOW)


        ######################### To count the encoder values  ############################

            state_en_a = GPIO.input(en_a)

            if state_en_a != last_en_a:
                if GPIO.input(en_b) != state_en_a:
                    count = count + 1
                else:
                    count = count - 1

                # print(count)
            last_en_a = state_en_a

    p.stop()



if __name__ == '__main__':

    try:
        counter()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
