#!/usr/bin/env python2
"""
Copyright (C) 2014, Michael Trunner

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of {{ project }} nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import argparse
import datetime
import wiringpi2
wiringpi2.wiringPiSetup()


class TevionCode(object):

    _delta_long = 1200
    _delta_short = 600

    WIRINGPI_OUTPUT_MODE = 1

    COMMAND_CODES = {
        0: {
            'on': (170, 85),
            'off': (169, 86),
            'brighter': (169, 154),
            'darker': (170, 153)
        },
        1: {
            'on': (86, 86),
            'off': (85, 85),
            'brighter': (85, 153),
            'darker': (86, 154)
        },
        2: {
            'on': (150, 90),
            'off': (149, 89),
            'brighter': (149, 149),
            'darker': (150, 150)
        },
        3: {
            'on': (166, 89),
            'off': (165, 90),
            'brighter': (165, 150),
            'darker': (166, 149)
        },
        4: {
            'on': (102, 85),
            'off': (101, 86),
            'brighter': (101, 154),
            'darker': (102, 153)
        }
    }

    def __init__(self, house_code, pin, adj=1):
        self.set_house_code(house_code)
        self.pin = pin
        self.pin_value = 0
        self._init_wiringpi()
        self.adj = adj

        self.toggles = 0
        self.duration = 0

    def _init_wiringpi(self):
        """
        Initializes the wiringpi pin of the 433 module
        """
        wiringpi2.pinMode(self.pin, self.WIRINGPI_OUTPUT_MODE)

    def get_controll_code(self, outlet_no, command):
        """
        Returns the tevion controll code of the given command for
        the given remote outlet.

        :return: command
        :rtype: tuple
        """
        return self.COMMAND_CODES[outlet_no][command]

    def _toggle_pin_value(self):
        """
        Toggles the internal pin state
        """
        if self.pin_value == 1:
            self.pin_value = 0
        else:
            self.pin_value = 1
        return self.pin_value

    def _get_long_delta(self):
        """
        Returns the adjusted delta for a long signal (logical one)
        """
        return int(self._delta_long * self.adj)

    def _get_short_delta(self):
        """
        Returns the adjusted delta for a short signal (logical zero)
        """
        return int(self._delta_short * self.adj)

    def _send_bit(self, value):
        """
        Sends the given logical bit
        """
        wiringpi2.digitalWrite(self.pin, self._toggle_pin_value())
        if value:
            wiringpi2.delayMicroseconds(self._get_long_delta())
            self.duration += self._delta_long
        else:
            wiringpi2.delayMicroseconds(self._get_short_delta())
            self.duration += self._delta_short
        self.toggles += 1

    def set_house_code(self, house_code):
        """
        Calculates and sets the internal representation of
        the tevion house code.
        """
        h = []
        for n in house_code:
            h.extend(self._bitfield(n))
        h.append(1)  # Parity hack!?!
        self._house_code = h

    def _bitfield(self, n):
        return [1 if digit == '1' else 0 for digit in '{0:08b}'.format(n)]

    def _send_house_code(self):
        for h in self._house_code:
            self._send_bit(h)

    def send_code(self, code):
        """
        Sends the given code (tuple)
        """
        self._send_house_code()
        for c in code:
            for bit in self._bitfield(c):
                self._send_bit(bit)

    def send_command(self, outlet_no, command):
        """
        Sends the given command code for the given remote outlet.
        """
        self.send_code(self.get_controll_code(outlet_no, command))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='Sends 433Mhz codes for the tevion remote control outlet')

    parser.add_argument(
        '-p', '--pin', type=int, default=1,
         help='Number of the wiringpi pin that should be used',
    )
    parser.add_argument(
        '-hc', '--housecode', type=int, nargs=3, default=[77, 42, 170],
        help='The Tevion house code of the outlets.\nDefault is 77, 42, 170.')
    parser.add_argument(
        'command', type=str, choices=['on', 'off', 'brighter', 'darker'])
    parser.add_argument(
        'outlet', type=int, nargs='?', default=0, choices=range(1, 5),
        help='Number of the power outlet, or all if omitted')
    parser.add_argument(
        '-r', '--repeat', type=int, default=5,
        help='Number of time the given code should be send.\n Default is 5.')
    parser.add_argument('-d', '--debug', action="store_true",
                        help='Activates debug output')
    parser.add_argument('--adj', type=float, default=1,
                        help='Adjust the sending speed.')
    args = parser.parse_args()

    start_time = datetime.datetime.now()

    tevion = TevionCode(args.housecode, args.pin, args.adj)
    for _i in range(args.repeat):
        tevion.send_command(args.outlet, args.command)

    if args.debug:
        print (datetime.datetime.now() - start_time).total_seconds() * 1000000
        print tevion.duration
        print tevion.toggles
