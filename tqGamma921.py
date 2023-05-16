 #variables = ('var', 'xtitle', nbins, xmin, xmax, 'fname')
variables = [#('parentpt',"Parent pt [MeV]", 40, 0, 200000, "parPT"),
             #('parenteta', "Parent eta", 10, -6, 6, "parEta"),
             #('parentE', "Parent Energy [MeV]", 70, 60000, 700000, "parE"),
             #('parentphi', "Parent phi", 10, -6, 6, "parPhi"),
             #('lep1pt', "Lepton pt [MeV]", 40, 0, 160000, "lep1PT"),
             #('lep1eta', "Lepton eta", 10, -6, 6, "lep1Eta"),
             #('lep1E', "Lepton Energy [MeV]", 70, 0, 300000, "lep1E"),
             #('lep1phi', "Lepton phi", 10, -6, 6, "lep1Phi"),
             #('lep1id', "Lepton ID", 60, -16, 16, "lep1ID"),
             #('lep2pt', "Neutrino 2 pt [MeV]", 40, 0, 200000, 'lep2PT'),
             #('lep2eta', "Neutrino eta", 10, -6, 6, "lep2Eta"),
             #('lep2E', "Neutrino Energy [MeV]", 70, 0, 400000, "lep2E"),
             #('lep2phi', "Neutrino phi", 10, -6, 6, "lep2Phi"),
             #('lep2id', "Neutrino ID", 60, -16, 16, "lep2ID"),
              #('photonpt', "Photon pt [MeV]", 30, 0, 140000, "phoPT"),
             #('photoneta', "Photon eta", 10, -6, 6, "phoEta"),
              #('photonE', "Photon Energy [MeV]", 50, 0, 350000, "phoE"),
             #('photonphi', "Photon phi", 10, -6, 6, "phoPhi"),
             ('toppt', "Top pt [MeV]", 40, 0, 400000, "topPT"),
             #('topeta', "Top eta", 10, -6, 6, "topEta"),
             ('topE', "Top Energy [MeV]", 80, 150000, 800000, "topE"),
             #('topphi', "Top phi", 10, -6, 6, "topPhi"),
             #('btpt', "Bottom from Top pt [MeV]", 40, 0, 200000, "btPT"),
             #('bteta', "Bottom from Top eta", 10, -6, 6, "btEta"),
             #('btE', "Bottom from Top Energy [MeV]", 70, 0, 700000, "btE"),
             #('btphi', "Bottom from Top phi", 10, -6, 6, "btPhi"),
             #('bglupt', "Bottom from Gluon pt [MeV]", 40, 0, 60000, "bgluPT"),
             #('bglueta', "Bottom from Gluon eta", 10, -6, 6, "bgluEta"),
             #('bgluE', "Bottom from Gluon Energy [MeV]", 60, 0, 200000, "bgluE")]
             #('bgluphi', "Bottom from Gluon phi", 10, -6, 6, "bgluPhi"),
             #('mlvbTopMother', 'Invariant Mass Top Mother [MeV]', 10, -0.1, 0.1, 'mlvbTopMom'),
             #('mlvbNoTopMother', 'Invariant Mass [MeV]', 40, 1500, 1900, 'mlvbNoTopMom'),
             #('mlvba','Invariant Mass with Photon [MeV]', 40, 0, 4000, "mlvba"),
             ('dral', 'Delta R Photon and Lepton', 10, -1, 6, "dral"),
             ('drat', 'Delta R Photon and Top Quark', 10, -1, 7, "drat")]

from ROOT import TCanvas, TH1D, TLegend, TPad, TRatioPlot
import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPalette(1)
ROOT.gROOT.LoadMacro("AtlasStyle.C")
ROOT.gROOT.LoadMacro("AtlasLabels.C")
ROOT.SetAtlasStyle()

path = '/data/bhollo/mgNLO/photonModeling/'

