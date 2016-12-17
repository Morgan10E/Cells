from sklearn.cluster import KMeans
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
	return X,y

if len(sys.argv) < 3:
    print "please specify filenames for training and testing"
    sys.exit()
train_filename = sys.argv[1]
test_filename = sys.argv[2]
print "Getting training features from " + train_filename
X,y = getFeaturesFromFile(train_filename)

print "Fitting k-means"

kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
matching = 0
different = 0
numClasses = [0] * 2
for i in range(len(y)):
    numClasses[kmeans.labels_[i]] += 1
    if y[i] == kmeans.labels_[i]:
        matching += 1
    else:
        different += 1
print numClasses

switched = False
if matching < different:
    switched = True

print "Getting testing features from " + test_filename
X_t,y_t = getFeaturesFromFile(test_filename)

print "Running prediction"
prediction = kmeans.predict(X_t)

numCorrect = 0
numWrong = 0
numGuessed = [0] * 2

for i in range(len(y_t)):
    correct_label = y_t[i]
    if switched:
        correct_label = 1 - correct_label
    guess = prediction[i]
    numGuessed[guess] += 1
    if guess == correct_label:
        numCorrect += 1
    else:
        numWrong += 1

print "Num Correct:", (numCorrect * 1.0 / (numCorrect + numWrong))
print "Guesses:", numGuessed
