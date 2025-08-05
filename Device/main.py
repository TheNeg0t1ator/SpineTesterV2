from machine import Pin
from hx711_multi import HX711
import time

# Initialize both sensors with unique state machines
hx1 = HX711(clock_pin=4, data_pin=5, sm_id=0)  # Sensor 1
hx2 = HX711(clock_pin=3, data_pin=2, sm_id=1)  # Sensor 2

# Calibration sequence
for hx in [hx1, hx2]:
    hx.set_gain(128)  # Set gain to 128
    time.sleep_ms(500)  # Stabilization time

try:
    while True:
        # Read both sensors
        val1 = hx1.read()
        val2 = hx2.read()
        
        # Print results
        print(f"A: {val1:>8} | B: {val2:>8}")
        time.sleep_ms(100)  # Adjust sampling rate
        
except KeyboardInterrupt:
    hx1.close()
    hx2.close()
    print("Sensors closed")