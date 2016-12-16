import numpy as np
import scipy
import scipy.linalg as linalg
import PIL

def PCA(data):
    num_data, dim = data.shape
    data_mean = data.mean(axis=0)
    centered_data = data - data_mean
    U,S,V = linalg.svd(centered_data)
    # V = V[:num_data]
    return V,S,data_mean

def trainPCA(datafile):
    data = np.genfromtxt('Data/train.csv', delimiter=",")
    class_labels = data[:, -1]
    # print class_labels.shape
    data = data[:, :-1] # remove the class labels
    print data.shape
    V,S,immean = PCA(data)
    vectors = V[0:10] # (10, 1600)
    vectors = vectors.transpose()
    pca_data = np.matmul(data, vectors)
    print pca_data.shape
    print class_labels.shape
    new_train_data = np.column_stack((pca_data, class_labels))
    print new_train_data.shape
    np.savetxt('Data/train_pca.csv', new_train_data, delimiter=',')
    np.savetxt('Data/train_pca_mat.csv', vectors, delimiter=',')

def testPCA(datafile):
    data = np.genfromtxt('Data/test.csv', delimiter=",")
    class_labels = data[:, -1]
    data = data[:, :-1] # remove the class labels
    vectors = np.genfromtxt('Data/train_pca_mat.csv', delimiter=",")
    pca_test = np.matmul(data, vectors)
    new_test_data = np.column_stack((pca_test, class_labels))
    np.savetxt('Data/test_pca.csv', new_test_data, delimiter=',')

testPCA(None)
