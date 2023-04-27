#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt

print('reading in MC')
MC_loose=pandas.read_csv('csv/MC_loose.csv')

#add PT cuts
MC_loose=MC_loose[(MC_loose['ZM0Pt']>=27)&(MC_loose['ZM1Pt']>=27)]
MC_loose=MC_loose[(MC_loose['FakeEPt']>=10)]
MC_loose=MC_loose[(MC_loose['MET']<=40)]

#eta -> abs(eta)
MC_loose['FakeEEta']=abs(MC_loose['FakeEEta'])

MC_tight=MC_loose 

#make tight selection
name='ID:Tight, Iso:FCLoose, d0sig<10, MET:40'

MC_tight=MC_tight[MC_tight['FakeEIDTight']==1] #Iso WP
MC_tight=MC_tight[MC_tight['FakeEd0sig']<=5] #Iso WP
MC_tight=MC_tight[MC_tight['FakeEIsolationFCTight']==1] #Iso WP

#define binedges
x_edges=[10,30,600] #pt edges
y_edges=[0,1.1,2.5] #eta edges
edges=[x_edges,y_edges]

#make 2d histograms with the respective binedges
print('making histograms')
hist_tight,xbins_tight,ybins_tight,im_tight=plt.hist2d(MC_tight['FakeEPt'], MC_tight['FakeEEta'], bins=edges, weights=MC_tight['weight'])
hist_loose,xbins_loose,ybins_loose,im_loose=plt.hist2d(MC_loose['FakeEPt'], MC_loose['FakeEEta'], bins=edges, weights=MC_loose['weight'])
#print('check1',hist_tight,hist_WZ_tight)
#print('check2',hist_loose,hist_WZ_loose)

#make transpose for plotting
hist_tight=hist_tight.T
hist_loose=hist_loose.T

#calculate fake eff by dividing the tight histogram with the loose histogram
print('calculate fake efficiency')
print(hist_tight)
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
plt.savefig('pic/FakeEfficiencyE_MC')

#composition
print('making composition histograms')

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