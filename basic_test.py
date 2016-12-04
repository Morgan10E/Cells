from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.datasets import ClassificationDataSet
from pybrain.structure.modules import SoftmaxLayer
import numpy
import csv
import sys
from PIL import Image
from pybrain.supervised.trainers import BackpropTrainer
from sklearn import svm
import feature_extractor

def getFeaturesFromFile(filename):
	X = []
	y = []
	dataCSV = open(filename)
	reader = csv.reader(dataCSV)
	for row in reader:
		X.append([float(i) for i in row[0:-1]])
		y.append(float(row[-1]))
	return X,y
	# im = Image.open(filename).convert('L')
	# return numpy.array(im.getdata())

numPixels = 457 * 365
numPixels = 89 * 221

clf = svm.LinearSVC()
# X = []
# y = []
# dataCSV = open('data/Originals/D10415/D10415_CellCountResults_2016-02-12_13-21-32.974_ManualSequence_2016-02-12-13-20-40.370_After_OEP_loading.csv')
# reader = csv.reader(dataCSV)
# first = True
# for row in reader:
# 	if first:
# 		first = False
# 		continue
# 	numCells = 0
# 	if float(row[4]) == 0:
# 		continue
# 	if float(row[4]) == 1:
# 		numCells = 1
# 	elif float(row[4]) > 1:
# 		numCells = 2
# 	y.append(numCells)
# 	filename = "data/Originals/D10415/" + row[3] + ".tiff"
# 	print filename, numCells
# 	im = Image.open(filename).convert('L')
# 	resized = list(im.getdata())[:numPixels]
# 	X.append(resized)
if len(sys.argv) < 2:
    print "please specify directory"
    sys.exit()
directory_name = sys.argv[1]
filename = feature_extractor.RunExtraction(directory_name)
print "Getting features from " + filename
X,y = getFeaturesFromFile(filename)
print "Fitting to features"

clf.fit(X,y)
print "Running prediction"
prediction = clf.predict(X)

numWrong = 0
numNotZero = 0
for i in range(len(y)):
	print y[i], prediction[i]
	if not y[i] == prediction[i]:
		numWrong += 1
	if not prediction[i] == 0:
		numNotZero += 1
print "Number missed: " + str(numWrong)
print "Number not predicted zero: " + str(numNotZero)

# # create the net
# net = buildNetwork(numPixels, 100, 1)
#
# # create the dataset
# ds = SupervisedDataSet(numPixels, 1)
#
# #find counts and image filenames
# dataCSV = open('cell_counts.csv')
# reader = csv.reader(dataCSV)
# data = {}
# for row in reader:
# 	data[row[0]] = float(row[1])
#
# # add the files to the dataset
# for key, numCells in data.items():
# 	ds.addSample(getFeaturesFromFile(key), (numCells,))
#
# # train the network
# trainer = BackpropTrainer(net, ds)
# for i in range(100):
# 	print trainer.train()
#
# # activate the net on the dataset to see what we get
# for key, numCells in data.items():
# 	guess = net.activate(getFeaturesFromFile(key))
# 	print guess, numCells
