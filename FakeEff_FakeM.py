import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt
from array import array

print('reading in data')
data_loose=pandas.read_csv('/eos/user/c/cbeier/csv_FakeM/Data_loose'+'.csv')

print('reading in WZ MC')
WZ_loose=pandas.read_csv('/eos/user/c/cbeier/csv_FakeM/WZ_loose.csv')

print('reading in MC')
MC_loose=pandas.read_csv('/eos/user/c/cbeier/csv_FakeM/MC_loose.csv')

#add PT cuts
data_loose=data_loose[(data_loose['ZE0Pt']>=27)&(data_loose['ZE1Pt']>=27)]
data_loose=data_loose[(data_loose['FakeMPt']>=10)]
data_loose=data_loose[(data_loose['MET']<=40)]
WZ_loose=WZ_loose[(WZ_loose['ZE0Pt']>=27)&(WZ_loose['ZE1Pt']>=27)]
WZ_loose=WZ_loose[(WZ_loose['FakeMPt']>=10)]
WZ_loose=WZ_loose[(WZ_loose['MET']<=40)]
MC_loose=MC_loose[(MC_loose['ZE0Pt']>=27)&(MC_loose['ZE1Pt']>=27)]
MC_loose=MC_loose[(MC_loose['FakeMPt']>=10)]
MC_loose=MC_loose[(MC_loose['MET']<=40)]

#loose cut
#print(len(data_loose))
#data_loose=data_loose[(data_loose['FakeMQualityTight']==1)]
#WZ_loose=WZ_loose[(WZ_loose['FakeMQualityTight']==1)]
#MC_loose=MC_loose[(MC_loose['FakeMQualityTight']==1)]
#data_loose=data_loose[(data_loose['FakeMIsolationFCTight']==1)]
#WZ_loose=WZ_loose[(WZ_loose['FakeMIsolationFCTight']==1)]
#MC_loose=MC_loose[(MC_loose['FakeMIsolationFCTight']==1)]
data_loose=data_loose[(data_loose['FakeMd0sig']<=3)]
WZ_loose=WZ_loose[(WZ_loose['FakeMd0sig']<=3)]
MC_loose=MC_loose[(MC_loose['FakeMd0sig']<=3)]
print(len(data_loose))

#eta -> abs(eta)
data_loose['FakeMEta']=abs(data_loose['FakeMEta'])
WZ_loose['FakeMEta']=abs(WZ_loose['FakeMEta'])
MC_loose['FakeMEta']=abs(MC_loose['FakeMEta'])

#test plotting
#data_loose=data_loose[(data_loose['FakeEEta']<1.1)]
#data_loose=data_loose[(data_loose['FakeEPt']>30)]
#WZ_loose=WZ_loose[(WZ_loose['FakeEEta']<1.1)]
#WZ_loose=WZ_loose[(WZ_loose['FakeEPt']>30)]

#truthmatching
WZ_loose=WZ_loose[(WZ_loose['FakeMID']==4)&(WZ_loose['ZE0ID']==2)&(WZ_loose['ZE1ID']==2)]

data_tight=data_loose
WZ_tight=WZ_loose 
MC_tight=MC_loose 

#make tight selection - don't touch! 
data_tight=data_tight[data_tight['FakeMQualityTight']==1] #Iso WP
data_tight=data_tight[data_tight['FakeMd0sig']<=3] #Iso WP
data_tight=data_tight[data_tight['FakeMIsolationFCTight']==1] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeMQualityTight']==1] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeMd0sig']<=3] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeMIsolationFCTight']==1] #Iso WP
MC_tight=MC_tight[MC_tight['FakeMQualityTight']==1] #Iso WP
MC_tight=MC_tight[MC_tight['FakeMd0sig']<=3] #Iso WP
MC_tight=MC_tight[MC_tight['FakeMIsolationFCTight']==1] #Iso WP
print(len(data_tight))

#define binedges
print('PT MAX:',data_loose['FakeMPt'].max(),MC_loose['FakeMPt'].max())
pt_bins=[10,15,27,35,1000] #pt edges
eta_bins=[0,2.5] #eta edges
edges=[pt_bins,eta_bins]

