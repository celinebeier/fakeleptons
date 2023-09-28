import numpy as np
import uproot as ur
import pandas
import os
from MC_Weights import MC_Weights

dir='/eos/user/c/cbeier/results/230730_addMC17_FakeERegions/'
name='Regions_add2MC17'
csv='csv'
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
branches_FakeN=['E1Pt','E1Eta','E1ID','E1IsolationFCTight','E1IsolationFCLoose','E1IDTight','E1IDMedium','E1d0sig',
                'E2Pt','E2Eta','E2ID','E2IsolationFCTight','E2IsolationFCLoose','E2IDTight','E2IDMedium','E2d0sig',
                'M1Pt','M1Eta','M1ID','M1IsolationFCTight','M1IsolationFCLoose','M1QualityTight','M1d0sig',
                'M2Pt','M2Eta','M2ID','M2IsolationFCTight','M2IsolationFCLoose','M2QualityTight','M2d0sig',
                'SRSelection','VRSelection','WyCRSelection','ZjetsCRSelection','WjetsCRSelection','ZyCRSelection',
                'invmWy_fit','M27Counter','E27Counter']

branches=branches_FakeL+branches_Selection+branches_PT+branches_MC+branches_FakeN

#find the right file paths with the correct name
filepaths=[]

events=[]

for path in os.listdir(dir):
    print(path)
    filepaths.append(dir+path+'/')
    
    eventsinfile=[]
    
    for a in os.listdir(dir+path):
        print(a)
        #files.append(path+file)
        datafile = ur.open(dir+path+'/'+a)
        tree = datafile['nominal_Loose']
        data=tree.pandas.df(branches)
        eventsinfile.append(data)
        
    eventsinfile=pandas.concat(eventsinfile, axis=0)
    eventsinfile = eventsinfile.reset_index(drop=True)
    
    if isMC:
        print('getting MC weights for', path)
        #get weights and add them to the dataframe
        weight_loose=MC_Weights(dir+path+'/','loose',year)

        eventsinfile=pandas.concat([eventsinfile, weight_loose], axis=1)
    else:
        eventsinfile['weight'] = 1
    
    events.append(eventsinfile)
      
events=pandas.concat(events, axis=0)
events= events.reset_index(drop=True)
print(len(events))
#print(events)

print('saving events')
events.to_csv('/eos/user/c/cbeier/'+csv+'/'+name+'_loose'+'.csv', index=False)
