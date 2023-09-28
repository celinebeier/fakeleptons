import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt
from array import array
plt.rc('text', usetex=True)
#plt.style.use('./.matplotlib/stylelib/atlas.mplstyle')

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
#data_loose=data_loose[(data_loose['FakeEIDTight']==1)]
#WZ_loose=WZ_loose[(WZ_loose['FakeEIDTight']==1)]
#MC_loose=MC_loose[(MC_loose['FakeEIDTight']==1)]
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
#print(data_loose['FakeEPt'].max(),data_loose['FakeEEta'].max())
pt_bins=[27,35,1000] #pt edges
eta_bins=[0,2.5] #eta edges
edges=[pt_bins,eta_bins]

######################################################################################

#make 2d histograms with the respective binedges
print('making eta histograms')
hist_tight,xbins_tight,ypatches_tight=plt.hist(data_tight['FakeMEta'], bins=eta_bins)
hist_loose,xbins_loose,ypatches_loose=plt.hist(data_loose['FakeMEta'], bins=eta_bins)

hist_WZ_tight,xbins_WZ_tight,ypatches_WZ_tight=plt.hist(WZ_tight['FakeMEta'], bins=eta_bins, weights=WZ_tight['weight'])
hist_WZ_loose,xbins_WZ_loose,ypatches_WZ_loose=plt.hist(WZ_loose['FakeMEta'], bins=eta_bins, weights=WZ_loose['weight'])

hist_WZ2_tight,xbins_WZ2_tight,ypatches_WZ2_tight=plt.hist(WZ_tight['FakeMEta'], bins=eta_bins, weights=(WZ_tight['weight'])**2)
hist_WZ2_loose,xbins_WZ2_loose,ypatches_WZ2_loose=plt.hist(WZ_loose['FakeMEta'], bins=eta_bins, weights=(WZ_loose['weight'])**2)

hist_MC_tight,xbins_MC_tight,ypatches_MC_tight=plt.hist(MC_tight['FakeMEta'], bins=eta_bins, weights=MC_tight['weight'])
hist_MC_loose,xbins_MC_loose,ypatches_MC_loose=plt.hist(MC_loose['FakeMEta'], bins=eta_bins, weights=MC_loose['weight'])

#calculate fake eff by dividing the tight histogram with the loose histogram
print('calculate fake efficiency')
print(hist_tight,hist_loose)
num=hist_tight-hist_WZ_tight
denom=hist_loose-hist_WZ_loose
fakeeff=num/denom

num_MC=hist_MC_tight
denom_MC=hist_MC_loose
fakeeff_MC=num_MC/denom_MC
#print(fakeeff)

#calculate errors    
print('calculate errors')
print(hist_tight,hist_WZ_tight,num)
#errorfakeeff=1/denom*np.sqrt(num*(1-num/denom))
#errorfakeeff=fakeeff*np.sqrt(1/num+1/denom)
#errorfakeeff=fakeeff*np.sqrt((hist_tight/(num**2))+(hist_WZ_tight/(num**2))+(hist_loose/(denom**2))+(hist_WZ_loose/(denom**2)))
errorfakeeff=fakeeff*np.sqrt((hist_tight/(num**2))+(hist_WZ2_tight/(num**2))+(hist_loose/(denom**2))+(hist_WZ2_loose/(denom**2)))
#print(errorfakeeff)
errorfakeeff_MC=fakeeff_MC*np.sqrt(1/num_MC+1/denom_MC)

#calculate the fake factor
print('calculate fake factor')
fakefactor=fakeeff/(1-fakeeff)
errorfakefactor=(errorfakeeff)/((1-fakeeff)**2)
fakefactor_MC=fakeeff_MC/(1-fakeeff_MC)
errorfakefactor_MC=(errorfakeeff_MC)/((1-fakeeff_MC)**2)

#plotting

outputFile=ROOT.TFile('/afs/cern.ch/user/c/cbeier/fakeleptons/root_FakeM/'+"2d.root","recreate")

eta_bins_plt=[0.001,2.5] #eta edges

hardcoded_bins = array('d', eta_bins_plt)

FE2dEta_DATA=ROOT.TH1F("FE2dEta_DATA","",len(hardcoded_bins)-1,hardcoded_bins)

for i in range(len(fakeeff)): #y axis - eta
    FE2dEta_DATA.SetBinContent(i+1,fakeeff[i])
    FE2dEta_DATA.SetBinError(i+1,errorfakeeff[i])
    
FE2dEta_DATA.Write()

FE2dEta_MC=ROOT.TH1F("FE2dEta_MC","",len(hardcoded_bins)-1,hardcoded_bins)

for i in range(len(fakeeff)): #y axis - eta
    FE2dEta_MC.SetBinContent(i+1,fakeeff_MC[i])
    FE2dEta_MC.SetBinError(i+1,errorfakeeff_MC[i])
    
FE2dEta_MC.Write()

FF2dEta_DATA=ROOT.TH1F("FF2dEta_DATA","",len(hardcoded_bins)-1,hardcoded_bins)

for i in range(len(fakefactor)): #y axis - eta
    FF2dEta_DATA.SetBinContent(i+1,fakefactor[i])
    FF2dEta_DATA.SetBinError(i+1,errorfakefactor[i])
    
FF2dEta_DATA.Write()

FF2dEta_MC=ROOT.TH1F("FF2dEta_MC","",len(hardcoded_bins)-1,hardcoded_bins)

