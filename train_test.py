import sys
import csv
from sklearn import svm
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.datasets import ClassificationDataSet
from pybrain.structure.modules import SoftmaxLayer
from pybrain.supervised.trainers import BackpropTrainer

def getFeaturesFromFile(filename):
	X = []
	y = []
	dataCSV = open(filename)
	reader = csv.reader(dataCSV)
	for row in reader:
		X.append([float(i) for i in row[0:-1]])
		y.append(int(row[-1]))
	return X,y

# ds = ClassificationDataSet(1600, 1, nb_classes=3)
# net = buildNetwork(ds.indim, 16, ds.outdim, outclass=SoftmaxLayer)
clf = svm.LinearSVC()
if len(sys.argv) < 3:
    print "please specify filenames for training and testing"
    sys.exit()
train_filename = sys.argv[1]
test_filename = sys.argv[2]
print "Getting training features from " + train_filename
X,y = getFeaturesFromFile(train_filename)
# print "Fitting to features"
# for i in range(len(y)):
# 	ds.addSample(X[i], [y[i]])
#
# ds._convertToOneOfMany

print "Fit clf"
clf.fit(X,y)
# trainer = BackpropTrainer(net, dataset=ds, momentum=0.1,
#                               verbose=True, weightdecay=0.01)
# for i in range(100):
# 	print trainer.train()

print "Getting testing features from " + test_filename
X,y = getFeaturesFromFile(test_filename)

print "Running prediction"
prediction = clf.predict(X)
# prediction = []
# for i in range(len(y)):
# 	guess = net.activate(X[i])
# 	prediction.append(guess)

numCorrect = [0]*3
numTotal = [0]*3
for i in range(len(y)):
	print y[i], prediction[i]
	numTotal[y[i]] += 1
	if y[i] == prediction[i]:
		numCorrect[y[i]] += 1
print "Number correct: " + str(numCorrect) + " out of " + str(numTotal)
print "Percentage: " + str(float(numCorrect[0])/numTotal[0]) + ", " + str(float(numCorrect[1])/numTotal[1]) + ", " + str(float(numCorrect[2])/numTotal[2])
print "Total percentage: " + str(float(sum(numCorrect))/sum(numTotal))
