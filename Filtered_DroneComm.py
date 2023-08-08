import serial
import time
from pymavlink import mavutil

# Input serial port parameters
serial_port = 'COM8'
baud_rate = 115200

# Establish a connection to the serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)

print("Starting...")
time.sleep(1)

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

    if "dwm>" in returnStr:
        tryInit = False

        # Send command 'lep' and return key to start the data collection
        ser.write(b"lep")
        ser.write(b"\r")

    time.sleep(1)
    print("Attempt #" + str(countTries))


# Set the size of the moving average window
window_size = 30
x_data_queue = []
y_data_queue = []
z_data_queue = []

# Set the systematic error offsets for x, y, and z coordinates
x_offset = 0
y_offset = 0
z_offset = 0

# Create a UDP connection to ArduPilot
udp_conn = mavutil.mavlink_connection('udpout:localhost:14550')  # Replace 'localhost' with the IP address of your ArduPilot device

# Main loop for data collection and MAVLink communication
try:
    while True:
        # Read the data from the serial port
        data = ser.readline().decode().strip()

        # Check if the line contains position coordinates
        if data.startswith("POS"):
            # Split data based on commas
            data_list = data.split(",")

            # Extract x, y, z position coordinates
            x_coord, y_coord, z_coord = map(float, data_list[1:4])  # Position coordinates are in the 2nd, 3rd, and 4th columns

            # Apply the systematic error offsets to the coordinates
            x_coord += x_offset
            y_coord += y_offset
            z_coord += z_offset

            # Append the new data points to the respective data queues
            x_data_queue.append(x_coord)
            y_data_queue.append(y_coord)
            z_data_queue.append(z_coord)

            # Calculate the moving average of the data points in the window
            x_avg = sum(x_data_queue) / window_size
            y_avg = sum(y_data_queue) / window_size
            z_avg = sum(z_data_queue) / window_size

            # Print the filtered values to the console
            print(f"{x_avg}, {y_avg}, {z_avg}")

            if len(x_data_queue) == window_size:
                x_data_queue.pop(0)
                y_data_queue.pop(0)
                z_data_queue.pop(0)

            # Prepare the MAVLink message with the averaged coordinates
            msg = udp_conn.mav.set_position_target_local_ned_encode(
                0,  # time_boot_ms (not used)
                1, 1,  # target_system, target_component
                9,  # coordinate_frame: MAV_FRAME_LOCAL_NED (Local coordinate frame)
                0b111111111000,  # type_mask: Include velocity, acceleration, and yaw
                x_avg, y_avg, z_avg,  # x, y, z coordinates in meters
                0.0, 0.0, 0.0,  # vx, vy, vz (not used)
                0.0, 0.0, 0.0,  # afx, afy, afz (not used)
                0.0, 0.0  # yaw, yaw_rate (not used)
            )

            # Send the MAVLink message to ArduPilot
            udp_conn.mav.send(msg)

            # Send heartbeat message to maintain the connection
            udp_conn.mav.heartbeat_send(
                mavutil.mavlink.MAV_TYPE_GCS,  # type
                mavutil.mavlink.MAV_AUTOPILOT_INVALID,  # autopilot
                0,  # base_mode
                0,  # custom_mode
                0,  # system_status
                0  # mavlink_version
            )

            time.sleep(0.1)  # Adjust the delay as needed for your application

except KeyboardInterrupt:
    pass

# Close the serial connection
ser.write(b"\r")
ser.close()
