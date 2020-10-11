import pycom
import time
from machine import Pin
from machine import PWM
from dth import DTH
from hx711 import HX711


#GPIO pins van de pycom

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

led_pin_1 = "P21"
led_pin_2 = "P20"
led_pin_3 = "P19"

#Constanten
#max temperatuur voordat de ventilator aangaat
TRESHOLD_TEMP = 24
#"gewicht" van één ei
EGG_WEIGHT = 21000
#het aantal eieren
EGG_COUNT = 0

#initialiseer alle pins van de motor controller
enable_gate = Pin(enableA, mode=Pin.OUT)
gate_open = Pin(in2, mode=Pin.OUT)
gate_close = Pin(in1, mode=Pin.OUT)

enable_fan = Pin(enableB, mode=Pin.OUT)
fan_1 = Pin(in3, mode=Pin.OUT)
fan_2 = Pin(in4, mode=Pin.OUT)


#leds
led_1 = Pin(led_pin_1, mode=Pin.OUT)
led_2 = Pin(led_pin_2, mode=Pin.OUT)
led_3 = Pin(led_pin_3, mode=Pin.OUT)
led_1.value(0)
led_2.value(0)
led_3.value(0)


#schakelaar voor de poort open te doen
switch = Pin(switch_pin, mode = Pin.IN)
switch_value = switch.value()

#load cell amplifier
load_amplifier = HX711(data_pin, clk_pin)
current_weight = 0

#dht sensor object aanmaken
dht_sensor = DTH(dht_pin,1)


def main():
    gate_is_open = False
    while True:
        check_temperature()
        load_init()
        if(switch_changed()):
            if(gate_is_open):
                close_gate()
                gate_is_open = False
            elif(not gate_is_open):
                open_gate()
                gate_is_open = True
        check_eggs()



#regelt de leds op basis van het aantal eieren
#maakt gebruik van bitshifting om het aantal eieren in binair om te zetten
def update_egg_counter():
    global EGG_COUNT
    led_1.value(((EGG_COUNT >> 0) % 2))
    led_2.value(((EGG_COUNT >> 1) % 2))
    led_3.value(((EGG_COUNT >> 2) % 2))

#geeft het huidige gewicht terug op basis van een gemiddelde van verschillende metingen
def get_weight():
    global load_amplifier
    readings = []
    for i in range(10):
        readings.append(load_amplifier.get_value())
    average = (sum(readings) / len(readings))
    return average

#stelt het huidige gewicht in
def load_init():
    global current_weight
    current_weight = get_weight()

#geeft het verschil in gewicht terug
def get_weight_difference():
    global current_weight
    old_weight = current_weight
    current_weight = get_weight()
    return (old_weight - current_weight)


#probeert het aantal eieren te berekenen op basis van het verschil in gewicht
#omdat niet alle eieren hetzelfde wegen rekenen we rekenen we ook met een marge van 15%
def check_eggs():
    global EGG_COUNT
    diff = get_weight_difference()
    abs_diff = abs(diff)
    quotient = abs_diff / EGG_WEIGHT
    eggs = int(quotient)
    remainder = quotient - eggs
    if (remainder >= 0.85):
        eggs = eggs + 1
    if(diff > 0):
        EGG_COUNT = EGG_COUNT + eggs
    if(diff <= 0):
        EGG_COUNT = EGG_COUNT - eggs
    update_egg_counter()


#kijkt of de waarde van de switch verandert is sinds de vorige keer
def switch_changed():
    global switch_value
    old_value = switch_value
    switch_value = switch.value()
    if(old_value == switch_value):
        return False
    else:
        return True

#leest de temperatuur van de dht sensor
def get_temperature():
    global dht_sensor
    result = dht_sensor.read()
    if result.is_valid():
        temperature = result.temperature
        return temperature
    else:
        return None

#kijkt of de temperatuur te hoog is en zet dan de ventilator aan
def check_temperature():
    temp = get_temperature()
    if(temp is not None):
        if(temp >= TRESHOLD_TEMP):
            start_fan()
        else:
            stop_fan()

#start de ventilator
def start_fan():
    fan_2.value(1)
    fan_1.value(0)
    enable_fan.value(0)

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
