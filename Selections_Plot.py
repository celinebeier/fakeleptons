#for data, without WZ!! I think this works!!

#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt

print('reading in data')
#only use loose sleection
loose=pandas.read_csv('csv/loose'+'.csv')
loose.name='loose'

#add PT cuts: 15GeV
print(len(loose))
loose=loose[(loose['ZM0Pt']>=27)&(loose['ZM1Pt']>=27)]
loose=loose[(loose['FakeEPt']>=15)]
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
loose=loose[abs(loose['FakeEd0sig'])<=10]
loose=loose[loose['FakeEIsolationFCLoose']==1]
print(len(loose))

print('here', len(tight),len(loose))

#add MET cut

#important: eta -> abs(eta)
tight['FakeEdEta']=abs(tight['FakeEEta'])
loose['FakeEEta']=abs(loose['FakeEEta'])

#make historgrams of pt and eta to get resonable binedges
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

#define binedges
print(loose['FakeEPt'].max(),loose['FakeEEta'].max())
x_edges=[27,50,400] #pt edges
y_edges=[0,1.1,2.5] #eta edges

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

#make 2d histograms with the respective binedges
print('making histograms')
hist_tight,xbins_tight,ybins_tight,im_tight=plt.hist2d(tight['FakeEPt'], abs(tight['FakeEEta']), bins=(x_edges,y_edges))
hist_loose,xbins_loose,ybins_loose,im_loose=plt.hist2d(loose['FakeEPt'], abs(loose['FakeEEta']), bins=(x_edges,y_edges))
#print(xbins_tight,ybins_tight,hist_tight,hist_loose)

print(hist_tight, hist_loose)

#make transpose for plotting
hist_tight=hist_tight.T
hist_loose=hist_loose.T

#calculate fake eff by dividing the tight histogram with the loose histogram
print('calculate fake efficiency')
num=hist_tight
denom=hist_loose
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

'''
#plot the given histrogram with the given binedges
print('plot the results')
c=np.array(fakeeff) #make array for plotting
fig, ax = plt.subplots()
x,y=np.meshgrid(x_edges,y_edges)
bar=plt.pcolormesh(x,y,fakeeff,cmap=plt.cm.jet)
plt.clim(0,1) #sets limits for colorbar
fig.colorbar(bar, ax=ax)
plt.xlabel('FakeMPt')
plt.ylabel('FakeMEta')
plt.title('FakeM'+name)

#print values !! add errors
for i in range(fakeeff.shape[0]):
    for j in range(fakeeff.shape[1]):
        #print(fakeeff[i,j])
        xpos=(x_edges[j]+x_edges[j+1])/2 - 5 #-50 to account for length of text
        ypos=(y_edges[i]+y_edges[i+1])/2
        #print(xpos,ypos)
        label=str(round(fakeeff[i,j],2)) + "+-" + str(round(errorfakeeff[i,j],2)) # + '/(' + str(num[i,j])+ '+'+str(denom[i,j]) + ')'
        ax.text(xpos, ypos, label)

print('save')
plt.savefig('pic/FakeEfficiencyE')
'''