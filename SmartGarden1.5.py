from m5stack import *
from m5ui import *
from uiflow import *
import time
import unit
import urequests
import json
import wifiCfg
import machine


setScreenColor(15)
Watering_0 = unit.get(unit.WATERING, unit.PORTB)  #definice na kterých pinech je připojen modul WATERING unit (vodní čerpadlo s kapacitním měřením vlhkosti půdy)
relay4_0 = unit.get(unit.RELAY4, unit.PORTA)  #definované piny pro 4 - Relay unit (4 relé)
dlight_0 = unit.get(unit.DLIGHT, (19,18)) #napevno nastavené piny pro HAT DLight modul (senzor úrovně osvětlení)

relay4_0.set_mode(1) #synchronizované LED s relé - svítí = zapnuto 
dlight_0.set_mode(0x10) #režim snímání zdroje světla
LuxSource = float #hodnota, kterou vrací HAT Dlight senzor
MoistureNumber = float  #hodnota vlhkosti, kterou vrací WATERING unit
LampState = str #stav lampy 
TimeNow = str #časová hodnota, kterou vrací RTC čip
Temp = float  #teplota z integrovaného SHT30 senzoru
Hum = float #relativní vlhkost vracená SHT30 senzorem
Baterie = str #stav baterie
sleeptime = 10*60*1000*1000 #proměnná pro dobu hlubokého spánku (10minut)

def prumerTeplot(seznamTeplot): #definice funkce, která zprůměruje naměřené hodnoty ze seznamu (list) "seznamTeplot", který je zde jako parametr dané funkce
  pocet = 0
  soucet = 0.0
  for n in seznamTeplot:
    soucet += n
    pocet += 1 
  prumerTeplot = soucet / pocet
  prumerTeplot = float("%.2f" % round(prumerTeplot, 2))
  return prumerTeplot
  
def prumerHum(seznamHum): #definice funkce, která zprůměruje naměřené hodnoty ze seznamu (list) "seznamHum", který je zde jako parametr dané funkce
  pocet = 0
  soucet = 0.0
  for n in seznamHum:
    soucet += n
    pocet += 1 
  prumerHum = soucet / pocet
  prumerHum = float("%.2f" % round(prumerHum, 2))
  return prumerHum

def prumerVlhkosti(seznamHodnotVlhkosti): #definice funkce, která zprůměruje naměřené hodnoty ze seznamu (list) "seznamHodnotVlhkosti", který je zde jako parametr dané funkce
  pocet = 0
  soucet = 0.0
  for n in seznamHodnotVlhkosti:
    soucet += n
    pocet += 1 
  prumerVlhkosti = soucet / pocet
  prumerVlhkosti = float("%.2f" % round(prumerVlhkosti, 2))
  return prumerVlhkosti  

def prumerLUX(seznamLUX): #definice funkce, která zprůměruje naměřené hodnoty ze seznamu (list) "seznamLUX", který je zde jako parametr dané funkce
  pocet = 0
  soucet = 0.0
  for n in seznamHodnotLUX:
    soucet += n
    pocet += 1 
  prumerLUX = soucet / pocet
  prumerLUX = float("%.2f" % round(prumerLUX, 2))
  return prumerLUX

def seznamTeplot(): #funkce, která provede 20x měření teploty ze senzoru SHT30 a každý výsledek měření zanese do seznamu 
 
  Temp = 0.00
  seznamTeplot = []
  
  for i in range(20):
    Temp = sht30.temperature
    seznamTeplot.append(Temp)
    wait(1)
  
  return seznamTeplot
  
def seznamHum():  #funkce, která provede 20x měření relativní vlhkosti ze senzoru SHT30 a každý výsledek měření zanese do seznamu 
 
  Hum = 0.00
  seznamHum = []
  
  for i in range(20):
    Hum = sht30.humidity
    seznamHum.append(Hum)
    wait(1)
  
  return seznamHum
  
def seznamHodnotVlhkosti(): #funkce, která provede 20x měření vlhkosti z kapacitního senzoru WATERING unit a každý výsledek měření zanese do seznamu 
 
  vlhkost = 0.00
  seznamHodnotVlhkosti = []
  
  for i in range(20):
    vlhkost = Watering_0.get_adc_value()
    seznamHum.append(vlhkost)
    wait(1)
  
  return seznamHodnotVlhkosti

def seznamLUX():  #funkce, která provede 20x měření úrovně osvětlení HAT Dlight senzorem a každý výsledek měření zanese do seznamu
 
  LUX = 0.00
  seznamLUX = []
  
  for i in range(20):
    LUX = dlight_0.get_lux()
    seznamLUX.append(LUX)
    wait(1)
  
  return seznamLUX
  

