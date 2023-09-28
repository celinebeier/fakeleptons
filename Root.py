import multiprocessing as mp
import numpy as np
import os
import ROOT
import sys
from time import sleep
from array import array
import math
import pandas as pd

from collections import defaultdict, namedtuple

ROOT.ROOT.EnableImplicitMT()

loopForHist_data=False
loopForHist_MC=False

maxPercentage=-1

variable="invmWy_fit"
WyCR_varBins = [0,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,470,500,530,570,610,650,750]
ZjetsCR_varBins = [0,80,100,120,140,160,180,200,220,240,260,280,300,330,360,400,500]
WjetsCR_varBins=[0,80,100,120,140,160,180,200,240,300,400]
ZyCR_varBins = [0,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,390,420,460,500,600]
SR_varBins = [0,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,235,250,270,290,310,340,370,400,450,500]
VR_varBins=[0,80,100,120,140,160,180,200,220,240,260,280,310,340,370,400,440,500,600]

region_varBins={'WyCRSelection':WyCR_varBins,'ZjetsCRSelection':ZjetsCR_varBins,
                'WjetsCRSelection':WjetsCR_varBins,'ZyCRSelection':ZyCR_varBins,'SRSelection':SR_varBins,
                'VRSelection':VR_varBins}
                
MZ=91.188
nbins=80
pt_bins = np.array([27,35,45,55,70,90,120,2000])
eta_bins = np.array([0.0,0.6,1.37,1.52,1.82,2.37])
ptBins=np.array([27,35,45,55,70,90,120,2000])
etaBins=[[0,0.6],[0.6,1.37],[1.52,1.82],[1.82,2.37]]

inputPathList={"a":"/eos/user/z/zhelun/output/MC16a_p14/","d":"/eos/user/u/upatel/ChargedHiggs/DAODPHYS_skim/p14_d/","e":"/eos/user/u/upatel/ChargedHiggs/DAODPHYS_skim/p14_e/"}
inputPath_MCList={"a":inputPathList["a"]+"Zjets","d":inputPathList["d"]+"Zjets","e":inputPathList["e"]+"Zjets"}
inputPath_dataList={"a":inputPathList["a"]+"Data","d":inputPathList["d"]+"Data","e":inputPathList["e"]+"Data"}
lumiList={"a":3244.54+33402.2,"d":44630.6,"e":58791.6}

tree_name="nominal"
egamma_region_name="ely"
ee_region_name="ee"

SaveDir="/afs/cern.ch/user/c/cbeier/fakeleptons/"
output_filepath_MC=SaveDir+"/egammaRates_MC/egammaFakesOutput.root"
output_filepath_data=SaveDir+"/egammaRates_data/egammaFakesOutput.root"
out_dir_data=SaveDir+"/egammaRates_data"
out_dir_MC=SaveDir+"/egammaRates_MC"

if not os.path.exists(out_dir_data):
    os.makedirs(out_dir_data)

if not os.path.exists(out_dir_MC):
    os.makedirs(out_dir_MC)

#For fit:
input_file_data=SaveDir+"/egammaRates_data/egammaFakesOutput.root"
input_file_MC=SaveDir+"/egammaRates_MC/egammaFakesOutput.root"

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

def addFile(inputPathList,chainName,lumiList):
    chain = ROOT.TChain(chainName)
    DSID_entryMarks=[]
    lumiMarks=[]
    for key,inputPath in inputPathList.items():
        for filename in os.listdir(inputPath):
            print("Producing Chain in {}".format(inputPath))
            print("Current DSID folder: {}".format(filename))
            filePath=inputPath+"/"+filename
            
            for file in os.listdir(filePath):
                chain.Add(filePath+"/"+file)
            tmpEntry=chain.GetEntries()
            DSID_entryMarks.append(tmpEntry)
            lumiMarks.append(lumiList[key])
    print(DSID_entryMarks)
    return chain,DSID_entryMarks,lumiMarks

