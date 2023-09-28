#dowload all files to EOS, make histograms

#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt

print('reading in MC')
MC_loose=pandas.read_csv('csv/MC_loose.csv')

#Pt cuts
MC_loose=MC_loose[(MC_loose['ZM0Pt']>=27)&(MC_loose['ZM1Pt']>=27)]
MC_loose=MC_loose[(MC_loose['FakeEPt']>=27)]
MC_loose=MC_loose[(MC_loose['MET']<=40)]

print('MC length',len(MC_loose),MC_loose['weight'].sum())

MC_tight=MC_loose

#print(len(tight))
MC_tight=MC_tight[MC_tight['FakeEIDTight']==1] #Iso WP
MC_tight=MC_tight[abs(MC_tight['FakeEd0sig'])<=5] #Iso WP
MC_tight=MC_tight[MC_tight['FakeEIsolationFCTight']==1] #Iso WP

print('WZlen',len(MC_tight))
print(MC_tight['weight'].sum())
print(MC_loose['weight'].sum())

print('making histograms')
#make 1D histograms

bins=[0,1,2,3,4,5,6,7,8,9,10,11]
xticks=bins
xticks_labels=['Unknown','KnownUnknown','Prompt electrons','Charge-flip electrons','Prompt muons','Prompt photon-conversions','Electrons from muons','Tau decays','b-hadron decays','c-hadron decays','Light-flavour decays','Charge-flip muons']

plt.figure(3)
fig,ax=plt.subplots()
ax.hist(MC_tight['FakeEID'],bins=bins,align='left',weights=MC_tight['weight']) #weights=MC_tight['weight']
ax.set_xticks(xticks)
ax.set_xticklabels(xticks_labels)
plt.xticks(rotation=-90)
plt.ylabel('# events')
plt.yscale('log')
plt.title('FakeEID')
#plt.yscale('log')
#plt.xlim(40, 160)
#plt.ylim(0, 0.03)
plt.tight_layout()
plt.savefig('pic/FakeEID_tight')
'''
#bins=[0,40,1000]
#plot MET
for i in [tight,loose]:
    fig,ax=plt.subplots()
    #ax.hist(i['FakeMID'],bins=bins,align='left',weights=i['weight']) #,weights=i['weight']
    #ax.hist(i['MET'],bins=bins)
    ax.hist(i['MET'])
    #ax.set_xticks(xticks)
    #ax.set_xticklabels(xticks_labels)
    #plt.xticks(rotation=-90)
    plt.ylabel('# events')
    plt.title('MET')
    plt.axvline(40,c='r')
    plt.tight_layout()
    plt.savefig('pic/FakeMMET_'+i.name)
'''