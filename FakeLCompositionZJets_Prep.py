#dowload all files to EOS, make histograms

#import ROOT
import numpy as np
import uproot as ur
import os
import pandas
import matplotlib.pyplot as plt
from MC_Weights import MC_Weights

eosdir='/eos/user/c/cbeier/results/230422_MC17_FakeE/'

filepaths=[]

#find the right file paths with the correct name
for path in os.listdir(eosdir):
    print(path)
    filepaths.append(eosdir+path+'/')
print(filepaths)

branches_FakeL=['ElectronCounter','MuonCounter','FakeEPt','FakeMPt','FakeEEta','FakeMEta']
branches_Selection=['FakeEIsolationFCTight','FakeEIsolationFCLoose',
                    'FakeMIsolationFCTight','FakeMIsolationFCLoose',
                    'FakeEIDTight','FakeEIDMedium','FakeMQualityTight',
                    'FakeMd0sig','FakeEd0sig']
branches_MC=['FakeEID','FakeMID','ZE0ID','ZE1ID','ZM0ID','ZM1ID']
branches_PT=['ZE0Pt','ZE1Pt','ZM0Pt','ZM1Pt','MET']
branches_test=['eventNumber']

branches=branches_FakeL+branches_Selection+branches_PT+branches_MC

tight=pandas.DataFrame(columns=branches+['weight'])
loose=pandas.DataFrame(columns=branches+['weight'])

#loop through file paths
for path in filepaths:
    #prep data into pd.dataframe
    file=path+'*.root' #all files in the directory
    print('reading in data for',path)
    #read in data and make a dataframe
    data_tight = ur.pandas.iterate(file, treepath='nominal', branches=branches)
    data_loose = ur.pandas.iterate(file, treepath='nominal_Loose', branches=branches)

    data_tight = pandas.concat([d for d in data_tight])
    data_loose = pandas.concat([d for d in data_loose])

    print('getting MC weights for',path)
    #get weights and add them to the dataframe
    weight_tight=MC_Weights(path,'tight','2017')
    weight_loose=MC_Weights(path,'loose','2017')

    data_tight=pandas.concat([data_tight, weight_tight], axis=1)
    data_loose=pandas.concat([data_loose, weight_loose], axis=1)

    print('saving events for',path)
    tight=tight.append(data_tight)
    loose=loose.append(data_loose)
    #save to one csv file

print('saving data')
tight.to_csv('csv/MC_tight'+'.csv', index=False)
loose.to_csv('csv/MC_loose'+'.csv', index=False)