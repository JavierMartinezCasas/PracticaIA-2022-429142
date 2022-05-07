import pandas as pd
import csv

filename = 'Data.csv'
columns = ['Initial traffic level N', 'Initial traffic level E', 'Initial traffic level W', 'Green traffic light',
           'Final traffic level N', 'Final traffic level E', 'Final traffic level W']

df = pd.read_csv(filename, sep=";", usecols=columns)

file = open('Data.csv', "r")
csvreader = csv.reader(filename)

rows = []
for row in csvreader:
    rows.append(row)

print(rows)

