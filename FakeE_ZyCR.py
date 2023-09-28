import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt
from array import array

name='ZyCR'

dic_bins={'VR':[0,80,100,120,140,160,180,200,220,240,260,280,310,340,370,400,440,500,600],
          'SR':[0,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,235,250,270,290,310,340,370,400,450,500], 
          'WyCR':[0,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,470,500,530,570,610,650,750],
          'ZyCR':[0,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,390,420,460,500,600],
          'ZjetsCR':[0,80,100,120,140,160,180,200,220,240,260,280,300,330,360,400,500],
          'WjetsCR':[0,80,100,120,140,160,180,200,240,300,400]}

bins=dic_bins[name]

print('reading in data')
data_loose=pandas.read_csv('/eos/user/c/cbeier/csv/'+name+'_Data_loose.csv')
print('reading in MC')
WZ_loose=pandas.read_csv('/eos/user/c/cbeier/csv/'+name+'_MC_loose.csv')
print('start',len(data_loose),len(WZ_loose),sum(WZ_loose['weight']))

#choose fake e's
data_loose=data_loose[(data_loose['E27Counter']==2)]
WZ_loose=WZ_loose[(WZ_loose['E27Counter']==2)]
#print('fake E',len(data_loose),len(WZ_loose),sum(WZ_loose['weight']))

#add PT cuts - 27GeV for analysis
data_loose=data_loose[(data_loose['E1Pt']>=27)]
WZ_loose=WZ_loose[(WZ_loose['E1Pt']>=27)]
#print('Pt cut',len(data_loose),len(WZ_loose),sum(WZ_loose['weight']))

#test that E1 is always the leading lepton
#print(len(data_loose))
#data_loose=data_loose.query('E1Pt > E2Pt')
#print(len(data_loose))

#loose cut
data_loose=data_loose[(data_loose['E1d0sig']<=5)]
WZ_loose=WZ_loose[(WZ_loose['E1d0sig']<=5)]
print('d0sig cut',len(data_loose),len(WZ_loose),sum(WZ_loose['weight']))

#eta -> abs(eta)
data_loose['E1Eta']=abs(data_loose['E1Eta'])
WZ_loose['E1Eta']=abs(WZ_loose['E1Eta'])

#truthmatching
WZ_loose=WZ_loose[(WZ_loose['E1ID']==2)]

#make column for fake factor
data_loose['F']=0
WZ_loose['F']=0
data_loose['EF']=0
WZ_loose['EF']=0
print('add F',len(data_loose),len(WZ_loose),sum(WZ_loose['weight']))

######## do 1 electron/ muon events first!

#select loose electrons/ muons from baseline sample
data_nt=data_loose[(data_loose['E1IsolationFCTight']==0)&(data_loose['E1IDTight']==0)]
WZ_nt=WZ_loose[(WZ_loose['E1IsolationFCTight']==0)&(WZ_loose['E1IDTight']==0)]
#data_nt_1m=data_loose[(data_loose['MuonCounter']==1)&(data_loose['M1IsolationFCTight']==0)&(data_loose['M1d0sig']>3)]
print('data nt',len(data_nt),len(WZ_nt))

#histogram edges
pt_bins=[10,15,20,27,35,50,1000] #pt edges
eta_bins=[0,1.37,1.52,2.5] #eta edges
edges=[pt_bins,eta_bins]

#get fake factor
fakefactor=np.genfromtxt("root/fakefactor.csv", delimiter=',')
errorfakefactor=np.genfromtxt("root/errorfakefactor.csv", delimiter=',')
print(fakefactor)

count=0

for i in range(0,len(data_loose)):
    if (data_loose.iloc[i]['E1IsolationFCTight'] == 0 and data_loose.iloc[i]['E1IDTight'] == 0):
        count=count+1
        #print(count)
        #print(data_loose.iloc[i]['E1Pt'],data_loose.iloc[i]['E1Eta'])
        row=data_loose.iloc[[i]]
        row=row.reset_index(drop=True)
        plt.figure(1)
        hist,xbins,ybins,im=plt.hist2d(row['E1Pt'], row['E1Eta'], bins=edges)
        hist=hist.T
        rowFF=hist*fakefactor
        rowFFerr=hist*errorfakefactor
        rowFF=np.sum(rowFF)
        rowFFerr=np.sum(rowFFerr)
        #print(type(data_loose))
        #print(data_loose)
        data_loose.iloc[[i],[-2]]=rowFF
        data_loose.iloc[[i],[-1]]=rowFFerr
    else: continue
        
