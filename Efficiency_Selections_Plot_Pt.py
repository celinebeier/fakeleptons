#for data, without WZ!!

#make histograms of a specific parameter

#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt

print('reading in data')
tight=pandas.read_csv('cvs/data_tight_selections'+'.csv')
tight.name='tight'
loose=pandas.read_csv('cvs/data_loose_selections'+'.csv')
loose.name='loose'

#tight=tight[tight['FakeMPt']>25]
#tight=tight[tight['ZE0Pt']>25]
#tight=tight[tight['ZE1Pt']>25]

number=len(tight)
print(number)

#make 1D histogram
print('make histogram')
plt.hist(tight['FakeMPt'],alpha=0.5,label='FakeM')
#plt.hist(loose['FakeMPt'],alpha=0.5)
plt.hist(tight['ZE0Pt'],alpha=0.5,label='RealE')
plt.hist(tight['ZE1Pt'],alpha=0.5,label='RealE')
plt.xlabel('Pt in GeV')
plt.ylabel('#')
plt.title('Lepton Pt/')
plt.vlines(15,0,50)
plt.vlines(27,0,50)
plt.legend()
plt.savefig('pic/Pt25')