from machine import Pin
import rp2
import time

class HX711:
    def __init__(self, clock_pin, data_pin, gain=128, sm_id=0):
        self.clock = Pin(clock_pin, Pin.OUT)
        self.data = Pin(data_pin, Pin.IN)
        self.clock.value(0)
        
        self.sm = rp2.StateMachine(sm_id, self.hx711_pio, 
                                  freq=1_000_000,
                                  sideset_base=self.clock,
                                  in_base=self.data,
                                  jmp_pin=self.data)
        self.sm.active(0)
        self.set_gain(gain)
        
    @rp2.asm_pio(
        sideset_init=rp2.PIO.OUT_LOW,
        in_shiftdir=rp2.PIO.SHIFT_LEFT,
        autopull=False,
        autopush=False
    )
    def hx711_pio():
        pull()              .side(0)   # Get clock cycles
        mov(x, osr)         .side(0)
        
        label("bitloop")
        nop()               .side(1)   # Clock high
        nop()               .side(1)   # Hold high
        in_(pins, 1)        .side(0)   # Clock low + read data
        jmp(x_dec, "bitloop").side(0)   # Loop for more bits
        
        push(block)         .side(0)   # Push result

    def set_gain(self, gain):
        if gain == 128:
            self.gain = 1
        elif gain == 64:
            self.gain = 3
        elif gain == 32:
            self.gain = 2
            
        # Reset sequence
        self.clock.value(1)
        time.sleep_us(60)
        self.clock.value(0)
        time.sleep_ms(1)

    def read(self):
        # Wait for data ready
        for _ in range(100):
            if not self.data.value():
                break
            time.sleep_us(100)
        else:
            raise OSError("Sensor not ready")
        
        # Start conversion
        self.sm.active(1)
        self.sm.put(self.gain + 24 - 1)  # 25-27 pulses
        result = self.sm.get() >> self.gain
        self.sm.active(0)
        
        # Handle negative values
        if result & 0x800000:
            result -= 0x1000000
            
        return result

    def close(self):
        self.sm.active(0)