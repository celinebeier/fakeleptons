#for data only, without WZ

#import ROOT
import numpy as np
import uproot as ur
import pandas
import os
from MC_Weights import MC_Weights

eosdir='/eos/user/c/cbeier/results/230421_WZ17_FakeE/'

filename='cbeier'
#filename='user.cbeier.700321.Sh.DAOD_PHYS.e8351_s3126_r9364_p5001.221004_ZjetsMC_TruthComposition_FakeM_NewSamples_output_FakeM_root'

filepaths=[]

#find the right file paths with the correct name
for path in os.listdir(eosdir):
    if filename in path: #select only files with the right name
        print(path)
        filepaths.append(eosdir+path+'/')
    else: continue #skip other files
print(filepaths)

branches_FakeL=['ElectronCounter','MuonCounter','FakeEPt','FakeMPt','FakeEEta','FakeMEta']
branches_Selection=['FakeEIsolationFCTight','FakeEIsolationFCLoose',
                    'FakeMIsolationFCTight','FakeMIsolationFCLoose',
                    'FakeEIDTight','FakeEIDMedium','FakeMQualityTight',
                    'FakeMd0sig','FakeEd0sig']
branches_PT=['ZE0Pt','ZE1Pt','ZM0Pt','ZM1Pt','MET']
branches_test=['eventNumber','Invm']

branches=branches_test+branches_FakeL+branches_PT+branches_Selection

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
tight.to_csv('csv/Zpeak_tight'+'.csv', index=False)
loose.to_csv('csv/Zpeak_loose'+'.csv', index=False)