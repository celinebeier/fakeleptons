import ROOT
import numpy as np

folder="root"

list_name=["FE2dEta","FF2dEta","FE2dPt","FF2dPt"]
dic1_name={'FE2dEta':'Fake Efficiency','FF2dEta':'Fake Factor', 'FE2dPt':'Fake Efficiency','FF2dPt':'Fake Factor'}
dic2e_name={'FE2dEta':'electron #eta','FF2dEta':'electron #eta', 'FE2dPt':'electron p_{T} [GeV]','FF2dPt':'electron p_{T} [GeV]'}
dic2m_name={'FE2dEta':'muon #eta','FF2dEta':'muon #eta', 'FE2dPt':'muon p_{T} [GeV]','FF2dPt':'muon p_{T} [GeV]'}

for name in list_name:

    histFileName = folder+"/2d.root"
    plotFileName = folder+"/"+name+".pdf"

    histFile = ROOT.TFile.Open(histFileName,"READ")

    hist1 = histFile.Get(name+"_DATA")
    hist2 = histFile.Get(name+"_MC")

    hist1.SetDirectory(0)
    hist2.SetDirectory(0)

    histFile.Close()

    canvas = ROOT.TCanvas("canvas")
    canvas.cd()

    canvas.Print(plotFileName +"[")

    #make histograms nice
    #pt_bins=[10,15,20,27,40,600]
    hist1.SetStats(0)
    #hist1.SetTitle("Data")
    
    if "FakeM" in folder:
        hist1.GetYaxis().SetTitle(dic1_name[name])
        hist1.GetXaxis().SetTitle(dic2m_name[name])
        
        if "Pt" in name:
            pt_bins=[27,35,1000]
            hist1.GetXaxis().SetNdivisions(-(len(pt_bins)-1))
            for i in range(len(pt_bins)):
                hist1.GetXaxis().ChangeLabel(i+1,-1,-1,-1,-1,-1,str(pt_bins[i]))
        
        if "FF" in name:
            hist1.SetMaximum(1)
            hist1.SetMinimum(0)
        else:
            hist1.SetMaximum(0.6)
            hist1.SetMinimum(0)
    else:
        if "Pt" in name:
            pt_bins=[27,35,50,1000]
            hist1.GetXaxis().SetNdivisions(-(len(pt_bins)-1))
            for i in range(len(pt_bins)):
                hist1.GetXaxis().ChangeLabel(i+1,-1,-1,-1,-1,-1,str(pt_bins[i]))
        
        hist1.GetYaxis().SetTitle(dic1_name[name])
        hist1.GetXaxis().SetTitle(dic2e_name[name])
        hist1.SetMaximum(0.6)
        hist1.SetMinimum(0)
        
    #hist1.SetLineColor(38)
    #hist2.SetLineColor(94)
    
    #c1=ROOT.TColor.GetColor("#F9FB0E")
    c1=ROOT.TColor.GetColor("#FEC832")
    c2=ROOT.TColor.GetColor("#009999")
    #c2=ROOT.TColor.GetColor("#352A87")
    
    hist1.SetLineColor(95)
    hist2.SetLineColor(c2)
    
    hist1.SetLineWidth(2)
    hist2.SetLineWidth(2)
    

    #hist.Draw("colz text e")
    hist1.Draw("colz")
    hist2.Draw("same")
    
    legend = ROOT.TLegend(0.75,0.8,0.95,0.95)
    legend.AddEntry(hist1, "Data")
    legend.AddEntry(hist2, "Z+jets MC")
    legend.SetTextSize(0.03)
    legend.SetBorderSize(1)
    legend.Draw("same")

    canvas.SetRightMargin(0.05)
    canvas.SetLeftMargin(0.1)
    canvas.SetTopMargin(0.05)
    canvas.SetBottomMargin(0.1)
    
    canvas.Print(plotFileName)
    canvas.Print(plotFileName +"]")