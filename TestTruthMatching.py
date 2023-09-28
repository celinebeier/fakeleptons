#import ROOT
import numpy as np
import uproot as ur
import pandas
import matplotlib.pyplot as plt

file = ur.open("/afs/cern.ch/user/c/cbeier/AnalysisTop/run/output_all.root")

events=file['nominal']

#events.show()

array=events.array('leptonTruthTypeCondensed')

#print(array)
print('events=',len(array))

notTruth=0

for i in np.arange(0,len(array),1):
    if (array[i][0]==2 or array[i][0]==4) and (array[i][1]==2 or array[i][1]==4) and (array[i][2]==2 or array[i][2]==4):
        continue;
    else:
        notTruth=notTruth+1

print('notTruthMatchedEvents=',notTruth)

#file=uproot.open('/afs/cern.ch/user/c/cbeier/AnalysisTop/run/output.root')

#inputFile="/afs/cern.ch/user/c/cbeier/AnalysisTop/run/output.root"

#branches=['ElectronCounter','leptonTruthTypeCondensed']

#data_tight = ur.pandas.iterate(inputFile, treepath='nominal', branches=branches)

#data_tight = pandas.concat([d for d in data_tight])

#fakeE='ElectronCounter==1'
#fakeM='ElectronCounter==2'

#data_tight_fakeE = data_tight.query(fakeE)

#data_tight_fakeE.to_csv('data_tight_fakeE.csv', index=False)