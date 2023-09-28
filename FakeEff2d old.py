import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt
from array import array
plt.rc('text', usetex=True)
#plt.style.use('./.matplotlib/stylelib/atlas.mplstyle')

print('reading in data')
data_loose=pandas.read_csv('/eos/user/c/cbeier/csv/Data_loose'+'.csv')

print('reading in WZ MC')
WZ_loose=pandas.read_csv('/eos/user/c/cbeier/csv/WZ_loose.csv')

print('reading in MC')
MC_loose=pandas.read_csv('/eos/user/c/cbeier/csv/MC_loose.csv')

#add PT cuts
data_loose=data_loose[(data_loose['ZM0Pt']>=27)&(data_loose['ZM1Pt']>=27)]
data_loose=data_loose[(data_loose['FakeEPt']>=10)]
data_loose=data_loose[(data_loose['MET']<=40)]
WZ_loose=WZ_loose[(WZ_loose['ZM0Pt']>=27)&(WZ_loose['ZM1Pt']>=27)]
WZ_loose=WZ_loose[(WZ_loose['FakeEPt']>=10)]
WZ_loose=WZ_loose[(WZ_loose['MET']<=40)]
MC_loose=MC_loose[(MC_loose['ZM0Pt']>=27)&(MC_loose['ZM1Pt']>=27)]
MC_loose=MC_loose[(MC_loose['FakeEPt']>=10)]
MC_loose=MC_loose[(MC_loose['MET']<=40)]

#loose cut
#print(len(data_loose))
#data_loose=data_loose[(data_loose['FakeEIDTight']==1)]
#WZ_loose=WZ_loose[(WZ_loose['FakeEIDTight']==1)]
#MC_loose=MC_loose[(MC_loose['FakeEIDTight']==1)]
data_loose=data_loose[(data_loose['FakeEd0sig']<=5)]
WZ_loose=WZ_loose[(WZ_loose['FakeEd0sig']<=5)]
MC_loose=MC_loose[(MC_loose['FakeEd0sig']<=5)]
print(len(data_loose))

#eta -> abs(eta)
data_loose['FakeEEta']=abs(data_loose['FakeEEta'])
WZ_loose['FakeEEta']=abs(WZ_loose['FakeEEta'])
MC_loose['FakeEEta']=abs(MC_loose['FakeEEta'])

#test plotting
#data_loose=data_loose[(data_loose['FakeEEta']<1.1)]
#data_loose=data_loose[(data_loose['FakeEPt']>30)]
#WZ_loose=WZ_loose[(WZ_loose['FakeEEta']<1.1)]
#WZ_loose=WZ_loose[(WZ_loose['FakeEPt']>30)]

#truthmatching
WZ_loose=WZ_loose[(WZ_loose['FakeEID']==2)&(WZ_loose['ZM0ID']==4)&(WZ_loose['ZM1ID']==4)]

data_tight=data_loose
WZ_tight=WZ_loose 
MC_tight=MC_loose 

#make tight selection - don't touch! 
data_tight=data_tight[data_tight['FakeEIDTight']==1] #Iso WP
data_tight=data_tight[data_tight['FakeEd0sig']<=5] #Iso WP
data_tight=data_tight[data_tight['FakeEIsolationFCTight']==1] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeEIDTight']==1] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeEd0sig']<=5] #Iso WP
WZ_tight=WZ_tight[WZ_tight['FakeEIsolationFCTight']==1] #Iso WP
MC_tight=MC_tight[MC_tight['FakeEIDTight']==1] #Iso WP
MC_tight=MC_tight[MC_tight['FakeEd0sig']<=5] #Iso WP
MC_tight=MC_tight[MC_tight['FakeEIsolationFCTight']==1] #Iso WP
print(len(data_tight))

#define binedges
#print(data_loose['FakeEPt'].max(),data_loose['FakeEEta'].max())
pt_bins=[27,50,1000] #pt edges
eta_bins=[0,1.37,1.52,2.5] #eta edges
edges=[pt_bins,eta_bins]

######################################################################################

