import user 
import sys
import ROOT
import csv
#import PyCintex
import AthenaROOTAccess.transientTree
#ROOT.gErrorIgnoreLevel = 10

def loop(begin, end):
    """Convert a pair of C++ iterators into a python generator"""
    while (begin != end):
        yield begin.__deref__()  #*b
        begin.__preinc__()       #++b 

def getDaughters(part):
    decayVtx = part.end_vertex()
    if decayVtx:
        pOut_beg = decayVtx.particles_out_const_begin()
        pOut_end = decayVtx.particles_out_const_end()
        return [x for x in loop(pOut_beg,pOut_end)]
    else:
        return list()

def getParents(part):
    prodVtx = part.production_vertex()
    if prodVtx:
        pIn_beg     = prodVtx.particles_in_const_begin()
        pIn_end     = prodVtx.particles_in_const_end()
        return [x for x in loop(pIn_beg,pIn_end)]
    else:
        return list()

def getSource(part):
    parents = getParents(part)
    #return parents
    if (len(parents)==1 and parents[0].pdg_id() != part.pdg_id()):
        return parents

    elif (len(parents)== 1 and parents[0].pdg_id() == part.pdg_id()) :
        return getSource(parents[0])

    elif len(parents) > 1:
        #print "Photon parents: ",[x.pdg_id() for x in parents]
        #print part.pdg_id()
        if [x for x in parents if x.pdg_id() != part.pdg_id()] == []:
            print [x.pdg_id() for x in parents]

        return [x for x in parents if x.pdg_id() != part.pdg_id()]

    elif len(parents) == 0:
        print "Error: Orphan particle found"
        return list()
    else:
        print "What is happening: ", part.pdg_id()
        return list()
    return list()
    #return getParents(part)

def getSiblings(part):
    prodVtx = part.production_vertex()
    if prodVtx:
        pIn_beg     = prodVtx.particles_out_const_begin()
        pIn_end     = prodVtx.particles_out_const_end()
        return [x for x in loop(pIn_beg,pIn_end)]
    else:
        return list()

def getLastInChain(part):
    if len([x for x in getDaughters(part) if x.pdg_id() == part.pdg_id()])==0 :
        return part
    else:
        for x in getDaughters(part):
            if x.pdg_id() == part.pdg_id():
                return getLastInChain(x)
        return part 
#f = ROOT.TFile.Open("/eos/atlas/user/n/narayan/mc16_13TeV.410470.PhPy8EG_A14_ttbar_hdamp258p75_nonallhad.EVNT/EVNT.12458444._006021.pool.root.1")

ch=ROOT.AthenaROOTAccess.TChainROOTAccess('CollectionTree')
with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for li in csv_reader:
        for smpl in li:
            ch.AddFile(smpl)

#f = ROOT.TFile.Open(sys.argv[1])

#tt = AthenaROOTAccess.transientTree.makeTree(f)
tt = AthenaROOTAccess.transientTree.makeTree(ch)
dsid = sys.argv[1].split('/')[-1].split('.')[0]
print dsid, tt.GetEntries()

fOut    = ROOT.TFile("tqgammaNLO"+".root","RECREATE")
treOut  = ROOT.TTree("selection","photon to lepton selection")

from array import array
#import numpy as n


#weight      = array('d',[0])
#phStatus    = array('i',[0])
#phMass      = array('d',[0])
#phPt        = array('d',[0])
#lep1id      = array('i',[0])
#lep1eta     = array('d',[0])
#lep1pt      = array('d',[0])
#lep1phi     = array('d',[0])
#lep2id      = array('i',[0])
#lep2eta     = array('d',[0])
#lep2pt      = array('d',[0])
#lep2phi     = array('d',[0])
#
#treOut.Branch("EventNumber",EventNumber,"EventNumber/I")
#treOut.Branch("weight",weight,"weight/D")
#treOut.Branch("phStatus",phStatus,"phStatus/I")
#treOut.Branch("lep1id",lep1id,"lep1id/I")
#treOut.Branch("lep1eta",lep1eta,"lep1eta/D")
#treOut.Branch("lep1pt",lep1pt,"lep1pt/D")
#treOut.Branch("lep1phi",lep1phi,"lep1phi/D")
#treOut.Branch("lep2id",lep2id,"lep2id/I")
#treOut.Branch("lep2eta",lep2eta,"lep2eta/D")
#treOut.Branch("lep2pt",lep2pt,"lep2pt/D")
#treOut.Branch("lep2phi",lep2phi,"lep2phi/D")
#treOut.Branch("phMass",phMass,"phMass/D")
#treOut.Branch("phPt",phPt,"phPt/D")

