import time
import serial
import socket


# -------------------------

# GREAT!!!! Recommendation given by DSI Ponehma
#  def recv_data(self):
#         length_bytes = self.dsi_serial.recv(2)
#         length = int.from_bytes(length_bytes, byteorder='big')
#         return self.dsi_serial.recv(length)

# --------------------------

# FIXME Huge improvement needed here, Arduino code is horrible....
# FIXME code getting better but lots to fix

class ArduinoCommunication:
    def __init__(self):
        self.arduino = None
        self.laser_names = ['a', 'b', 'c', 'd']

    def start_communication(self, port=str('COM4'), baud=float(9600), timeout=float(0.1)):
        # add functions to try to connect if not throw message error
        self.arduino = serial.Serial(port, baud, timeout=timeout)
        print('Arduino communication established')

    def close_communication(self):
        self.arduino.close()

    def test_communication(self,):
        print("Verify that the LEDs change STATE")
        for pin, state in enumerate([1, 1, 1, 1]):
            self.send(pin, state)
            print(create_string(pin, state))
            time.sleep(1.5)

        for pin, state in enumerate([0, 0, 0, 0]):
            self.send(pin, state)
            print(create_string(pin, state))
            time.sleep(1.5)

    def send(self, pin, laserState):
        # str1 = ","
        # str1 = str1.join(self.create_string(laserState))
        str1 = self.create_string(pin, laserState)
        self.arduino.write(str.encode(str1))
        # print(str1, end='\n')
        return True

    # def laserOFF(self, pin):
    #     self.arduino.write(str.encode(''.join([str(pin), '-0'])))
    #     print('laser OFF')
    #     return False
    def create_string(self, pin, state=0):
        str1 = '-'.join([self.laser_names[pin], str(state)])
        return ''.join([str1, ';'])

    # @staticmethod
    # def create_string(state=[0, 0, 0, 0]):
    #     laser_names = ['OneLaser', 'TwoLaser', 'ThreeLaser', 'FourLaser']
    #     dataZip = list(zip(laser_names, state))
    #     return list(map(lambda x: '-'.join([x[0], str(x[1])]), dataZip))


# %%  DSI COMMUNICATIONS


class DSICommunications:
    def __init__(self, host=None, port=None, decode=None):

        if decode is None:
            self.decode = 1251
            print(f'decoding method set to default: {self.decode}')
        if decode:
            self.decode = decode
        if host is None:
            self.host = 'COP-J7N5CH2'
            print(f'host value set to default: {self.host}')
        if host:
            self.host = host
        if port is None:
            self.port = 6732
            print(f'port value set to default: {self.port}')
        if port:
            self.port = port

        self.dsi_serial = None

    def start_communications(self):
        self.dsi_serial = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dsi_serial.connect((self.host, self.port))
        self.dsi_serial.setblocking(0)  # Maybe?

    def start_loop(self, seconds=None):

        if seconds is None:
            seconds = 10
            print(f'Program starts in {seconds} seconds')
        if seconds:
            sec = seconds
        for n in range(sec):
            # data = self.dsi_serial.recv(self.decode) # Maybe not needed
            if data:
                print(f"program starts in {sec - n}")
                data = []
            time.sleep(1)
    # Great update here? Thank DSI later

    def recv_data(self):
        try:
            length_bytes = self.dsi_serial.recv(2)
            length = int.from_bytes(length_bytes, byteorder='big')
            return self.dsi_serial.recv(length)
        except:
            pass

    def decode_data(self):
        return self.recv_data().decode(self.decode)
    # Stops here :P

    def test_communication(self):
        data = self.dsi_serial.recv(self.decode)
        print(f'testing communication, data recv:\n {data}')
