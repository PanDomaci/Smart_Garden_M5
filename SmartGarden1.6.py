from m5stack import *
from m5ui import *
from uiflow import *
import time
import unit
import urequests
import json
import wifiCfg

setScreenColor(15)
Watering_0 = unit.get(unit.WATERING, unit.PORTB)
relay4_0 = unit.get(unit.RELAY4, unit.PORTA)
dlight_0 = unit.get(unit.DLIGHT, (19,18))

relay4_0.set_mode(1)
dlight_0.set_mode(0x10)
LuxSource = int
MoistureNumber = int
LampState = str
TimeNow = str
Temp = float
Hum = float
Baterie = str #stav baterie
SSID = '' #WiFi SSID pro login
HESLO = '' #WiFi heslo 



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
wifiCfg.doConnect(SSID, HESLO) # připojení k síti WiFi SSID+heslo 


wait(1)
label20.setText(str(wifiCfg.wlan_sta.ifconfig()))
lcd.show()

while True:
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

  
  Baterie = bat.voltage()
  label26.setText(str(Baterie))
  
  if MoistureNumber > 1900:
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
    req = urequests.request(method='GET', url='https://api.thingspeak.com/update?api_key=XXX&field1='+str(LuxSource)+'&field2='+str(MoistureNumber)+'&field3='+str(Hum)+'&field4='+str(Temp)+'&field5='+str(Baterie))
    label24.setText('succeeded')
    print(req.text)
  except:
    label24.setText('failed')


  lcd.show()
  wait(518)
  wait_ms(250)
  wait_ms(2)
