#import ROOT
import numpy as np
import uproot as ur
import pandas
import matplotlib.pyplot as plt
from MC_Weights import MC_Weights

fakes=['FakeM'] #fakes=['FakeM','FakeE']

for f in fakes:
    data_input='/afs/cern.ch/user/c/cbeier/AnalysisTop/run/*'+f+'.root' #all files in the directory
    WZ_input='/afs/cern.ch/user/c/cbeier/AnalysisTop/run/*'+f+'.root'
    WZ_dir='/afs/cern.ch/user/c/cbeier/AnalysisTop/run/' #copy WZ_input, but only specify folder here. could be done better.

    branches=['FakeEPt','FakeMPt','FakeEEta','FakeMEta']

    print('reading in data')
    data_tight = ur.pandas.iterate(data_input, treepath='nominal', branches=branches)
    data_loose = ur.pandas.iterate(data_input, treepath='nominal_Loose', branches=branches)

    data_tight = pandas.concat([d for d in data_tight])
    data_loose = pandas.concat([d for d in data_loose])

    print('saving data')
    data_tight.to_csv('data_tight_'+f+'.csv', index=False)
    data_loose.to_csv('data_loose_'+f+'.csv', index=False)

    print('reading in WZ MC')
    WZ_tight = ur.pandas.iterate(WZ_input, treepath='nominal', branches=branches)
    WZ_loose = ur.pandas.iterate(WZ_input, treepath='nominal_Loose', branches=branches)

    WZ_tight = pandas.concat([d for d in WZ_tight])
    WZ_loose = pandas.concat([d for d in WZ_loose])

    print('getting MC weights')
    #get weights and add them to the dataframe
    weight_tight=MC_Weights(WZ_dir,f,'tight','2016')
    weight_loose=MC_Weights(WZ_dir,f,'loose','2016')

    WZ_tight=pandas.concat([WZ_tight, weight_tight], axis=1)
    WZ_loose=pandas.concat([WZ_loose, weight_loose], axis=1)

    print('saving WZ MC')
    #print(WZ_tight, WZ_loose)
    WZ_tight.to_csv('WZ_tight_'+f+'.csv', index=False)
    WZ_loose.to_csv('WZ_loose_'+f+'.csv', index=False)