def produceHist(etaBins,ptBins,name):
    egammaHist=[]
    eeHist=[]
    #ee1Hist=[]
    #ee2Hist=[]
    for i in range(len(etaBins)):
        for j in range(len(ptBins)-1):
            hist_suffix = "_eta{}_pt{}".format(etaBins[i][0],int(ptBins[j]))
            egammaHist.append(ROOT.TH1F(name+"_egamma"+hist_suffix,name+"_egamma"+hist_suffix,nbins,MZ-25,MZ+25))
            eeHist.append(ROOT.TH1F(name+"_ee"+hist_suffix,name+"_ee"+hist_suffix,nbins,MZ-25,MZ+25))
            #ROOT.TH1F("data_ee1"+hist_suffix,"data_ee1"+hist_suffix,nbins,MZ-25,MZ+25)
            #ROOT.TH1F("data_ee2"+hist_suffix,"data_ee2"+hist_suffix,nbins,MZ-25,MZ+25)
    return egammaHist,eeHist
    
def getWeight(chain,sumOfWeights,lumi):
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
    return weight

def getBin(pt,eta):
    absEta=abs(eta)
       
    ptIndex=-1
    for i in range(len(ptBins)-1):
        if((pt>ptBins[i])and(pt<ptBins[i+1])):
            ptIndex=i
    etaIndex=-1
    for i in range(len(etaBins)):
        if((absEta>etaBins[i][0])and(absEta<etaBins[i][1])):
            etaIndex=i
    index=-1
    if((ptIndex>=0) and (etaIndex>=0)):
        index= etaIndex*(len(ptBins)-1)+ptIndex

    return index

def getVariables(chain,sowList,EntryMarks,lumiMarks,isMC):

    if(isMC):
        eyHist,eeHist=produceHist(etaBins,ptBins,"MC")
    else:
        eyHist,eeHist=produceHist(etaBins,ptBins,"data")

    tmpDSID_markCount=0
    sumOfWeights=sowList[0]
    lumi=lumiMarks[0]
    print("Starting with DSID #{}, with sumOfWeights = {}, and luminosity = {}".format(tmpDSID_markCount,sumOfWeights,lumi))
    selectedWeights=0
    eventPrintoutMarker=int(chain.GetEntries()*0.01)
    for entryNum in range(0,chain.GetEntries()):
        chain.GetEntry(entryNum)

        if ((maxPercentage>0) and (entryNum*100.0/chain.GetEntries()>maxPercentage)):
            break

        if (isMC):
            if(entryNum>EntryMarks[tmpDSID_markCount]):
                tmpDSID_markCount+=1
                sumOfWeights=sowList[tmpDSID_markCount]
                lumi=lumiMarks[tmpDSID_markCount]
                print("jumping to DSID #{}, with sumOfWeights = {}, and luminosity = {}".format(tmpDSID_markCount,sumOfWeights,lumi))

        if(entryNum%eventPrintoutMarker==0 and entryNum>0):
            print("{} Events processed, {}% finished".format(entryNum,entryNum*100.0/chain.GetEntries()))
        
        if isMC:
            weight=getWeight(chain,sumOfWeights,lumi)
        else:
            weight=1

        ee = getattr(chain ,"ee")
        ey = getattr(chain ,"ely")
        targetVar = getattr(chain ,variable)

        if(ee):
            leadLepPt=getattr(chain,"leptonPt")[0]
            leadLepEta=getattr(chain,"leptonEta")[0]
            subLeadLepPt=getattr(chain,"leptonPt")[1]
            subLeadLepEta=getattr(chain,"leptonEta")[1]
            invmll=getattr(chain,"invmll")
            leadBin=getBin(leadLepPt,leadLepEta)
            subLeadBin=getBin(subLeadLepPt,subLeadLepEta)
            eeHist[leadBin].Fill(invmll,weight)
            eeHist[subLeadBin].Fill(invmll,weight)
        elif (ey):

            leadLepPt=getattr(chain,"leptonPt")[0]
            leadLepEta=getattr(chain,"leptonEta")[0]
            closPhoPosition=getattr(chain,"closPhoPosition")
            closPhoPt=getattr(chain,"photonPt")[closPhoPosition]
            closPhoEta=getattr(chain,"photonEta")[closPhoPosition]
            invmlg=getattr(chain,"invmlg")
            photonBin=getBin(closPhoPt,closPhoEta)
            eyHist[photonBin].Fill(invmlg,weight)

    return eyHist,eeHist