######################################################################################

#make 2d histograms with the respective binedges
print('making histograms')
hist_tight,xbins_tight,ybins_tight,im_tight=plt.hist2d(data_tight['FakeMPt'], data_tight['FakeMEta'], bins=edges)
hist_loose,xbins_loose,ybins_loose,im_loose=plt.hist2d(data_loose['FakeMPt'], data_loose['FakeMEta'], bins=edges)

hist_WZ_tight,xbins_WZ_tight,ybins_WZ_tight,im_WZ_tight=plt.hist2d(WZ_tight['FakeMPt'], WZ_tight['FakeMEta'], bins=edges, weights=WZ_tight['weight'])
hist_WZ_loose,xbins_WZ_loose,ybins_WZ_loose,im_WZ_loose=plt.hist2d(WZ_loose['FakeMPt'], WZ_loose['FakeMEta'], bins=edges, weights=WZ_loose['weight'])

hist_WZ2_tight,xbins_WZ2_tight,ybins_WZ2_tight,im_WZ2_tight=plt.hist2d(WZ_tight['FakeMPt'], WZ_tight['FakeMEta'], bins=edges, weights=(WZ_tight['weight'])**2)
hist_WZ2_loose,xbins_WZ2_loose,ybins_WZ2_loose,im_WZ2_loose=plt.hist2d(WZ_loose['FakeMPt'], WZ_loose['FakeMEta'], bins=edges, weights=(WZ_loose['weight'])**2)

hist_MC_tight,xbins_MC_tight,ybins_MC_tight,im_MC_tight=plt.hist2d(MC_tight['FakeMPt'], MC_tight['FakeMEta'], bins=edges, weights=MC_tight['weight'])
hist_MC_loose,xbins_MC_loose,ybins_MC_loose,im_MC_loose=plt.hist2d(MC_loose['FakeMPt'], MC_loose['FakeMEta'], bins=edges, weights=MC_loose['weight'])
#print('check1',hist_tight,hist_WZ_tight)
#print('check2',hist_loose,hist_WZ_loose)

#make transpose for plotting
hist_tight=hist_tight.T
hist_loose=hist_loose.T
hist_WZ_tight=hist_WZ_tight.T
hist_WZ_loose=hist_WZ_loose.T
hist_WZ2_tight=hist_WZ2_tight.T
hist_WZ2_loose=hist_WZ2_loose.T
hist_MC_tight=hist_MC_tight.T
hist_MC_loose=hist_MC_loose.T

#calculate fake eff by dividing the tight histogram with the loose histogram
print('calculate fake efficiency')
print('Tight:',hist_tight,'Loose:',hist_loose,'WZ:',hist_WZ_tight, hist_WZ_loose)
num=hist_tight-hist_WZ_tight
denom=hist_loose-hist_WZ_loose
print('Num:',num,'Denom:',denom)
fakeeff=num/denom

num_MC=hist_MC_tight
denom_MC=hist_MC_loose
fakeeff_MC=num_MC/denom_MC
print('Fakeeff:',fakeeff)

#calculate errors    
print('calculate errors')
print(hist_tight,hist_WZ_tight,num)
#errorfakeeff=1/denom*np.sqrt(num*(1-num/denom))
#errorfakeeff=fakeeff*np.sqrt(1/num+1/denom)
#errorfakeeff=fakeeff*np.sqrt((hist_tight/(num**2))+(hist_WZ_tight/(num**2))+(hist_loose/(denom**2))+(hist_WZ_loose/(denom**2)))
errorfakeeff=fakeeff*np.sqrt((hist_tight/(num**2))+(hist_WZ2_tight/(num**2))+(hist_loose/(denom**2))+(hist_WZ2_loose/(denom**2)))
print('Errorfakeeff:',errorfakeeff)
errorfakeeff_MC=fakeeff_MC*np.sqrt(1/num_MC+1/denom_MC)

#calculate the fake factor
print('calculate fake factor')
fakefactor=fakeeff/(1-fakeeff)
errorfakefactor=(errorfakeeff)/((1-fakeeff)**2)
fakefactor_MC=fakeeff_MC/(1-fakeeff_MC)
errorfakefactor_MC=(errorfakeeff_MC)/((1-fakeeff_MC)**2)

