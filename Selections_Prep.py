#for data only, without WZ

#import ROOT
import numpy as np
import uproot as ur
import pandas
import os

eosdir='/eos/user/c/cbeier/results/230414_Data16_FakeE/'

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
                    'FakeMd0sig','FakeEd0sig','MET']
branches_PT=['ZE0Pt','ZE1Pt','ZM0Pt','ZM1Pt']
branches_test=['eventNumber']

branches=branches_FakeL+branches_Selection+branches_PT

tight=pandas.DataFrame(columns=branches)
loose=pandas.DataFrame(columns=branches)

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

    print('saving events for',path)
    tight=tight.append(data_tight)
    loose=loose.append(data_loose)
    #save to one csv file

print('saving data')
tight.to_csv('csv/tight'+'.csv', index=False)
loose.to_csv('csv/loose'+'.csv', index=False)