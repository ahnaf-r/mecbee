# We FUCKING love libraries <3 (but she doesn't love me :( )
import serial
import time
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
x_data_queue = [] #deque(maxlen=window_size)
y_data_queue = [] #deque(maxlen=window_size)
z_data_queue = [] #deque(maxlen=window_size)

# Set the systematic error offsets for x, y, and z coordinates
x_offset = 0  # offset value for the x coordinate
y_offset = 0  # offset value for the y coordinate
z_offset = 0  # offset value for the z coordinate

# Initialize the plots
fig, (ax_x, ax_y, ax_z) = plt.subplots(3, 1, sharex=True, figsize=(8, 12))
lines_unfiltered = []
lines_filtered = []
labels = ['X', 'Y', 'Z']

for i, ax in enumerate([ax_x, ax_y, ax_z]):
    unfiltered_line, = ax.plot([], [], 'b-', label='Unfiltered')
    filtered_line, = ax.plot([], [], 'r-', label='Filtered')
    ax.set_ylabel(labels[i])
    ax.legend()
    lines_unfiltered.append(unfiltered_line)
    lines_filtered.append(filtered_line)

ax_z.set_xlabel('Time')
ax_x.set_title('Live Plot of X, Y, Z Coordinates')

# Create empty lists to store the data
maxPlotWindow = 200
time_data = []
x_unfiltered_data = []
y_unfiltered_data = []
z_unfiltered_data = []
x_filtered_data = []
y_filtered_data = []
z_filtered_data = []

# Update function for live plotting
def update_plot(i):
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

        if len(x_data_queue)==window_size:
            x_data_queue.pop(0)
            y_data_queue.pop(0)
            z_data_queue.pop(0)

        # Append the data to the lists
        time_data.append(time.time())
        x_unfiltered_data.append(x_coord)
        y_unfiltered_data.append(y_coord)
        z_unfiltered_data.append(z_coord)
        x_filtered_data.append(x_avg)
        y_filtered_data.append(y_avg)
        z_filtered_data.append(z_avg)

        if len(time_data)==maxPlotWindow:
            time_data.pop(0)
            x_unfiltered_data.pop(0)
            y_unfiltered_data.pop(0)
            z_unfiltered_data.pop(0)
            x_filtered_data.pop(0)
            y_filtered_data.pop(0)
            z_filtered_data.pop(0)

        # Update the plot data for each coordinate
        # Alternatively, use the listed variables to redirect data to the blimp controller, in the future
        lines_unfiltered[0].set_data(time_data, x_unfiltered_data)
        lines_filtered[0].set_data(time_data, x_filtered_data)
        lines_unfiltered[1].set_data(time_data, y_unfiltered_data)
        lines_filtered[1].set_data(time_data, y_filtered_data)
        lines_unfiltered[2].set_data(time_data, z_unfiltered_data)
        lines_filtered[2].set_data(time_data, z_filtered_data)

        # Adjust the plot limits
        for ax in [ax_x, ax_y, ax_z]:
            ax.relim()
            ax.autoscale_view()

    return lines_unfiltered + lines_filtered

# Animate the plot
animate = animation.FuncAnimation(fig, update_plot, interval=10)

# Show the plot
plt.show()

# Close the serial connection
ser.write(b"\r")
ser.close()
