import serial
import time
import argparse

parser = argparse.ArgumentParser(description='Send an sms to number')
parser.add_argument('-n','--number', type=str, help='a number for sms', required=True)
parser.add_argument('-p','--port', type=str, help='port number to use', required=True)
parser.add_argument('-m','--message', type=str, help='message to send', required=True)
args = parser.parse_args()

print("Using number: " + args.number + ", message: " + args.message + ", and port: /dev/ttyUSB" + args.port)

class TextMessage:
    """Class to set up GSM-connection and send SMS"""

    def __init__(self, recipient, message):
        self.recipient = recipient
        self.content = message

    def setRecipient(self, number):
        self.recipient = number

    def setContent(self, message):
        self.content = message

    def connectGSM(self, port):
        print("using port: " + '/dev/' + 'ttyUSB' + port)
        self.ser = serial.Serial(
            port='/dev/' + 'ttyUSB' + port,
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

message = TextMessage(args.number, args.message)
message.connectGSM(args.port)
message.sendMessage()
message.disconnectGSM()