#make 2d histograms with the respective binedges
print('making eta histograms')
hist_tight,xbins_tight,ypatches_tight=plt.hist(data_tight['FakeEEta'], bins=eta_bins)
hist_loose,xbins_loose,ypatches_loose=plt.hist(data_loose['FakeEEta'], bins=eta_bins)

hist_WZ_tight,xbins_WZ_tight,ypatches_WZ_tight=plt.hist(WZ_tight['FakeEEta'], bins=eta_bins, weights=WZ_tight['weight'])
hist_WZ_loose,xbins_WZ_loose,ypatches_WZ_loose=plt.hist(WZ_loose['FakeEEta'], bins=eta_bins, weights=WZ_loose['weight'])

hist_WZ2_tight,xbins_WZ2_tight,ypatches_WZ2_tight=plt.hist(WZ_tight['FakeEEta'], bins=eta_bins, weights=(WZ_tight['weight'])**2)
hist_WZ2_loose,xbins_WZ2_loose,ypatches_WZ2_loose=plt.hist(WZ_loose['FakeEEta'], bins=eta_bins, weights=(WZ_loose['weight'])**2)

hist_MC_tight,xbins_MC_tight,ypatches_MC_tight=plt.hist(MC_tight['FakeEEta'], bins=eta_bins, weights=MC_tight['weight'])
hist_MC_loose,xbins_MC_loose,ypatches_MC_loose=plt.hist(MC_loose['FakeEEta'], bins=eta_bins, weights=MC_loose['weight'])

#calculate fake eff by dividing the tight histogram with the loose histogram
print('calculate fake efficiency')
print(hist_tight,hist_loose)
num=hist_tight-hist_WZ_tight
denom=hist_loose-hist_WZ_loose
fakeeff=num/denom
fakeeff[1:2]=0

num_MC=hist_MC_tight
denom_MC=hist_MC_loose
fakeeff_MC=num_MC/denom_MC
fakeeff_MC[1:2]=0
#print(fakeeff)

#calculate errors    
print('calculate errors')
print(hist_tight,hist_WZ_tight,num)
#errorfakeeff=1/denom*np.sqrt(num*(1-num/denom))
#errorfakeeff=fakeeff*np.sqrt(1/num+1/denom)
#errorfakeeff=fakeeff*np.sqrt((hist_tight/(num**2))+(hist_WZ_tight/(num**2))+(hist_loose/(denom**2))+(hist_WZ_loose/(denom**2)))
errorfakeeff=fakeeff*np.sqrt((hist_tight/(num**2))+(hist_WZ2_tight/(num**2))+(hist_loose/(denom**2))+(hist_WZ2_loose/(denom**2)))
#print(errorfakeeff)
errorfakeeff[1:2]=0
errorfakeeff_MC=fakeeff_MC*np.sqrt(1/num_MC+1/denom_MC)
errorfakeeff_MC[1:2]=0

#calculate the fake factor
print('calculate fake factor')
fakefactor=fakeeff/(1-fakeeff)
errorfakefactor=(errorfakeeff)/((1-fakeeff)**2)
fakefactor_MC=fakeeff_MC/(1-fakeeff_MC)
errorfakefactor_MC=(errorfakeeff_MC)/((1-fakeeff_MC)**2)

#plot the given histrogram with the given binedges
print('plot the results')
plt.figure(6)
y_edges=np.array(eta_bins)
x_bins=0.5*(y_edges[1:]+y_edges[:-1])
x_errors=0.5*(y_edges[1:]-y_edges[:-1])
plt.errorbar(x_bins, fakeeff, yerr=errorfakeeff, xerr=x_errors, ls='none',label='Data')
plt.errorbar(x_bins, fakeeff_MC, yerr=errorfakeeff_MC, xerr=x_errors, ls='none',label='Z+jets MC')
plt.ylim([0,1.5])
plt.xlabel(r'electron $\eta$', horizontalalignment='right', x=1.0)
plt.ylabel(r'Fake Efficiency', horizontalalignment='right', y=1.0)
plt.title('Fake Efficiency, Electron Channel')
plt.legend()
print('save')
plt.savefig('root/FE_2dEta')