print('count',count)
data_test=data_loose[(data_loose['F']!=0)]
print('test',len(data_test))
#print(data_test)
#print(data_loose_new)

for i in range(0,len(WZ_loose)):
    if (WZ_loose.iloc[i]['E1IsolationFCTight'] == 0 and WZ_loose.iloc[i]['E1IDTight'] == 0):
        #count=count+1
        #print(count)
        #print(data_loose.iloc[i]['E1Pt'],data_loose.iloc[i]['E1Eta'])
        row=WZ_loose.iloc[[i]]
        row=row.reset_index(drop=True)
        plt.figure(2)
        hist,xbins,ybins,im=plt.hist2d(row['E1Pt'], row['E1Eta'], bins=edges)
        hist=hist.T
        rowFF=hist*fakefactor
        rowFFerr=hist*errorfakefactor
        rowFF=np.sum(rowFF)*(-1) #-1 for MC
        rowFFerr=np.sum(rowFFerr)
        #print(type(data_loose))
        #print(data_loose)
        WZ_loose.iloc[[i],[-2]]=rowFF
        WZ_loose.iloc[[i],[-1]]=rowFFerr
    else: continue

#print(data_loose,WZ_loose)
#data_loose['fweight']=data_loose['F']*data_loose['weight']
#WZ_loose['fweight']=WZ_loose['F']*WZ_loose['weight']

#######concat two dataframes
print(len(data_loose),len(WZ_loose),sum(WZ_loose['weight']))
data_plot=pandas.concat([data_loose,WZ_loose])
#data_plot=data_loose
#print(len(data_plot))
print(data_plot)

#plot
plt.figure(2)
n,bins,patches=plt.hist(data_plot['invmWy_fit'],weights=data_plot['F']*data_plot['weight'],bins=bins)
#plt.xlabel('invmWy_fit')
#plt.savefig('root/FakeEVR')

print('n',n)
#plt.figure(2)
#n_data,bins_1,patches_1=plt.hist(data_loose['invmWy_fit'],weights=data_loose['F']*data_loose['weight'],bins=bins)
#plt.figure(3)
#n_2,bins_1,patches_1=plt.hist(WZ_loose['invmWy_fit'],weights=WZ_loose['F']*WZ_loose['weight'],bins=bins)

#calculate errors

#plt.figure(3)
#n_data,bins_1,patches_1=plt.hist(data_loose['invmWy_fit'],bins=bins)
#print(n_data)
#n_data is the amount of data events in a bin
#plt.figure(4)
#n_MC,bins_1,patches_1=plt.hist(WZ_loose['invmWy_fit'],weights=(WZ_loose['weight'])**2,bins=bins)
#print(n_MC)
#n_MC is the real subtracted number, but with weights to make it equal
#n_error=np.sqrt(n_data+n_MC)

#plt.figure(3)
n_error,bins,patches=plt.hist(data_plot['invmWy_fit'],weights=(data_plot['EF']*data_plot['weight'])**2,bins=bins)
#print(n_error)
n_error=np.sqrt(n_error)
print(n_error)

expectedFakes=sum(data_plot['F']*data_plot['weight'])
print('expectedFakes',expectedFakes)
error=sum(n_error)
print('error:',error)
expectedFakes_str=str(expectedFakes)
error_str=str(error)
with open('root/'+name+'_FakeE.txt', "w") as file:
   lines = [name+'\n', 'total expexted fakes: '+expectedFakes_str+'\n', 'error: '+error_str+'\n']
   file.writelines(lines)
   file.close()

outputFile=ROOT.TFile('/afs/cern.ch/user/c/cbeier/fakeleptons/root/'+name+"_FakeE.root","recreate")

hardcoded_bins = array('d', bins)

hist=ROOT.TH1F(name,"",len(hardcoded_bins)-1,hardcoded_bins)

for i in range(len(n)): #y axis - eta
    hist.SetBinContent(i+1,n[i])
    hist.SetBinError(i+1,n_error[i])
    
hist.Write()