sowList=[]
for key, value in inputPath_MCList.items():
        for folder in os.listdir(value):
            print("loading Zjets MC16"+key+" SoW")
            sowList.append(getSumWeights(value+"/"+folder))
print("SoW: ",sowList)
ZjetsChain,Zjets_entryMarks,Zjets_lumiMarks=addFile(inputPath_MCList,"nominal",lumiList)
dataChain,data_entryMarks,data_lumiMarks=addFile(inputPath_dataList,"nominal",lumiList)


if loopForHist_MC:
    eyHist_MC,eeHist_MC=produceHist(etaBins,ptBins,"MC")
    
    print("Start filling MC histograms for rates")
    eyHist_MC,eeHist_MC=getVariables(ZjetsChain,sowList,Zjets_entryMarks,Zjets_lumiMarks,True)
    outfile_MC = ROOT.TFile(output_filepath_MC, "RECREATE")
    for hist in eyHist_MC:
        hist.Write()
    for hist in eeHist_MC:
        hist.Write()
    outfile_MC.Close()

if loopForHist_data:
    print("Start filling data histograms for rates")
    eyHist_data,eeHist_data=getVariables(dataChain,sowList,data_entryMarks,data_lumiMarks,False)
    outfile_data = ROOT.TFile(output_filepath_data, "RECREATE")
    for hist in eyHist_data:
        hist.Write()
    for hist in eeHist_data:
        hist.Write()
    outfile_data.Close()


hardcoded_eta_bins = array('d', eta_bins)
hardcoded_pt_bins = array('d', pt_bins)
MZ = 91.188
Z_window = 10
Range=20
fit_range = [MZ-Range, MZ+Range]

print("start loading data")
tfile_data = ROOT.TFile(input_file_data, "UPDATE")
egammaHist_data=[]
eeHist_data=[]
for key in tfile_data.GetListOfKeys():
    obj = key.ReadObj()
    name=obj.GetName()
    if "data_egamma" in name:
        egammaHist_data.append(obj)
    elif "data_ee" in name:
        eeHist_data.append(obj)

print("start loading MC")
tfile_MC= ROOT.TFile(input_file_MC, "UPDATE")
egammaHist_MC=[]
eeHist_MC=[]
for key in tfile_MC.GetListOfKeys():
    obj = key.ReadObj()
    name=obj.GetName()
    if "MC_egamma" in name:
        egammaHist_MC.append(obj)
    elif "MC_ee" in name:
        eeHist_MC.append(obj)

h_FR_data = ROOT.TH2F("h_FR_data", "h_FR_data", len(hardcoded_eta_bins)-1, hardcoded_eta_bins, len(hardcoded_pt_bins)-1, hardcoded_pt_bins)
h_FR_MC = ROOT.TH2F("h_FR_MC", "h_FR_MC", len(hardcoded_eta_bins)-1, hardcoded_eta_bins, len(hardcoded_pt_bins)-1, hardcoded_pt_bins)
print("start fitting")


def get_bin_edges_from_hist_name(hname):
    split = hname.split("_")
    return float(split[2][3:]), float(split[3][2:])
def quadAdd(x,y):
    return np.sqrt(x**2+y**2)

fakeRateList_data=[]
fakeRateList_MC=[]

fakeRateRatioList=[]
fitErrorList=[]
WindowDiffList=[]
fitFuncDiffList=[]

outPutArray={"MCegamma_nominal":[],"MCee_nominal":[],"Dataegamma_nominal":[],"Dataee_nominal":[],
            "MCegamma_fitError":[],"MCee_fitError":[],"Dataegamma_fitError":[],"Dataee_fitError":[],
            "MCegamma_fitFunc":[],"MCee_fitFunc":[],"Dataegamma_fitFunc":[],"Dataee_fitFunc":[],
            "MCegamma_window":[],"MCee_window":[],"Dataegamma_window":[],"Dataee_window":[]
            }
