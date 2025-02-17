import csv
import time
import sys
import serial
import codecs
from collections import OrderedDict

class UM:
    def __init__(self, port):
        self.port = port
        self.serial = None
        self.higher_resolution = True 

    def open(self):
        self.serial = serial.Serial(self.port, baudrate=9600, timeout=1)

    def close(self):
        if self.serial:
            self.serial.close()

    def send(self, command):
        self.serial.write(bytes.fromhex(command))
        time.sleep(0.1)

    def read(self):
        self.send("f0")  # Send request command
        data = self.serial.read(130)  # Read response
        return self.parse(data)

    def parse(self, data):
        if len(data) < 130:
            return None
        
        data = codecs.encode(data, "hex").decode("utf-8")
        result = OrderedDict()
        multiplier = 10 if self.higher_resolution else 1
        
        result["timestamp"] = time.time()
        result["voltage"] = int("0x" + data[4:8], 0) / (100 * multiplier) # Volts
        result["current"] = int("0x" + data[8:12], 0) / (1000 * multiplier) # Amps
        result["power"] = int("0x" + data[12:20], 0) / 1000 # Watts
        result["temperature"] = int("0x" + data[20:24], 0)
        result["data_plus"] = int("0x" + data[192:196], 0) / 100
        result["data_minus"] = int("0x" + data[196:200], 0) / 100
        result["mode_id"] = int("0x" + data[200:204], 0)
        result["accumulated_current"] = int("0x" + data[204:212], 0)
        result["accumulated_power"] = int("0x" + data[212:220], 0)
        result["accumulated_time"] = int("0x" + data[224:232], 0)
        result["resistance"] = int("0x" + data[244:252], 0) / 10
        
        return result

def log_data(com_port, output_file):
    attempts = 0
    um25c = None
    while attempts < 10:
        try:
            um25c = UM(com_port)
            um25c.open()
            print(f"Connected {com_port}. Logging to {output_file}...")
            break
        except Exception as e:
            print(f"Attempt {attempts + 1}: Error - {e}")
            attempts += 1
            time.sleep(1)
    
    if um25c is None:
        print("Failed to connect after 10 attempts. Exiting...")
        return
    
    try:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Voltage (V)", "Current (A)", "Power (W)", "Temperature", "Data+", "Data-", "Mode ID", "Accumulated Current", "Accumulated Power", "Accumulated Time", "Resistance"])
            
            while True:
                try:
                    parsed_data = um25c.read()
                    if parsed_data:
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([timestamp] + list(parsed_data.values())[1:])
                        print(f"{timestamp} - {parsed_data}")
                except KeyboardInterrupt:
                    print("\nLogging interrupted. Saving file and exiting...")
                    break
    finally:
        um25c.close()
        print("Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <COM Port> <Output CSV File>")
        sys.exit(1)
    
    com_port = sys.argv[1]
    output_file = sys.argv[2]
    
    log_data(com_port, output_file)
