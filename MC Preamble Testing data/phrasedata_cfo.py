import os
import csv
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
    directory = f'/home/spencer/Documents/SeniorDesign/Git/dynamic-preambles/MC Preamble Testing data/Preamble_mc{preamble_number}/CFO'

    # Initialize lists to store CFO and PDR values for the current preamble
    CFO_values = []
    PDR_values = []

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.startswith("cfo"):
            CFO = int(filename.split('.')[0][3:])  # Extract CFO value from file name
            file_path = os.path.join(directory, filename)
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

# Plotting PDR vs CFO for each preamble
plt.figure(figsize=(10, 10))
for i, preamble_data in enumerate(all_preambles_data):
    CFO_values, PDR_values = zip(*preamble_data)
    plt.plot(CFO_values, PDR_values,marker='o', label=f'Preamble {i}')

plt.xlabel('CFO (kHz)', fontsize= 32)
plt.ylabel('PDR (1000 packet set)', fontsize= 32)
plt.title('PDR vs CFO', fontsize= 38)
plt.tick_params(axis='both', which='major', labelsize=28)
plt.legend(fontsize= 30)
plt.grid(True)
plt.show()

