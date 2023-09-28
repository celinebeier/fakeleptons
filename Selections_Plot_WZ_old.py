#for data, without WZ!! I think this works!!

#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt

##########################################################################################
##### import data, make tight and loose selection

print('reading in data')
loose=pandas.read_csv('csv/Data_loose'+'.csv')
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
name_short='IDTight_IsoFCLoose_d0sig5_MET#'

#print(len(loose))
#loose=loose[loose['FakeEIDTight']==1]
#loose=loose[abs(loose['FakeEd0sig'])<=10]
loose=loose[loose['FakeEIsolationFCLoose']==1]
#print(len(loose))

print('here', len(tight), len(loose))

#important: eta -> abs(eta)
tight['FakeEEta']=abs(tight['FakeEEta'])
loose['FakeEEta']=abs(loose['FakeEEta'])

##########################################################################################
##### determine bin edges
'''
# make historgrams of pt and eta to get resonable binedges
plt.figure(1)
plt.hist(loose['FakeEPt'],bins=50)
#n,bins,patches=plt.hist(loose['FakeEPt'],bins=30)
#print(bins)
plt.xlabel('FakeEPt')
plt.title('Fake Electron Pt')
plt.savefig('pic/HistE_Pt')

plt.figure(2)
plt.hist(loose['FakeEEta'],bins=50)
plt.xlabel('FakeEEta')
plt.title('Fake Electron Eta')
plt.savefig('pic/HistE_Eta')
'''
#define binedges
print(loose['FakeEPt'].max(),loose['FakeEEta'].max())
x_edges=[10,30,600] #pt edges
y_edges=[0,1.1,2.5] #eta edges
edges=[x_edges,y_edges]
'''
#check binedges
plt.figure(3)
plt.hist(loose['FakeEPt'],bins=x_edges)
plt.xlabel('FakeEPt')
plt.title('Fake Electron Pt in bins')
plt.savefig('pic/HistE_Pt_check')

plt.figure(4)
plt.hist(loose['FakeEEta'],bins=y_edges)
plt.xlabel('FakeEEta')
plt.title('Fake Electron Eta in bins')
plt.savefig('pic/HistE_Eta_check')
'''
##########################################################################################
##### import real WZ events

print('reading in WZ MC')
WZ_loose=pandas.read_csv('csv/WZ_loose.csv')

#Pt cuts
WZ_loose=WZ_loose[(WZ_loose['ZM0Pt']>=27)&(WZ_loose['ZM1Pt']>=27)]
WZ_loose=WZ_loose[(WZ_loose['FakeEPt']>=10)]
WZ_loose=WZ_loose[(WZ_loose['MET']<=40)]

#truthmatching 
#WZ_loose=WZ_loose[(WZ_loose['FakeEID']==2)&(WZ_loose['ZM0ID']==4)&(WZ_loose['ZM1ID']==4)]

print('WZlen',len(WZ_loose))
print(WZ_loose['weight'].sum())

'''
WZ_loose=WZ_loose[abs(WZ_loose['FakeEd0sig'])<=10]
WZ_loose=WZ_loose[WZ_loose['FakeEIsolationFCLoose']==1]

WZ_tight=pandas.read_csv('csv/WZ_tight.csv')

#Pt cuts
WZ_tight=WZ_tight[(WZ_tight['FakeEPt']>=27)&(WZ_tight['ZM0Pt']>=27)&(WZ_tight['ZM1Pt']>=27)]
WZ_tight=WZ_tight[(WZ_tight['MET']<=40)]

#truthmatching 
WZ_tight=WZ_tight[(WZ_tight['FakeEID']==2)&(WZ_tight['ZM0ID']==4)&(WZ_tight['ZM1ID']==4)]
'''

WZ_tight=WZ_loose

#print(len(tight))
WZ_tight=WZ_tight[WZ_tight['FakeEIDTight']==1] #Iso WP
WZ_tight=WZ_tight[abs(WZ_tight['FakeEd0sig'])<=5] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeEIsolationFCTight']==1] #Iso WP

#WZ_loose=WZ_loose[abs(WZ_loose['FakeEd0sig'])<=10]
WZ_loose=WZ_loose[WZ_loose['FakeEIsolationFCLoose']==1]

#important: eta -> abs(eta)
WZ_tight['FakeEEta']=abs(WZ_tight['FakeEEta'])
WZ_loose['FakeEEta']=abs(WZ_loose['FakeEEta'])

