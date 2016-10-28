from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet

numPixels = 457 * 365

# create the net
net = buildNetwork(numPixels, 100, 1)

# create the dataset
ds = SupervisedDataSet(numPixels, 1)
