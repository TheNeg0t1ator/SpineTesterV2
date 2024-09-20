import serial

class uartSensor:
    def __init__(self) -> None:
        # initialize uart on com port
        self.com_port = serial.Serial('COM1', baudrate=115200)
        
        pass
    def getUART(self):
        # get the two values from the uart
        # return the list of values
        self.com_port.write(b'getWeight\n')
        weights = self.com_port.readline().decode().split()
        return [float(weight) for weight in weights]
        