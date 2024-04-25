import os
import csv
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Function to count occurrences of a phrase in a file
def count_phrase_occurrences(file_path, phrase):
    with open(file_path, 'r') as file:
        content = file.read()
        count = content.count(phrase)
        return count

# Initialize a list to store data for each preamble
all_preambles_data = []

# Iterate through different Preamble_mcX directories for SNR and PDR data
for preamble_number in range(5):  # Range 5 for Preamble_mc0 to Preamble_mc4
    snr_directory = f'/Users/spenceralbano/Desktop/UConn/Fall 2023/Senior Design 4901/2402-Git/dynamic-preambles/MC Preamble Testing data/Preamble_mc{preamble_number}/Noise'

    # Initialize lists to store SNR and PDR values for the current preamble
    SNR_values = []
    PDR_values = []

    # Iterate through each file in the SNR directory
    for filename in os.listdir(snr_directory):
        if filename.startswith("noise"):
            noise_voltage = float(filename.split('.')[0][5:])/10  # Extract noise voltage value from file name
            file_path = os.path.join(snr_directory, filename)
            phrase_count = count_phrase_occurrences(file_path, "Packet detected at sample")
            PDR = phrase_count / 1000  # Calculate PDR
            if noise_voltage == 0:
                noise_voltage = 0.1 
            SNR_values.append(10 * math.log10(1/(noise_voltage*noise_voltage)))
            PDR_values.append(PDR)

    # Sort the data by SNR values
    sorted_data = sorted(zip(SNR_values, PDR_values))

    # Append the sorted data to the list of all preamble data
    all_preambles_data.append(sorted_data)

# Plotting PDR vs SNR for each preamble
fig, ax1 = plt.subplots(figsize=(16, 10))

ax1.set_xlabel('SNR (dB)', fontsize=24)
ax1.set_ylabel('PDR (1000 packet set)', fontsize=24)
ax1.set_title('PDR vs SNR and CFO\n', fontsize=30, weight='bold')
ax1.tick_params(axis='both', which='major', labelsize=22)

# Define a list of colors for each preamble
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

# Plotting PDR vs SNR for each preamble
legend_elements = []
legend_elements.append(Line2D([0], [0], marker='None', color="black", linewidth=3.25, label='SNR'))
legend_elements.append(Line2D([0], [0], marker='None', color="black", linewidth=3.25, linestyle=(0, (5, 1)), label='CFO'))
for i, preamble_data in enumerate(all_preambles_data):
    SNR_values, PDR_values = zip(*preamble_data)
    line = Line2D([0], [0], marker='s', color=colors[i], markersize=20, linestyle = 'None', label=f'Preamble {i}') 
    ax1.plot(SNR_values, PDR_values, marker='o', color=colors[i])
    legend_elements.append(line)

ax1.legend(handles=legend_elements, fontsize=22, loc='lower center')
ax1.grid(True)

# Reset the all_preambles_data for CFO and PDR data
all_preambles_data = []

# Iterate through different Preamble_mcX directories for CFO and PDR data
for preamble_number in range(5):  # Range 5 for Preamble_mc0 to Preamble_mc4
    cfo_directory = f'/Users/spenceralbano/Desktop/UConn/Fall 2023/Senior Design 4901/2402-Git/dynamic-preambles/MC Preamble Testing data/Preamble_mc{preamble_number}/CFO'

    # Initialize lists to store CFO and PDR values for the current preamble
    CFO_values = []
    PDR_values = []

    # Iterate through each file in the CFO directory
    for filename in os.listdir(cfo_directory):
        if filename.startswith("cfo"):
            CFO = int(filename.split('.')[0][3:])  # Extract CFO value from file name
            file_path = os.path.join(cfo_directory, filename)
            phrase_count = count_phrase_occurrences(file_path, "Packet detected at sample")
            PDR = phrase_count / 1000  # Calculate PDR
            CFO_values.append(CFO)
            PDR_values.append(PDR)
        CFO_values.append(12)
        PDR_values.append(0)

    # Sort the data by CFO values
    sorted_data = sorted(zip(CFO_values, PDR_values))

    # Append the sorted data to the list of all preamble data
    all_preambles_data.append(sorted_data)

# Creating second x-axis
ax2 = ax1.twiny()

ax2.set_xlabel('CFO (kHz)', fontsize=24)
ax2.set_ylabel('PDR (1000 packet set)', fontsize=24)
ax2.tick_params(axis='both', which='major', labelsize=22)

# Plotting PDR vs CFO for each preamble
for i, preamble_data in enumerate(all_preambles_data):
    CFO_values, PDR_values = zip(*preamble_data)
    ax2.plot(CFO_values, PDR_values, marker='D', linestyle=(0, (5, 1)), color=colors[i])


fig.tight_layout()
plt.grid(True)
plt.savefig('/Users/spenceralbano/Desktop/UConn/Fall 2023/Senior Design 4901/2402-Git/dynamic-preambles/MC Preamble Testing data/SNR_CFO_VS_PDR.png')
plt.show()

