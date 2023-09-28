#this file takes a output.root and calculates a weight for each MC event in there to scale it to the data

import ROOT
import numpy as np
from array import array
import os
import pandas as pd

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
    print('SOW=',sow)
    return sow

#luminosity values are in pb^-1 and from https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/TopGroupDataDerivationList#Lumicalc_GRL_and_PRW_files
#that corresponds to lumitag OflLumi-13TeV-009 for toroid-on data set (see: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/GoodRunListsForAnalysisRun2)
lumi_2015=3.24454*10**3
lumi_2016=33.4022*10**3
lumi_2017=44.6306*10**3
lumi_2018=58.7916*10**3

#dictionaries
dic_lumi={'2016':lumi_2015+lumi_2016, '2017':lumi_2017, '2018':lumi_2018}
dic_name={'tight':'nominal','loose':'nominal_Loose'}

#replace both for loops with funktion, use dic to convert tight to nominal, return weightlist
def MC_Weights(MCinput,branch,year):

    #use the input to get all the needed variables, mostly via dics
    inputPath=MCinput
    chainName=dic_name[branch]
    lumi=dic_lumi[year]

    sumOfWeights=getSumWeights(inputPath)

    chain=ROOT.TChain(chainName)
    for files in os.listdir(inputPath):
        chain.Add(inputPath+"/"+files)

    print('chain=',chain)

    #print(chain.GetEntries())
    print('calculating MC weights in {}'.format(MCinput),'for',chainName)

    #calculate weights for each entry
    weightList=[]

    for entryNum in range(0,chain.GetEntries()):
        chain.GetEntry(entryNum)
        weight_mc=getattr(chain,"weight_mc")
        #print('weight_mc=',weight_mc)
        weight_pileup=getattr(chain,"weight_pileup")
        #print('weight_pileup=',weight_pileup)
        weight_leptonSF=getattr(chain,"weight_leptonSF")
        #print('weight_leptonSF=',weight_leptonSF)
        weight_photonSF=getattr(chain,"weight_photonSF")
        #print('weight_photonSF=',weight_photonSF)
        weight_jvt=getattr(chain,"weight_jvt")
        #print('weight_jvt=',weight_jvt)
        weight_bTagSF_DL1r_77=getattr(chain,"weight_bTagSF_DL1r_77")
        #print('weight_b=',weight_bTagSF_DL1r_77)
        xsec=getattr(chain,"xsec")
        #print('xsec=',xsec)
        kfactor=getattr(chain,"kfactor")
        #print('kfactor=',kfactor)
                
        MCfactor=(xsec)*(kfactor)*(weight_pileup)*(weight_leptonSF)*(weight_photonSF)*(weight_bTagSF_DL1r_77)*(weight_jvt)
        #print('MCfactor=',MCfactor)
        #print(sumOfWeights)
        #print('weight_mc/sumOfWeights=',weight_mc/sumOfWeights)
        weight=lumi*MCfactor*weight_mc/sumOfWeights
        #print('weight=',weight)

        weightList.append(weight)

        #print(len(weightList))

    weightList=pd.DataFrame(weightList,columns=['weight'])

    return weightList
    #weightList.to_csv('WZ_'+dic[n]+'_'+f+'_weight.csv', index=False)