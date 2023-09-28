#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt

print('reading in MC')
MC_loose_1=pandas.read_csv('/eos/user/c/cbeier/csv/SR_MC17_loose.csv')
MC_loose_2=pandas.read_csv('/eos/user/c/cbeier/csv/SR_addMC17_loose.csv')
MC_loose_3=pandas.read_csv('/eos/user/c/cbeier/csv/SR_add2MC17_loose.csv')

MC_loose=pandas.concat([MC_loose_1, MC_loose_2, MC_loose_3])
print(len(MC_loose))

MC_loose=MC_loose[(MC_loose['E27Counter']==1)]

#add PT cuts
#MC_loose=MC_loose[(MC_loose['ZM0Pt']>=27)&(MC_loose['ZM1Pt']>=27)]
#MC_loose=MC_loose[(MC_loose['FakeEPt']>=10)]
#MC_loose=MC_loose[(MC_loose['MET']<=40)]
MC_loose=MC_loose[(MC_loose['E1Pt']>=27)]

#loose cut
#MC_loose=MC_loose[(MC_loose['FakeEd0sig']<=5)]
MC_loose=MC_loose[(MC_loose['E1d0sig']<=5)]

#eta -> abs(eta)
#MC_loose['FakeEEta']=abs(MC_loose['FakeEEta'])
MC_loose['E1Eta']=abs(MC_loose['E1Eta'])

#tight selection
MC_tight=MC_loose 

#make tight selection - don't touch! 
MC_tight=MC_tight[MC_tight['E1IDTight']==1] #Iso WP
MC_tight=MC_tight[MC_tight['E1d0sig']<=5] #Iso WP
MC_tight=MC_tight[MC_tight['E1IsolationFCTight']==1] #Iso WP
#MC_tight=MC_tight[MC_tight['E1ID']==2] #Iso WP

print('making histograms')
#make 1D histograms

bins=[0,1,2,3,4,5,6,7,8,9,10,11]
xticks=bins
xticks_labels=['Unknown','KnownUnknown','Prompt electrons','Charge-flip electrons','Prompt muons','Prompt photon-conversions','Electrons from muons','Tau decays','b-hadron decays','c-hadron decays','Light-flavour decays','Charge-flip muons']

plt.figure(1)
fig,ax=plt.subplots()
n,bins,patches=ax.hist(MC_tight['E1ID'],bins=bins,align='left',weights=MC_tight['weight']) #weights=MC_tight['weight']
print(n)
ax.set_xticks(xticks)
ax.set_xticklabels(xticks_labels)
plt.xticks(rotation=-90)
plt.ylabel('# events')
plt.ylim(0.1, 10000)
plt.yscale('log')
#plt.title('FakeEID')
plt.tight_layout()
plt.savefig('root/EID_tight_SR_add2')
'''
plt.figure(2)
fig,ax=plt.subplots()
ax.hist(MC_loose['E1ID'],bins=bins,align='left',weights=MC_loose['weight']) #weights=MC_tight['weight']
ax.set_xticks(xticks)
ax.set_xticklabels(xticks_labels)
plt.xticks(rotation=-90)
plt.ylabel('# events')
plt.yscale('log')
plt.title('FakeEID')
plt.tight_layout()
plt.savefig('root/FakeEID_loose_VR')
'''