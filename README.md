# NanoTuples

Custom NanoAOD ntuple producers with additional boosted jet taggers.

This branch provides a recipe for integrating a self-trained tagger into the MiniAODv6-NanoAODv15 workflow.

The code is compatible with CMSSW_15_0_X.

<!-- TOC -->

- [NanoTuples](#nanotuples)
    - [Version](#version)
    - [Setup](#setup)
        - [Set up CMSSW](#set-up-cmssw)
        - [Get customized NanoAOD producers](#get-customized-nanoaod-producers)
        - [Download the models](#download-the-models)
        - [Compile](#compile)
        - [Test](#test)
        - [Model configuration (optional)](#model-configuration-optional)
        - [Adding new models (optional)](#adding-new-models-optional)
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
git clone https://github.com/colizz/NanoTuples.git PhysicsTools/NanoTuples -b release/nanov15
```

### Download the models

```bash
# Model paths to download
models=(
    "InclParticleTransformer-MD/ak8/V01/model.onnx"                     # GloParT v1
    "InclParticleTransformer-MD/ak8/V02-HidLayer/model_embed.onnx"      # GloParT v2 (exposing hidden-layer)
    "InclParticleTransformer-MD/ak8/V03/model.onnx"                     # GloParT v3 (the cmssw version)
    "InclParticleTransformer-MD/ak8/V03FullScore/model_full_score.onnx" # GloParT v3 (the full-score version, w/ hidden layer)
    "InclParticleTransformer-MD/ak15/V02/model.onnx"                    # GloParT v2 for AK15 jets
)

for path in "${models[@]}"; do
  wget "https://coli.web.cern.ch/coli/repo/NanoTuples_data/$path" -O "$CMSSW_BASE/src/PhysicsTools/NanoTuples/data/$path" --quiet --show-progress
done
```

### Compile

```bash
scram b -j8
```

### Test

Test commands

MC (Summer24, MiniAODv6):

```bash
cmsDriver.py  --python_filename test_nanoTuples_mc2024.py --eventcontent NANOAODSIM --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --datatier NANOAODSIM --fileout file:nano_mc2024.root --conditions 150X_mcRun3_2024_realistic_v2 --step NANO --scenario pp --filein /store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-800to1000_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/120000/1b7182ab-2d1d-4c1f-96bf-930e464d0ac7.root --era Run3_2024 --mc -n 10
```

Data (Summer24, MiniAODv6):

```bash
cmsDriver.py --python_filename test_nanoTuples_data2024.py --eventcontent NANOAOD --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --datatier NANOAOD --fileout file:nano_data2024.root --conditions 150X_dataRun3_v2 --step NANO --scenario pp --filein /store/data/Run2024C/JetMET1/MINIAOD/MINIv6NANOv15-v1/2530000/f91e593e-2d71-4e88-91cb-116eb66cb80d.root --era Run3_2024 --data -n 10
```

**Note for running from earlier MiniAODs**

This nanoTuples release supports taking earlier MiniAODs (v2 for the Run 2 UL dataset or v4 for the early Run 3 dataset) as inputs and running reMINO-NANO workflows. You only need to add the above `--customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customize(MC|data)` on top of the standard cmsDriver configuration. However, note that in this case you need to add two lines after the line `process = nanoAOD_customizeCommon(process)` in the generated configuration.
```
process.packedpuppi.useExistingWeights = cms.bool(False)
process.packedpuppiNoLep.useExistingWeights = cms.bool(False)
```
TODO: hope to fix this issue later.

### Model configuration (optional)

To configure which models are run and which outputs are saved in NanoAOD, edit `python/nanoTuples_cff.py`:
- Add new models to the `customAK8Taggers` and (if `addAK15=True`) `customAK15Taggers` lists.
- Use `keepBranchMap` to specify which model output scores should be stored in the NanoAOD files.

### Adding new models (optional)

- Place your model directory (containing the ONNX and JSON files) under `data/`. The directory should include:
  - The model file in `.onnx` format.
  - A pre-processing JSON file, which is required by CMSSW's `boostedJetONNXJetTagsProducer` module to correctly run the model inference.
- Add the model's cff file in `python/newTagger/`, which defines the inference module:  
  - Includes **"TagInfos"** (to acquire input variables for inference) and **"JetTags"** (the inference module).  
- Integrate the **"TagInfos"** and **"JetTags"** modules for the new model into `python/newTagger/jetTools.py` and `python/newTagger/bTaggingCustomUtils.py`.  
- Modify `python/nanoTuples_cff.py` to enable the additional tagger inference using the **"updateJetCollection"** utility and specify the scores to store in NanoAOD.

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
