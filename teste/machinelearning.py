import csv
import os

# import pandas as pd
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split


file_list = []
while True:
    folder = os.listdir('/Users/uendellmagno/Downloads/')
    txt_present = False
    if len(folder) > 0:
        for file in os.listdir('/Users/uendellmagno/Downloads/'):
            file_list.append(file)
            if file.endswith('.txt'):
                txt_present = True
                with open(f'/Users/uendellmagno/Downloads/{file}', 'r') as in_file:
                    stripped = (line.strip() for line in in_file)
                    lines = (line.split(",") for line in stripped if line)

                    renamed_csv = file.replace('.txt', '.csv')
                    with open(f'/Users/uendellmagno/Downloads/{renamed_csv}', 'w') as out_file:
                        writer = csv.writer(out_file)
                        writer.writerows(lines)
                        print('Done')
    if txt_present is False:
        print(f"There are no TXT files in this folder: {folder}")
        break
    else:
        break

training_data = []
while True:
    for file in os.listdir('/Users/uendellmagno/Downloads/'):
        if file.endswith('.csv'):
            training_data.append(file)
            print(training_data)
    break
