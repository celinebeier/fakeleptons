#import ROOT
import numpy as np
import pandas
import matplotlib.pyplot as plt
import ROOT
from array import array

#name_list=["Wy","Zy","tty","VVy","Vyy","Zjets","Wjets","tt","yy","yjets","VV"]
name_list=["Wy","Zy","tty","VVy","Vyy","Zjets","Wjets","tt","yy","VV","error"]
outputFile=ROOT.TFile('/afs/cern.ch/user/c/cbeier/fakeleptons/root/'+"Comp_CR.root","recreate")

list_light=[]
list_c=[]
list_b=[]
l_0=0
l_1=0
l_2=0
l_3=0
l_4=0
l_5=0
l_6=0
l_7=0
l_8=0
l_9=0
l_10=0
l_11=0
l_error_0=[]
l_error_1=[]
l_error_2=[]
l_error_3=[]
l_error_4=[]
l_error_5=[]
l_error_6=[]
l_error_7=[]
l_error_8=[]
l_error_9=[]
l_error_10=[]
l_error_11=[]

for name in name_list:
    if name=="Zjets":
        print('reading in'+name)
        MC_loose=pandas.read_csv('/eos/user/c/cbeier/csv/MC_loose.csv')
    
        MC_loose=MC_loose[(MC_loose['ZM0Pt']>=27)&(MC_loose['ZM1Pt']>=27)]
        MC_loose=MC_loose[(MC_loose['MET']<=40)]
        MC_loose=MC_loose[(MC_loose['FakeEPt']>=27)]

        #loose cut
        MC_loose=MC_loose[(MC_loose['FakeEd0sig']<=5)]

        #tight selection
        MC_tight=MC_loose 

        #make tight selection - don't touch! 
        MC_tight=MC_tight[MC_tight['FakeEIDTight']==1] #Iso WP
        MC_tight=MC_tight[MC_tight['FakeEd0sig']<=5] #Iso WP
        MC_tight=MC_tight[MC_tight['FakeEIsolationFCTight']==1] #Iso WP

        print('making histograms')

        bins=[0,1,2,3,4,5,6,7,8,9,10,11,12]
        #xticks=bins
        #xticks_labels=['Unknown','KnownUnknown','Prompt electrons','Charge-flip electrons','Prompt muons','Prompt photon-conversions','Electrons from muons','Tau decays','b-hadron decays','c-hadron decays','Light-flavour decays','Charge-flip muons']

        plt.figure(1)
        fig,ax=plt.subplots()
        n,bins,patches=ax.hist(MC_tight['FakeEID'],bins=bins,align='left',weights=MC_tight['weight']) #weights=MC_tight['weight']
        n_error,bins,patches=ax.hist(MC_tight['FakeEID'],bins=bins,align='left',weights=(MC_tight['weight'])**2) #weights=MC_tight['weight']
        n_error=np.sqrt(n_error)

        list_light.append(n[10])
        list_b.append(n[8])
        list_c.append(n[9])
        l_0=l_0+n[0]
        l_1=l_1+n[1]
        l_2=l_2+n[2]
        l_3=l_3+n[3]
        l_4=l_4+n[4]
        l_5=l_5+n[5]
        l_6=l_6+n[6]
        l_7=l_7+n[7]
        l_8=l_8+n[8]
        l_9=l_9+n[9]
        l_10=l_10+n[10]
        l_11=l_11+n[11]
        l_error_0.append(n_error[0])
        l_error_1.append(n_error[1])
        l_error_2.append(n_error[2])
        l_error_3.append(n_error[3])
        l_error_4.append(n_error[4])
        l_error_5.append(n_error[5])
        l_error_6.append(n_error[6])
        l_error_7.append(n_error[7])
        l_error_8.append(n_error[8])
        l_error_9.append(n_error[9])
        l_error_10.append(n_error[10])
        l_error_11.append(n_error[11])
        #save in root file
        hardcoded_bins = array('d', bins)

        hist=ROOT.TH1F(name,"",len(hardcoded_bins)-1,hardcoded_bins)

        for i in range(len(n)): #y axis - eta
            hist.SetBinContent(i+1,n[i])
            hist.SetBinError(i+1,n_error[i])
    
        hist.Write()
        
    elif name=="error":
        error_0=np.sqrt(sum(x**2 for x in l_error_0 if x > 0))    
        error_1=np.sqrt(sum(x**2 for x in l_error_1 if x > 0))    
        error_2=np.sqrt(sum(x**2 for x in l_error_2 if x > 0))    
        error_3=np.sqrt(sum(x**2 for x in l_error_3 if x > 0))    
        error_4=np.sqrt(sum(x**2 for x in l_error_4 if x > 0))    
        error_5=np.sqrt(sum(x**2 for x in l_error_5 if x > 0))    
        error_6=np.sqrt(sum(x**2 for x in l_error_6 if x > 0))    
        error_7=np.sqrt(sum(x**2 for x in l_error_7 if x > 0))    
        error_8=np.sqrt(sum(x**2 for x in l_error_8 if x > 0))    
        error_9=np.sqrt(sum(x**2 for x in l_error_9 if x > 0))    
        error_10=np.sqrt(sum(x**2 for x in l_error_10 if x > 0))    
        error_11=np.sqrt(sum(x**2 for x in l_error_11 if x > 0))

        errors=[error_0,error_1,error_2,error_3,error_4,error_5,error_6,error_7,error_8,error_9,error_10,error_11]    
        print('errors',errors)
        n=[l_0,l_1,l_2,l_3,l_4,l_5,l_6,l_7,l_8,l_9,l_10,l_11]

        #save in root file
        hardcoded_bins = array('d', bins)

        hist=ROOT.TH1F(name,"",len(hardcoded_bins)-1,hardcoded_bins)

        for i in range(len(n)): #y axis - eta
            hist.SetBinContent(i+1,n[i])
            hist.SetBinError(i+1,errors[i])
    
        hist.Write()
        
    else:
        bins=[0,1,2,3,4,5,6,7,8,9,10,11,12]
        n=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        n_error=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        hardcoded_bins = array('d', bins)

        hist=ROOT.TH1F(name,"",len(hardcoded_bins)-1,hardcoded_bins)

        for i in range(len(n)): #y axis - eta
            hist.SetBinContent(i+1,n[i])
            hist.SetBinError(i+1,n_error[i])
    
        hist.Write()
        
print('sum non-neg light:',sum(x for x in list_light if x > 0))
print('sum non-neg heavy:',(sum(x for x in list_b if x > 0)+sum(x for x in list_c if x > 0)))
print('------')
print('sum light:',l_10)
print('error light:',np.sqrt(sum(x**2 for x in l_error_10 if x > 0)))
print('sum heavy:',l_8+l_9)
error_heavy=np.sqrt((np.sqrt(sum(x**2 for x in l_error_8 if x > 0)))**2+(np.sqrt(sum(x**2 for x in l_error_9 if x > 0)))**2)
print('error light:',error_heavy)