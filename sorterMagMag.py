import os
import csv

def do(deepDir):
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

magnitudes = [6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0]
backMags = [26, 24, 22, 20, 18, 16, 14, 12, 10, 8]

magLength = len(magnitudes)
bacLength = len(backMags)

rows, cols = (magLength + 1, bacLength + 1)
fileMatrix = [[0]*cols for _ in range(rows)]

for i, m in enumerate(magnitudes):
    fileMatrix[i + 1][0] = m

for i, e in enumerate(backMags):
    fileMatrix[0][i + 1] = e

bacInd = 1
magInd = 1

directory = os.path.join(os.getcwd(), "outputMagMag/")
directories = os.listdir(directory)

for i, d in enumerate(directories):
    directories[i] = os.path.join(directory, d)

for dir in directories:

    if magInd == rows:
        print("Too many arguments.")
        break

    deepDir = os.path.join(dir, "ImageFiles/")
    
    # Matrix of number of streaks per image
    fileMatrix[magInd][bacInd] = do(deepDir)

    bacInd += 1
    if bacInd == cols:
        bacInd = 1
        magInd += 1

csv_file = 'MagMagOutput.csv'

# Print out all data to csv file called MagExpOutput.csv
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(fileMatrix)

print(f"Data has been output to {csv_file}.")

input()