from MadGraphControl.MadGraph_NNPDF30NLO_Base_Fragment import *
from MadGraphControl.MadGraphUtils import *
import os,subprocess,fileinput

# General settings 

nevents = runArgs.maxEvents*1.1 if runArgs.maxEvents>0 else 1.1*evgenConfig.nEventsPerJob



name = 'tqgammaSM_tchan_4fl'
runName='madgraph.'+str(runArgs.runNumber)+'.MadGraph_'+str(name)



process = """
import model sm
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~ 
define l+ = e+ mu+ ta+ 
define l- = e- mu- ta-
define vl = ve vm vt 
define vl~ = ve~ vm~ vt~
generate p p > t b~ j a $$ w+, (t > l+ vl b)
add process p p > t b~ j $$ w+, (t > l+ vl b a)
add process p p > t~ b j a $$ w-, (t~ > l- vl~ b~)
add process p p > t~ b j $$ w-, (t~ > l- vl~ b~ a) 
output -f
"""


beamEnergy=-999
if hasattr(runArgs,'ecmEnergy'):
    beamEnergy = runArgs.ecmEnergy / 2.
else:
    raise RuntimeError("No center of mass energy found.")



#Fetch default LO run_card.dat and set parameters

extras = { 'cut_decays'    : 'T',
		   'lhe_version'   : 3.0,
           'pta'           :10,
           'maxjetflavor'  :4,
           'drab'          :0.2, 
           'draj'          :0.2, 
           'dral'          :0.2,
           'dynamical_scale_choice': '3', #sum of the transverse mass divided by 2
           'ptl'           :0.0,
           'ptj'           :0.0,
           'etal'          :5.0,
           'etaa'          :5.0,
           'etaj'          :-1,
           'etab'          :-1,
           'drjj'          :0.0,
           'drjl'          :0.0,
           'drll'          :0.0,
           'draa'          :0.0,
           'nevents'       :int(nevents),
           }

process_dir = new_process(process)#grid_pack=gridpack_dir)

modify_run_card(process_dir=process_dir,runArgs=runArgs,settings=extras)



print_cards()

generate(runArgs=runArgs, process_dir=process_dir) #,grid_pack=gridpack_mode,gridpack_dir=gridpack_dir,gridpack_compile=True)
outputDS=arrange_output(runArgs=runArgs, process_dir=process_dir,lhe_version=3, saveProcDir=True)

#### Shower
evgenConfig.description = 'MadGraph_'+str(name)
evgenConfig.generators += ["MadGraph", "Pythia8"]
evgenConfig.keywords+= ['SM', 'top',  'photon','singleTop','lepton'] 
evgenConfig.contact = ['harish.potti@cern.ch']
runArgs.inputGeneratorFile=outputDS


include("Pythia8_i/Pythia8_A14_NNPDF23LO_EvtGen_Common.py")



if 'ATHENA_PROC_NUMBER' in os.environ:
    evgenLog.info('Noticed that you have run with an athena MP-like whole-node setup.  Will re-configure now to make sure that the remainder of the job runs serially.')
    njobs = os.environ.pop('ATHENA_PROC_NUMBER')
    # Try to modify the opts underfoot
    if not hasattr(opts,'nprocs'): 
        mglog.warning('Did not see option!')
    else: opts.nprocs = 0
    print opts

include("Pythia8_i/Pythia8_MadGraph.py")
include("Pythia8_i/Pythia8_ShowerWeights.py")
