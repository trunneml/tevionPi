#!/usr/bin/env python2
import wiringpi2
import datetime
import math

wiringpi2.wiringPiSetup()

start_time = datetime.datetime.now()
#		wiringpi2.delayMicroseconds(100)

INPUT_MODE = 0
OUTPUT_MODE = 1

READ_PIN = 1

SCAN_TIME = 5*1000*1000 

def getSignalLevel():
    c = 20
    cur_level = 0
    for x in range(c):
        cur_level = cur_level + wiringpi2.digitalRead(READ_PIN)
    return cur_level <= 0


wiringpi2.pinMode(READ_PIN, INPUT_MODE)

t = 0
level = getSignalLevel()
last_flip = datetime.datetime.now()

toggel_list = []

sl = 0
while t < SCAN_TIME:
    cur_level = getSignalLevel()
    if cur_level != level:
        toggel_list.append((cur_level, sl))
        level = cur_level
        sl = 0
    sl = sl + 200
    t = t + 200

print (datetime.datetime.now() - start_time)

max_d = 0
avg_d = 0
bit_lists = []
bit_list = []
for t in toggel_list:
    # Do some statistics here
    d = t[1]
    avg_d = avg_d + d
    if d > max_d:
        max_d = d
    # Real work down here
    if d >= 400 and d <= 1600:
        # Only append valid values
        bit_list.append(d)
    else:
        # Gap detected
        if len(bit_list) >= 41:
            # Gap is end of bit_list so add the list
            bit_lists.append(bit_list)
        # Reset the bit list
        bit_list = []


def extract_byte(time_list):
    b = 255
    for x in range(8):
        if time_list[x] < 900:
            b = b - math.pow(2, 7-x)
    return int(b)

print "toggels: ", len(toggel_list)
print "avg signal time", avg_d/len(toggel_list)
print "max signal time", max_d
for l in bit_lists:
#    print "bits: ", len(l)
#    print float(sum(l))/len(l) if len(l) > 0 else float('nan')
#    print min(l)
#    print max(l)
    if len(l) == 41:
        #print map(lambda x: x < 900, l)
        print extract_byte(l[0:8]), extract_byte(l[8:16]), extract_byte(l[16:24]), l[24] > 900
        print extract_byte(l[25:33]), extract_byte(l[33:41])
        #print map(lambda x: x < 900, l[25:33])
