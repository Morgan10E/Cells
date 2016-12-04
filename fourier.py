import numpy as np
from sklearn import svm
import csv
from PIL import Image

numPixels = 89 * 221

clf = svm.LinearSVC()
X = []
y = []
dataCSV = open('data/Originals/D10415/D10415_CellCountResults_2016-02-12_13-21-32.974_ManualSequence_2016-02-12-13-20-40.370_After_OEP_loading.csv')
reader = csv.reader(dataCSV)

numEach = [0]*2
first = True
for row in reader:
    if first:
        first = False
        continue
    numCells = 0
    if float(row[4]) == 0:
        numEach[0] += 1
    else:
        numCells = 1
        numEach[1] += 1
    # if float(row[4]) == 1:
    #     numCells = 1
    #     numEach[1] += 1
    # elif float(row[4]) > 1:
    #     numEach[2] += 1
    #     numCells = 2
    y.append(numCells)
    filename = "data/Originals/D10415/" + row[3] + ".tiff"
    im = Image.open(filename).convert('L')
    resized = np.array(im)
    # resized = np.reshape(resized, (89, 221))
    fft = np.fft.fft2(resized)
    print len(fft.flatten())
    X.append(fft.flatten()[:19669])
    print filename, numCells

Xnew = []
ynew = []
trimTo = min(numEach)
numEach = [0]*3
print "Trimming to: " + str(trimTo)
for i in range(len(y)):
    if numEach[y[i]] < trimTo:
        Xnew.append(X[i])
        ynew.append(y[i])
    numEach[y[i]]+=1

clf.fit(Xnew,ynew)
prediction = clf.predict(Xnew)

numWrong = 0
numNotZero = 0
for i in range(len(ynew)):
	print ynew[i], prediction[i]
	if not ynew[i] == prediction[i]:
		numWrong += 1
	if not prediction[i] == 0:
		numNotZero += 1
print "Number missed: " + str(numWrong)
print "Number not predicted zero: " + str(numNotZero)
