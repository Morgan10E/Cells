from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np
import sys
import csv

def getFeaturesFromFile(filename):
    X = []
    y = []
    dataCSV = open(filename)
    reader = csv.reader(dataCSV)
    for row in reader:
        X.append([float(i) for i in row[0:-1]])
        klass = int(float(row[-1]))
        if klass > 1:
            klass = 1
        y.append(klass)
    return np.array(X), np.array(y, dtype=int)

if len(sys.argv) < 3:
    print "please specify filenames for training and testing"
    sys.exit()
train_filename = sys.argv[1]
test_filename = sys.argv[2]
print "Getting training features from " + train_filename
X,y = getFeaturesFromFile(train_filename)

print "Fitting k-means"

clf = QuadraticDiscriminantAnalysis()
clf.fit(X, y)

print "Getting testing features from " + test_filename
X_t,y_t = getFeaturesFromFile(test_filename)

print "Running prediction"
prediction = clf.predict(X_t)

numCorrect = 0
numWrong = 0
numGuessed = [0] * 2

for i in range(len(y_t)):
    correct_label = y_t[i]
    guess = prediction[i]
    numGuessed[guess] += 1
    if guess == correct_label:
        numCorrect += 1
    else:
        numWrong += 1

print "Num Correct:", (numCorrect * 1.0 / (numCorrect + numWrong))
print "Guesses:", numGuessed