for i in range(len(egammaHist_MC)):
    Range=20
    fit_range = [MZ-Range, MZ+Range]
    sig_model="CB"
    bkg_model="B5"
    print("fitting egamma")
    data_egamma_sigyield,data_egamma_fitUnc = fit_a_hist(egammaHist_data[i], sig_model, bkg_model, out_dir_data)
    print("fitting ee")
    data_ee_sigyield,data_ee_fitUnc = fit_a_hist(eeHist_data[i], sig_model, bkg_model, out_dir_data)

    print("fitting egamma")
    MC_egamma_sigyield,MC_egamma_fitUnc = fit_a_hist(egammaHist_MC[i], sig_model, bkg_model, out_dir_MC)
    print("fitting ee")
    MC_ee_sigyield,MC_ee_fitUnc = fit_a_hist(eeHist_MC[i], sig_model, bkg_model, out_dir_MC)
    
    FR_data = data_egamma_sigyield/(data_ee_sigyield)
    FR_MC = MC_egamma_sigyield/(MC_ee_sigyield)
    outPutArray["Dataegamma_nominal"].append(data_egamma_sigyield)
    outPutArray["Dataee_nominal"].append(data_ee_sigyield)
    outPutArray["MCegamma_nominal"].append(MC_egamma_sigyield)
    outPutArray["MCee_nominal"].append(MC_ee_sigyield)
    
    etaIndex=int(np.floor(i/(len(ptBins)-1)))
    ptIndex=i % (len(ptBins)-1)
    h_FR_data.Fill(etaBins[etaIndex][0]+0.1,ptBins[ptIndex]+0.1,FR_data)
    h_FR_MC.Fill(etaBins[etaIndex][0]+0.1,ptBins[ptIndex]+0.1,FR_MC)
    fakeRateList_data.append(FR_data)
    fakeRateList_MC.append(FR_MC)
    FR_ratio=FR_data/FR_MC
    fakeRateRatioList.append(FR_ratio)

    #FitError:
    error_MC= quadAdd(MC_egamma_fitUnc/MC_egamma_sigyield,MC_ee_fitUnc/MC_ee_sigyield)
    error_data= quadAdd(data_egamma_fitUnc/data_egamma_sigyield,data_ee_fitUnc/data_ee_sigyield)
    fitErrorList.append(FR_ratio*quadAdd(error_MC,error_data))

    outPutArray["Dataegamma_fitError"].append(data_egamma_fitUnc)
    outPutArray["Dataee_fitError"].append(data_ee_fitUnc)
    outPutArray["MCegamma_fitError"].append(MC_egamma_fitUnc)
    outPutArray["MCee_fitError"].append(MC_ee_fitUnc)

    #fitfunc:
    Range=20
    fit_range = [MZ-Range, MZ+Range]
    sig_model="Gauss"
    bkg_model="B5"
    print("fitting egamma")
    data_egamma_sigyield,data_egamma_fitUnc = fit_a_hist(egammaHist_data[i], sig_model, bkg_model, out_dir_data)
    print("fitting ee")
    data_ee_sigyield,data_ee_fitUnc = fit_a_hist(eeHist_data[i], sig_model, bkg_model, out_dir_data)
    print("fitting egamma")
    MC_egamma_sigyield,MC_egamma_fitUnc = fit_a_hist(egammaHist_MC[i], sig_model, bkg_model, out_dir_MC)
    print("fitting ee")
    MC_ee_sigyield,MC_ee_fitUnc = fit_a_hist(eeHist_MC[i], sig_model, bkg_model, out_dir_MC)
    FR_data_fitFunc= data_egamma_sigyield/(data_ee_sigyield)
    FR_MC_fitFunc = MC_egamma_sigyield/(MC_ee_sigyield)
    fitFuncDiffList.append(abs(FR_ratio-FR_data_fitFunc/FR_MC_fitFunc))

    outPutArray["Dataegamma_fitFunc"].append(data_egamma_sigyield)
    outPutArray["Dataee_fitFunc"].append(data_ee_sigyield)
    outPutArray["MCegamma_fitFunc"].append(MC_egamma_sigyield)
    outPutArray["MCee_fitFunc"].append(MC_ee_sigyield)

    #window size:
    Range=15
    fit_range = [MZ-Range, MZ+Range]
    sig_model="CB"
    bkg_model="B5"
    print("fitting egamma")
    data_egamma_sigyield,data_egamma_fitUnc = fit_a_hist(egammaHist_data[i], sig_model, bkg_model, out_dir_data)
    print("fitting ee")
    data_ee_sigyield,data_ee_fitUnc = fit_a_hist(eeHist_data[i], sig_model, bkg_model, out_dir_data)
    print("fitting egamma")
    MC_egamma_sigyield,MC_egamma_fitUnc = fit_a_hist(egammaHist_MC[i], sig_model, bkg_model, out_dir_MC)
    print("fitting ee")
    MC_ee_sigyield,MC_ee_fitUnc = fit_a_hist(eeHist_MC[i], sig_model, bkg_model, out_dir_MC)
    
    FR_data_window = data_egamma_sigyield/(data_ee_sigyield)
    FR_MC_window = MC_egamma_sigyield/(MC_ee_sigyield)
    WindowDiffList.append(abs(FR_ratio-FR_data_window/FR_MC_window))
    outPutArray["Dataegamma_window"].append(data_egamma_sigyield)
    outPutArray["Dataee_window"].append(data_ee_sigyield)
    outPutArray["MCegamma_window"].append(MC_egamma_sigyield)
    outPutArray["MCee_window"].append(MC_ee_sigyield)

