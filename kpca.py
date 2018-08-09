import numpy as np
from scipy.linalg import eigh
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

def get_kernel(sigma=100):
    def kernel(x0, x1):
        return np.exp(- sigma * ((x0 - x1) ** 2)) # Gaussian kernel
        #return (np.dot(x0,x1) + 1) ** sigma # Polynomial kernel
        #return np.dot(x0,x1) # Linear kernel
    return kernel

def kpca(df, kernel): # Karnel PCA
    N = len(df)
    k0 = np.zeros(shape=(N,N))

    for n0, x0 in df.iterrows():
        for n1, x1 in df.iterrows():
            k0[n0,n1] = kernel(x0, x1)

    one_n = np.ones(shape=(N,N)) / N
    gram = k0 - one_n.dot(k0) - k0.dot(one_n) + one_n.dot(k0).dot(one_n)
    eigvals, eigvecs = eigh(gram)
    
    def projection(x, i):
        pc = 0
        for n in range(N):
            pc += eigvecs[n,-i] * kernel(x, train_data.iloc[n])
        return pc / np.sqrt(eigvals[-i] * N)
    return projection