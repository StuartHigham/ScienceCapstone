import os
import csv

def countStreaks(deepDir):
    aList = ""

    txt_file = "streaks.txt"

    
    for dir in os.listdir(deepDir):
        dir = os.path.join(deepDir, dir)
        
        if os.path.isdir(dir):
            file_path = os.path.join(dir, txt_file)

            file = open(file_path, 'r')
            line_count = sum(1 for line in file)
            aList += (str(line_count - 1) + " ")
        
    return aList

rows, cols = (8, 6)
fileMatrix05 = [[0]*cols for _ in range(rows)]
fileMatrix15 = [[0]*cols for _ in range(rows)]
fileMatrix25 = [[0]*cols for _ in range(rows)]

magnitudes = [6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
exposures = [0.1, 0.2, 0.3, 0.4, 0.5]
samples = [5, 15, 25]

for i, m in enumerate(magnitudes):
    fileMatrix05[i + 1][0] = m
    fileMatrix15[i + 1][0] = m
    fileMatrix25[i + 1][0] = m

for i, e in enumerate(exposures):
    fileMatrix05[0][i + 1] = e
    fileMatrix15[0][i + 1] = e
    fileMatrix25[0][i + 1] = e

expInd = 1
magInd = 1
samInd = 0

baseDirectory = os.path.join(os.getcwd(), "outputMultiStreak/")
directories = os.listdir(baseDirectory)

for i, d in enumerate(directories):
    directories[i] = os.path.join(baseDirectory, d)

for dir in directories:
    
    if magInd == 8:
        print("Too many arguments.")
        break

    deepDir = os.path.join(dir, "ImageFiles/")

    match samInd:
        case 0:
            fileMatrix05[magInd][expInd] = countStreaks(deepDir)
        case 1:
            fileMatrix15[magInd][expInd] = countStreaks(deepDir)
        case 2:
            fileMatrix25[magInd][expInd] = countStreaks(deepDir)
    
    samInd += 1

    if samInd == 3:
        samInd = 0
        expInd += 1
    
    if expInd == 6:
        expInd = 1
        magInd += 1

csv_file05 = 'MultiStreakOutput05.csv'
csv_file15 = 'MultiStreakOutput15.csv'
csv_file25 = 'MultiStreakOutput25.csv'

with open(csv_file05, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(fileMatrix05)

with open(csv_file15, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(fileMatrix15)

with open(csv_file25, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(fileMatrix25)

print(f"Data has been output to {csv_file05}, {csv_file15}, {csv_file25}.")

input()