import pandas as pd
import matplotlib.pyplot as plt
import statistics

# Read the Excel file
sheet_name = 'TF03h'  # Replace with the desired sheet name
data_frame = pd.read_excel('C:/Users/ahnaf/Downloads/MECBee/Data/data2.xlsx', sheet_name=sheet_name)

# Select column names
x_column = 'x'  # Replace with the actual name of the x column
y_column = 'y'  # Replace with the actual name of the y column
z_column = 'z'  # Replace with the actual name of the z column

# Remove rows with missing values
data_frame.dropna(subset=[x_column, y_column, z_column], inplace=True)

# Get data for x, y, and z columns
x_data = data_frame[x_column]
y_data = data_frame[y_column]
z_data = data_frame[z_column]

# Get Mean + St Dev for x,y,z
print("St Dev of x % s "% (statistics.stdev(x_data)))
print("Mean of x % s "% (statistics.mean(x_data))) 

print("St Dev of y % s "% (statistics.stdev(y_data)))
print("Mean of y % s "% (statistics.mean(y_data))) 

print("St Dev of z % s "% (statistics.stdev(z_data)))
print("Mean of z % s "% (statistics.mean(z_data)))

# Calculate the frequency of each unique value
x_values, x_counts = pd.Series(x_data).value_counts().sort_index().index, pd.Series(x_data).value_counts().sort_index().values
y_values, y_counts = pd.Series(y_data).value_counts().sort_index().index, pd.Series(y_data).value_counts().sort_index().values
z_values, z_counts = pd.Series(z_data).value_counts().sort_index().index, pd.Series(z_data).value_counts().sort_index().values

# Set the width of the bars
bar_width = 0.005

# Plot the frequencies for x
plt.figure()
plt.bar(x_values, x_counts, alpha=1, color='red', width=bar_width)
plt.xlabel('')
plt.ylabel('Occurrences of x')
plt.title('Distribution of x')
plt.xticks(rotation='vertical')

# Plot the frequencies for y
plt.figure()
plt.bar(y_values, y_counts, alpha=1, color='green', width=bar_width)
plt.xlabel('')
plt.ylabel('Occurrences of y')
plt.title('Distribution of y')
plt.xticks(rotation='vertical')

# Plot the frequencies for z
plt.figure()
plt.bar(z_values, z_counts, alpha=1, color='blue', width=bar_width)
plt.xlabel('')
plt.ylabel('Occurrences of z')
plt.title('Distribution of z')
plt.xticks(rotation='vertical')

plt.show()
