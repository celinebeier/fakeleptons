#for data, without WZ!! I think this works!!

#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt

print('reading in data')
tight=pandas.read_csv('cvs/data_tight_selections'+'.csv')
tight.name='tight'
loose=pandas.read_csv('cvs/data_loose_selections'+'.csv')
loose.name='loose'

#here: make alterations to loose dataframe to account for different selections
name='ID: Tight, Iso: FCLoose, d0sig < 3, MET: -'
name_short='IDTight_IsoFCLoose_d0sig3_MET#'

#print(len(tight))
#print(len(loose))
loose=loose[loose['FakeMQualityTight']==1] #ID WP == Tight
loose=loose[loose['FakeMIsolationFCLoose']==1] #Iso WP = FCLoose
loose=loose[loose['FakeMd0sig']<3] #d0sig = 1000
#print(len(loose))
#add MET cut


#define binedges
#print(loose['FakeMPt'].max(),loose['FakeMEta'].max())
x_edges=[0,10,1000] #pt edges
y_edges=[0,1,5] #eta edges

#make 2d histograms with the respective binedges
print('making histograms')
hist_tight,xbins_tight,ybins_tight,im_tight=plt.hist2d(tight['FakeMPt'], abs(tight['FakeMEta']), bins=(x_edges,y_edges))
hist_loose,xbins_loose,ybins_loose,im_loose=plt.hist2d(loose['FakeMPt'], abs(loose['FakeMEta']), bins=(x_edges,y_edges))
#print(xbins_tight,ybins_tight,hist_tight,hist_loose)

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
        xpos=(x_edges[j]+x_edges[j+1])/2
        ypos=(y_edges[i]+y_edges[i+1])/2
        #print(xpos,ypos)
        label=str(round(fakeeff[i,j],2)) + "+-" + str(round(errorfakeeff[i,j],2))
        ax.text(xpos, ypos, label)

print('save')
plt.savefig('pic/test')