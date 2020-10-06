import pycom
from machine import Pin
from machine import PWM
import time
from dth import DTH
from hx711 import HX711


#Pins op het motor control board
enableA = "P12"
enableB = "P7"
in1 = "P11"
in2 = "P10"
in3 = "P9"
in4 = "P8"
dht_pin = "P22"
data_pin = "P6"
clk_pin = "P5"
switch_pin = "P13"

#snelheid variable van 1 tot 100
speed = 100



#initialiseer alle pins van de pycom
enable_gate =   Pin(enableA, mode=Pin.OUT)
gate_open =     Pin(in2, mode=Pin.OUT)
gate_close =    Pin(in1, mode=Pin.OUT)

enable_fan =   Pin(enableB, mode=Pin.OUT)
fan_1 = Pin(in3, mode=Pin.OUT)
fan_2 = Pin(in4, mode=Pin.OUT)


switch = Pin(switch_pin, mode = Pin.IN)


#maak een pwm aan met timer 0 & frequentie van 5KHz
pwm = PWM(0, frequency=5000)

#creer een pwm kaneel op pin enableA met een duty cycle van 0
gate_speed = pwm.channel(0, pin=enableA, duty_cycle=0)
fan_speed = pwm.channel(0, pin=enableB, duty_cycle=0)



load_amp = HX711(data_pin, clk_pin)
#load_amp.tare()
weight_offset = 969850

def main():
    isOpen = False
    while True:
        #print("started")
        if(switch.value() and isOpen):
            print("gate is closing")
            close_gate()
            isOpen = False
        elif(switch.value() and (not isOpen)):
            print("gate is opening")
            open_gate()
            isOpen = True

        print(load_amp.get_value() + weight_offset )

    #read_dht()
    #gewicht.append(load_amp.get_value())

    #print(switch.value())

def weight():
    while True:
        time.sleep(5)
        first = load_amp.get_value() + 87000
        print("go")
        time.sleep(5)
        second = load_amp.get_value() + 87000
        print("off")
        time.sleep(5)
        diff = first - second
        print("gewicht   {}".format(diff/1500))


def read_load_cell():
    value = hx711.read()
    value = hx711.get_value()
    print(value)
    print("ok")


def read_dht():
    th = DTH(dht_pin,1)
    result = th.read()
    if result.is_valid():
        print('Temperature: {:3.2f}'.format(result.temperature/1.0))
        print('Humidity: {:3.2f}'.format(result.humidity/1.0))
    else:
        print("Invalid Result")

def start_fan():
    fan_2.value(0)
    fan_1.value(1)
    enable_fan.value(1)

def stop_fan():
    enable_fan.value(0)
    fan_2.value(0)
    fan_1.value(0)


def open_gate():
    gate_open.value(1)
    time.sleep(44) #hoelang het duurt om de poort open te doen
    stop_gate()

def close_gate():
    gate_close.value(1)
    time.sleep(41) #hoelang het duurt om de poort dicht te doen
    stop_gate()


def stop_gate():
    enable_gate.value(0)
    gate_close.value(0)
    gate_open.value(0)

if __name__ == "__main__":
    main()
