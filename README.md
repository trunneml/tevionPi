tevionPi
========
This is a small python script to controll the Tevion remote controlled outlets.
This outlets are using a non Elro compatible code so the normall 433 Mhz
controll tools are not working.


Acknowledgements
----------------
This program is based on the informations from
<http://etherrape.de/index.php/HowToRFM12_ASK>.
Without this webside and work this project wouldn't be possible.

Requirements
------------
To use the `send_tevion.py` script you need a raspberry pi with the following
software installed:

* Python2
* wiringpi2

You need also a connected 433 Mhz send module. The data pin should be connected
on pin 1, but you can change that (see the command line options of
send_tevion.py)

Installation
------------
Just checkout out this repository on your raspberry pi.

Usage
-----
`send_tevion.py` needs root permissions, so please run it as root or use
`sudo`.

The following command will light on all remote outlets, that are using the
initial tevion house code:
```
$ sudo ./send_tevion.py on
```

You can specify a outlet by it number:
```
$ sudo ./send_tevion.py off 2
```
That will turn on the outlet number 2.

You can also dimm the outlets with `brighter` and `darker`:
```
$ sudo ./send_tevion.py brighter 3
$ sudo ./send_tevion.py darker 3
```

Housecodes
----------
For a list of valid house codes see:
<http://etherrape.de/index.php/Tevion-codes>