#save fake factor to csv file
print('save fake factor')
print(fakefactor)
#np.savetxt("root_FakeM/"+"MET10Up/"+"fakefactor.csv", fakefactor, delimiter=",")
#np.savetxt("root_FakeM/"+"MET10Up/"+"errorfakefactor.csv", errorfakefactor, delimiter=",")
np.savetxt("root_FakeM/"+"fakefactor.csv", fakefactor, delimiter=",")
np.savetxt("root_FakeM/"+"errorfakefactor.csv", errorfakefactor, delimiter=",")

#plot the given histrogram with the given binedges
print('plot the results')

#outputFile=ROOT.TFile('/afs/cern.ch/user/c/cbeier/fakeleptons/root_FakeM/'+'MET10Up'+"FakeEff.root","recreate")
outputFile=ROOT.TFile('/afs/cern.ch/user/c/cbeier/fakeleptons/root_FakeM/'+"FakeEff.root","recreate")

pt_bins=np.array(pt_bins)
eta_bins=np.array(eta_bins)
pt_bins_lin=np.linspace(0,1,num=len(pt_bins))
hardcoded_eta_bins = array('d', eta_bins)
hardcoded_pt_bins = array('d', pt_bins_lin)

etaBins=[[0,2.5]]
ptBins=pt_bins

FE_DATA=ROOT.TH2F("FE_DATA", "", len(hardcoded_pt_bins)-1, hardcoded_pt_bins, len(hardcoded_eta_bins)-1, hardcoded_eta_bins)

for i in range(fakeeff.shape[0]): #y axis - eta
    for j in range(fakeeff.shape[1]): #x axis -pt
        #print(i,j)
        #h_MC.Fill(pt_bins[j]+0.1,eta_bins[i]+0.1,fakeeff[i][j])
        FE_DATA.SetBinContent(j+1,i+1,fakeeff[i][j])
        FE_DATA.SetBinError(j+1,i+1,errorfakeeff[i][j])
    
FE_DATA.Write()

FF_DATA=ROOT.TH2F("FF_DATA", "", len(hardcoded_pt_bins)-1, hardcoded_pt_bins, len(hardcoded_eta_bins)-1, hardcoded_eta_bins)

for i in range(fakeeff.shape[0]): #y axis - eta
    for j in range(fakeeff.shape[1]): #x axis -pt
        #print(i,j)
        #h_MC.Fill(pt_bins[j]+0.1,eta_bins[i]+0.1,fakeeff[i][j])
        FF_DATA.SetBinContent(j+1,i+1,fakefactor[i][j])
        FF_DATA.SetBinError(j+1,i+1,errorfakefactor[i][j])
    
FF_DATA.Write()

FE_MC=ROOT.TH2F("FE_MC", "", len(hardcoded_pt_bins)-1, hardcoded_pt_bins, len(hardcoded_eta_bins)-1, hardcoded_eta_bins)

for i in range(fakeeff.shape[0]): #y axis - eta
    for j in range(fakeeff.shape[1]): #x axis -pt
        #print(i,j)
        #h_MC.Fill(pt_bins[j]+0.1,eta_bins[i]+0.1,fakeeff[i][j])
        FE_MC.SetBinContent(j+1,i+1,fakeeff_MC[i][j])
        FE_MC.SetBinError(j+1,i+1,errorfakeeff_MC[i][j])
    
FE_MC.Write()

FF_MC=ROOT.TH2F("FF_MC", "", len(hardcoded_pt_bins)-1, hardcoded_pt_bins, len(hardcoded_eta_bins)-1, hardcoded_eta_bins)

for i in range(fakeeff.shape[0]): #y axis - eta
    for j in range(fakeeff.shape[1]): #x axis -pt
        #print(i,j)
        #h_MC.Fill(pt_bins[j]+0.1,eta_bins[i]+0.1,fakeeff[i][j])
        FF_MC.SetBinContent(j+1,i+1,fakefactor_MC[i][j])
        FF_MC.SetBinError(j+1,i+1,errorfakefactor_MC[i][j])
    
FF_MC.Write()
