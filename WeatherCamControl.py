import serial
import binascii

from Configuration import Configuration


class WeatherCamControl:
    commands = {
        "ENMI": ["808801010000F6", "enhancer: middle"],
        "ENHI": ["808800010000F7", "enhancer: high"],
        "GATA": ["808900010000F6", "gamma: type A"],
        "GATB": ["808901010000F5", "gamma: type B"],
        "CMAU": ["808E00010000F1", "color mode: auto"],
        "CMDA": ["808E01010000F0", "color mode: day"],
        "CMNI": ["808E02010000EF", "color mode: night"],
        "CMEX": ["808E03010000EE", "color mode: ext"],
        "WAWB": ["808301010000FB", "white balance: AWB"],
        "WATW": ["808300010000FC", "white balance: ATW"],
        "PRSS": ["818B01010000F2", "priority: slow shutter"],
        "PRAG": ["818B00010000F3", "priority: AGC"],
        "FLC1": ["808C01010000F2", "FLC: on"],
        "FLC0": ["808C00010000F3", "FLC: off"],
        "AGC1": ["808201010000FC", "AGC: on"],
        "AGC0": ["808200010000FD", "AGC: off"],
        "BLC1": ["808601010000F8", "BLC: on"],
        "BLC0": ["808600010000F9", "BLC: off"],
        "SAES": ["808B00010000F4", "AES"],
        "SALC": ["808B01010000F3", "ALC"],
        "ALC7": ["808F07010000E9", "ALC: 1/10000"],
        "ALC6": ["808F06010000EA", "ALC: 1/4000"],
        "ALC5": ["808F05010000EB", "ALC: 1/2000"],
        "ALC4": ["808F04010000EC", "ALC: 1/1000"],
        "ALC3": ["808F03010000ED", "ALC: 1/500"],
        "ALC2": ["808F02010000EE", "ALC: 1/250"],
        "ALC1": ["808F01010000EF", "ALC: 1/100"],
        "ALC0": ["808F00010000F0", "ALC: OFF"],
        "SSH1": ["808D01010000F1", "slow shutter: on"],
        "SSH0": ["808D00010000F2", "slow shutter: off"],
        "SSX0": ["818200010000FC", "slow shutter: x2"],
        "SSX1": ["818201010000FB", "slow shutter: x4"],
        "SSX2": ["818202010000FA", "slow shutter: x8"],
        "SSX3": ["818203010000F9", "slow shutter: x16"],
        "SSX4": ["818204010000F8", "slow shutter: x32"],
        "SSX5": ["818205010000F7", "slow shutter: x64"],
        "SSX6": ["818206010000F6", "slow shutter: x128"],
        "SSX7": ["818207010000F5", "slow shutter: x256"],
    }

    def __init__(self, port = Configuration.defaultSerialPort):
        self.port = port
        self.serialCon = None
        self.nightMode = False

    def open(self, port):
        self.serialCon = serial.Serial(port)

    def close(self):
        self.serialCon.close()
        self.serialCon = None

    def sendSerialCommand(self, command):
        if self.serialCon is None:
            return

        self.serialCon.write(bytearray(binascii.unhexlify(WeatherCamControl.commands[command][0])))

    def setDayNight(self, night = False):
        if(not night):
            command = Configuration.day_settings
        else:
            command = Configuration.night_settings

        self.open(self.port)
        
        for i in range(3):
            for command in commands:
                self.sendSerialCommand(command)
                time.sleep(Configuration.time_between_commands)

        self.close()

    def setDay(self):
        self.setDayNight(False)

    def setNight(self):
        self.setDayNight(True)