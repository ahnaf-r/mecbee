import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Read the Excel file
sheet_name = 'TF01e'  # Replace with the desired sheet name
data_frame = pd.read_excel('C:/Users/ahnaf/Downloads/MECBee/Data/data2.xlsx', sheet_name=sheet_name)

# Select column names
x_column = 'x'  # Replace with the actual name of the x column
y_column = 'y'  # Replace with the actual name of the y column
z_column = 'z'  # Replace with the actual name of the z column

# Get data for x, y, and z columns
x_data = data_frame[x_column]
y_data = data_frame[y_column]
z_data = data_frame[z_column]

# Plot the normal distribution for x
plt.figure()
plt.hist(x_data, bins=30, alpha=1, density=True, label='x')
x_mean, x_std = np.mean(x_data), np.std(x_data)
x_range = np.linspace(x_data.min(), x_data.max(), 100)
x_pdf = norm.pdf(x_range, x_mean, x_std)
plt.plot(x_range, x_pdf, label='Normal Distribution')
plt.xlabel('x')
plt.ylabel('Frequency / Probability Density')
plt.title('Distribution of x')
plt.legend()

# Plot the normal distribution for y
plt.figure()
plt.hist(y_data, bins=30, alpha=1, density=True, label='y')
y_mean, y_std = np.mean(y_data), np.std(y_data)
y_range = np.linspace(y_data.min(), y_data.max(), 100)
y_pdf = norm.pdf(y_range, y_mean, y_std)
plt.plot(y_range, y_pdf, label='Normal Distribution')
plt.xlabel('y')
plt.ylabel('Frequency / Probability Density')
plt.title('Distribution of y')
plt.legend()

# Plot the normal distribution for z
plt.figure()
plt.hist(z_data, bins=30, alpha=1, density=True, label='z')
z_mean, z_std = np.mean(z_data), np.std(z_data)
z_range = np.linspace(z_data.min(), z_data.max(), 100)
z_pdf = norm.pdf(z_range, z_mean, z_std)
plt.plot(z_range, z_pdf, label='Normal Distribution')
plt.xlabel('z')
plt.ylabel('Frequency / Probability Density')
plt.title('Distribution of z')
plt.legend()

plt.show()
