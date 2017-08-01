'''
Created on Nov 21, 2016

@author: xuwang
'''
from numpy import recfromcsv

gcpFile = recfromcsv("F:/Xu/2017_RF_BYD_GCPs.csv",delimiter=',')
for gcp in gcpFile:
    print(gcp[2])
