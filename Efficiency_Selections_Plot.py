#DO NOT USE.

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

print(len(tight))

print(len(loose))
loose=loose[loose['FakeMQualityTight']==1] #ID WP == Tight
print(len(loose))
loose=loose[loose['FakeMIsolationFCLoose']==1] #Iso WP = FCLoose
print(len(loose))
loose=loose[loose['FakeMd0sig']<=3] #d0sig = 1000
print(len(loose))

#add MET cut


#define binedges
print(loose['FakeMPt'].max(),loose['FakeMEta'].max())
binedges=[[0,200,1000],[0,2,5]]

#make 2d histograms with the respective binedges
print('making histograms')
hist_tight,xbins_tight,ybins_tight,im_tight=plt.hist2d(tight['FakeMPt'], abs(tight['FakeMEta']), bins=binedges)
hist_loose,xbins_loose,ybins_loose,im_loose=plt.hist2d(loose['FakeMPt'], abs(loose['FakeMEta']), bins=binedges)
#print(hist_tight,hist_loose,xbins_tight)

#calculate fake eff by dividing the tight histogram with the loose histogram
print('calculate fake efficiency')
num=hist_tight
denom=hist_loose
fakeeff=num/denom

#calculate errors    
print('calculate errors')
errorfakeeff=1/denom*np.sqrt(num*(1-num/denom))

#plot the given histrogram with the given binedges
print('plot and save the results')
extent=[binedges[0][0],binedges[0][-1],binedges[1][0],binedges[1][-1]] #[-1] gives last value
fig, ax = plt.subplots()
hist=plt.imshow(fakeeff,interpolation='none',extent=extent, aspect='auto',cmap=plt.cm.jet)
plt.clim(0,1) #sets limits for colorbar
fig.colorbar(hist, ax=ax)
plt.xlabel('FakeMPt')
plt.ylabel('FakeEEta')
plt.title('FakeM'+name)

#print values !! add errors

#num_mod=num[[1,0]]
#denom_mod=denom[[1,0]]
#fakeeff_mod=fakeeff[[1, 0]] #rearange the matrix to work for the for loop, [3,2,1,0]
#errorfakeeff_mod=errorfakeeff[[1,0]]
#y_width=(ybins_tight[1]-ybins_tight[0])/2
#x_width=(xbins_tight[1]-xbins_tight[0])/2
#for i in range(len(ybins_tight)-1):
#    for j in range(len(xbins_tight)-1):
#        label=str(round(fakeeff_mod[i,j],2)) + "+-" + str(round(errorfakeeff_mod[i,j],2)) + '/(' + str(num_mod[i,j])+ '+'+str(denom_mod[i,j]) + ')'
#        ax.text(xbins_tight[j]+x_width,ybins_tight[i]+y_width, label, 
#                color="k", ha="center", va="center", fontweight="bold")

plt.savefig('pic/FakeEfficiency_FakeM_'+name_short)