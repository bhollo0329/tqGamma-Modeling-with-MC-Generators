 #variables = ('var', 'xtitle', nbins, xmin, xmax, 'fname')
variables = [#('parentpt',"Parent pt [MeV]", 40, 0, 200000, "parPT"),
             #('parenteta', "Parent eta", 10, -6, 6, "parEta"),
             #('parentE', "Parent Energy [MeV]", 70, 60000, 700000, "parE"),
             #('parentphi', "Parent phi", 10, -6, 6, "parPhi"),
             #('lep1pt', "Lepton 1 pt [MeV]", 40, 0, 160000, "lep1PT"),
             #('lep1eta', "Lepton 1 eta", 10, -6, 6, "lep1Eta"),
             #('lep1E', "Lepton 1 Energy [MeV]", 70, 0, 300000, "lep1E"),
             #('lep1phi', "Lepton 1 phi", 10, -6, 6, "lep1Phi"),
             #('lep1id', "Lepton 1 ID", 60, -16, 16, "lep1ID"),
             #('lep2pt', "Lepton 2 pt [MeV]", 40, 0, 200000, 'lep2PT'),
             #('lep2eta', "Lepton 2 eta", 10, -6, 6, "lep2Eta"),
             #('lep2E', "Lepton 2 Energy [MeV]", 70, 0, 400000, "lep2E"),
             #('lep2phi', "Lepton 2 phi", 10, -6, 6, "lep2Phi"),
             #('lep2id', "Lepton 2 ID", 60, -16, 16, "lep2ID"),
             ('photonpt', "Photon pt [MeV]", 40, 0, 200000, "phoPT"),
             ('photoneta', "Photon eta", 10, -6, 6, "phoEta"),
             ('photonE', "Photon Energy [MeV]", 70, 0, 600000, "phoE"),
             ('photonphi', "Photon phi", 10, -6, 6, "phoPhi")]
             #('toppt', "Top pt [MeV]", 40, 0, 400000, "topPT"),
             #('topeta', "Top eta", 10, -6, 6, "topEta"),
             #('topE', "Top Energy [MeV]", 80, 150000, 800000, "topE"),
             #('topphi', "Top phi", 10, -6, 6, "topPhi"),
             #('btpt', "Bottom from Top pt [MeV]", 40, 0, 200000, "btPT"),
             #('bteta', "Bottom from Top eta", 10, -6, 6, "btEta"),
             #('btE', "Bottom from Top Energy [MeV]", 70, 0, 700000, "btE"),
             #('btphi', "Bottom from Top phi", 10, -6, 6, "btPhi"),
             #('bglupt', "Bottom from Gluon pt [MeV]", 40, 0, 60000, "bgluPT"),
             #('bglueta', "Bottom from Gluon eta", 10, -6, 6, "bgluEta"),
             #('bgluE', "Bottom from Gluon Energy [MeV]", 60, 0, 200000, "bgluE"),
             #('bgluphi', "Bottom from Gluon phi", 10, -6, 6, "bgluPhi"),
             #('mlvbTopMother', 'Invariant Mass Top Mother [MeV]', 10, -0.1, 0.1, 'mlvbTopMom'),
             #('mlvbNoTopMother', 'Invariant Mass [MeV]', 40, 1500, 1900, 'mlvbNoTopMom'),
             #('mlvba','Invariant Mass with Photon [MeV]', 40, 0, 4000, "mlvba")]


from ROOT import TCanvas, TH1D, TLegend, TPad, TRatioPlot
import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(1)
ROOT.gROOT.LoadMacro("AtlasStyle.C")
ROOT.gROOT.LoadMacro("AtlasLabels.C")
ROOT.SetAtlasStyle()

path = '/data/bhollo/mgNLO/photonModeling/'

f1 = ROOT.TFile.Open(path+'tqNLO2.root', 'r')
t1 = f1.Get("selection")
tw1 = f1.Get("totalWeight").GetBinContent(1)
ew1 = 1.0/(tw1)