f1 = ROOT.TFile.Open(path+'tqNLO.root', 'r')
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
    pad0.SetBottomMargin(0.1);
    pad0.SetLeftMargin(0.14);
    pad0.SetRightMargin(0.05);
    pad0.SetFrameBorderMode(0);
    pad0.SetFillStyle(0);

    pad1 = ROOT.TPad("pad1","pad1",0,0,1,0.28,0,0,0);
    pad1.SetTicks(1,1);
    pad1.SetTopMargin(0.0);
    pad1.SetBottomMargin(0.37);
    pad1.SetLeftMargin(0.14);
    pad1.SetRightMargin(0.05);
    pad1.SetFrameBorderMode(0);
    pad1.SetFillStyle(0);
    pad1.Draw()
    pad0.Draw()
    pad0.cd()

    err = ROOT.Double()

    hNtq = TH1D('hNtq', 'hNtq', var[2], var[3], var[4])
    hNtq.Sumw2()
    hNtq.SetTitle(var[1])
    t1.Draw("%s >> hNtq" %var[0], "(%.10f*weight)*(photonpt>10e3&&lep1pt>27e3&&abs(photoneta)<2.5&&abs(lep1eta)<2.5&&dral>0.2)" %ew1)
    hNtq.Scale((62.41)*(1.39e+05))

    
    #hNtq.Integral(0, var[2]+1)/var[2]
    int1 = hNtq.IntegralAndError(0, var[2]+1, err)
    print int1, err

    hNtqg = TH1D('hNtqg', 'hNtqg', var[2], var[3], var[4])
    hNtqg.Sumw2()
    t2.Draw("%s >> hNtqg" %var[0], "(%.10f*weight)*(photonpt>10e3&&lep1pt>27e3&&abs(photoneta)<2.5&&abs(lep1eta)<2.5&&dral>0.2)" %ew2)
    hNtqg.Scale((1.1802)*(1.39e+05))

    
    #hNtqg.Integral(0, var[2]+1)/var[2]
    int2 = hNtqg.IntegralAndError(0, var[2]+1, err)
    print int2, err

    hLtqg = TH1D('hLtqg', 'hLtqg', var[2], var[3], var[4])
    hLtqg.Sumw2()
    t3.Draw("%s >> hLtqg" %var[0], "(%.10f*weight)*(photonpt>10e3&&lep1pt>27e3&&abs(photoneta)<2.5&&abs(lep1eta)<2.5&&dral>0.2)" %ew3)
    hLtqg.Scale((1.412)*(1.39e+05)*2)
    
    
    #hLtqg.Integral(0, var[2]+1)/var[2]
    int3 = hLtqg.IntegralAndError(0, var[2]+1, err)
    print int3, err

    leg = TLegend(0.63, 0.60, 0.78, 0.75)
    leg.AddEntry(hNtq, 'NLOtq')
    leg.AddEntry(hNtqg, 'NLOtqgamma')
    leg.AddEntry(hLtqg, 'LOtqgamma')

    hNtq.SetLineColor(ROOT.kBlue)
    hNtqg.SetLineColor(ROOT.kViolet)
    hLtqg.SetLineColor(ROOT.kGreen)
    hNtq.SetMaximum(2.7*hNtqg.GetMaximum())
    hNtq.Draw('hist')
    hNtqg.Draw('hist same')
    hLtqg.Draw('hist same')
    leg.Draw()

    hratio = hLtqg.Clone("ratio")
    hadd = hNtq.Clone("add")
    hadd.Add(hNtqg)

    hratio.Divide(hadd)
    hratio.SetLineColor(ROOT.kRed)
    #hratio.GetXaxis().SetTitle(var[1])
    #hratio.GetXaxis().SetTitleSize(20)
   
    hratio.SetMarkerStyle(21);
    hratio.SetMarkerSize(0.8);
    hratio.SetMarkerColor(ROOT.kBlack);
    hratio.SetLineWidth(2);
    hratio.SetFillStyle(0);
    '''
    if hratio.GetMaximum() > 5.0 or hratio.GetMaximum() < 2.0:
        hratio.SetMaximum(2.0)
    if hratio.GetMinimum() > 0.5:
        hratio.GetMinimum(0.5)
    '''
    hratio.SetMinimum(0)
    hratio.SetMaximum(2)
    
    hratio.GetYaxis().SetTitle("LOtqGamma/(NLOtq + NLOtqGamma)");
    hratio.GetYaxis().SetNdivisions(505);
    #hratio.GetYaxis().SetRangeUser(-0.5, 3);
    hratio.GetYaxis().SetTitleSize(12);
    hratio.GetYaxis().SetTitleFont(43);
    hratio.GetYaxis().SetTitleOffset(1.55);
    hratio.GetYaxis().SetLabelFont(43);
    hratio.GetYaxis().SetLabelSize(15);    

    hratio.GetXaxis().SetTitle(var[1])
    hratio.GetXaxis().SetNdivisions(hLtqg.GetXaxis().GetNdivisions());
    hratio.GetXaxis().SetTitleSize(20);
    hratio.GetXaxis().SetTitleFont(43);
    hratio.GetXaxis().SetTitleOffset(4.);
    hratio.GetXaxis().SetLabelFont(43);
    hratio.GetXaxis().SetLabelSize(15);

    pad1.cd()
    hratio.Draw('e0')
    myline = ROOT.TLine(var[3], 1, var[4], 1)
    myline.SetLineWidth(2)
    myline.SetLineColor(ROOT.kBlack)
    myline.SetLineStyle(ROOT.kDashed)
    myline.Draw("SAME")
    c1.RedrawAxis()

    c1.SaveAs('tqGammaPlots0921/'+var[5]+'.png')
    #c1.SaveAs('tqGammaPlots0804/'+var[5]+'.pdf')

    del c1, pad1, pad0, hNtq, hNtqg, hLtqg, hratio, hadd
