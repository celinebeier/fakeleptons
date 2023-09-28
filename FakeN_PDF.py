import ROOT
import numpy as np

folder="root_FakeM"

list_name=["VR","SR","WyCR","WjetsCR","ZyCR","ZjetsCR"]

for name in list_name:

    histFileName = folder+"/"+name+"_FakeE.root"
    plotFileName = folder+"/"+name+"_FakeE.pdf"

    histFile = ROOT.TFile.Open(histFileName,"READ")

    hist1 = histFile.Get(name)

    hist1.SetDirectory(0)

    histFile.Close()

    canvas = ROOT.TCanvas("canvas")
    canvas.cd()

    canvas.Print(plotFileName +"[")

    #make histograms nice
    #pt_bins=[10,15,20,27,40,600]
    hist1.Draw("hist")
    hist1.SetStats(0)
    hist1.GetYaxis().SetTitle("Events")
    hist1.GetXaxis().SetTitle("m_{W\gamma} [GeV]")
    if "VR" in name:
        hist1.GetXaxis().SetRangeUser(80,600)
    if "SR" in name:
        hist1.GetXaxis().SetRangeUser(80,500)
    if "WyCR" in name:
        hist1.GetXaxis().SetRangeUser(80,750)
    if "WjetsCR" in name:
        hist1.GetXaxis().SetRangeUser(80,400)
    if "ZyCR" in name:
        hist1.GetXaxis().SetRangeUser(80,600)
    if "ZjetsCR" in name:
        hist1.GetXaxis().SetRangeUser(80,500)

    #hist1.SetFillStyle(3004)
    #hist1.SetFillColor(1)
    #hist1.Draw("E2")
    hist1.SetFillStyle(4050)
    c2=ROOT.TColor.GetColor("#009999")
    hist1.SetFillColor(c2)
    hist1.SetLineWidth(0)
    hist1.SetMarkerSize(0)
    hist1.Draw("HIST")
    hist2 = hist1.DrawCopy("E2 SAME")
    #hist2.SetFillStyle(0)
    #hist2.SetLineColor(1)
    hist2.SetFillStyle(3004)
    hist2.SetFillColor(1)
    hist2.SetLineWidth(0)
    hist2.SetMarkerSize(0)
    #hh.SetLineWidth(3)

    canvas.SetRightMargin(0.05)
    canvas.SetLeftMargin(0.1)
    canvas.SetTopMargin(0.05)
    canvas.SetBottomMargin(0.1)

    legend = ROOT.TLegend(0.75,0.8,0.95,0.95)
    if "FakeM" in folder:
        legend.AddEntry(hist1, "Fake Muons")
    else:
        legend.AddEntry(hist1, "Fake Electrons")
    #legend.AddEntry(hist2, "Uncertainty")
    legend.SetTextSize(0.03)
    legend.SetBorderSize(1)
    legend.Draw("same")

    canvas.Print(plotFileName)
    canvas.Print(plotFileName +"]")