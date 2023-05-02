#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt
#print(plt.style.available)
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
#plt.style.use('./.matplotlib/stylelib/atlas.mplstyle')

print('reading in data')
data_loose=pandas.read_csv('csv/Data_loose'+'.csv')

print('reading in WZ MC')
WZ_loose=pandas.read_csv('csv/WZ_loose.csv')

#add PT cuts
data_loose=data_loose[(data_loose['ZM0Pt']>=27.3)&(data_loose['ZM1Pt']>=27.3)]
data_loose=data_loose[(data_loose['FakeEPt']>=10)]
data_loose=data_loose[(data_loose['MET']<=40)]
WZ_loose=WZ_loose[(WZ_loose['ZM0Pt']>=27.3)&(WZ_loose['ZM1Pt']>=27.3)]
WZ_loose=WZ_loose[(WZ_loose['FakeEPt']>=10)]
WZ_loose=WZ_loose[(WZ_loose['MET']<=40)]

#loose cut
#data_loose=data_loose[(data_loose['FakeEIsolationFCTight']==1)]
#WZ_loose=WZ_loose[(WZ_loose['FakeEIsolationFCTight']==1)]
#data_loose=data_loose[(data_loose['FakeEd0sig']<=5)]
#WZ_loose=WZ_loose[(WZ_loose['FakeEd0sig']<=5)]

#eta -> abs(eta)
data_loose['FakeEEta']=abs(data_loose['FakeEEta'])
WZ_loose['FakeEEta']=abs(WZ_loose['FakeEEta'])

#test plotting
#data_loose=data_loose[(data_loose['FakeEEta']<1.1)]
#data_loose=data_loose[(data_loose['FakeEPt']>30)]
#WZ_loose=WZ_loose[(WZ_loose['FakeEEta']<1.1)]
#WZ_loose=WZ_loose[(WZ_loose['FakeEPt']>30)]

#truthmatching
WZ_loose=WZ_loose[(WZ_loose['FakeEID']==2)&(WZ_loose['ZM0ID']==4)&(WZ_loose['ZM1ID']==4)]

data_tight=data_loose
WZ_tight=WZ_loose 

#make tight selection
name='ID:Tight, Iso:FCLoose, d0sig<-, MET:40'

data_tight=data_tight[data_tight['FakeEIDTight']==1] #Iso WP
data_tight=data_tight[data_tight['FakeEd0sig']<=5] #Iso WP
data_tight=data_tight[data_tight['FakeEIsolationFCTight']==1] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeEIDTight']==1] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeEd0sig']<=5] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeEIsolationFCTight']==1] #Iso WP

#define binedges
print(data_loose['FakeEPt'].max(),data_loose['FakeEEta'].max())
x_edges=[10,27,40,600] #pt edges
y_edges=[0,1.37,1.52,2.5] #eta edges
edges=[x_edges,y_edges]

print('plots comparing data and MC')
print('tight',len(data_tight),WZ_tight['weight'].sum())
print('loose',len(data_loose),WZ_loose['weight'].sum())

plt.figure(1)
n,bins,patches=plt.hist(data_loose['FakeEPt'],label='Data',bins=50,alpha=0.5)
plt.hist(WZ_loose['FakeEPt'],bins=bins,weights=WZ_loose['weight'],label='WZ',alpha=0.5)
plt.xlabel('FakeEPt')
plt.title('Fake Electron Pt')
plt.legend()
plt.savefig('pic/CompDataMC_Pt')

plt.figure(2)
n,bins,patches=plt.hist(data_loose['FakeEEta'],bins=50,label='Data',alpha=0.5)
plt.hist(WZ_loose['FakeEEta'],bins=bins,weights=WZ_loose['weight'],label='WZ',alpha=0.5)
plt.xlabel('FakeEEta')
plt.title('Fake Electron Eta')
plt.legend()
plt.savefig('pic/CompDataMC_Eta')

#make 2d histograms with the respective binedges
print('making histograms')
hist_tight,xbins_tight,ybins_tight,im_tight=plt.hist2d(data_tight['FakeEPt'], data_tight['FakeEEta'], bins=edges)
hist_loose,xbins_loose,ybins_loose,im_loose=plt.hist2d(data_loose['FakeEPt'], data_loose['FakeEEta'], bins=edges)

hist_WZ_tight,xbins_WZ_tight,ybins_WZ_tight,im_WZ_tight=plt.hist2d(WZ_tight['FakeEPt'], WZ_tight['FakeEEta'], bins=edges, weights=WZ_tight['weight'])
hist_WZ_loose,xbins_WZ_loose,ybins_WZ_loose,im_WZ_loose=plt.hist2d(WZ_loose['FakeEPt'], WZ_loose['FakeEEta'], bins=edges, weights=WZ_loose['weight'])
print('check1',hist_tight,hist_WZ_tight)
#print('check2',hist_loose,hist_WZ_loose)

