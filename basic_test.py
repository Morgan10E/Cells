from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.datasets import ClassificationDataSet
from pybrain.structure.modules import SoftmaxLayer
import numpy
import csv
from PIL import Image
from pybrain.supervised.trainers import BackpropTrainer

def getFeaturesFromFile(filename):
	im = Image.open(filename).convert('L')
	return numpy.array(im.getdata())

numPixels = 457 * 365

# create the net
net = buildNetwork(numPixels, 100, 1)

# create the dataset
ds = SupervisedDataSet(numPixels, 1)

#find counts and image filenames
dataCSV = open('cell_counts.csv')
reader = csv.reader(dataCSV)
data = {}
for row in reader:
	data[row[0]] = float(row[1])

# add the files to the dataset
for key, numCells in data.items():
	ds.addSample(getFeaturesFromFile(key), (numCells,))

# train the network
trainer = BackpropTrainer(net, ds)
for i in range(100):
	print trainer.train()

# activate the net on the dataset to see what we get
for key, numCells in data.items():
	guess = net.activate(getFeaturesFromFile(key))
	print guess, numCells
