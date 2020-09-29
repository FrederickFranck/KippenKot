from machine import ADC
adc = ADC(0)
adc_1 = adc.channel(pin='P13')
adc_2 = adc.channel(pin='P14')
adc_1()
adc_2()


while(True):
    print(adc_1.value())
    print(adc_2.value())
