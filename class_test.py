from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.datasets import ClassificationDataSet
from pybrain.structure.modules import SoftmaxLayer
import numpy
import csv
from PIL import Image
from pybrain.supervised.trainers import BackpropTrainer

#find counts and image filenames
data = []
alldata = ClassificationDataSet(16, 1, nb_classes=3)
uncloned = ClassificationDataSet(16, 1, nb_classes=3)
expected = []

with open("d10482.csv") as f:
	for line in f:
		vals = line.split(",")
		hist = [float(x) for x in vals[:-1]]
		klass = int(vals[-1])
		alldata.addSample(numpy.array(hist), [klass])
		uncloned.addSample(numpy.array(hist), [klass])
		data.append((numpy.array(hist), klass))
		expected.append(klass)

# alldata._convertToOneOfMany()

# create the net
net = buildNetwork(alldata.indim, 16, 1, outclass=SoftmaxLayer)
# net = buildNetwork(alldata.indim, 16, alldata.outdim, outclass=SoftmaxLayer)
# net = buildNetwork(alldata.indim, 16, 1)

# # create the dataset
# ds = SupervisedDataSet(numPixels, 1)
#
# # add the files to the dataset
# for key, numCells in data.items():
# 	ds.addSample(getFeaturesFromFile(key), (numCells,))

# train the network
trainer = BackpropTrainer(net, alldata)
for i in range(50):
	# print trainer.train()
	trainer.train()

# activate the net on the dataset to see what we get
for hist, count in data:
	guess = net.activate(hist)
	print guess, count

# out = net.activateOnDataset(alldata)
# out = out.argmax(axis=1)  # the highest output activation gives the class
# for i in range(len(out)):
# 	print out[i], expected[i]
