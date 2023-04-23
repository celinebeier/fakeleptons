#import ROOT
import numpy as np
import uproot as ur
import pandas
import matplotlib.pyplot as plt

print('reading in data')
data_tight=pandas.read_csv('cvs/data_tight'+'.csv')
data_loose=pandas.read_csv('cvs/data_loose'+'.csv')

print('making histograms')
#make 1D histograms

bins=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5]

plt.hist(data_tight['FakeMID'],bins=bins,weights=data_tight['weight'])
plt.xlabel('FakeMID')
plt.ylabel('# events')
plt.title('FakeMID')
#plt.xlim(40, 160)
#plt.ylim(0, 0.03)
plt.savefig('pic/FakeMID_tight')

plt.hist(data_loose['FakeMID'],bins=bins,weights=data_loose['weight'])
plt.xlabel('FakeMID')
plt.ylabel('# events')
plt.title('FakeMID')
#plt.xlim(40, 160)
#plt.ylim(0, 0.03)
plt.savefig('pic/FakeMID_loose')