f2 = ROOT.TFile.Open(path+'tqgammaNLO.root', 'r')
t2 = f2.Get("selection")
tw2 = f2.Get("totalWeight").GetBinContent(1)
ew2 = 1.0/(tw2)

f3 = ROOT.TFile.Open(path+'tqgammaLO.root', 'r')
t3 = f3.Get("selection")
tw3 = f3.Get("totalWeight").GetBinContent(1)
ew3 = 1.0/(tw3)

for var in variables:
    c1 = TCanvas('c1', ' ', 1000, 1000)
    
    pad0 = ROOT.TPad("pad0","pad0",0,0.20,1,1,0,0,0);
    pad0.SetTicks(1,1);
    pad0.SetTopMargin(0.05);
    pad0.SetBottomMargin(0.0);
    pad0.SetFillStyle(0);

    pad1 = ROOT.TPad("pad1","pad1",0,0,1,0.28,0,0,0);
    pad1.SetTicks(1,1);
    pad1.SetTopMargin(0.0);
    pad1.SetBottomMargin(0.25);
    pad1.SetFillStyle(0);
    pad1.Draw()
    pad0.Draw()
    pad0.cd()
    

    hNtq = TH1D('hNtq', 'hNtq', var[2], var[3], var[4])
    hNtq.Sumw2()
    #fill each histogram with first var by drawing the tree
    t1.Draw("%s >> hNtq" %var[0], "(%.10f*weight)*(photonpt>10e3&&lep1pt>27e3&&abs(photoneta)<2.5&&abs(lep1eta)<2.5&&dral>0.2)" %ew1)
    hNtq.Scale((62.84)*(1.39e+05))
        
    hNtqg = TH1D('hNtqg', 'hNtqg', var[2], var[3], var[4])
    hNtqg.Sumw2()
    t2.Draw("%s >> hNtqg" %var[0], "(%.10f*weight)*(photonpt>10e3&&lep1pt>27e3&&abs(photoneta)<2.5&&abs(lep1eta)<2.5&&dral>0.2)" %ew2)
    hNtqg.Scale((1.1802)*(1.39e+05))

    hLtqg = TH1D('hLtqg', 'hLtqg', var[2], var[3], var[4])
    hLtqg.Sumw2()
    t3.Draw("%s >> hLtqg" %var[0], "(%.10f*weight)*(photonpt>10e3&&lep1pt>27e3&&abs(photoneta)<2.5&&abs(lep1eta)<2.5&&dral>0.2)" %ew3)
    hLtqg.Scale((1.412)*(1.39e+05))

    leg = TLegend(0.63, 0.60, 0.78, 0.75)
    leg.AddEntry(hNtq, 'NLOtq')
    leg.AddEntry(hNtqg, 'NLOtqgamma')
    leg.AddEntry(hLtqg, 'LOtqgamma')

    hNtq.SetLineColor(ROOT.kBlue)
    hNtqg.SetLineColor(ROOT.kViolet)
    hLtqg.SetLineColor(ROOT.kGreen)
    hNtq.Draw('hist')
    hNtqg.Draw('hist same')
    hLtqg.Draw('hist same')
    leg.Draw()

    hratio = hLtqg.Clone("ratio")
    hadd = hNtq.Clone("add")
    hadd.Add(hNtqg)
    
    #rp = TRatioPlot(hratio, hadd, "divsym")
    hratio.Divide(hadd)
    hratio.SetLineColor(ROOT.kRed)
    hratio.GetXaxis().SetTitle(var[1])
    hratio.GetYaxis().SetRangeUser(-0.5,3)

    pad1.cd()
    #rp.SetLineColor(ROOT.kRed)
    hratio.Draw('e0')

    c1.SaveAs('tqGammaPlots714/'+var[5]+'.png')

    del c1, pad1, pad0
    
