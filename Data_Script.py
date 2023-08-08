# Libraries galore
import serial
import time
import csv


# Input serial port parameters
serial_port = 'COM8'
baud_rate = 115200

# Establish a connection to the serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)

#print("Starting...")
#time.sleep(1)

# Sends return command to init
print("Sending Init.")
tryInit = True
countTries = 0

while tryInit:
    ser.write(b'\r')
    time.sleep(0.1)
    ser.write(b'\r')
    countTries += 1
    dataBuf = []

    while ser.inWaiting():
        data = ser.read()
        dataBuf.append(data.decode())

    returnStr = ''.join(dataBuf)
    print(returnStr)

    if ("dwm>" in returnStr):
        tryInit = False
        
        # Send command 'lec' and return key to start the data collection
        ser.write(b"lec")
        ser.write(b"\r")

    time.sleep(1)
    print("Attempt #"+str(countTries))


# Open the CSV file for writing
csv_file_path = "C:/Users/ahnaf/Downloads/MECBee/Data/data.csv"
with open(csv_file_path, "a", newline='') as csv_file:
    writer = csv.writer(csv_file)

    try:
        while True:
            data = ser.readline().decode().strip()
            print(data)

            # Split data based on commas and write each value as a separate column
            data_list = data.split(",")
            writer.writerow(data_list)
            csv_file.flush()

    except KeyboardInterrupt:
        print("alright buddy boy")
    finally:
        ser.write(b"\r")
        ser.close()
