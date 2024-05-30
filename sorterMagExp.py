import os
import csv

def do(deepDir, expInd, magInd):
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

rows, cols = (10, 10)
fileMatrix = [[0]*cols for _ in range(rows)]

magnitudes = [6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0]
exposures = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

for i, m in enumerate(magnitudes):
    fileMatrix[i + 1][0] = m

for i, e in enumerate(exposures):
    fileMatrix[0][i + 1] = e

expInd = 1
magInd = 1

directory = os.path.join(os.getcwd(), "outputMagExp/")
directories = os.listdir(directory)

for i, d in enumerate(directories):
    directories[i] = os.path.join(directory, d)

for dir in directories:

    if magInd == 10:
        print("Too many arguments.")
        break

    deepDir = os.path.join(dir, "ImageFiles/")
    
    # Matrix of number of streaks per image
    fileMatrix[magInd][expInd] = do(deepDir, expInd, magInd)

    expInd += 1
    if expInd == 10:
        expInd = 1
        magInd += 1

csv_file = 'MagExpOutput.csv'

# Print out all data to csv file called MagExpOutput.csv
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(fileMatrix)

print(f"Data has been output to {csv_file}.")

input()