fakeRateRatioList=np.array(fakeRateRatioList)
fitErrorList=np.array(fitErrorList)
fitFuncDiffList=np.array(fitFuncDiffList)
WindowDiffList=np.array(WindowDiffList)
allDiffList=quadAdd(quadAdd(fitErrorList,fitFuncDiffList),WindowDiffList)
outPutArray=pd.DataFrame(outPutArray)
outPutArray.to_pickle(out_dir_data+'/FakeRates.pk')

#2D histograms of fake rates
canvas_rates_data=ROOT.TCanvas()
hist_ptBinsArray=array('d',ptBins)
hist_etaBinsArray=array('d',np.array(etaBins).reshape(np.array(etaBins).shape[0]*np.array(etaBins).shape[1]))
hist_ptBinsArray[-1]=hist_ptBinsArray[-2]+30 # For better plots
hist_rates_data=ROOT.TH2F("h_rates_data","h_rates_data; photon $\eta$; photon p_{T} [GeV];fake rate",len(hist_etaBinsArray)-1,hist_etaBinsArray,len(hist_ptBinsArray)-1,hist_ptBinsArray)
hist_rates_MC=ROOT.TH2F("h_rates_MC","h_rates_MC; photon $\eta$; photon p_{T} [GeV];fake rate",len(hist_etaBinsArray)-1,hist_etaBinsArray,len(hist_ptBinsArray)-1,hist_ptBinsArray)
hist_rates_ratio=ROOT.TH2F("h_rates_ratio","h_rates_ratio; photon $\eta$; photon p_{T} [GeV];fake rate",len(hist_etaBinsArray)-1,hist_etaBinsArray,len(hist_ptBinsArray)-1,hist_ptBinsArray)
hist_rates_ratioUp=ROOT.TH2F("h_rates_ratio_up","h_rates_ratio_up; photon $\eta$; photon p_{T} [GeV];fake rate",len(hist_etaBinsArray)-1,hist_etaBinsArray,len(hist_ptBinsArray)-1,hist_ptBinsArray)
hist_rates_ratioDown=ROOT.TH2F("h_rates_ratio_down","h_rates_ratio_down; photon $\eta$; photon p_{T} [GeV];fake rate",len(hist_etaBinsArray)-1,hist_etaBinsArray,len(hist_ptBinsArray)-1,hist_ptBinsArray)