for i in range(len(fakefactor)): #y axis - eta
    FF2dEta_MC.SetBinContent(i+1,fakefactor_MC[i])
    FF2dEta_MC.SetBinError(i+1,errorfakefactor_MC[i])
    
FF2dEta_MC.Write()

del fakeeff, errorfakeeff, fakeeff_MC, errorfakeeff_MC, fakefactor, errorfakefactor, fakefactor_MC, errorfakefactor_MC

##############

print('making pt histograms')
hist_tight,xbins_tight,ypatches_tight=plt.hist(data_tight['FakeMPt'], bins=pt_bins)
hist_loose,xbins_loose,ypatches_loose=plt.hist(data_loose['FakeMPt'], bins=pt_bins)

hist_WZ_tight,xbins_WZ_tight,ypatches_WZ_tight=plt.hist(WZ_tight['FakeMPt'], bins=pt_bins, weights=WZ_tight['weight'])
hist_WZ_loose,xbins_WZ_loose,ypatches_WZ_loose=plt.hist(WZ_loose['FakeMPt'], bins=pt_bins, weights=WZ_loose['weight'])

hist_WZ2_tight,xbins_WZ2_tight,ypatches_WZ2_tight=plt.hist(WZ_tight['FakeMPt'], bins=pt_bins, weights=(WZ_tight['weight'])**2)
hist_WZ2_loose,xbins_WZ2_loose,ypatches_WZ2_loose=plt.hist(WZ_loose['FakeMPt'], bins=pt_bins, weights=(WZ_loose['weight'])**2)

hist_MC_tight,xbins_MC_tight,ypatches_MC_tight=plt.hist(MC_tight['FakeMPt'], bins=pt_bins, weights=MC_tight['weight'])
hist_MC_loose,xbins_MC_loose,ypatches_MC_loose=plt.hist(MC_loose['FakeMPt'], bins=pt_bins, weights=MC_loose['weight'])

#calculate fake eff by dividing the tight histogram with the loose histogram
print('calculate fake efficiency')
print(hist_tight,hist_loose)
num=hist_tight-hist_WZ_tight
denom=hist_loose-hist_WZ_loose
fakeeff=num/denom
#fakeeff[1:2]=0

num_MC=hist_MC_tight
denom_MC=hist_MC_loose
fakeeff_MC=num_MC/denom_MC
#fakeeff_MC[1:2]=0
#print(fakeeff)

#calculate errors    
print('calculate errors')
print(hist_tight,hist_WZ_tight,num)
#errorfakeeff=1/denom*np.sqrt(num*(1-num/denom))
#errorfakeeff=fakeeff*np.sqrt(1/num+1/denom)
#errorfakeeff=fakeeff*np.sqrt((hist_tight/(num**2))+(hist_WZ_tight/(num**2))+(hist_loose/(denom**2))+(hist_WZ_loose/(denom**2)))
errorfakeeff=fakeeff*np.sqrt((hist_tight/(num**2))+(hist_WZ2_tight/(num**2))+(hist_loose/(denom**2))+(hist_WZ2_loose/(denom**2)))
#print(errorfakeeff)
#errorfakeeff[1:2]=0
errorfakeeff_MC=fakeeff_MC*np.sqrt(1/num_MC+1/denom_MC)
#errorfakeeff_MC[1:2]=0

#calculate the fake factor
print('calculate fake factor')
fakefactor=fakeeff/(1-fakeeff)
errorfakefactor=(errorfakeeff)/((1-fakeeff)**2)
fakefactor_MC=fakeeff_MC/(1-fakeeff_MC)
errorfakefactor_MC=(errorfakeeff_MC)/((1-fakeeff_MC)**2)

#plotting
pt_bins=np.array(pt_bins)
pt_bins_lin=np.array([0,0.5,1])
hardcoded_bins = array('d', pt_bins_lin)

FE2dPt_DATA=ROOT.TH1F("FE2dPt_DATA","",len(hardcoded_bins)-1,hardcoded_bins)

for i in range(len(fakeeff)): #y axis - eta
    FE2dPt_DATA.SetBinContent(i+1,fakeeff[i])
    FE2dPt_DATA.SetBinError(i+1,errorfakeeff[i])
    
FE2dPt_DATA.Write()

FE2dPt_MC=ROOT.TH1F("FE2dPt_MC","",len(hardcoded_bins)-1,hardcoded_bins)

for i in range(len(fakeeff)): #y axis - eta
    FE2dPt_MC.SetBinContent(i+1,fakeeff_MC[i])
    FE2dPt_MC.SetBinError(i+1,errorfakeeff_MC[i])
    
FE2dPt_MC.Write()

FF2dPt_DATA=ROOT.TH1F("FF2dPt_DATA","",len(hardcoded_bins)-1,hardcoded_bins)

for i in range(len(fakefactor)): #y axis - eta
    FF2dPt_DATA.SetBinContent(i+1,fakefactor[i])
    FF2dPt_DATA.SetBinError(i+1,errorfakefactor[i])
    
FF2dPt_DATA.Write()

FF2dPt_MC=ROOT.TH1F("FF2dPt_MC","",len(hardcoded_bins)-1,hardcoded_bins)

for i in range(len(fakefactor)): #y axis - eta
    FF2dPt_MC.SetBinContent(i+1,fakefactor_MC[i])
    FF2dPt_MC.SetBinError(i+1,errorfakefactor_MC[i])
    
FF2dPt_MC.Write()