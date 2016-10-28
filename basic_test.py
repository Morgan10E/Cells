from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
import numpy

def getFeaturesFromFile(filename):
	im = Image.open(filename).convert('L')
	return numpy.array(im.getdata())

numPixels = 457 * 365

# create the net
net = buildNetwork(numPixels, 100, 1)

# create the dataset
ds = SupervisedDataSet(numPixels, 1)

# add the files to the dataset
ds.addSample(features, (numCells,))

# train the network
trainer = BackpropTrainer(net, ds)
for i in range(10):
	print trainer.train()

# activate the net on the dataset to see what we get
net.activate(features)