for etaIndex in range(len(etaBins)):
    for ptIndex in range(len(ptBins)-1):
        avgEta=0.5*(etaBins[etaIndex][0]+etaBins[etaIndex][1])
        avgPt=ptBins[ptIndex]+0.1
        index=etaIndex*(len(ptBins)-1)+ptIndex
        hist_rates_data.Fill(avgEta,avgPt,fakeRateList_data[index])
        hist_rates_MC.Fill(avgEta,avgPt,fakeRateList_MC[index])
        hist_rates_ratio.Fill(avgEta,avgPt,fakeRateRatioList[index])
        hist_rates_ratioUp.Fill(avgEta,avgPt,fakeRateRatioList[index]*(1+allDiffList[index]))
        hist_rates_ratioDown.Fill(avgEta,avgPt,fakeRateRatioList[index]*(1-allDiffList[index]))

outputFile=ROOT.TFile(SaveDir+"/egamFakes_MCdata.root",'recreate')
ROOT.gStyle.SetOptTitle(0)
hist_rates_data.Draw("Colz TEXT")
hist_rates_data.SetStats(ROOT.kFALSE)
hist_rates_data.Write()
canvas_rates_data.Draw()
canvas_rates_data.SaveAs(out_dir_data+"/FakeRate_2D_data.png")

canvas_rates_MC=ROOT.TCanvas()
hist_rates_MC.Draw("Colz TEXT")
hist_rates_MC.SetStats(ROOT.kFALSE)
hist_rates_MC.Write()
canvas_rates_MC.Draw()
canvas_rates_MC.SaveAs(out_dir_MC+"/FakeRate_2D_MC.png")


canvas_rates_ratio=ROOT.TCanvas()

hist_rates_ratio.Draw("Colz TEXT")
hist_rates_ratio.SetStats(ROOT.kFALSE)
hist_rates_ratio.Write()
canvas_rates_ratio.Draw()
canvas_rates_ratio.SaveAs(out_dir_data+"/FakeRate_2D_ratio.png")

canvas_rates_ratioUp=ROOT.TCanvas()
hist_rates_ratioUp.Draw("Colz TEXT")
hist_rates_ratioUp.Write()
hist_rates_ratioUp.SetStats(ROOT.kFALSE)
canvas_rates_ratioUp.Draw()
canvas_rates_ratioUp.SaveAs(out_dir_data+"/FakeRate_2D_ratioUp.png")

canvas_rates_ratioDown=ROOT.TCanvas()
hist_rates_ratioDown.Draw("Colz TEXT")
hist_rates_ratioDown.SetStats(ROOT.kFALSE)
hist_rates_ratioDown.Write()
canvas_rates_ratioDown.Draw()
canvas_rates_ratioDown.SaveAs(out_dir_data+"/FakeRate_2D_ratioDown.png")

def getFakeRateRatio(pt,eta,rates):
     absEta=abs(eta)
     rate=0.0
       
     ptIndex=-1
     for i in range(len(ptBins)-1):
         if((pt>ptBins[i])and(pt<ptBins[i+1])):
             ptIndex=i
     etaIndex=-1
     for i in range(len(etaBins)):
         if((absEta>etaBins[i][0])and(absEta<etaBins[i][1])):
             etaIndex=i
     index=-1
     if((ptIndex>=0) and (etaIndex>=0)):
         index= etaIndex*(len(ptBins)-1)+ptIndex
         rate=rates[index]

     return rate

