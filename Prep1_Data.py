import numpy as np
import uproot as ur
import pandas
import os
from MC_Weights import MC_Weights

dir='/eos/user/c/cbeier/results/230724_WZ17_FakeM/'
name='WZ17'
csv='csv_FakeM'
isMC=True
year='2017'

branches_FakeL=['ElectronCounter','MuonCounter','FakeEPt','FakeMPt','FakeEEta','FakeMEta']
branches_Selection=['FakeEIsolationFCTight','FakeEIsolationFCLoose',
                    'FakeMIsolationFCTight','FakeMIsolationFCLoose',
                    'FakeEIDTight','FakeEIDMedium','FakeMQualityTight',
                    'FakeMd0sig','FakeEd0sig']
branches_MC=['FakeEID','FakeMID','ZE0ID','ZE1ID','ZM0ID','ZM1ID']
branches_PT=['ZE0Pt','ZE1Pt','ZM0Pt','ZM1Pt','MET']
branches_test=['eventNumber']

branches=branches_FakeL+branches_Selection+branches_PT+branches_MC

#find the right file paths with the correct name
filepaths=[]

for path in os.listdir(dir):
    print(path)
    filepaths.append(dir+path+'/')
print('filepaths:',filepaths)

#tight=pandas.DataFrame(columns=branches+['weight'])
loose=pandas.DataFrame(columns=branches+['weight'])

#loop through file paths
for path in filepaths:
    #prep data into pd.dataframe
    file=path+'*.root' #all files in the directory
    print('reading in data for',path)
    #read in data and make a dataframe
    #path_tight = ur.pandas.iterate(file, treepath='nominal', branches=branches)
    path_loose = ur.pandas.iterate(file, treepath='nominal_Loose', branches=branches)

    #path_tight = pandas.concat([d for d in path_tight])
    path_loose = pandas.concat([d for d in path_loose])
    
    if isMC:
        print('getting MC weights for', path)
        #get weights and add them to the dataframe
        #weight_tight=MC_Weights(path,'tight',year)
        weight_loose=MC_Weights(path,'loose',year)

        #path_tight=pandas.concat([path_tight, weight_tight], axis=1)
        path_loose=pandas.concat([path_loose, weight_loose], axis=1)
    else:
        #path_tight['weight'] = 1
        path_loose['weight'] = 1

    print('saving events for',path)
    #tight=tight.append(path_tight)
    loose=loose.append(path_loose)

#save to one csv file
print('saving events')
#tight.to_csv('/eos/user/c/cbeier/'+csv+'/'+name+'_tight'+'.csv', index=False)
loose.to_csv('/eos/user/c/cbeier/'+csv+'/'+name+'_loose'+'.csv', index=False)
