import serial
import time

class TextMessage:
    """Class to set up GSM-connection and send SMS"""

    def __init__(self, recipient, message):
        self.recipient = recipient
        self.content = message

    def setRecipient(self, number):
        self.recipient = number

    def setContent(self, message):
        self.content = message

    def connectGSM(self):
        self.ser = serial.Serial(
            port='/dev/ttyUSB1',  # port for usb modem
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            rtscts=True,
            #Added to prevent error on USB1 
            dsrdtr=True,
            #Added to prevent error on USB1
            timeout=1
        )
        time.sleep(0.5)

    def sendMessage(self):
        print("sending to {}".format(self.recipient))
        print("sending message: {}".format(self.content))
        # modem has to be AT+CFUN=1, not AT+CFUN=4 wich is default
        self.ser.write(('AT+CFUN=1\r').encode())
        print(self.ser.read(100))
        time.sleep(3)
        self.ser.write(('AT\r').encode())
        print(self.ser.read(100))
        time.sleep(1)
        # pin is deactivated on sim card. Uncomment for pin
        # self.ser.write(('AT+CPIN=<pin-code>\r').encode())
        time.sleep(1)
        self.ser.write(('AT+CMGF=1\r').encode())
        print(self.ser.read(100))
        time.sleep(1)
        self.ser.write(('''AT+CMGS="''' + self.recipient + '''"\r''').encode())
        print(self.ser.read(100))
        time.sleep(1)
        self.ser.write((self.content + "\r").encode())
        #Added CTRL+Z for sms transmission
        print(self.ser.read(100))
        time.sleep(2)
        self.ser.write(chr(26).encode())
        print(self.ser.read(100))
        time.sleep(1)

    def disconnectGSM(self):
        self.ser.close()