print('plots comparing data and MC')
print(len(loose),WZ_loose['weight'].sum())
print(len(tight),WZ_tight['weight'].sum())
plt.figure(1)
#plt.hist(loose['FakeEPt'],bins=50,label='data',alpha=0.5)
n,bins,patches=plt.hist(loose['FakeEPt'],label='data',bins=50,alpha=0.5)
plt.hist(WZ_loose['FakeEPt'],bins=bins,weights=WZ_loose['weight'],label='WZ',alpha=0.5)
#n,bins,patches=plt.hist(loose['FakeEPt'],bins=30)
#print(bins)
plt.xlabel('FakeEPt')
plt.title('Fake Electron Pt')
plt.legend()
plt.savefig('pic/HistE_Pt')

plt.figure(2)
#plt.hist(loose['FakeEEta'],bins=50,label='data')
n,bins,patches=plt.hist(loose['FakeEEta'],bins=50,label='data',alpha=0.5)
plt.hist(WZ_loose['FakeEEta'],bins=bins,weights=WZ_loose['weight'],label='WZ',alpha=0.5)
plt.xlabel('FakeEEta')
plt.title('Fake Electron Eta')
plt.legend()
plt.savefig('pic/HistE_Eta')

##########################################################################################
##### make histograms, calculate efficiency, plot

#make 2d histograms with the respective binedges
print('making histograms')
print(edges)

hist_tight,xbins_tight,ybins_tight,im_tight=plt.hist2d(tight['FakeEPt'], tight['FakeEEta'], bins=edges)
hist_loose,xbins_loose,ybins_loose,im_loose=plt.hist2d(loose['FakeEPt'], loose['FakeEEta'], bins=edges)
#print(xbins_tight,xbins_loose)
#hist_tight,xbins_tight,ybins_tight,im_tight=plt.hist2d(tight['FakeEPt'], tight['FakeEEta'], bins=(x_edges,y_edges))
#hist_loose,xbins_loose,ybins_loose,im_loose=plt.hist2d(loose['FakeEPt'], loose['FakeEEta'], bins=(x_edges,y_edges))

hist_WZ_tight,xbins_WZ_tight,ybins_WZ_tight,im_WZ_tight=plt.hist2d(WZ_tight['FakeEPt'], abs(WZ_tight['FakeEEta']), bins=edges, weights=WZ_tight['weight'])
hist_WZ_loose,xbins_WZ_loose,ybins_WZ_loose,im_WZ_loose=plt.hist2d(WZ_loose['FakeEPt'], abs(WZ_loose['FakeEEta']), bins=edges, weights=WZ_loose['weight'])
print('check1',hist_tight,hist_WZ_tight)
print('check2',hist_loose,hist_WZ_loose)

#make transpose for plotting
hist_tight=hist_tight.T
hist_loose=hist_loose.T
hist_WZ_tight=hist_WZ_tight.T
hist_WZ_loose=hist_WZ_loose.T

#calculate fake eff by dividing the tight histogram with the loose histogram
print('calculate fake efficiency')
print(hist_tight,hist_WZ_tight)
num=hist_tight-hist_WZ_tight
denom=hist_loose-hist_WZ_loose
fakeeff=num/denom
print(fakeeff)

#calculate errors    
print('calculate errors')
errorfakeeff=1/denom*np.sqrt(num*(1-num/denom))

#plot the given histrogram with the given binedges
print('plot the results')
c=np.array(fakeeff) #make array for plotting
plt.figure(5)
fig, ax = plt.subplots()
a=[x_edges[0],x_edges[0]+(x_edges[-1]-x_edges[0])/2,x_edges[-1]] #but make the diagram equal sizes
b=[y_edges[0],y_edges[0]+(y_edges[-1]-y_edges[0])/2,y_edges[-1]]
print(a,b)
x,y=np.meshgrid(a,b)
bar=plt.pcolormesh(x,y,fakeeff,cmap=plt.cm.jet)
plt.clim(0,1) #sets limits for colorbar
fig.colorbar(bar, ax=ax)
plt.xlabel('FakeEPt')
plt.xticks(a,x_edges)
plt.yticks(b,y_edges)
plt.ylabel('FakeEEta')
plt.title('FakeE '+name)

#print values !! add errors
for i in range(fakeeff.shape[0]):
    for j in range(fakeeff.shape[1]):
        #print(fakeeff[i,j])
        xpos=(a[j]+a[j+1])/2 -50 #-50 to account for length of text
        ypos=(b[i]+b[i+1])/2
        #print(xpos,ypos)
        label=str(round(fakeeff[i,j],2)) + "+-" + str(round(errorfakeeff[i,j],2)) # + '/(' + str(num[i,j])+ '+'+str(denom[i,j]) + ')'
        ax.text(xpos, ypos, label)

print('save')
plt.savefig('pic/FakeEfficiencyE')
