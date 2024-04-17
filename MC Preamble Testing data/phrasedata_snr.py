import os
import csv
import math
import matplotlib.pyplot as plt

# Function to count occurrences of a phrase in a file
def count_phrase_occurrences(file_path, phrase):
    with open(file_path, 'r') as file:
        content = file.read()
        count = content.count(phrase)
        return count

# Initialize a dictionary to store CFO values and corresponding PDR (Phrase Count divided by 1000) for each preamble
all_preambles_data = []

# Iterate through different Preamble_mcX directories
for preamble_number in range(5):  # Range 5 for Preamble_mc0 to Preamble_mc4
    directory = f'/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/MC Preamble Testing data/Preamble_mc{preamble_number}/Noise'

    # Initialize lists to store CFO and PDR values for the current preamble
    SNR_values = []
    PDR_values = []

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.startswith("noise"):
            noise_voltage = float(filename.split('.')[0][5:])/10  # Extract noise voltage value from file name
            file_path = os.path.join(directory, filename)
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
plt.figure(figsize=(10, 11))
for i, preamble_data in enumerate(all_preambles_data):
    SNR_values, PDR_values = zip(*preamble_data)
    plt.plot(SNR_values, PDR_values,marker='o', label=f'Preamble {i}')

plt.xlabel('SNR (dB)', fontsize= 26)
plt.ylabel('PDR (1000 packet set)', fontsize= 26)
plt.title('PDR vs SNR', fontsize= 30)
plt.tick_params(axis='both', which='major', labelsize=20)
plt.legend(fontsize= 22)
plt.grid(True)
plt.show()

