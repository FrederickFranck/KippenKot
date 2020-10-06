import pycom
from machine import Pin
from machine import PWM
import time
from dth import DTH
from hx711 import HX711


#Pins op van de pycom
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


#initialiseer alle pins van de pycom
enable_gate =   Pin(enableA, mode=Pin.OUT)
gate_open =     Pin(in2, mode=Pin.OUT)
gate_close =    Pin(in1, mode=Pin.OUT)

enable_fan =   Pin(enableB, mode=Pin.OUT)
fan_1 = Pin(in3, mode=Pin.OUT)
fan_2 = Pin(in4, mode=Pin.OUT)

#schakelaar voor de poort open te doen
switch = Pin(switch_pin, mode = Pin.IN)

#maak een pwm aan met timer 0 & frequentie van 5KHz
pwm = PWM(0, frequency=5000)

#creer een pwm kaneel op pin enableA met een duty cycle van 0
gate_speed = pwm.channel(0, pin=enableA, duty_cycle=0)
fan_speed = pwm.channel(0, pin=enableB, duty_cycle=0)
#deze worden niet gebruikt want de motoren bewegen pas vanaf 90% duty cycle

#de load cell amplifier
load_amp = HX711(data_pin, clk_pin)

#wordt gebruikt om de load cell waarde op null te zetten
weight_offset = 969850

def main():
    #kijkt of de poort open of dicht is en sluit/opent deze als de schakelaar gebruikt wordt (zie video)
    gateIsOpen = False
    while True:
        if(switch.value() and gateIsOpen):
            print("gate is closing")
            close_gate()
            isOpen = False
        elif(switch.value() and (not gateIsOpen)):
            print("gate is opening")
            open_gate()
            isOpen = True

        #print(load_amp.get_value() + weight_offset )
        #read_dht()

#WIP
#functie om het gewicht te lezen van de load cell
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

#leest de waardes van dht en print deze
def read_dht():
    th = DTH(dht_pin,1)
    result = th.read()
    if result.is_valid():
        print('Temperature: {:3.2f}'.format(result.temperature/1.0))
        print('Humidity: {:3.2f}'.format(result.humidity/1.0))
    else:
        print("Invalid Result")

#start de ventilator
def start_fan():
    fan_2.value(0)
    fan_1.value(1)
    enable_fan.value(1)

#stopt de ventilator
def stop_fan():
    enable_fan.value(0)
    fan_2.value(0)
    fan_1.value(0)

#opent de poort
def open_gate():
    gate_open.value(1)
    time.sleep(44) #hoelang het duurt om de poort open te doen in seconden
    stop_gate()

#sluit de poort
def close_gate():
    gate_close.value(1)
    time.sleep(41) #hoelang het duurt om de poort dicht te doen in seconden
    stop_gate()

#stopt de motor die de poort aanstuurt
def stop_gate():
    enable_gate.value(0)
    gate_close.value(0)
    gate_open.value(0)

if __name__ == "__main__":
    main()