EventNumber  = array('L',[0])
RunNumber    = array('L',[0])
weight       = array('d',[0])
parentStatus = array('i',[0])
parentPDG    = array('i',[0])
parentpt     = array('d',[0])
parenteta    = array('d',[0])
parentE      = array('d',[0])
parentphi    = array('d',[0])
parentrap    = array('d',[0])
lepPairMass = array('d',[0])
lepPairPt   = array('d',[0])
lep1id      = array('i',[0])
lep1bc      = array('i',[0])
lep1eta     = array('d',[0])
lep1pt      = array('d',[0])
lep1E       = array('d',[0])
lep1phi     = array('d',[0])
lep2id      = array('i',[0])
lep2bc      = array('i',[0])
lep2eta     = array('d',[0])
lep2pt      = array('d',[0])
lep2E       = array('d',[0])
lep2phi     = array('d',[0])
photonpt    = array('d',[0])
photoneta   = array('d',[0])
photonE     = array('d',[0])
photonphi   = array('d',[0])
toppt    = array('d',[0])
topeta   = array('d',[0])
topE     = array('d',[0])
topphi   = array('d',[0])
toprap   = array('d',[0])
btpt    = array('d',[0]) # b quark from the top
bteta   = array('d',[0])
btE     = array('d',[0])
btphi   = array('d',[0])
bglupt    = array('d',[0]) # b quark from the gluon
bglueta   = array('d',[0])
bgluE     = array('d',[0])
bgluphi   = array('d',[0])
fjetpt    = array('d',[0]) # forward jet in the event
fjeteta   = array('d',[0])
fjetE     = array('d',[0])
fjetphi   = array('d',[0])
mlvb   = array('d',[0])
mlvbTopMother   = array('d',[0])
mlvbNoTopMother = array('d',[0])
mlvba   = array('d',[0])
phparPDG = array('i',[0])
drab     = array('d',[0])
dral     = array('d',[0])
draj     = array('d',[0])
drat     = array('d',[0])
draw     = array('d',[0])
#topphpt  = array('d',[0])
#topphdr      = array('d',[0])
#wphpt     = array('d',[0])
#wphdr     = array('d',[0])
#reswphpt     = array('d',[0])
#reswphdr     = array('d',[0])
#bphpt     = array('d',[0])
#bphdr     = array('d',[0])
#lepphpt     = array('d',[0])
#lepphdr     = array('d',[0])
#isrphpt     = array('d',[0])
#isrphdr     = array('d',[0])
#mesphpt     = array('d',[0])
#mesphdr     = array('d',[0])
#othphpt     = array('d',[0])
#othphdr     = array('d',[0])