#make transpose for plotting
hist_tight=hist_tight.T
hist_loose=hist_loose.T
hist_WZ_tight=hist_WZ_tight.T
hist_WZ_loose=hist_WZ_loose.T

#calculate fake eff by dividing the tight histogram with the loose histogram
print('calculate fake efficiency')
num=hist_tight-hist_WZ_tight
denom=hist_loose-hist_WZ_loose
fakeeff=num/denom
fakeeff[1:2]=0
print('fake efficiency:',fakeeff)

#calculate errors    
print('calculate errors for fake efficiency')
errorfakeeff=1/denom*np.sqrt(num*(1-num/denom))
errorfakeeff[1:2]=0

#calculate the fake factor
print('calculate fake factor')
fakefactor=fakeeff/(1-fakeeff)
errorfakefactor=np.sqrt(fakefactor)
print('fake factor:',fakefactor)

#plot the given histrogram with the given binedges
print('plot the results')
c=np.array(fakeeff) #make array for plotting
plt.figure(3)
fig, ax = plt.subplots()
#a=[x_edges[0],x_edges[0]+(x_edges[-1]-x_edges[0])/2,x_edges[-1]] #but make the diagram equal sizes
#b=[y_edges[0],y_edges[0]+(y_edges[-1]-y_edges[0])/2,y_edges[-1]]
a=[x_edges[0],x_edges[0]+(x_edges[-1]-x_edges[0])/3,x_edges[0]+(x_edges[-1]-x_edges[0])*2/3,x_edges[-1]] #but make the diagram equal sizes
#b=[y_edges[0],y_edges[0]+(y_edges[-1]-y_edges[0])/3,y_edges[0]+(y_edges[-1]-y_edges[0])*2/3,y_edges[-1]]
b=y_edges
print(a,b)
x,y=np.meshgrid(a,b)
bar=plt.pcolormesh(x,y,fakeeff,cmap=plt.cm.Blues)
plt.clim(0,1) #sets limits for colorbar
fig.colorbar(bar, ax=ax)
plt.xlabel(r'electron $p_T$ [GeV]', horizontalalignment='right', x=1.0)
plt.xticks(a,x_edges)
plt.yticks(b,y_edges)
plt.ylabel(r'electron $\eta$', horizontalalignment='right', y=1.0)
plt.title('Fake Efficiency, Electron Channel')

#print values !! add errors
for i in range(fakeeff.shape[0]): #y axis
    for j in range(fakeeff.shape[1]): #x axis
        #print(fakeeff[i,j])
        #print(i,j)
        xpos=(a[j]+a[j+1])/2 -50 #-50 to account for length of text
        ypos=(b[i]+b[i+1])/2
        #print(xpos,ypos)
        if fakeeff[i,j]!=0:
            label=str(format(fakeeff[i,j], '.2f')) + "+-" + str(format(errorfakeeff[i,j], '.2f'))
            ax.text(xpos, ypos, label)
        else: continue

print('save')
plt.savefig('pic/FakeEfficiencyE_Data')

#plot the given histrogram with the given binedges
print('plot the results')
c=np.array(fakefactor) #make array for plotting
plt.figure(4)
fig, ax = plt.subplots()
a=[x_edges[0],x_edges[0]+(x_edges[-1]-x_edges[0])/3,x_edges[0]+(x_edges[-1]-x_edges[0])*2/3,x_edges[-1]] #but make the diagram equal sizes
#b=[y_edges[0],y_edges[0]+(y_edges[-1]-y_edges[0])/3,y_edges[0]+(y_edges[-1]-y_edges[0])*2/3,y_edges[-1]]
b=y_edges
print(a,b)
x,y=np.meshgrid(a,b)
bar=plt.pcolormesh(x,y,fakefactor,cmap=plt.cm.Blues)
plt.clim(0,1) #sets limits for colorbar
fig.colorbar(bar, ax=ax)
plt.xlabel(r'electron $p_T$ [GeV]', horizontalalignment='right', x=1.0)
plt.xticks(a,x_edges)
plt.yticks(b,y_edges)
plt.ylabel(r'electron $\eta$', horizontalalignment='right', y=1.0)
plt.title('Fake Factor, Electron Channel')

#print values !! add errors
for i in range(fakeeff.shape[0]):
    for j in range(fakeeff.shape[1]):
        #print(fakeeff[i,j])
        xpos=(a[j]+a[j+1])/2 -50 #-50 to account for length of text
        ypos=(b[i]+b[i+1])/2
        #print(xpos,ypos)
        if fakefactor[i,j]!=0:
            label=str(format(fakefactor[i,j], '.2f')) + "+-" + str(format(errorfakefactor[i,j], '.2f'))
            ax.text(xpos, ypos, label)
        else: continue

print('save')
plt.savefig('pic/FakeFactorE_Data')
