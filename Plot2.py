
import numpy as np
import pandas
import matplotlib.pyplot as plt
import ROOT
from array import array

print('reading in data')

inputPath="/eos/user/c/cbeier/results/230310_Data16B_FakeE/user.cbeier.periodB.physics_Main.DAOD_PHYS.grp16_v01_p5314.230310_Data16B_FakeE_output_FakeE_root/"

chainName_tight="nominal"
chain_tight=ROOT.TChain(chainName_tight)
chain_tight.Add(inputPath+"*.root") #loop for multiple files

chainName_loose="nominal_Loose"
chain_loose=ROOT.TChain(chainName_loose)
chain_loose.Add(inputPath+"*.root") #loop for multiple files

print(chain_tight.GetEntries())

list_events=[1417308731.0,1336849883.0,633056496.0,1891546255.0,709057206.0,515927285.0]

loose=[]
'''
for entryNum in range(0,chain_loose.GetEntries()):
    chain_loose.GetEntry(entryNum)
    evNum=getattr(chain_loose,"eventNumber")
    loose.append(evNum)
    
print(loose)
        
for entryNum in range(0,chain_tight.GetEntries()):
    chain_tight.GetEntry(entryNum)
    evNum=getattr(chain_tight,"eventNumber")
    if evNum in loose: 
        continue
    else: 
        print(evNum)

'''
for entryNum in range(0,chain_tight.GetEntries()):
    chain_tight.GetEntry(entryNum)
    evNum=getattr(chain_tight,"eventNumber")
    if evNum not in list_events: 
        continue
    else: 
        print('tight')
        print(evNum)
        
for entryNum in range(0,chain_loose.GetEntries()):
    chain_loose.GetEntry(entryNum)
    evNum=getattr(chain_loose,"eventNumber")
    if evNum not in list_events: 
        continue
    else: 
        print('loose')
        print(evNum)
        