import serial
import serial.tools.list_ports

class uartSensor:
    def __init__(self, vid: int, pid: int) -> None:
        # Automatically find the COM port based on the USB VID and PID
        self.com_port_name = self.find_com_port(vid, pid)
        
        if not self.com_port_name:
            raise Exception(f"No device found with specified VID: {vid}, PID: {pid}")
        
        # Initialize UART connection on the detected COM port
        try:
            self.com_port = serial.Serial(self.com_port_name, baudrate=115200)
        except serial.SerialException as e:
            raise Exception(f"Failed to open COM port {self.com_port_name}: {e}")
    
    def find_com_port(self, vid: int, pid: int) -> str:
        # List all connected COM ports
        ports = serial.tools.list_ports.comports()
        
        # Debugging: Print out all connected ports and their VID/PID
        if False:
            print("Connected serial ports:")
            for port in ports:
                print(f"Port: {port.device}, VID: {port.vid}, PID: {port.pid}, Description: {port.description}")
        
        # Search for the port that matches the VID and PID (in decimal)
        for port in ports:
            if port.vid == vid and port.pid == pid:
                return port.device
        
        # If no device matches, return None
        return None
    
    def getUART(self) -> list[float]:
        # Request weight data from the device
        try:
            self.com_port.write(b'getWeight\n')
            response = self.com_port.readline().decode().strip()
        except serial.SerialTimeoutException as e:
            raise Exception(f"Timeout occurred while reading from the UART device: {e}")
        except Exception as e:
            raise Exception(f"Error communicating with the UART device: {e}")
        
        # Split and extract the weights (assuming format "A value B value")
        data = response.split()
        
        if len(data) == 4 and data[0] == 'A' and data[2] == 'B':
            try:
                weight_A = float(data[1])
                weight_B = float(data[3])
                return [weight_A, weight_B]
            except ValueError as e:
                raise ValueError(f"Error parsing weights from the response: {e}")
        else:
            raise ValueError("Invalid response format")

# Main function to run the UART sensor reading

VID+ = 11914  # Decimal for 0x2E8A
PID = 5      # Decimal for 0x0005

try:
    # Initialize the UART sensor object (auto-detects COM port)
    uart = uartSensor(VID, PID)
    
    # Get the weights from UART
    weights = uart.getUART()
    
    # Print the results
    print(f"Weight A: {weights[0]}, Weight B: {weights[1]}")

except Exception as e:
    # Catch any exceptions and print an error message
    print(f"Error: {e}")