treOut.Branch("EventNumber",EventNumber,"EventNumber/I")
treOut.Branch("RunNumber",RunNumber,"RunNumber/I")
treOut.Branch("weight",weight,"weight/D")
treOut.Branch("parentStatus",parentStatus,"parentStatus/I") # W boson from top decay
treOut.Branch("parentPDG",parentPDG,"parentPDG/I")
treOut.Branch("parenteta",parenteta,"parenteta/D")
treOut.Branch("parentpt",parentpt,"parentpt/D")
treOut.Branch("parentE",parentE,"parentE/D")
treOut.Branch("parentphi",parentphi,"parentphi/D")
treOut.Branch("parentrap",parentrap,"parentrap/D")
treOut.Branch("lep1id",lep1id,"lep1id/I") # charged lepton
treOut.Branch("lep1bc",lep1bc,"lep1bc/I")
treOut.Branch("lep1eta",lep1eta,"lep1eta/D")
treOut.Branch("lep1pt",lep1pt,"lep1pt/D")
treOut.Branch("lep1E",lep1E,"lep1E/D")
treOut.Branch("lep1phi",lep1phi,"lep1phi/D")
treOut.Branch("lep2id",lep2id,"lep2id/I")   # neutral lepton
treOut.Branch("lep2bc",lep2bc,"lep2bc/I")
treOut.Branch("lep2eta",lep2eta,"lep2eta/D")
treOut.Branch("lep2pt",lep2pt,"lep2pt/D")
treOut.Branch("lep2E",lep2E,"lep2E/D")
treOut.Branch("lep2phi",lep2phi,"lep2phi/D")
treOut.Branch("lepPairMass",lepPairMass,"lepPairMass/D")
treOut.Branch("lepPairPt",lepPairPt,"lepPairPt/D")
treOut.Branch("photoneta",photoneta,"photoneta/D")
treOut.Branch("photonpt",photonpt,"photonpt/D")
treOut.Branch("photonE",photonE,"photonE/D")
treOut.Branch("photonphi",photonphi,"photonphi/D")
treOut.Branch("topeta",topeta,"topeta/D")
treOut.Branch("toppt",toppt,"toppt/D")
treOut.Branch("topE",topE,"topE/D")
treOut.Branch("topphi",topphi,"topphi/D")
treOut.Branch("toprap",toprap,"toprap/D")
treOut.Branch("bteta",bteta,"bteta/D")
treOut.Branch("btpt",btpt,"btpt/D")
treOut.Branch("btE",btE,"btE/D")
treOut.Branch("btphi",btphi,"btphi/D")
treOut.Branch("bglueta",bglueta,"bglueta/D")
treOut.Branch("bglupt",bglupt,"bglupt/D")
treOut.Branch("bgluE",bgluE,"bgluE/D")
treOut.Branch("bgluphi",bgluphi,"bgluphi/D")
treOut.Branch("fjeteta",fjeteta,"fjeteta/D")
treOut.Branch("fjetpt",fjetpt,"fjetpt/D")
treOut.Branch("fjetE",fjetE,"fjetE/D")
treOut.Branch("fjetphi",fjetphi,"fjetphi/D")
treOut.Branch("mlvb",mlvb,"mlvb/D")
treOut.Branch("mlvbTopMother",mlvbTopMother,"mlvbTopMother/D")
treOut.Branch("mlvbNoTopMother",mlvbNoTopMother,"mlvbNoTopMother/D")
treOut.Branch("mlvba",mlvba,"mlvba/D")
treOut.Branch("phparPDG",phparPDG,"phparPDG/I")
treOut.Branch("drab",drab,"drab/D")
treOut.Branch("dral",dral,"dral/D")
treOut.Branch("draj",draj,"draj/D")
treOut.Branch("drat",drat,"drat/D")
treOut.Branch("draw",draw,"draw/D")
#treOut.Branch("topphpt",topphpt,"topphpt/D")
#treOut.Branch("topphdr",topphdr,"topphdr/D")
#treOut.Branch("wphpt",wphpt,"wphpt/D")
#treOut.Branch("wphdr",wphdr,"wphdr/D")
#treOut.Branch("reswphpt",reswphpt,"reswphpt/D")
#treOut.Branch("reswphdr",reswphdr,"reswphdr/D")
#treOut.Branch("bphpt",bphpt,"bphpt/D")
#treOut.Branch("bphdr",bphdr,"bphdr/D")
#treOut.Branch("lepphpt",lepphpt,"lepphpt/D")
#treOut.Branch("lepphdr",lepphdr,"lepphdr/D")
#treOut.Branch("isrphpt",isrphpt,"isrphpt/D")
#treOut.Branch("isrphdr",isrphdr,"isrphdr/D")
#treOut.Branch("mesphpt",mesphpt,"mesphpt/D")
#treOut.Branch("mesphdr",mesphdr,"mesphdr/D")
#treOut.Branch("othphpt",othphpt,"othphpt/D")
#treOut.Branch("othphdr",othphdr,"othphdr/D")


