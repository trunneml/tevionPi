#!/usr/bin/env python2
import wiringpi2
import datetime


wiringpi2.wiringPiSetup()

HOUSE_CODE = (77, 42, 170)

SEND_PIN = 1
OUTPUT_MODE = 1

wiringpi2.pinMode(SEND_PIN, OUTPUT_MODE)


class TevionCode(object):

    _delta_long = 1200
    _delta_short = 600

    def __init__(self, house_code, pin):
        self.set_house_code(house_code)
        self.pin = pin
        self.pin_value = 0
        self.toggles = 0
        self.duration = 0

    def _toggle_pin_value(self):
        if self.pin_value == 1:
            self.pin_value = 0
        else:
            self.pin_value = 1
        return self.pin_value

    def _send_bit(self, value):
        wiringpi2.digitalWrite(self.pin, self._toggle_pin_value())
        if value:
            wiringpi2.delayMicroseconds(int(self._delta_long*0.8))
            self.duration += self._delta_long
        else:
            wiringpi2.delayMicroseconds(int(self._delta_short*0.8))
            self.duration += self._delta_short
        self.toggles += 1

    def set_house_code(self, house_code):
        h = []
        for n in house_code:
            h.extend(self._bitfield(n))
        h.append(1) # Parity hack!?!
        self._house_code = h
        
    def _bitfield(self, n):
        return [1 if digit=='1' else 0 for digit in '{0:08b}'.format(n)]
    
    def _send_house_code(self):
        for h in self._house_code:
            self._send_bit(h)
    
    def send_code(self, code):
        self._send_house_code()
        for c in code:
            for bit in self._bitfield(c):
                self._send_bit(bit)

tevion = TevionCode(HOUSE_CODE, SEND_PIN)
start_time = datetime.datetime.now()
for _i in range(10):
    tevion.send_code((86, 86))

for _i in range(10):
    tevion.send_code((85, 85))

print (datetime.datetime.now() - start_time)
print tevion.duration
print tevion.toggles
