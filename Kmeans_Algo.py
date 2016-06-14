import numpy as np
import matplotlib.pyplot as plt
import sys
import csv


class Point:
    def __init__(self, x, y, realFlag):
        self.x = x
        self.y = y
        self.realFlag = realFlag
        self.guessFlag = None

    def __repr__(self):
        return "(x, y) = (" + str(self.x) + ", " + str(
            self.y) + ") , realFlag: " + self.realFlag + " guessFlag: " + self.guessFlag

    def setFlag(self, guessFlag):
        self.guessFlag = guessFlag


def generateSeed(density, distance, scale):
    mu = 0
    sigma = scale
    s = np.random.normal(mu, sigma, density)
    return s


def generatePoint(x, y, x0, y0):
    point = []

    for i in range(0, len(x0)):
        point.append([x + x0[i], y + y0[i]])

    return point


def generateData(number1, number2, staD1, staD2, distance):
    mean = 0

    x1 = generateSeed(number1, mean, staD1)
    x2 = generateSeed(number2, mean, staD2)
    y1 = generateSeed(number1, mean, staD1)
    y2 = generateSeed(number2, mean, staD2)

    len1 = max(x1)
    len2 = max(x2)

    x = 3
    y = 3

    cluster1 = generatePoint(x, y, x1, y1)
    cluster2 = generatePoint(x + distance, y, x2, y2)

    return cluster1 + cluster2


def kMeans_Algo(cluster, cluster1, cluster2):
    seedRed = initialSeed(cluster1, 1)
    seedBlue = initialSeed(cluster2, 2)

    E = 0.1
    K = 100

    e = sys.maxsize
    k = 0

    guessRed = []
    guessBlue = []

    while e > E and k < K:

        ##plt.plot(seedRed[0], seedRed[1], 'ro')
        ##plt.plot(seedBlue[0], seedBlue[1], 'bo')

        for data in cluster:
            distance1 = (data.x - seedRed[0]) ** (2) + (data.y - seedRed[1]) ** (2)
            distance2 = (data.x - seedBlue[0]) ** (2) + (data.y - seedBlue[1]) ** (2)

            if distance1 < distance2:
                data.setFlag("red")
                guessRed.append(data)
            else:
                data.setFlag("blue")
                guessBlue.append(data)

        cenRed = calCentroid(guessRed)
        cenBlue = calCentroid(guessBlue)

        e = ((seedRed[0] - cenRed[0]) ** (2) + (seedBlue[1] - cenBlue[1]) ** (2)) ** (0.5)
        k = k + 1

        seedRed = cenRed
        seedBlue = cenBlue


        ##for data in guessRed:
            ##plt.plot(data.x, data.y, 'rx')

        ##for data in guessBlue:
            ##plt.plot(data.x, data.y, 'bx')

        ##plt.show()

    return [cenRed, cenBlue]


def calCentroid(cluster):
    sumX = 0
    sumY = 0

    for data in cluster:
        sumX = sumX + data.x
        sumY = sumY + data.y

    cenX = sumX / len(cluster)
    cenY = sumY / len(cluster)

    return [cenX, cenY]


def initialSeed(cluster, parameter):
    sumX = 0
    sumY = 0
    maxY = -100000000
    minY = sys.maxsize

    for data in cluster:
        sumX = sumX + data.x
        sumY = sumY + data.y

        if data.y > maxY:
            maxY = data.y

        if data.y < minY:
            minY = data.y

    if parameter == 1:
        seed = [sumX / len(cluster), sumY / len(cluster) + (maxY - minY) / 3]

    if parameter == 2:
        seed = [sumX / len(cluster), sumY / len(cluster) - (maxY - minY) / 3]

    return seed


def calCorrectRate(center, distance):
    d1 = ((center[0][0] - 3) ** (2) + (center[0][1] - 3) ** (2)) ** (0.5)
    d2 = ((center[1][0] - (3 + distance)) ** (2) + (center[1][1] - 3) ** (2)) ** (0.5)

    return d1 + d2


def outputData(fileName, writeList):
    with open(fileName, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["number1", "number2", "staD1", "staD2", "distance", "errorRate"])
        for data in writeList:
            spamwriter.writerow([data[0], data[1], data[2], data[3], data[4], data[5]])


##########MAIN FUNCTION##########
number1 = 50
staD1 = 1
learnRate = 1
dr=1

while dr < 20:

    T = 0
    staD2 = 1
    number2 = int((number1 / (staD1) ** (2)) * (staD2 ** (2)))*dr
    writeList=[]
    parameter = 4

    while parameter < 8:

        distance = parameter * staD1 + parameter * staD2

        cluster = generateData(number1, number2, staD1, staD2, distance)
        cluster1 = []
        cluster2 = []

        ## print("iteration: " + str(T))

        for i in range(0, number1):
            data = Point(cluster[i][0], cluster[i][1], "red")
            cluster1.append(data)

        for i in range(number1, number1 + number2):
            data = Point(cluster[i][0], cluster[i][1], "blue")
            cluster2.append(data)

        cluster = cluster1 + cluster2

        center = kMeans_Algo(cluster, cluster1, cluster2)

        correctRate = calCorrectRate(center, distance)
        writeList.append([number1, number2, staD1, staD2, distance, correctRate])
        parameter=parameter+0.1
        T=T+1
        print(T)

    dr=dr+learnRate

    outputData("StandardDeviation0.1_dr=" + str(dr-learnRate)
               + ".csv", writeList)

