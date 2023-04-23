###### outdated ######

#this file takes a output.root and calculates a weight for each MC event in there to scale it to the data

import ROOT
import numpy as np
from array import array
import os
import pandas as pd

inputPath="/afs/cern.ch/user/c/cbeier/AnalysisTop/run"
outputPath="/afs/cern.ch/user/c/cbeier/PyRoot/" #maybe change to EOS

chainName="nominal"
chain=ROOT.TChain(chainName)
chain.Add(inputPath+"/"+"output_FakeM.root") #loop for multiple files

print(chain.GetEntries())

histbins=[-1e-4,-1e-5,-1e-6,0,1e-6,1e-5,1e-4]
bins=array("d",histbins)

hist=ROOT.TH1F("hist1","hist1",len(bins)-1,bins)

#get sum of weights from root file
def getSumWeights(dsidPath):
    sow=0
    sowChain=ROOT.TChain("sumWeights")
    print("calculating SoW in {}".format(dsidPath))
    for files in os.listdir(dsidPath):
        sowChain.Add(dsidPath+"/"+files)
    for entryNum in range(0,sowChain.GetEntries()):
        sowChain.GetEntry(entryNum)
        totalEventsWeighted = getattr(sowChain ,"totalEventsWeighted") 
        sow+=totalEventsWeighted
    return sow

sumOfWeights=getSumWeights('/afs/cern.ch/user/c/cbeier/AnalysisTop/run')

#luminosity values are in fb and from #all are in fb and from https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/TopGrou
lumi_2015=3.220
lumi_2016=32.99
lumi_2017=44.31
lumi_2018=58.45
lumi=lumi_2015+lumi_2016

#calculate weights for each entry in output.root
weightList=[]

for entryNum in range(0,chain.GetEntries()):
    chain.GetEntry(entryNum)
    weight_mc=getattr(chain,"weight_mc")
    weight_pileup=getattr(chain,"weight_pileup")
    weight_leptonSF=getattr(chain,"weight_leptonSF")
    weight_photonSF=getattr(chain,"weight_photonSF")
    weight_jvt=getattr(chain,"weight_jvt")
    weight_bTagSF_DL1r_77=getattr(chain,"weight_bTagSF_DL1r_77")
    xsec=getattr(chain,"xsec")
    kfactor=getattr(chain,"kfactor")

        
    MCfactor=(xsec)*(kfactor)*(weight_pileup)*(weight_leptonSF)*(weight_photonSF)*(weight_bTagSF_DL1r_77)*(weight_jvt)
    weight=lumi*MCfactor*(weight_mc)/sumOfWeights

    weightList.append(weight)
    hist.Fill(weight)

print(weightList)

outputFile=ROOT.TFile(outputPath+"hist.root","recreate")
hist.Write()

weightList=pd.DataFrame(weightList)

weightList.to_csv('WZ_tight_FakeM_weight.csv', index=False)