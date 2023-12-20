import numpy as np
import matplotlib.pyplot as plt

# Your 2D list of data
data = [
    [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]],
    [[0.2, 0.3], [0.4, 0.5], [0.6, 0.7]],
    [[0.3, 0.4], [0.5, 0.6], [0.7, 0.8]],
]

# Flatten the data and extract rho values
flat_data = np.array([item for sublist in data for item in sublist])
rho_values = flat_data[:, 0]

# Create a color map that transitions from one color to another
colors = np.arange(len(rho_values))

# Create a scatter plot
plt.scatter(flat_data[:, 0], flat_data[:, 1], c=colors, cmap='viridis', marker='o')

# Add color bar
plt.colorbar(label='Generation')

# Set labels and title
plt.xlabel('Rho Values')
plt.ylabel('Alpha Values')
plt.title('Scatter Plot with Color Transition')

# Show the plot
plt.show()