plt.figure(2)
y_edges=np.array(eta_bins)
x_bins=0.5*(y_edges[1:]+y_edges[:-1])
x_errors=0.5*(y_edges[1:]-y_edges[:-1])
plt.errorbar(x_bins, fakefactor, yerr=errorfakefactor, xerr=x_errors, ls='none',label='Data')
plt.errorbar(x_bins, fakefactor_MC, yerr=errorfakefactor_MC, xerr=x_errors, ls='none',label='Z+jets MC')
plt.ylim([0,1.5])
plt.xlabel(r'electron $\eta$', horizontalalignment='right', x=1.0)
plt.ylabel(r'Fake Efficiency', horizontalalignment='right', y=1.0)
plt.title('Fake Factor, Electron Channel')
plt.legend()
print('save')
plt.savefig('root/FF_2dEta')

##############

print('making pt histograms')
hist_tight,xbins_tight,ypatches_tight=plt.hist(data_tight['FakeEPt'], bins=pt_bins)
hist_loose,xbins_loose,ypatches_loose=plt.hist(data_loose['FakeEPt'], bins=pt_bins)

hist_WZ_tight,xbins_WZ_tight,ypatches_WZ_tight=plt.hist(WZ_tight['FakeEPt'], bins=pt_bins, weights=WZ_tight['weight'])
hist_WZ_loose,xbins_WZ_loose,ypatches_WZ_loose=plt.hist(WZ_loose['FakeEPt'], bins=pt_bins, weights=WZ_loose['weight'])

hist_WZ2_tight,xbins_WZ2_tight,ypatches_WZ2_tight=plt.hist(WZ_tight['FakeEPt'], bins=pt_bins, weights=(WZ_tight['weight'])**2)
hist_WZ2_loose,xbins_WZ2_loose,ypatches_WZ2_loose=plt.hist(WZ_loose['FakeEPt'], bins=pt_bins, weights=(WZ_loose['weight'])**2)

hist_MC_tight,xbins_MC_tight,ypatches_MC_tight=plt.hist(MC_tight['FakeEPt'], bins=pt_bins, weights=MC_tight['weight'])
hist_MC_loose,xbins_MC_loose,ypatches_MC_loose=plt.hist(MC_loose['FakeEPt'], bins=pt_bins, weights=MC_loose['weight'])

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

#plot the given histrogram with the given binedges
print('plot the results')
plt.figure(3)
x_edges=np.array(pt_bins)
x_bins=0.5*(x_edges[1:]+x_edges[:-1])
x_errors=0.5*(x_edges[1:]-x_edges[:-1])
plt.errorbar(x_bins, fakeeff, yerr=errorfakeeff, xerr=x_errors, ls='none',label='Data')
plt.errorbar(x_bins, fakeeff_MC, yerr=errorfakeeff_MC, xerr=x_errors, ls='none',label='Z+jets MC')
plt.ylim([0,1.5])
plt.xlabel(r'electron $p_T$', horizontalalignment='right', x=1.0)
plt.ylabel(r'Fake Efficiency', horizontalalignment='right', y=1.0)
plt.title('Fake Efficiency, Electron Channel')
plt.legend()
print('save')
plt.savefig('root/FE_2dPt')

plt.figure(4)
x_edges=np.array(pt_bins)
x_bins=0.5*(x_edges[1:]+x_edges[:-1])
x_errors=0.5*(x_edges[1:]-x_edges[:-1])
plt.errorbar(x_bins, fakefactor, yerr=errorfakefactor, xerr=x_errors, ls='none',label='Data')
plt.errorbar(x_bins, fakefactor_MC, yerr=errorfakefactor_MC, xerr=x_errors, ls='none',label='Z+jets MC')
plt.ylim([0,1.5])
plt.xlabel(r'electron $p_T$', horizontalalignment='right', x=1.0)
plt.ylabel(r'Fake Efficiency', horizontalalignment='right', y=1.0)
plt.title('Fake Factor, Electron Channel')
plt.legend()
print('save')
plt.savefig('root/FF_2dPt')
