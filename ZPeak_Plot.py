#for data, without WZ!! I think this works!!

#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt

print('reading in data')
#only use loose sleection
loose=pandas.read_csv('csv/Zpeak_loose_Data'+'.csv')
loose.name='loose'

#add PT cuts: 15GeV
print(len(loose))
loose=loose[(loose['ZM0Pt']>=27)&(loose['ZM1Pt']>=27)]
loose=loose[(loose['FakeEPt']>=10)]
loose=loose[(loose['MET']<=40)]
print(len(loose))

#make tight selection
tight=loose

#print(len(tight))
tight=tight[tight['FakeEIDTight']==1] #Iso WP
tight=tight[abs(tight['FakeEd0sig'])<=5] #Iso WP
tight=tight[tight['FakeEIsolationFCTight']==1] #Iso WP
print(len(tight))

#here: make alterations to loose dataframe to account for different selections
name='ID:Tight, Iso:FCLoose, d0sig<10, MET:40'
#name_short='IDTight_IsoFCLoose_d0sig5_MET#'

print(len(loose))
#loose=loose[loose['FakeEIDTight']==1]
#loose=loose[abs(loose['FakeEd0sig'])<=10]
loose=loose[loose['FakeEIsolationFCLoose']==1]
print(len(loose))

print('here', len(tight),len(loose))

#add MET cut

#important: eta -> abs(eta)
tight['FakeEdEta']=abs(tight['FakeEEta'])
loose['FakeEEta']=abs(loose['FakeEEta'])

print('reading in MC')
#only use loose sleection
WZ_loose=pandas.read_csv('csv/Zpeak_loose'+'.csv')
WZ_loose.name='loose'

#add PT cuts: 15GeV
print(len(loose))
WZ_loose=WZ_loose[(WZ_loose['ZM0Pt']>=27)&(WZ_loose['ZM1Pt']>=27)]
WZ_loose=WZ_loose[(WZ_loose['FakeEPt']>=10)]
WZ_loose=WZ_loose[(WZ_loose['MET']<=40)]
print(len(loose))

#make tight selection

WZ_tight=WZ_loose

#print(len(tight))
WZ_tight=WZ_tight[WZ_tight['FakeEIDTight']==1] #Iso WP
WZ_tight=WZ_tight[abs(WZ_tight['FakeEd0sig'])<=5] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeEIsolationFCTight']==1] #Iso WP
print(len(WZ_tight))

#loose=loose[loose['FakeEIDTight']==1]
WZ_loose=WZ_loose[abs(WZ_loose['FakeEd0sig'])<=10]
WZ_loose=WZ_loose[WZ_loose['FakeEIsolationFCLoose']==1]

print('here',WZ_tight['weight'].sum(),WZ_loose['weight'].sum())

#add MET cut

#important: eta -> abs(eta)
WZ_tight['FakeEdEta']=abs(WZ_tight['FakeEEta'])
WZ_loose['FakeEEta']=abs(WZ_loose['FakeEEta'])

#make historgrams of pt and eta to get resonable binedges
plt.figure(1)
n,bins,patches=plt.hist(WZ_tight['Invm'],bins=50,weights=WZ_tight['weight'],label='WZ',alpha=0.5)
plt.hist(tight['Invm'],bins=bins,label='data',alpha=0.5)
#print(bins)
plt.xlabel('Invariant Mass Z leptons')
plt.title('Z Peak')
plt.legend()
plt.savefig('pic/ZPeak_Tight')

plt.figure(2)
n,bins,patches=plt.hist(WZ_loose['Invm'],bins=50,weights=WZ_loose['weight'],label='WZ',alpha=0.5)
plt.hist(loose['Invm'],bins=bins,label='data',alpha=0.5)
#print(bins)
plt.xlabel('Invariant Mass Z leptons')
plt.title('Z Peak')
plt.legend()
plt.savefig('pic/ZPeak_Loose')