totalWeight = ROOT.TH1D("totalWeight","totalWeight",1,0.5,1.5)
totalWeight.Sumw2()
myWeight = 0
countj = 0
for iev in tt:
    countj += 1
    if (countj%50000 == 0):
        print countj
        #break
    evt = iev.GEN_EVENT[0]
    EventNumber[0] = iev.McEventInfo.event_ID().event_number()
    RunNumber[0] = iev.McEventInfo.event_ID().run_number()
    #print runNumber
    weight[0]   = evt.weights().front()
    totalWeight.Fill(1,weight[0])
    myWeight += weight[0]
    beg = evt.particles_begin()
    end = evt.particles_end()
    selPair = []
    #print "EventNumber: ",EventNumber[0]
    cand_topo = []
    lqids = [1,2,3,4]
    list_photons = []
    list_tops = []
    list_btms = [] 
    list_wbsn = []
    list_bgls = []
    list_fjts = []
    for part in loop(beg,end):
        if (abs(part.pdg_id()) == 6): # find top quark and decay particles W and b
            top = getLastInChain(part)
            if (top not in list_tops):
                list_tops.append(top)
                topdaughters = getDaughters(top)
                for td in topdaughters:
                    if (abs(td.pdg_id()) == 5):
                        list_btms.append(td)
                    elif (abs(td.pdg_id()) == 24):
                        list_wbsn.append(td)
                    elif (abs(td.pdg_id()) not in [22, 11, 12, 13, 14, 15, 16]):
                        print "Error: Invalid top daughter", td.pdg_id()

        if (abs(part.pdg_id()) == 22): #and part.status() == 1): # find photon
            if (getLastInChain(part) not in list_photons):
                list_photons.append(getLastInChain(part))
                #print part.momentum().perp()
        if (abs(part.pdg_id()) in lqids ): # find forward jet (a W and a light jet in Parents+Siblings)
            sibpar = getParents(part) + getSiblings(part)
            sibparid = [x.pdg_id() for x in sibpar]
            if (24 in sibparid or -24 in sibparid):
                for pvid in sibparid:
                    if abs(pvid) in lqids:
                        list_fjts.append(part)
                        break
        if (abs(part.pdg_id()) == 5 ): # find b-jet (pdgid = 5 and another b as sibling and parent = gluon)
            sibpar = getParents(part) + getSiblings(part)
            parid = [abs(x.pdg_id()) for x in getParents(part)]
            sibparid = [x.pdg_id() for x in sibpar]
            if (( (-1* part.pdg_id()) in sibparid) and (21 in parid) ):
                list_bgls.append(part)

        if ( abs(part.pdg_id()) in [11, 13, 15] ):    # find lepton
            prodVtx     = part.production_vertex()
            if prodVtx:
                pOut_beg    = prodVtx.particles_out_const_begin()
                pIn_beg     = prodVtx.particles_in_const_begin()
                pOut_end    = prodVtx.particles_out_const_end()
                pIn_end     = prodVtx.particles_in_const_end()

                daughterpair=()
                for sibling in loop(pOut_beg,pOut_end):
                    #print (sibling.pdg_id()*part.pdg_id())
                    if ( (sibling.pdg_id()*part.pdg_id()) in [-132, -182, -240] ):
                        daughterpair = (part,sibling)

                if daughterpair:
                    if getLastInChain(daughterpair[0]) not in sum(cand_topo,()):
                        for parent in loop(pIn_beg,pIn_end):
                            if (abs(parent.pdg_id()) == 24 ):
                                #print parent, daughterpair[0], daughterpair[1]
                                cand_topo.append( ( parent, getLastInChain(daughterpair[0]), getLastInChain(daughterpair[1]) ) )
                            else:
                                pass #print "New Parent found: ", parent.pdg_id()
    

    if len(cand_topo) != 1:                            
        pass
        #print "Error: 2 W bosons found",len(cand_topo)
    if len(list_tops) != 1:
        print "Error: More than one top quark found", len(list_tops)
    list_bgls = [x for x in list_bgls if x.pdg_id()*list_tops[0].pdg_id() == -30]
    if len(list_bgls) != 1:
        pass
        #print "Error: More than one bottom quark from gluon found", len(list_bgls)
    if len(list_fjts) != 1:
        pass
        #print "Error: More than one forward quark found", len(list_fjts)

    if len(list_wbsn) > 0 and len(cand_topo) > 0:
        if cand_topo[0][0] != getLastInChain(list_wbsn[0]):
            print "Error: Leptons mother is not the top quark's daughter"

    if len(cand_topo)>0:
        for i in xrange(len(cand_topo)):
        #print "Parent: ",cand_topo[0][0].pdg_id()," children: ",cand_topo[0][1].pdg_id()," ", cand_topo[0][2].pdg_id()
            #print "Parent: %d(%d) child1: %d(%d) child2: %d(%d)"%(cand_topo[i][0].pdg_id(),cand_topo[i][0].barcode(),cand_topo[i][1].pdg_id(),cand_topo[i][1].barcode(),cand_topo[i][2].pdg_id(),cand_topo[i][2].barcode())
            parentStatus[0] = cand_topo[i][0].status()
            parentPDG[0]   = cand_topo[i][0].pdg_id()
            parenteta[0]     = cand_topo[i][0].momentum().eta()
            parentpt[0]      = cand_topo[i][0].momentum().perp()
            parentE[0]       = cand_topo[i][0].momentum().e()
            parentphi[0]     = cand_topo[i][0].momentum().phi()

            #cand_topo[i][1]= getLastInChain(cand_topo[i][1])
            lep1id[0]      = cand_topo[i][1].pdg_id()
            lep1bc[0]      = cand_topo[i][1].barcode()
            lep1eta[0]     = cand_topo[i][1].momentum().eta()
            lep1pt[0]      = cand_topo[i][1].momentum().perp()
            lep1E[0]       = cand_topo[i][1].momentum().e()
            lep1phi[0]     = cand_topo[i][1].momentum().phi()

            #cand_topo[i][2] = getLastInChain(cand_topo[i][2])
            lep2id[0]      = cand_topo[i][2].pdg_id()
            lep2bc[0]      = cand_topo[i][2].barcode()
            lep2eta[0]     = cand_topo[i][2].momentum().eta()
            lep2pt[0]      = cand_topo[i][2].momentum().perp()
            lep2E[0]       = cand_topo[i][2].momentum().e()
            lep2phi[0]     = cand_topo[i][2].momentum().phi()

            list_photons.sort(key=lambda x: x.momentum().perp(), reverse=True)
            list_photons[0] = getLastInChain(list_photons[0])
            if list_photons[0].status() in [23, 44, 51, 52]:
                continue
                #pass
            elif list_photons[0].status() != 1:
                print "Photon status: ", list_photons[0].status()

            Photonparents = getSource(list_photons[0])
            phFromHadrons = False

            for parent in Photonparents:
                if abs(parent.pdg_id()) > 100:
                    phFromHadrons = True
                    continue
                if abs(parent.pdg_id())< 100:
                    print parent.pdg_id()

            if phFromHadrons:
                continue

            '''for photonItr in list_photons:
                if photonItr.status() == 1:
                    break
                else:
                    print "Photon status and parents: ", photonItr.status(), [x.pdg_id() for x in getParents(photonItr)]
                    print "Daughters: ", [x.pdg_id() for x in getDaughters(photonItr)]
                    break'''

            photoneta[0]     = list_photons[0].momentum().eta()
            photonpt[0]      = list_photons[0].momentum().perp()
            photonE[0]       = list_photons[0].momentum().e()
            photonphi[0]     = list_photons[0].momentum().phi()
            av          = ROOT.TLorentzVector()
            av.SetPtEtaPhiE(photonpt[0],photoneta[0],photonphi[0],photonE[0])
            #topphpt[0] = -99
            #topphdr[0] = -99
            #wphpt[0] = -99
            #wphdr[0] = -99
            #reswphpt[0] = -99
            #reswphdr[0] = -99
            #bphpt[0] = -99
            #bphdr[0] = -99
            #lepphpt[0] = -99
            #lepphdr[0] = -99
            #isrphpt[0] = -99
            #isrphdr[0] = -99
            #mesphpt[0] = -99
            #mesphdr[0] = -99
            #othphpt[0] = -99
            #othphdr[0] = -99
            phparents = getSource(list_photons[0])

            if (len(phparents) >= 1):
                '''while len(phparents) >= 1 and abs(phparents[0].pdg_id()) > 100:
                    if (len(getSource(phparents[0])) ==0):
                        print "breaker", phparents[0].pdg_id()
                        break;
                    phparents = getSource(phparents[0])'''
                phparPDG[0] = phparents[0].pdg_id()
                #if abs(phparPDG[0]) < 100:
                #print phparPDG[0]
                #phparparPdg = 0
                #parentfv = ROOT.TLorentzVector()
                #if (phparPDG[0] in [6, -6, 24, -24, 5,-5, 11,-11,13,-13,15,-15, 111, 221, 223]):
                 #   parentfv.SetPtEtaPhiE(phparents[0].momentum().perp(),phparents[0].momentum().eta(),phparents[0].momentum().phi(),phparents[0].momentum().e())
                  #  phparpar = getSource(phparents[0])
                    #if(len (phparpar)>= 1):
                     #   phparparPdg = phparpar[0].pdg_id()

                #print phparents[0].momentum().perp(), phparents[0].momentum().eta(),phparents[0].momentum().phi(),phparents[0].momentum().e()
