from MadGraphControl.MadGraphUtils import *
import os,subprocess,fileinput
from MadGraphControl.MadGraph_NNPDF30NLOnf4_Base_Fragment import *

# General settings 

nevents = runArgs.maxEvents*1.1 if runArgs.maxEvents>0 else 1.1*evgenConfig.nEventsPerJob


name = 'tqgammaSM_tchan_4fl_NLO'
runName='madgraph.'+str(runArgs.runNumber)+'.MadGraph_'+str(name)


process = """
import model loop_sm
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~ 
define l+ = e+ mu+ ta+ 
define l- = e- mu- ta-
define vl = ve vm vt 
define vl~ = ve~ vm~ vt~
generate p p > t b~ j a $$ w+ w- [QCD]
add process p p > t~ b j a $$ w+ w- [QCD] 
output -f
"""


process_dir = new_process(process)#grid_pack=gridpack_dir)


beamEnergy=-999
if hasattr(runArgs,'ecmEnergy'):
    beamEnergy = runArgs.ecmEnergy / 2.
else:
    raise RuntimeError("No center of mass energy found.")



#Fetch default LO run_card.dat and set parameters

extras = { 'lhe_version'  : '3.0',
           'parton_shower' :'PYTHIA8',
           'ptgmin'        :10,
           'r0gamma'       :0.2, 
           'maxjetflavor'  :4,
           'dynamical_scale_choice': '3', #sum of the transverse mass divided by 2  
           'ptl'           :0.0,
           'ptj'           :0.0,
           'etal'          :5.0,
           'etagamma'      :5.0,
           'etaj'          :-1,
           'drll'          :0.0,
           'store_rwgt_info':True,
           'nevents' : int(nevents),
           }




modify_run_card(process_dir=process_dir, runArgs=runArgs, settings=extras)

WT = 1.320000e+00
WW = 2.085000e+00

decays = {'6':"""DECAY  6  """+str(WT)+""" #WT
        #  BR             NDA  ID1    ID2   ...
        1.000000e+00   2   5  24 # 1.32
        #""",
        '24':"""DECAY  24  """+str(WW)+""" #WW
        #  BR             NDA  ID1    ID2   ...
        3.377000e-01   2    -1  2
        3.377000e-01   2    -3  4
        1.082000e-01   2   -11 12
        1.082000e-01   2   -13 14
        1.082000e-01   2   -15 16
        #"""}



modify_param_card(process_dir=process_dir,params={'DECAY':decays})

               
               
madspin_card=process_dir+'/Cards/madspin_card.dat'
if os.access(madspin_card,os.R_OK):
    os.unlink(madspin_card)                                                                                                                                    
mscard = open(madspin_card,'w')  
                                                                                                                                  
mscard.write("""#************************************************************                                                                                          
#*                        MadSpin                           *                                                                                                              
#*                                                          *                                                                                                              
#*    P. Artoisenet, R. Frederix, R. Rietkerk, O. Mattelaer *                                                                                                              
#*                                                          *                                                                                                              
#*    Part of the MadGraph5_aMC@NLO Framework:              *                                                                                                              
#*    The MadGraph5_aMC@NLO Development Team - Find us at   *                                                                                                              
#*    https://server06.fynu.ucl.ac.be/projects/madgraph     *                                                                                                              
#*                                                          *                                                                                                              
#************************************************************                                                                                                              
#Some options (uncomment to apply)                                                                                                                                         
#                                                                                                                                                                          
# set seed 1                                                                                                                                                               
# set Nevents_for_max_weigth 75 # number of events for the estimate of the max. weight                                                                                     
# set BW_cut 15                # cut on how far the particle can be off-shell                                                                                              
 set max_weight_ps_point 400  # number of PS to estimate the maximum for each event                                                                                        
#                                                                                                                                                                          
set seed %i                                                                                                                                                                
# specify the decay for the final state particles                                                                                                                          
decay t > w+ b, w+ > l+ vl                                                                                                                                               
decay t~ > w- b~, w- > l- vl~                                                                                                                                                                                                                                                                                                      
# running the actual code                                                                                                                                                  
launch"""%runArgs.randomSeed)                                                                                                                                              
mscard.close()

print_cards()

generate(runArgs=runArgs, process_dir=process_dir)#,grid_pack=gridpack_mode,gridpack_dir=gridpack_dir,gridpack_compile=True)

outputDS=arrange_output(runArgs=runArgs, process_dir=process_dir,lhe_version=3, saveProcDir= True)

#### Shower
evgenConfig.description = 'aMC@NLO_'+str(name)
evgenConfig.generators += ["aMcAtNlo", "Pythia8"]
evgenConfig.keywords+= ['SM', 'top',  'photon','singleTop','lepton'] 
evgenConfig.contact = ['bjorn.wendland@cern.ch']
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

include("Pythia8_i/Pythia8_aMcAtNlo.py")
include("Pythia8_i/Pythia8_ShowerWeights.py")
