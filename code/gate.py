import pycom
from machine import Pin
from machine import PWM
import time

#Pins op het motor control board
enableA = "P12"
enableB = "P9"
in1 = "P11"
in2 = "P10"
in3 = ""
in4 = ""

#snelheid variable van 1 tot 100
speed = 100



#initialiseer alle pins van de pycom
enable_gate =   Pin(enableA, mode=Pin.OUT)
gate_open =     Pin(in1, mode=Pin.OUT)
gate_close =    Pin(in2, mode=Pin.OUT)

enable_fan =   Pin(enableB, mode=Pin.OUT)

#maak een pwm aan met timer 0 & frequentie van 5KHz
pwm = PWM(0, frequency=5000)

#creer een pwm kaneel op pin enableA met een duty cycle van 0
gate_speed = pwm.channel(0, pin=enableA, duty_cycle=0)

def main():
    open_gate(speed)
    time.sleep(5)
    close_gate(speed)


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


if __name__ == "__main__":
    main()
