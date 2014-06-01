#!/usr/bin/env python2
import argparse

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


def get_controll_code(outlet_no, command):
    return COMMAND_CODES[outlet_no][command]

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
    args = parser.parse_args()

    wiringpi_pin = args.pin
    housecode = args.housecode
    command = args.command
    outlet = args.outlet

    print wiringpi_pin
    print housecode
    print get_controll_code(outlet, command)