label0 = M5TextBox(27, 20, "LUX: ", lcd.FONT_DejaVu24, 0, rotate=0)
label1 = M5TextBox(184, 20, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label2 = M5TextBox(27, 68, "Humidity: ", lcd.FONT_DejaVu24, 0, rotate=0)
label3 = M5TextBox(184, 68, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label4 = M5TextBox(27, 116, "Watering: ", lcd.FONT_DejaVu24, 0, rotate=0)
label5 = M5TextBox(184, 116, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label6 = M5TextBox(27, 203, "Relay Stat: ", lcd.FONT_DejaVu24, 0, rotate=0)
label7 = M5TextBox(184, 170, "1", lcd.FONT_DejaVu24, 0, rotate=0)
label8 = M5TextBox(266, 170, "2", lcd.FONT_DejaVu24, 0, rotate=0)
label9 = M5TextBox(355, 170, "3", lcd.FONT_DejaVu24, 0, rotate=0)
label10 = M5TextBox(436, 170, "4", lcd.FONT_DejaVu24, 0, rotate=0)
label11 = M5TextBox(184, 203, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label12 = M5TextBox(266, 203, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label13 = M5TextBox(355, 203, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label14 = M5TextBox(436, 203, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label15 = M5TextBox(33, 256, "Air Humidity: ", lcd.FONT_DejaVu24, 0, rotate=0)
label16 = M5TextBox(205, 255, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label17 = M5TextBox(33, 304, "Temperature: ", lcd.FONT_DejaVu24, 0, rotate=0)
label18 = M5TextBox(205, 304, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label19 = M5TextBox(33, 350, "IP Address: ", lcd.FONT_DejaVu24, 0, rotate=0)
label20 = M5TextBox(190, 350, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label21 = M5TextBox(33, 400, "Time", lcd.FONT_DejaVu24, 0, rotate=0)
label22 = M5TextBox(150, 400, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label23 = M5TextBox(33, 450, "HTTP stat: ", lcd.FONT_DejaVu24, 0, rotate=0)
label24 = M5TextBox(200, 450, "Text", lcd.FONT_DejaVu24, 0, rotate=0)
label25 = M5TextBox(33, 480, "Battery", lcd.FONT_DejaVu24, 0, rotate=0)
label26 = M5TextBox(200, 480, "Text", lcd.FONT_DejaVu24, 0, rotate=0)


#rtc.set_datetime((23, 3, 3, 5, 13, 06, 30)) # nastavení RTC čipu (nutné pouze při úplném vybití baterie)
wifiCfg.doConnect('SSID', 'PASSWORD') # připojení k síti WiFi SSID+heslo 


wait(1) #počká 1s po připojení k wifi
label20.setText(str(wifiCfg.wlan_sta.ifconfig())) #vypíše údaje o síti - vlastní adresu, bránu, adresu sítě, masku 
lcd.show()  #funkce displeje - vyvolá změnu obrazu displeje 

while True: #nekonečný cyklus (loop)
  
  LuxSource = dlight_0.get_lux()
  label1.setText(str(LuxSource))
  
  TimeNow = rtc.datetime()
  label22.setText(str(TimeNow))
  
  Temp = sht30.temperature
  label18.setText(str(Temp))
  
  Hum = sht30.humidity
  label16.setText(str(Hum))
  
  MoistureNumber = Watering_0.get_adc_value()
  label3.setText(str(MoistureNumber))

  baterie = str(map_value((bat.voltage() / 1000), 3.2, 4.3, 0, 100)) + '%'
  label26.setText(baterie)
  
  print((str('Water: ') + str((Watering_0.get_adc_value()))))
  if (MoistureNumber) > 1890:
    Watering_0.set_pump_status(1)
    label5.setText("YES")
    lcd.show()
    wait(5)
    Watering_0.set_pump_status(0)
    label5.setText("NO")
    lcd.show()
  else:
    Watering_0.set_pump_status(0)
    label5.setText("NO")
  if LuxSource < 200:
    relay4_0.set_relay_status(4, 1)
    label14.setText("ON")
    lcd.show()
  else:
    relay4_0.set_relay_status(4, 0)
    label14.setText("OFF")
    lcd.show()
  try:
    req = urequests.request('thingspeak REST API + key')
    label24.setText('succeeded')
    print(req.text)
  except:
    label24.setText('failed')


  
  lcd.show()
  wait(10)
  wait_ms(250)
  wait_ms(2)
