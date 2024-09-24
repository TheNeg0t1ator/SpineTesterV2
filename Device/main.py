import machine
from hx711 import HX711 as fs

hx = fs(machine.Pin(2), machine.Pin(3), 128)

hx2 = fs(machine.Pin(4), machine.Pin(5), 128)
while True:
    print("A",hx.read(), "B",hx2.read())