#dowload all files to EOS, make histograms

#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt

print('reading in MC')
MC_loose=pandas.read_csv('/eos/user/c/cbeier/csv_FakeM/MC_loose.csv')

#add PT cuts
MC_loose=MC_loose[(MC_loose['ZE0Pt']>=27)&(MC_loose['ZE1Pt']>=27)]
MC_loose=MC_loose[(MC_loose['FakeMPt']>=10)]
MC_loose=MC_loose[(MC_loose['MET']<=40)]

#loose cut
MC_loose=MC_loose[(MC_loose['FakeMd0sig']<=3)]

#eta -> abs(eta)
MC_loose['FakeMEta']=abs(MC_loose['FakeMEta'])

#tight selection
MC_tight=MC_loose 

#make tight selection - don't touch! 
MC_tight=MC_tight[MC_tight['FakeMQualityTight']==1] #Iso WP
MC_tight=MC_tight[MC_tight['FakeMd0sig']<=5] #Iso WP
MC_tight=MC_tight[MC_tight['FakeMIsolationFCTight']==1] #Iso WP

print('making histograms')
#make 1D histograms

bins=[0,1,2,3,4,5,6,7,8,9,10,11]
xticks=bins
xticks_labels=['Unknown','KnownUnknown','Prompt electrons','Charge-flip electrons','Prompt muons','Prompt photon-conversions','Electrons from muons','Tau decays','b-hadron decays','c-hadron decays','Light-flavour decays','Charge-flip muons']

plt.figure(1)
fig,ax=plt.subplots()
ax.hist(MC_tight['FakeMID'],bins=bins,align='left',weights=MC_tight['weight']) #weights=MC_tight['weight']
ax.set_xticks(xticks)
ax.set_xticklabels(xticks_labels)
plt.xticks(rotation=-90)
plt.ylabel('# events')
plt.yscale('log')
plt.title('FakeEID')
plt.tight_layout()
plt.savefig('root_FakeM/FakeMID_tight')

plt.figure(2)
fig,ax=plt.subplots()
ax.hist(MC_loose['FakeMID'],bins=bins,align='left',weights=MC_loose['weight']) #weights=MC_tight['weight']
ax.set_xticks(xticks)
ax.set_xticklabels(xticks_labels)
plt.xticks(rotation=-90)
plt.ylabel('# events')
plt.yscale('log')
plt.title('FakeEID')
plt.tight_layout()
plt.savefig('root_FakeM/FakeMID_loose')