def produceHist(CRname):
    varBins=region_varBins[CRname]
    bins=array('d',varBins)
    eChannel=[]
    muChannel=[]
    allChannel=[]
    eChannel.append(ROOT.TH1F(CRname+"_nominal_EChannel",CRname+"_nominal_EChannel",len(bins)-1,bins))
    muChannel.append(ROOT.TH1F(CRname+"_nominal_MuChannel",CRname+"_nominal_MuChannel",len(bins)-1,bins))
    allChannel.append(ROOT.TH1F(CRname+"_nominal_",CRname+"_nominal_",len(bins)-1,bins))

    eChannel.append(ROOT.TH1F(CRname+"_noRatio_EChannel",CRname+"_noRatio_EChannel",len(bins)-1,bins))
    muChannel.append(ROOT.TH1F(CRname+"_noRatio_MuChannel",CRname+"_noRatio_MuChannel",len(bins)-1,bins))
    allChannel.append(ROOT.TH1F(CRname+"_noRatio_",CRname+"_noRatio_",len(bins)-1,bins))

    variation=["fitError","windowError","functionError"]
    for item in variation:
        eChannel.append(ROOT.TH1F(CRname+"_egamFakes_"+item+"Up_EChannel",CRname+"_egamFakes_"+item+"Up_EChannel",len(bins)-1,bins))
        eChannel.append(ROOT.TH1F(CRname+"_egamFakes_"+item+"Down_EChannel",CRname+"_egamFakes_"+item+"Down_EChannel",len(bins)-1,bins))
        muChannel.append(ROOT.TH1F(CRname+"_egamFakes_"+item+"Up_MuChannel",CRname+"_egamFakes_"+item+"Up_MuChannel",len(bins)-1,bins))
        muChannel.append(ROOT.TH1F(CRname+"_egamFakes_"+item+"Down_MuChannel",CRname+"_egamFakes_"+item+"Down_MuChannel",len(bins)-1,bins))
        allChannel.append(ROOT.TH1F(CRname+"_egamFakes_"+item+"Up",CRname+"_egamFakes_"+item+"Up",len(bins)-1,bins))
        allChannel.append(ROOT.TH1F(CRname+"_egamFakes_"+item+"Down",CRname+"_egamFakes_"+item+"Down",len(bins)-1,bins))
    return eChannel,muChannel,allChannel

def writeHist(histList):
     for hist in histList:
         hist.Write()

fitError_up=fakeRateRatioList+fitErrorList
fitError_down=fakeRateRatioList-fitErrorList
window_up=fakeRateRatioList+WindowDiffList
window_down=fakeRateRatioList-WindowDiffList
fitFunc_up=fakeRateRatioList+fitFuncDiffList
fitFunc_down=fakeRateRatioList-fitFuncDiffList

variedRates=[fakeRateRatioList,np.ones(len(fakeRateRatioList)),fitError_up,fitError_down,window_up,window_down,fitFunc_up,fitFunc_down]

WyCRhistE,WyCRhistMu,WyCRhistAll=produceHist("WyCRSelection")
ZjetsCRhistE,ZjetsCRhistMu,ZjetsCRhistAll=produceHist("ZjetsCRSelection")
WjetsCRhistE,WjetsCRhistMu,WjetsCRhistAll=produceHist("WjetsCRSelection")
ZyCRhistE,ZyCRhistMu,ZyCRhistAll=produceHist("ZyCRSelection")
SRHistE,SRHistMu,SRHistAll=produceHist("SRSelection")
VRHistE,VRHistMu,VRHistAll=produceHist("VRSelection")



def fillHist(isEchannel,targetVar,closPhoPt,closPhoEta,eChannel,muChannel,allChannel,weight):
    if(isEchannel):
        for index in range(len(eChannel)):
            eChannel[index].Fill(targetVar,getFakeRateRatio(closPhoPt,closPhoEta,variedRates[index])*weight)
    else:
        for index in range(len(muChannel)):
            muChannel[index].Fill(targetVar,getFakeRateRatio(closPhoPt,closPhoEta,variedRates[index])*weight)

    for index in range(len(allChannel)):
        allChannel[index].Fill(targetVar,getFakeRateRatio(closPhoPt,closPhoEta,variedRates[index])*weight)


