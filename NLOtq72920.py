#variables = ('var', 'xtitle', nbins, xmin, xmax, 'fname')
variables = [#('parentpt',"Parent pt [MeV]", 40, 0, 200000, "parPT"),
             #('parenteta', "Parent eta", 10, -6, 6, "parEta"),
             #('parentE', "Parent Energy [MeV]", 128, 60000, 700000, "parE"),
             #('parentphi', "Parent phi", 10, -6, 6, "parPhi"),
             #('lep1pt', "Lepton 1 pt [MeV]", 32, 0, 160000, "lep1PT"),
             #('lep1eta', "Lepton 1 eta", 10, -6, 6, "lep1Eta"),
             #('lep1E', "Lepton 1 Energy [MeV]", 60, 0, 300000, "lep1E"),
             #('lep1phi', "Lepton 1 phi", 10, -6, 6, "lep1Phi"),
             #('lep1id', "Lepton 1 ID", 60, -16, 16, "lep1ID"),
             #('lep2pt', "Lepton 2 pt [MeV]", 40, 0, 200000, 'lep2PT'),
             #('lep2eta', "Lepton 2 eta", 10, -6, 6, "lep2Eta"),
             #('lep2E', "Lepton 2 Energy [MeV]", 80, 0, 400000, "lep2E"),
             #('lep2phi', "Lepton 2 phi", 10, -6, 6, "lep2Phi"),
             #('lep2id', "Lepton 2 ID", 60, -16, 16, "lep2ID"),
             ('photonpt', "Photon pt [MeV]", 20, 0, 60000, "phoPT"),
             #('photoneta', "Photon eta", 10, -6, 6, "phoEta"),
             ('photonE', "Photon Energy [MeV]", 40, 0, 200000, "phoE")]
             #('photonphi', "Photon phi", 10, -6, 6, "phoPhi"),
             #('toppt', "Top pt [MeV]", 40, 0, 400000, "topPT"),
             #('topeta', "Top eta", 10, -6, 6, "topEta"),
             #('topE', "Top Energy [MeV]", 80, 150000, 800000, "topE"),
             #('topphi', "Top phi", 10, -6, 6, "topPhi"),
             #('btpt', "Bottom from Top pt [MeV]", 40, 0, 200000, "btPT"),
             #('bteta', "Bottom from Top eta", 10, -6, 6, "btEta"),
             #('btE', "Bottom from Top Energy [MeV]", 140, 0, 700000, "btE"),
             #('btphi', "Bottom from Top phi", 10, -6, 6, "btPhi"),
             #('bglupt', "Bottom from Gluon pt [MeV]", 12, 0, 60000, "bgluPT"),
             #('bglueta', "Bottom from Gluon eta", 10, -6, 6, "bgluEta"),
             #('bgluE', "Bottom from Gluon Energy [MeV]", 40, 0, 200000, "bgluE"),
             #('bgluphi', "Bottom from Gluon phi", 10, -6, 6, "bgluPhi"),
             #('mlvbTopMother', 'Invariant Mass Top Mother [MeV]', 10, -0.1, 0.1, 'mlvbTopMom'),
             #('mlvbNoTopMother', 'Invariant Mass [MeV]', 40, 1500, 1900, 'mlvbNoTopMom'),
             #('mlvba','Invariant Mass with Photon [MeV]', 40, 0, 4000, "mlvba")

from ROOT import TCanvas, TH1D, TLegend, TPad
import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(1)
ROOT.gROOT.LoadMacro("AtlasStyle.C")
ROOT.gROOT.LoadMacro("AtlasLabels.C")
ROOT.SetAtlasStyle()

f = ROOT.TFile.Open("/data/bhollo/mgNLO/photonModeling/tqNLO2.root", "r")
t = f.Get("selection")
tw = f.Get("totalWeight").GetBinContent(1)
ew = 1/(tw)

for var in variables:
    c1 = TCanvas('c1',' ' , 1000, 1000)

    hNtq = TH1D('hNtq', 'hNtq', var[2], var[3], var[4])
    hNtq.Sumw2()
    t.Draw("%s >> hNtq" %var[0], "%.10f*weight" %ew) #%s is a place holder for a string

    leg = TLegend(0.63, 0.60, 0.78, 0.75)
    leg.AddEntry(hNtq, "NLOtq")

    hNtq.SetLineColor(ROOT.kBlue)
    hNtq.GetXaxis().SetTitle(var[1])
    nevents = (62.84)*(1.39e+05) #xsec(pb)*luminosity(pb^-1)
    hNtq.Scale(nevents)
    hNtq.Draw('hist')
    leg.Draw()

    c1.SaveAs('NLOtqPlots2/'+var[5]+'.png')
