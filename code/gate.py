import pycom
from machine import Pin
from machine import PWM
import time
from dth import DTH

#Pins op het motor control board
enableA = "P12"
enableB = "P7"
in1 = "P11"
in2 = "P10"
in3 = "P9"
in4 = "P8"

#snelheid variable van 1 tot 100
speed = 100



#initialiseer alle pins van de pycom
enable_gate =   Pin(enableA, mode=Pin.OUT)
gate_open =     Pin(in1, mode=Pin.OUT)
gate_close =    Pin(in2, mode=Pin.OUT)

enable_fan =   Pin(enableB, mode=Pin.OUT)
fan_1 = Pin(in3, mode=Pin.OUT)
fan_2 = Pin(in4, mode=Pin.OUT)

#maak een pwm aan met timer 0 & frequentie van 5KHz
pwm = PWM(0, frequency=5000)

#creer een pwm kaneel op pin enableA met een duty cycle van 0
#gate_speed = pwm.channel(0, pin=enableA, duty_cycle=0)
fan_speed = pwm.channel(0, pin=enableB, duty_cycle=0)
def main():
    fan_1.value(1)
    #enable_fan.value(1)
    fan_speed.duty_cycle(0)
    while True:
        th = DTH('P22',1)
        result = th.read()
        if result.is_valid():
            print('Temperature: {:3.2f}'.format(result.temperature/1.0))
            print('Humidity: {:3.2f}'.format(result.humidity/1.0))


    '''
    open_gate(speed)
    time.sleep(5)
    close_gate(speed)
    '''

'''
def open_gate(speed=100):
    gate_open.value(1)
    gate_speed.duty_cycle(speed/100)
    time.sleep(5) #hoelang het duurt om de poort open te doen
    stop_gate()

def close_gate(speed=100):
    gate_close.value(1)
    gate_speed.duty_cycle(speed/100)
    time.sleep(5) #hoelang het duurt om de poort dicht te doen
    stop_gate()


def stop_gate():
    gate_speed.duty_cycle(0)
    gate_close.value(0)
    gate_open.value(0)
'''

if __name__ == "__main__":
    main()
