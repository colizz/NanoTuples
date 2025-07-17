# NanoTuples

Custom NanoAOD ntuple producers with additional boosted jet taggers and their PF candidates.

This branch provides a recipe for integrating a self-trained tagger into the MiniAODv6-NanoAODv15 workflow.

The code is compatible with CMSSW_15_0_X.

<!-- TOC -->

- [NanoTuples](#nanotuples)
    - [Version](#version)
    - [Setup](#setup)
        - [Set up CMSSW](#set-up-cmssw)
        - [Get customized NanoAOD producers](#get-customized-nanoaod-producers)
        - [Compile](#compile)
        - [Test](#test)
    - [Production](#production)

<!-- /TOC -->

------

## Version

The current version is based on [NanoAODv15](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Releases/NanoAODv15).

------

## Setup

### Set up CMSSW

```bash
cmsrel CMSSW_15_0_10
cd CMSSW_15_0_10/src
cmsenv
```

### Get customized NanoAOD producers

```bash
git clone https://github.com/colizz/NanoTuples.git PhysicsTools/NanoTuples -b dev-custom-tagger-nanov15
```

### Get the custom model

Example for the GloParTv3 full-score model:
```bash
wget https://coli.web.cern.ch/coli/tmp/.230626-003937_partv2_model/ak8/V03FullScore/model_full_score.onnx -O $CMSSW_BASE/src/PhysicsTools/NanoTuples/data/InclParticleTransformer-MD/ak8/V03FullScore/model_full_score.onnx
```

### Update the model configs

- Place the model directory (containing the ONNX and JSON files) in `data/`.  
- Add the model's cff file in `python/newTagger/`, which defines the inference module:  
  - Includes **"TagInfos"** (to acquire input variables for inference) and **"JetTags"** (the inference module).  
- Integrate the **"TagInfos"** and **"JetTags"** modules for the new model into `python/newTagger/jetTools.py` and `python/newTagger/bTaggingCustomUtils.py`.  
- Modify `python/newTagger/nanoTuples_cff.py` to enable the additional tagger inference using the **"updateJetCollection"** utility and specify the scores to store in NanoAOD.

### Compile

```bash
scram b -j16
```

### Test

<!-- 
MC (UL16, MiniAODv1):

```bash
cmsDriver.py test_nanoTuples_mc2016 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_mcRun2_asymptotic_v15 --step NANO --nThreads 1 --era Run2_2016,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIISummer16MiniAODv3/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/80000/FEC61D42-F5F5-E811-8435-001E67A4061D.root --fileout file:nano_mc2016.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_mc2016.log &

less +F test_mc2016.log
```

Data (UL16, MiniAODv1):

```bash
cmsDriver.py test_nanoTuples_data2016 -n 1000 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 106X_dataRun2_v32 --step NANO --nThreads 1 --era Run2_2016,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein /store/data/Run2016H/MET/MINIAOD/17Jul2018-v2/00000/0A0B71F7-75B8-E811-BAB7-0425C5DE7BE4.root --fileout file:nano_data2016.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_data2016.log &

less +F test_data2016.log
```


MC (UL17, MiniAODv1):

```bash
cmsDriver.py test_nanoTuples_mc2017 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_mc2017_realistic_v8 --step NANO --nThreads 1 --era Run2_2017,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIIFall17MiniAODv2/DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/60000/F492A0D0-3F56-E811-9387-FA163EB32A35.root --fileout file:nano_mc2017.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_mc2017.log &

less +F test_mc2017.log
```

Data (UL17, MiniAODv1):

```bash
cmsDriver.py test_nanoTuples_data2017 -n 1000 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 106X_dataRun2_v32 --step NANO --nThreads 1 --era Run2_2017,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein /store/data/Run2017F/SingleElectron/MINIAOD/31Mar2018-v1/90002/EC099452-C938-E811-9922-0CC47A7C354C.root --fileout file:nano_data2017.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_data2017.log &

less +F test_data2017.log
``` 
-->

Test commands

MC (Summer24, MiniAODv6):

```bash
cmsDriver.py  --python_filename test_nanoTuples_mc2024.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --datatier NANOAODSIM --fileout file:nano_mc2024.root --conditions 150X_mcRun3_2024_realistic_v2 --step NANO --scenario pp --filein /store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-800to1000_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/120000/1b7182ab-2d1d-4c1f-96bf-930e464d0ac7.root --era Run3_2024 --mc -n 10
```

Data (Summer24, MiniAODv6):

```bash
cmsDriver.py --python_filename test_nanoTuples_data2024.py --eventcontent NANOAOD --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --datatier NANOAOD --fileout file:nano_data2024.root --conditions 150X_dataRun3_v2 --step NANO --scenario pp --filein /store/data/Run2024C/JetMET1/MINIAOD/MINIv6NANOv15-v1/2530000/f91e593e-2d71-4e88-91cb-116eb66cb80d.root --era Run3_2024 --data -n 10
```

<!--
------

## Production

**Step 0**: switch to the crab production directory and set up grid proxy, CRAB environment, etc.

```bash
cd $CMSSW_BASE/src/PhysicsTools/NanoTuples/crab
# set up grid proxy
voms-proxy-init -rfc -voms cms --valid 168:00
# set up CRAB env (must be done after cmsenv)
source /cvmfs/cms.cern.ch/common/crab-setup.sh
```

**Step 1**: generate the python config file with `cmsDriver.py` with the following commands:


MC (UL16, Run B-F, pre-VFP/APV, MiniAODv1):

```bash
cmsDriver.py mc2016 -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_mcRun2_asymptotic_preVFP_v9 --step NANO --nThreads 1 --era Run2_2016,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

MC (UL16, Run G-H, post-VFP, MiniAODv1):

```bash
cmsDriver.py mc2016 -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_mcRun2_asymptotic_v15 --step NANO --nThreads 1 --era Run2_2016,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (UL16, MiniAODv1):

```bash
cmsDriver.py data2016 -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 106X_dataRun2_v32 --step NANO --nThreads 1 --era Run2_2016,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec
```


MC (UL17, MiniAODv1):

```bash
cmsDriver.py mc2017 -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_mc2017_realistic_v8 --step NANO --nThreads 1 --era Run2_2017,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (UL17, MiniAODv1):

```bash
cmsDriver.py data2017 -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 106X_dataRun2_v32 --step NANO --nThreads 1 --era Run2_2017,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec
```

MC (UL18, MiniAODv1):

```bash
cmsDriver.py mc2018 -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_upgrade2018_realistic_v15_L1v1 --step NANO --nThreads 1 --era Run2_2018,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (UL18, MiniAODv1):

```bash
cmsDriver.py data2018abc -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 106X_dataRun2_v32 --step NANO --nThreads 1 --era Run2_2018,run2_nanoAOD_106Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec
```


**Step 2**: use the `crab.py` script to submit the CRAB jobs:

For MC:

`python crab.py -p mc_NANO.py --site T2_CH_CERN -o /store/user/$USER/outputdir -t NanoTuples-[version] -i mc.txt --num-cores 1 --send-external -s FileBased -n 2 --work-area crab_projects_mc --dryrun`

For data:

`python crab.py -p data_NANO.py --site T2_CH_CERN -o /store/user/$USER/outputdir -t NanoTuples-[version] -i data.txt --num-cores 1 --send-external -s EventAwareLumiBased -n 100000 -j [json_file] --work-area crab_projects_data --dryrun`


A JSON file can be applied for data samples with the `-j` options.

Golden JSON, 2016:

```
https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt
```

Golden JSON, 2017:

```
https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt
```

Golden JSON, 2018:

```
https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt
```

These command will perform a "dryrun" to print out the CRAB configuration files. Please check everything is correct (e.g., the output path, version number, requested number of cores, etc.) before submitting the actual jobs. To actually submit the jobs to CRAB, just remove the `--dryrun` option at the end.

**Step 3**: check job status

The status of the CRAB jobs can be checked with:

```bash
./crab.py --status --work-area crab_projects_*  --options "maxjobruntime=2500 maxmemory=2500" && ./crab.py --summary
```

Note that this will also **resubmit** failed jobs automatically.

The crab dashboard can also be used to get a quick overview of the job status:

- [https://monit-grafana.cern.ch/d/cmsTMGlobal/cms-tasks-monitoring-globalview?orgId=11](https://monit-grafana.cern.ch/d/cmsTMGlobal/cms-tasks-monitoring-globalview?orgId=11)

More options of this `crab.py` script can be found with:

```bash
./crab.py -h
```

-->
