import ROOT
import numpy as np

folder="root"

list_name=["FE_MC","FF_MC","FE_DATA","FF_DATA"]
dic_name={'FE_MC':'Fake Efficiency (Z+jets MC)','FF_MC':'Fake Factor (Z+jets MC)', 'FE_DATA':'Fake Efficiency (Data)','FF_DATA':'Fake Factor (Data)'}

for name in list_name:

    histFileName = folder+"/FakeEff.root"
    plotFileName = folder+"/"+name+".pdf"

    histFile = ROOT.TFile.Open(histFileName,"READ")

    hist = histFile.Get(name)

    hist.SetDirectory(0)

    histFile.Close()

    canvas = ROOT.TCanvas("canvas")
    canvas.cd()

    canvas.Print(plotFileName +"[")

    #make histograms nice
    hist.SetStats(0)
    hist.GetZaxis().SetTitle(dic_name[name])
    if "FakeM" in folder:
        hist.GetYaxis().SetTitle("muon #eta")
        hist.GetXaxis().SetTitle("muon p_{T} [GeV]")
        
        pt_bins=[10,15,27,35,1000]
        hist.GetXaxis().SetNdivisions(-(len(pt_bins)-1))
        for i in range(len(pt_bins)):
            hist.GetXaxis().ChangeLabel(i+1,-1,-1,-1,-1,-1,str(pt_bins[i]))
        
        if "FF" in name:
            hist.SetMaximum(1)
            hist.SetMinimum(0)
        else:
            hist.SetMaximum(0.6)
            hist.SetMinimum(0)
    else:
        hist.GetYaxis().SetTitle("electron #eta")
        hist.GetXaxis().SetTitle("electron p_{T} [GeV]")
        hist.SetMaximum(0.6)
        hist.SetMinimum(0)
        
        pt_bins=[10,15,20,27,35,50,1000]
        hist.GetXaxis().SetNdivisions(-(len(pt_bins)-1))
        for i in range(len(pt_bins)):
            hist.GetXaxis().ChangeLabel(i+1,-1,-1,-1,-1,-1,str(pt_bins[i]))
    
    ROOT.gStyle.SetPaintTextFormat(".3f")
    canvas.UseCurrentStyle()
    canvas.SetRightMargin(0.15)
    canvas.SetLeftMargin(0.1)
    canvas.SetTopMargin(0.05)
    canvas.SetBottomMargin(0.1)

    hist.Draw("colz text e")

    canvas.Print(plotFileName)
    canvas.Print(plotFileName +"]")