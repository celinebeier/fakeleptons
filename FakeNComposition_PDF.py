import ROOT
import numpy as np
from Plot import Plot

folder="root"

histFileName = folder+"/Comp_SR.root"
plotFileName = folder+"/Comp_SR.pdf"

histFile = ROOT.TFile.Open(histFileName,"READ")

hist1 = histFile.Get("Zjets")
hist2 = histFile.Get("Zy")
hist3 = histFile.Get("Wjets")
hist4 = histFile.Get("Wy")
hist5 = histFile.Get("VVy")
hist6 = histFile.Get("VV")
hist7 = histFile.Get("Vyy")
hist8 = histFile.Get("tty")
hist9 = histFile.Get("tt")
hist10 = histFile.Get("yy")
#hist10 = histFile.Get("yjets")
hist_err = histFile.Get("error")


hist1.SetDirectory(0)
hist2.SetDirectory(0)
hist3.SetDirectory(0)
hist4.SetDirectory(0)
hist5.SetDirectory(0)
hist6.SetDirectory(0)
hist7.SetDirectory(0)
hist8.SetDirectory(0)
hist9.SetDirectory(0)
hist10.SetDirectory(0)
#hist11.SetDirectory(0)
hist_err.SetDirectory(0)

histFile.Close()

#canvas = ROOT.TCanvas("canvas")
#canvas.cd()

#canvas.Print(plotFileName +"[")

    #make histograms nice
    #pt_bins=[10,15,20,27,40,600]
#hist1.SetStats(0)
    #hist1.SetTitle("Data")
    
'''
    if "FakeM" in folder:
        hist1.GetYaxis().SetTitle(dic1_name[name])
        hist1.GetXaxis().SetTitle(dic2m_name[name])
        if "FF" in name:
            hist1.SetMaximum(1)
            hist1.SetMinimum(0)
        else:
            hist1.SetMaximum(0.6)
            hist1.SetMinimum(0)
    else:
        hist1.GetYaxis().SetTitle(dic1_name[name])
        hist1.GetXaxis().SetTitle(dic2e_name[name])
        hist1.SetMaximum(0.6)
        hist1.SetMinimum(0)
        
    hist1.SetLineColor(2)
    hist2.SetLineColor(4)
'''

    #hist.Draw("colz text e")
#hist1.Draw("colz")
#hist2.Draw("same")

hs1 = ROOT.THStack("hs1","")


c1=ROOT.TColor.GetColor("#004949")
c2=ROOT.TColor.GetColor("#009999")
c3=ROOT.TColor.GetColor("#22cf22")
c4=ROOT.TColor.GetColor("#490092")
c5=ROOT.TColor.GetColor("#006ddb")
c6=ROOT.TColor.GetColor("#b66dff")
c7=ROOT.TColor.GetColor("#ff6db6")
c8=ROOT.TColor.GetColor("#920000")
c9=ROOT.TColor.GetColor("#db6d00")
c10=ROOT.TColor.GetColor("#ffdf4d")

hist1.SetFillColor(c1)
hist1.SetLineWidth(0)
hs1.Add(hist1,"HIST")
hist2.SetFillColor(c2)
hist2.SetLineWidth(0)
hs1.Add(hist2,"HIST")
hist3.SetFillColor(c3)
hist3.SetLineWidth(0)
hs1.Add(hist3,"HIST")
hist4.SetFillColor(c4)
hist4.SetLineWidth(0)
hs1.Add(hist4,"HIST")
hist5.SetFillColor(c5)
hist5.SetLineWidth(0)
hs1.Add(hist5,"HIST")
hist6.SetFillColor(c6)
hist6.SetLineWidth(0)
hs1.Add(hist6,"HIST")
hist7.SetFillColor(c7)
hist7.SetLineWidth(0)
hs1.Add(hist7,"HIST")
hist8.SetFillColor(c8)
hist8.SetLineWidth(0)
hs1.Add(hist8,"HIST")
hist9.SetFillColor(c9)
hist9.SetLineWidth(0)
hs1.Add(hist9,"HIST")
#hist10.SetFillColor(11)
#hist10.SetLineWidth(0)
#hs1.Add(hist10)
hist10.SetFillColor(c10)
hist10.SetLineWidth(0)
hs1.Add(hist10,"HIST")
#hist13.SetFillColor(1)
#hist13.SetLineWidth(0)
#hs1.Add(hist13)

'''
hist_err.SetFillStyle(3004)
hist_err.SetFillColor(1)
hist_err.SetLineWidth(0)
hist_err.SetMarkerSize(0)
hs1.Add(hist_err,"E2")
'''
canvas=ROOT.TCanvas("canvas","stacked hists")
canvas.SetLogy()
canvas.cd()
canvas.Print(plotFileName +"[")
hs1.SetMaximum(10000)
hs1.SetMinimum(0.1)
hs1.Draw("")
bins=['Unknown','KnownUnknown','Prompt Electrons','Charge-Flip Electrons','Prompt Muons','Prompt Photon Conversion','Electrons From Muons','Tau Decays','b-Hadron Decays','c-Hadron Decays','Light Flavour Decays','Charge-Flip Muons']
#hs1.GetXaxis().SetNdivisions(len(bins))
for i in range(len(bins)):
    hs1.GetXaxis().SetBinLabel(i+1,bins[i])
    hs1.GetYaxis().SetTitle("Events")
#    hs1.GetXaxis().ChangeLabel(i+1,-1,-1,-1,-1,-1,bins[i])
#hist1.GetXaxis().LabelsDeflate()
#hs1.GetXaxis().LabelsOption("v")

hist_err.Draw("E2 SAME")
hist_err.SetFillStyle(3004)
hist_err.SetFillColor(1)
hist_err.SetLineWidth(0)
hist_err.SetMarkerSize(0)

#hist1.Draw("")

legend = ROOT.TLegend(0.9,0.1,0.99,0.95)
legend.AddEntry(hist10, "#gamma#gamma")
legend.AddEntry(hist9, "t#bar{t}")
legend.AddEntry(hist8, "t#bar{t}#gamma")
legend.AddEntry(hist7, "V#gamma#gamma")
legend.AddEntry(hist6, "VV")
legend.AddEntry(hist5, "VV#gamma")
legend.AddEntry(hist4, "W#gamma")
legend.AddEntry(hist3, "W+jets")
legend.AddEntry(hist2, "Z#gamma")
legend.AddEntry(hist1, "Z+jets")
#legend.AddEntry(hist10, "yjets")
    #legend.SetTextSize(0.03)
    #legend.SetBorderSize(1)
legend.Draw("same")

#canvas.SetRightMargin(0.4)
canvas.SetLeftMargin(0.1)
canvas.SetTopMargin(0.05)
#canvas.SetBottomMargin(0.5)
    
canvas.Print(plotFileName)
canvas.Print(plotFileName +"]")