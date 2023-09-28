import ROOT
import numpy as np
from array import array

inputPath="/afs/cern.ch/user/c/cbeier/AnalysisTop/run/"
outputPath="/afs/cern.ch/user/c/cbeier/PyRoot/" #maybe change to EOS

chainName="nominal"
chain=ROOT.TChain(chainName)
chain.Add(inputPath+"output.root") #loop for multiple files

print(chain.GetEntries())

histbins=[0,10,100,1000,10000,100000,1000000,10000000]
bins=array("d",histbins)

hist=ROOT.TH1F("hist1","hist1",len(bins)-1,bins)

for entryNum in range(0,chain.GetEntries()):
    chain.GetEntry(entryNum)
    ElectronE=getattr(chain,"ElectronE")
    MuonE=getattr(chain,"MuonE")
    ElectronNum=getattr(chain,"ElectronCounter")
    #print(leptonPx)
    if ElectronNum=2:
        hist.Fill(ElectronE[0]+ElectronE[1])    #(leptonPx,weight)
    elif ElectronNum=1:
        hist.Fill(MuonE[0]+MuonE[1])
    else:
        print("something went wrong :(")

outputFile=ROOT.TFile(outputPath+"hist.root","recreate")

hist.Write()