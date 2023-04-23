----- outdated ----

#this file takes a output.root and calculates a weight for each MC event in there to scale it to the data

import ROOT
import numpy as np
from array import array
import os
import pandas as pd

#get sum of weights from root file
def getSumWeights(dsidPath,f):
    sow=0
    sowChain=ROOT.TChain("sumWeights")
    print("calculating SoW in {}".format(dsidPath),'for',f)
    for files in os.listdir(dsidPath):
        if f in files: #select only files with the right fake lepton
            #print(files)
            sowChain.Add(dsidPath+"/"+files)
        else: continue #skip other files
    for entryNum in range(0,sowChain.GetEntries()):
        sowChain.GetEntry(entryNum)
        totalEventsWeighted = getattr(sowChain ,"totalEventsWeighted") 
        sow+=totalEventsWeighted
    return sow

#luminosity values are in fb and from #all are in fb and from https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/TopGroupDataDerivationList#Lumicalc_GRL_and_PRW_files
lumi_2015=3.220
lumi_2016=32.99
lumi_2017=44.31
lumi_2018=58.45

#dictionaries
dic_lumi={'2016':lumi_2015+lumi_2016, '2017':lumi_2017, '2018':lumi_2018}
dic_name={'tight':'nominal','loose':'nominal_Loose'}

#replace both for loops with funktion, use dic to convert tight to nominal, return weightlist
def MC_Weights(MCinput,f,branch,year):

    #use the input to get all the needed variables, mostly via dics
    inputPath=MCinput
    chainName=dic_name[branch]
    lumi=dic_lumi[year]

    sumOfWeights=getSumWeights(inputPath,f)

    chain=ROOT.TChain(chainName)
    for files in os.listdir(inputPath):
        if f in files: #select only files with the right fake lepton
            chain.Add(inputPath+"/"+files)
        else: continue #skip other files
    #chain.Add(inputPath+'/'+'output_'+f+'.root') #loop for multiple files

    #print(chain.GetEntries())
    print('calculating MC weights in {}'.format(MCinput),'for',f,chainName)

    #calculate weights for each entry
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

        #print(len(weightList))

    weightList=pd.DataFrame(weightList,columns=['weight'])

    return weightList
    #weightList.to_csv('WZ_'+dic[n]+'_'+f+'_weight.csv', index=False)