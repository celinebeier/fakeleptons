#for data only, without WZ

#import ROOT
import numpy as np
import uproot as ur
import pandas
import os
from MC_Weights import MC_Weights

branches_FakeL=['ElectronCounter','MuonCounter','FakeEPt','FakeMPt','FakeEEta','FakeMEta']
branches_Selection=['FakeEIsolationFCTight','FakeEIsolationFCLoose',
                    'FakeMIsolationFCTight','FakeMIsolationFCLoose',
                    'FakeEIDTight','FakeEIDMedium','FakeMQualityTight',
                    'FakeMd0sig','FakeEd0sig']
branches_MC=['FakeEID','FakeMID','ZE0ID','ZE1ID','ZM0ID','ZM1ID']
branches_PT=['ZE0Pt','ZE1Pt','ZM0Pt','ZM1Pt','MET']
branches_test=['eventNumber']

branches=branches_FakeL+branches_Selection+branches_PT+branches_MC
branches1=branches_FakeL+branches_Selection+branches_PT

####### data

data_dir='/eos/user/c/cbeier/results/230418_Data17_FakeE/'

data_filepaths=[]

#find the right file paths with the correct name
for path in os.listdir(data_dir):
    print(path)
    data_filepaths.append(data_dir+path+'/')
print(data_filepaths)

data_tight=pandas.DataFrame(columns=branches1)
data_loose=pandas.DataFrame(columns=branches1)

#loop through file paths
for path in data_filepaths:
    #prep data into pd.dataframe
    file=path+'*.root' #all files in the directory
    print('reading in data for',path)
    #read in data and make a dataframe
    tight = ur.pandas.iterate(file, treepath='nominal', branches=branches1)
    loose = ur.pandas.iterate(file, treepath='nominal_Loose', branches=branches1)

    tight = pandas.concat([d for d in tight])
    loose = pandas.concat([d for d in loose])

    print('saving events for',path)
    data_tight=data_tight.append(tight)
    data_loose=data_loose.append(loose)
    #save to one csv file

print('saving data')
data_tight.to_csv('csv/data_tight'+'.csv', index=False)
data_loose.to_csv('csv/data_loose'+'.csv', index=False)

#### MC

WZ_dir='/eos/user/c/cbeier/results/230421_WZ17_FakeE/'

WZ_filepaths=[]

#find the right file paths with the correct name
for path in os.listdir(WZ_dir):
    print(path)
    WZ_filepaths.append(WZ_dir+path+'/')
print('WZ_filepaths',WZ_filepaths)

WZ_tight=pandas.DataFrame(columns=branches)
WZ_loose=pandas.DataFrame(columns=branches)

#loop through file paths
for path in WZ_filepaths:
    #prep data into pd.dataframe
    file=path+'*.root' #all files in the directory
    print('reading in data for',path)
    #read in data and make a dataframe
    tight = ur.pandas.iterate(file, treepath='nominal', branches=branches)
    loose = ur.pandas.iterate(file, treepath='nominal_Loose', branches=branches)

    tight = pandas.concat([d for d in tight])
    loose = pandas.concat([d for d in loose])
    
    print('getting MC weights')
    print(path)
    #get weights and add them to the dataframe
    weight_tight=MC_Weights(path,'tight','2017')
    weight_loose=MC_Weights(path,'loose','2017')

    tight=pandas.concat([tight, weight_tight], axis=1)
    loose=pandas.concat([loose, weight_loose], axis=1)

    print('saving events for',path)
    WZ_tight=WZ_tight.append(tight)
    WZ_loose=WZ_loose.append(loose)
    #save to one csv file

print('saving MC')
WZ_tight.to_csv('csv/WZ_tight'+'.csv', index=False)
WZ_loose.to_csv('csv/WZ_loose'+'.csv', index=False)