#if(phparPDG[0] in [6, -6]):
#    topphpt[0] = list_photons[0].momentum().perp()
#    topphdr[0] = parentfv.DeltaR(av)
#elif (phparPDG[0] in [24, -24] and phparparPdg in [6, -6]):
#    wphpt[0] = list_photons[0].momentum().perp()
#    wphdr[0] = parentfv.DeltaR(av)
#elif (phparPDG[0] in [24, -24]):
#    reswphpt[0] = list_photons[0].momentum().perp()
#    reswphdr[0] = parentfv.DeltaR(av)
#elif (phparPDG[0] in [5, -5] and phparparPdg in [6, -6]):
#    bphpt[0] = list_photons[0].momentum().perp()
#    bphdr[0] = parentfv.DeltaR(av)
#elif (phparPDG[0] in [11, -11, 13, -13, 15, -15] and phparparPdg in [6, -6, 24, -24]):
#    lepphpt[0] = list_photons[0].momentum().perp()
#    lepphdr[0] = parentfv.DeltaR(av)
#elif (phparPDG[0] in [1,-1, 2,-2, 3, -3, 4,-4, 21]):
#    isrphpt[0] = list_photons[0].momentum().perp()
#    #isrphdr[0] = parentfv.DeltaR(av)
#elif (phparPDG[0] in [111,221,223]):
#    mesphpt[0] = list_photons[0].momentum().perp()
#    mesphdr[0] = parentfv.DeltaR(av)
#    #print phparPDG[0], phparparPdg
#else:
#    othphpt[0] = list_photons[0].momentum().perp()
#    #othphdr[0] = parentfv.DeltaR(av)
#
#if (phparPDG[0] in [24, -24] and phparparPdg not in [6, -6]):
#    #print phparPDG[0], phparparPdg
#    pass
#elif (phparPDG[0] in [5, -5, 11,-11,13,-13, 15, -15] and phparparPdg not in [6, -6,24,-24]):
#    #print phparPDG[0], phparparPdg
#    pass
#
            else:
                phparPDG[0] = -999
                print "Orphan"
            '''elif (len(phparents) > 1):
                phparPDG[0] = phparents[0].pdg_id()
                for x in phparents:
                    print "  Error: More photon parents found  ", x.pdg_id(),'''

            topeta[0]     = list_tops[0].momentum().eta()
            toppt[0]      = list_tops[0].momentum().perp()
            topE[0]       = list_tops[0].momentum().e()
            topphi[0]     = list_tops[0].momentum().phi()

            bteta[0]     = list_btms[0].momentum().eta()
            btpt[0]      = list_btms[0].momentum().perp()
            btE[0]       = list_btms[0].momentum().e()
            btphi[0]     = list_btms[0].momentum().phi()

            if len(list_bgls) > 0:
                bglueta[0]     = list_bgls[0].momentum().eta()
                bglupt[0]      = list_bgls[0].momentum().perp()
                bgluE[0]       = list_bgls[0].momentum().e()
                bgluphi[0]     = list_bgls[0].momentum().phi()
            else:
                bglueta[0]     = -99.0
                bglupt[0]      = -99.0
                bgluE[0]       = -99.0
                bgluphi[0]     = -99.0
            
            if len(list_fjts) > 0:
                fjeteta[0]     = list_fjts[0].momentum().eta()
                fjetpt[0]      = list_fjts[0].momentum().perp()
                fjetE[0]       = list_fjts[0].momentum().e()
                fjetphi[0]     = list_fjts[0].momentum().phi()

            lv1         = ROOT.TLorentzVector()
            lv2         = ROOT.TLorentzVector()
            bgv         = ROOT.TLorentzVector()
            btv         = ROOT.TLorentzVector()
            tv          = ROOT.TLorentzVector()
            pv          = ROOT.TLorentzVector()



            lv1.SetPtEtaPhiE(lep1pt[0],lep1eta[0],lep1phi[0],lep1E[0])
            lv2.SetPtEtaPhiE(lep2pt[0],lep2eta[0],lep2phi[0],lep2E[0])
            bgv.SetPtEtaPhiE(bglupt[0],bglueta[0],bgluphi[0],bgluE[0])
            btv.SetPtEtaPhiE(btpt[0],bteta[0],btphi[0],btE[0])
            tv.SetPtEtaPhiE(toppt[0],topeta[0],topphi[0],topE[0])
            pv.SetPtEtaPhiE(parentpt[0],parenteta[0],parentphi[0],parentE[0])

            dral[0] = lv1.DeltaR(av)
            drab[0] = btv.DeltaR(av)
            drat[0] = tv.DeltaR(av)
            draw[0] = pv.DeltaR(av)
            toprap[0] = tv.Rapidity()
            parentrap[0] = pv.Rapidity()
            draj[0] = -1.0
            lepPairMass[0]  = (lv1 + lv2).M()
            lepPairPt[0]    = (lv1 + lv2).Perp()
            mlvb[0]   = (lv1+lv2+btv).M()
            mlvba[0] = (lv1+lv2+btv+av).M()
            mlvbTopMother[0] = 0
            mlvbNoTopMother[0] = 0
            topDtrs = [abs(x.pdg_id()) for x in getDaughters(list_tops[0])]
            if (22 in topDtrs):
                mlvbTopMother[0] = (lv1+lv2+btv).M()
            else:
                mlvbNoTopMother[0]   = (lv1+lv2+btv).M()


            treOut.Fill()

    #for part in loop(beg,end):
    #    if abs(part.pdg_id()) == 6:
    #        decayVtx = part.end_vertex()
    #        li_daughters=[]
    #        if (decayVtx):
    #            pOut_begin = decayVtx.particles_out_const_begin()
    #            pOut_end   = decayVtx.particles_out_const_end()
    #            for daughter in loop(pOut_begin,pOut_end):
    #                li_daughters.append(daughter)
    #                if abs(daughter.pdg_id() ==11):
    #                    print "Electron Found"
    #for part in loop(beg,end):
    #    if abs(part.pdg_id())==11 and part.status() ==1 and len(getSiblings(part))==2 and getSiblings(part)[0].pdg_id() == -getSiblings(part)[1].pdg_id():
    #        selPair.append((getSiblings(part)[0],getSiblings(part)[1]))
    #for x in selPair:
    #    lv1 = ROOT.TLorentzVector()
    #    lv2 = ROOT.TLorentzVector()
    #    lv1.SetPxPyPzE(x[0].momentum().px(),x[0].momentum().py(),x[0].momentum().pz(),x[0].momentum().e())
    #    lv2.SetPxPyPzE(x[1].momentum().px(),x[1].momentum().py(),x[1].momentum().pz(),x[1].momentum().e())

    #    if ( lv1 + lv2 ).M() >1000 :
    #        print [(x[0].pdg_id(),y.pdg_id()) for y in getParents(x[0])],[(x[1].pdg_id(),y.pdg_id()) for y in getParents(x[1])]




            #print [x.pdg_id() for x in getDaughters(part)]
    #    if(abs(part.pdg_id())==11):
    #        sel_parents = []
    #        prodVtx = part.production_vertex()
    #        if prodVtx:
    #            pP_beg  = part.production_vertex().particles_in_const_begin()
    #            pP_end  = part.production_vertex().particles_in_const_end();
    #            for parent in loop(pP_beg,pP_end):
    #                if part.status()==1 and parent.pdg_id() != 111 and abs(parent.pdg_id()) != 24 and abs(parent.pdg_id()) !=15:
    #                    print parent.pdg_id()
    #        else: 
    #             print "No production vertex"

        #if(part.pdg_id() == 22 and part.status() >=50 and part.status()<60):
        #    pOut_beg = part.end_vertex().particles_out_const_begin()
        #    pOut_end = part.end_vertex().particles_out_const_end()
        #    
        #    sel_daughter=[]
        #    for daughter in loop(pOut_beg,pOut_end):
        #        if(abs(daughter.pdg_id())==11 or abs(daughter.pdg_id()==13)):
        #            sel_daughter.append(daughter)

        #    if(len(sel_daughter) ==2):
        #        lvd1 = ROOT.TLorentzVector()
        #        lvd2 = ROOT.TLorentzVector()
        #        lvd1.SetPxPyPzE(sel_daughter[0].momentum().px(),sel_daughter[0].momentum().py(),sel_daughter[0].momentum().pz(),sel_daughter[0].momentum().e())
        #        lvd2.SetPxPyPzE(sel_daughter[1].momentum().px(),sel_daughter[1].momentum().py(),sel_daughter[1].momentum().pz(),sel_daughter[1].momentum().e())
        #        
        #        gamma_lv = (lvd1 + lvd2)
        #        phMass[0]   = gamma_lv.M()
        #        phPt[0]     = gamma_lv.Perp()
        #        phStatus[0] = part.status()

        #        print gamma_lv.M()
        #        print gamma_lv.Perp()
        #        
        #        lep1id[0]   = sel_daughter[0].pdg_id()
        #        lep1eta[0]  = sel_daughter[0].momentum().eta()
        #        lep1pt[0]   = sel_daughter[0].momentum().perp()
        #        lep1phi[0]  = sel_daughter[0].momentum().phi()
        #        lep2id[0]   = sel_daughter[1].pdg_id()
        #        lep2eta[0]  = sel_daughter[1].momentum().eta()
        #        lep2pt[0]   = sel_daughter[1].momentum().perp()
        #        lep2phi[0]  = sel_daughter[1].momentum().phi()
        #        treOut.Fill()
print "my Total weight: ", myWeight
treOut.Write()
totalWeight.Write()
fOut.Close()
