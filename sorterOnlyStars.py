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

shape_cut = [0.2, 0.3, 0.4, 0.5]
densities = [0] * 30

shaLength = len(shape_cut)
denLength = len(densities)

rows, cols = (denLength + 1, shaLength + 1)
fileMatrix = [[0]*cols for _ in range(rows)]

for i, d in enumerate(densities):
    fileMatrix[i + 1][0] = i + 1

for i, s in enumerate(shape_cut):
    fileMatrix[0][i + 1] = s

expInd = 1
magInd = 1

directory = os.path.join(os.getcwd(), "outputOnlyStars/")
directories = os.listdir(directory)

for i, d in enumerate(directories):
    directories[i] = os.path.join(directory, d)

for dir in directories:

    if magInd == rows:
        print("Too many arguments.")
        break

    deepDir = os.path.join(dir, "ImageFiles/")
    
    # Matrix of number of streaks per image
    fileMatrix[magInd][expInd] = do(deepDir, expInd, magInd)

    expInd += 1
    if expInd == cols:
        expInd = 1
        magInd += 1

csv_file = 'OnlyStarsOutput.csv'

# Print out all data to csv file called OnlyStarsOutput.csv
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(fileMatrix)

print(f"Data has been output to {csv_file}.")

input()