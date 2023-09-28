#for data, without WZ!! I think this works!!

#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt

print('reading in data')
#tight=pandas.read_csv('cvs/tight'+'.csv')
#tight.name='tight'
loose=pandas.read_csv('cvs/e_loose'+'.csv')
loose.name='loose'

#here: make alterations to loose dataframe to account for different selections
name='ID: Tight, Iso: FCLoose, d0sig < 10, MET: -'
name_short='IDTight_IsoFCLoose_d0sig10_MET#'

#add PT cuts: 15GeV
#print(len(tight))
#tight=tight[(tight['FakeMPt']>=27)&(tight['ZE0Pt']>=27)&(tight['ZE1Pt']>=27)]
#print(len(tight))
#print(len(loose))
#loose=loose[(loose['FakeMPt']>=27)&(loose['ZE0Pt']>=27)&(loose['ZE1Pt']>=27)]
#print(len(loose))

print(len(tight))
tight=tight[tight['FakeEIDTight']==1] #Iso WP
tight=tight[abs(tight['FakeEd0sig'])<=5] #Iso WP
tight=tight[tight['FakeEIsolationFCTight']==1] #Iso WP
print(len(tight))


list_events=[1417308731.0,1336849883.0,633056496.0,1891546255.0,709057206.0,515927285.0]

for i in range(len(tight)):
    #print(i)
    #print(loose.iloc[i]['eventNumber'])
    if tight.iloc[i]['eventNumber'] in list_events:
        #print('FakeEIDTight',tight.iloc[i]['FakeEIDTight'])
        print(tight.iloc[i]['eventNumber'])
    else: 
        #print('here')
        #print(tight.iloc[i]['eventNumber'])
        continue
        #print('FakeEIDTight',tight.iloc[i]['FakeEIDTight'])
        #print('FakeEd0sig',tight.iloc[i]['FakeEd0sig'])
        #print('FakeEIsolationFCTight',tight.iloc[i]['FakeEIsolationFCTight'])
        #print(tight.iloc[i])

'''
print(len(loose))
#loose=loose[loose['FakeMQualityTight']==1] #ID WP
loose=loose[loose['FakeEIDTight']==1]
#print(len(loose))
#loose=loose[abs(loose['FakeMd0sig'])<=3] #d0sig = 1000
loose=loose[abs(loose['FakeEd0sig'])<=5]
#print(len(loose))
#loose=loose[loose['FakeMIsolationFCTight']==1] #Iso WP
loose=loose[loose['FakeEIsolationFCTight']==1]
print(len(loose))
'''
#print(loose['eventNumber'])
'''
for i in range(len(tight)):
    #print(i)
    #print(loose.iloc[i]['eventNumber'])
    if tight.iloc[i]['eventNumber'] in loose['eventNumber'].values:
        #print('FakeEIDTight',tight.iloc[i]['FakeEIDTight'])
        #print('yes')
        continue
    else: 
        #print('here')
        print(tight.iloc[i]['eventNumber'])
        #print('FakeEIDTight',tight.iloc[i]['FakeEIDTight'])
        #print('FakeEd0sig',tight.iloc[i]['FakeEd0sig'])
        #print('FakeEIsolationFCTight',tight.iloc[i]['FakeEIsolationFCTight'])
        #print(tight.iloc[i])

'''
#loose=loose[abs(loose['FakeMEta'])>=1] #d0sig = 1000
#print(len(loose))
'''
#add MET cut

#define binedges
print(loose['FakeMPt'].max(),loose['FakeMEta'].max())
x_edges=[27,35,400] #pt edges
y_edges=[0,1,2.5] #eta edges

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
        xpos=(x_edges[j]+x_edges[j+1])/2 - 50 #-50 to account for length of text
        ypos=(y_edges[i]+y_edges[i+1])/2
        #print(xpos,ypos)
        label=str(round(fakeeff[i,j],2)) + "+-" + str(round(errorfakeeff[i,j],2)) # + '/(' + str(num[i,j])+ '+'+str(denom[i,j]) + ')'
        ax.text(xpos, ypos, label)

print('save')
plt.savefig('pic/FakeEfficiency_FakeM_'+name_short)

'''