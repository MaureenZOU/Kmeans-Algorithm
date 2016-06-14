import csv
import matplotlib.pyplot as plt
import math


def readData(fileName):
    dataList = []

    with open(fileName, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        count = 0
        for row in spamreader:
            if count != 0:
                dataList.append(
                    [int(row[0]), int(row[1]), int(row[2]), float(row[3]), float(row[4]), int(row[5]), float(row[6])])
            count = count + 1

    return dataList


def plotData(dataList):
    for data in dataList:
        plt.plot(data[5], data[6], 'ro')
        plt.xlabel("number of wrong clustering in the first iteration")
        plt.ylabel("error")

    plt.show()


T = 40

while T < 61:
    dataList = readData("StandardDeviation0.1_d=50_n=20.csv")
    print()
    T = T + 1
    plotData(dataList)
