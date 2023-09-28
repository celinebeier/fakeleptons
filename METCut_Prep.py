#import ROOT
import numpy as np
import uproot as ur
import pandas
import matplotlib.pyplot as plt
from MC_Weights import MC_Weights

f='FakeM' #fakes=['FakeM','FakeE']

data_dir='/eos/user/c/cbeier/results/user.cbeier.700321.Sh.DAOD_PHYS.e8351_s3126_r9364_p5001.221004_ZjetsMC_TruthComposition_FakeM_NewSamples_output_FakeM_root/'
data_input=data_dir+'*.root' #all files in the directory
print(data_input)

branches=['FakeEID','FakeMID','MET']

print('reading in data')
#read in data and make a dataframe
data_tight = ur.pandas.iterate(data_input, treepath='nominal', branches=branches)
data_loose = ur.pandas.iterate(data_input, treepath='nominal_Loose', branches=branches)

data_tight = pandas.concat([d for d in data_tight])
data_loose = pandas.concat([d for d in data_loose])

print('getting MC weights')
#get weights and add them to the dataframe
weight_tight=MC_Weights(data_dir,'tight','2016')
weight_loose=MC_Weights(data_dir,'loose','2016')

data_tight=pandas.concat([data_tight, weight_tight], axis=1)
data_loose=pandas.concat([data_loose, weight_loose], axis=1)

print('saving data')
data_tight.to_csv('cvs/data_tight'+'.csv', index=False)
data_loose.to_csv('cvs/data_loose'+'.csv', index=False)