def getEstimation(chain,sowList,EntryMarks,lumiMarks):

    tmpDSID_markCount=0
    sumOfWeights=sowList[0]
    lumi=lumiMarks[0]
    print("Starting with DSID #{}, with sumOfWeights = {}".format(tmpDSID_markCount,sumOfWeights))
    selectedWeights=0
    eventPrintoutMarker=int(chain.GetEntries()*0.01)
    for entryNum in range(0,chain.GetEntries()):
        chain.GetEntry(entryNum)
        if(entryNum>EntryMarks[tmpDSID_markCount]):
            tmpDSID_markCount+=1
            sumOfWeights=sowList[tmpDSID_markCount]
            lumi=lumiMarks[tmpDSID_markCount]
            print("jumping to DSID #{}, with sumOfWeights = {}".format(tmpDSID_markCount,sumOfWeights))

        if(entryNum%eventPrintoutMarker==0 and entryNum>0):
            print("{} Events processed, {}% finished".format(entryNum,entryNum*100.0/chain.GetEntries()))
        
        
        
        if ((maxPercentage>0) and (entryNum*100.0/chain.GetEntries()>maxPercentage)):
            break

        WyCRSelection=getattr(chain,"WyCRSelection")
        ZjetsCRSelection=getattr(chain,"ZjetsCRSelection")
        WjetsCRSelection=getattr(chain,"WjetsCRSelection")
        ZyCRSelection=getattr(chain,"ZyCRSelection")
        SRSelection=getattr(chain,"SRSelection")
        VRSelection=getattr(chain,"VRSelection")
        passVyOR=getattr(chain,"passVyOR")
        passSelection = WyCRSelection or ZjetsCRSelection or WjetsCRSelection or ZyCRSelection or SRSelection or VRSelection
        passSelection = passSelection and passVyOR
        if(not passSelection):
            continue
        closPhoPosition=getattr(chain,"closPhoPosition")
        closPhoPt=getattr(chain,"photonPt")[closPhoPosition]
        leadLepPt=getattr(chain,"leptonPt")[0]
          
                
        closPhoEta=getattr(chain,"photonEta")[closPhoPosition]
        truthType=getattr(chain,"photonTruthTypeCondensed")[closPhoPosition]
        isEchannel=getattr(chain,"isEchannel")
        targetVar=getattr(chain,variable)
        weight=getWeight(chain,sumOfWeights,lumi)

        closPhoDR=getattr(chain,"photonDR")[closPhoPosition]
        # if truthType!=3:
        #     continue 

        if(WyCRSelection):
            fillHist(isEchannel,targetVar,closPhoPt,closPhoEta,WyCRhistE,WyCRhistMu,WyCRhistAll,weight)
        elif(ZjetsCRSelection):
            fillHist(isEchannel,targetVar,closPhoPt,closPhoEta,ZjetsCRhistE,ZjetsCRhistMu,ZjetsCRhistAll,weight)
        elif(WjetsCRSelection):
            fillHist(isEchannel,targetVar,closPhoPt,closPhoEta,WjetsCRhistE,WjetsCRhistMu,WjetsCRhistAll,weight)    
        elif(ZyCRSelection):
            fillHist(isEchannel,targetVar,closPhoPt,closPhoEta,ZyCRhistE,ZyCRhistMu,ZyCRhistAll,weight)
        elif(SRSelection):
            fillHist(isEchannel,targetVar,closPhoPt,closPhoEta,SRHistE,SRHistMu,SRHistAll,weight)
        elif(VRSelection):
            fillHist(isEchannel,targetVar,closPhoPt,closPhoEta,VRHistE,VRHistMu,VRHistAll,weight)
       
getEstimation(ZjetsChain,sowList,Zjets_entryMarks,Zjets_lumiMarks)

writeHist(WyCRhistE)
writeHist(WyCRhistMu)
writeHist(WyCRhistAll)

writeHist(ZjetsCRhistE)
writeHist(ZjetsCRhistMu)
writeHist(ZjetsCRhistAll)

writeHist(WjetsCRhistE)
writeHist(WjetsCRhistMu)
writeHist(WjetsCRhistAll)

writeHist(ZyCRhistE)
writeHist(ZyCRhistMu)
writeHist(ZyCRhistAll)

writeHist(SRHistE)
writeHist(SRHistMu)
writeHist(SRHistAll) 

writeHist(VRHistE)
writeHist(VRHistMu)
writeHist(VRHistAll) 
