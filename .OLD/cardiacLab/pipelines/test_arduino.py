# %%
import time
import serial
import socket

# %%


class ArduinoCommunication:
    def __init__(self):
        self.arduino = None

    def start_communication(self, port=str('COM4'), baud=float(9600), timeout=float(0.1)):
        # add functions to try to connect if not throw message error
        self.arduino = serial.Serial(port, baud, timeout=timeout)
        print('Arduino communication established')

    def close_communication(self):
        self.arduino.close()

    def test_communication(self,):
        print("Verify that the LEDs change STATE")

        self.send([1, 1, 1, 1])
        time.sleep(5)
        self.send([0, 0, 0, 0])

    def send(self, laserState: list):
        str1 = ","
        str1 = str1.join(self.create_string(laserState))
        self.arduino.write(str.encode(str1))
        print(str1)
        return True

    def laserOFF(self, pin):
        self.arduino.write(str.encode(''.join([str(pin), '-0'])))
        print('laser OFF')
        return False

    @staticmethod
    def create_string(state=[0, 0, 0, 0]):
        laser_names = ['OneLaser', 'TwoLaser', 'ThreeLaser', 'FourLaser']
        dataZip = list(zip(laser_names, state))
        return list(map(lambda x: '-'.join([x[0], str(x[1])]), dataZip))


# %%

arduino_test = ArduinoCommunication()
arduino_test.start_communication()
# %%
arduino_test.test_communication()
# %%
