#import ROOT
import numpy as np
import uproot as ur
import pandas
import matplotlib.pyplot as plt

fakes=['FakeM'] #fakes=['FakeM','FakeE']

for f in fakes:

    print('reading in data')
    data_tight=pandas.read_csv('data_tight_'+f+'.csv')
    data_loose=pandas.read_csv('data_loose_'+f+'.csv')

    print('reading in WZ MC')
    WZ_tight=pandas.read_csv('WZ_tight_'+f+'.csv')
    WZ_loose=pandas.read_csv('WZ_loose_'+f+'.csv')

    #define binedges
    binedges=[[0,100,200],[0,1.5,3]]

    #make 2d histograms with the respective binedges
    print('making histograms')
    hist_tight,xbins_tight,ybins_tight,im_tight=plt.hist2d(data_tight[f+'Pt'], abs(data_tight[f+'Eta']), bins=binedges)
    hist_loose,xbins_loose,ybins_loose,im_loose=plt.hist2d(data_loose[f+'Pt'], abs(data_loose[f+'Eta']), bins=binedges)
    hist_WZ_tight,xbins_WZ_tight,ybins_WZ_tight,im_WZ_tight=plt.hist2d(WZ_tight[f+'Pt'], abs(WZ_tight[f+'Eta']), bins=binedges, weights=WZ_tight['weight'])
    hist_WZ_loose,xbins_WZ_loose,ybins_WZ_loose,im_WZ_loose=plt.hist2d(WZ_loose[f+'Pt'], abs(WZ_loose[f+'Eta']), bins=binedges, weights=WZ_loose['weight'])

    #print(hist_tight,hist_loose)
    #print(hist_tight/hist_loose)
    #print(hist_WZ_tight,hist_WZ_loose)
    #print(hist_WZ_tight/hist_WZ_loose)

    #calculate fake eff by dividing the tight histogram with the loose histogram
    print('calculate fake efficiency')
    #fakeeff=hist_tight/hist_loose
    num=hist_tight-hist_WZ_tight
    denom=hist_loose-hist_WZ_loose
    fakeeff=num/denom

    #here: errors!!    
    print('calculate errors')
    errorfakeeff=1/denom*np.sqrt(num*(1-num/denom))

    #plot the given histrogram with the given binedges
    print('plot and save the results')
    extent=[binedges[0][0],binedges[0][-1],binedges[1][0],binedges[1][-1]] #[-1] gives last value
    fig, ax = plt.subplots()
    hist=plt.imshow(fakeeff,interpolation='none',extent=extent, aspect='auto',cmap=plt.cm.jet)
    plt.clim(0,1) #sets limits for colorbar
    fig.colorbar(hist, ax=ax)
    plt.xlabel(f+'Pt')
    plt.ylabel(f+'Eta')
    plt.title(f)
    #plt.legend()

    #print values !! add errors
    fakeeff_mod=fakeeff[[1, 0]] #rearange the matrix to work for the for loop, [3,2,1,0]
    errorfakeeff_mod=errorfakeeff[[1,0]]
    y_width=(ybins_tight[1]-ybins_tight[0])/2
    x_width=(xbins_tight[1]-xbins_tight[0])/2
    for i in range(len(ybins_tight)-1):
        for j in range(len(xbins_tight)-1):
            label=str(round(fakeeff_mod[i,j],2)) + "+-" + str(round(errorfakeeff_mod[i,j],2))
            ax.text(xbins_tight[j]+x_width,ybins_tight[i]+y_width, label, 
                    color="w", ha="center", va="center", fontweight="bold")

    plt.savefig('FakeEfficiency'+f)