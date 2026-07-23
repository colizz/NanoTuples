import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoTuples.ak15_cff import setupAK15
from PhysicsTools.NanoTuples.ak8_cff import addCustomTaggerAK8

_default_cfg = {
    'addAK15': False,
    'customAK8Taggers': ['GlobalParticleTransformerV3FullScore', 'GlobalParticleTransformerV3-Finetuned-DeepHggV2'],
    'customAK15Taggers': [],

    'keepBranchMap': {
        'GlobalParticleTransformerV2': [
            # default branches to store for GloParT2
            'probHbb', 'probHcc', 'probHss', 'probHqq', 'probHbc', 'probHbs', 'probHcs', 'probHgg', 'probHee', 'probHmm', 'probHtauhtaue', 'probHtauhtaum', 'probHtauhtauh', 
            'probTopbWcs', 'probTopbWqq', 'probTopbWc', 'probTopbWs', 'probTopbWq', 'probTopbWev', 'probTopbWmv', 'probTopbWtauev', 'probTopbWtaumv', 'probTopbWtauhv', 'probTopWcs', 'probTopWqq', 'probTopWev', 'probTopWmv', 'probTopWtauev', 'probTopWtaumv', 'probTopWtauhv', 
            'probQCDbb', 'probQCDcc', 'probQCDb', 'probQCDc', 'probQCDothers', 
            'resonanceMassCorr', 'visiableMassCorr',
        ],
        'GlobalParticleTransformerV2-AK15': [
            # default branches to store for GloParT2
            'probHbb', 'probHcc', 'probHss', 'probHqq', 'probHbc', 'probHbs', 'probHcs', 'probHgg', 'probHee', 'probHmm', 'probHtauhtaue', 'probHtauhtaum', 'probHtauhtauh', 
            'probTopbWcs', 'probTopbWqq', 'probTopbWc', 'probTopbWs', 'probTopbWq', 'probTopbWev', 'probTopbWmv', 'probTopbWtauev', 'probTopbWtaumv', 'probTopbWtauhv', 'probTopWcs', 'probTopWqq', 'probTopWev', 'probTopWmv', 'probTopWtauev', 'probTopWtaumv', 'probTopWtauhv', 
            'probQCDbb', 'probQCDcc', 'probQCDb', 'probQCDc', 'probQCDothers', 
            'resonanceMassCorr', 'visiableMassCorr',
        ],
        'GlobalParticleTransformerV3FullScore': [
            # default nanoAOD branches have included GloParT3's standard discriminants
            # modify the scores below to keep additional ones by inferring GloParT3's full-score model
            'probRawHbb', 'probRawHcc', 'probRawHss', 'probRawHqq', 'probRawHee', 'probRawHmm', 'probRawHaa',
            'massCorrRawHaa', 'massCorrRawQCDb', 'massCorrRawQCDbb', 'massCorrRawQCDc', 'massCorrRawQCDcc', 'massCorrRawQCDothers',
        ],

        # fine-tuned models
        'GlobalParticleTransformerV3-Finetuned-DeepHggV2': [
            'probHaa', 'probQCDbb', 'probQCDcc',
            'probQCDb', 'probQCDc', 'probQCDothers',
        ],
        'GlobalParticleTransformerV3-Finetuned-DeepHgg': [
            # GloParT fine-tuned for H->gamgam
            'probHaa', 'probP', 'probNP', 'probPP', 'probPNP', 'probNPNP', 'probQCDb', 'probQCDbb', 'probQCDc', 'probQCDcc', 'probQCDothers',
        ],
    }
}


def nanoTuples_customizeCommon(process, runOnMC,
                               addAK15=_default_cfg['addAK15'],
                               customAK8Taggers=_default_cfg['customAK8Taggers'],
                               customAK15Taggers=_default_cfg['customAK15Taggers'],
                               keepBranchMap=_default_cfg['keepBranchMap']):
    '''Customize the NanoTuples to include additional taggers for AK8/AK15 jets
       Options:
         - customAK8Taggers: available taggers are (refer to ak8_cff.py):
             ['DeepHWWV1', 'InclParticleTransformerV1', 'GlobalParticleTransformerV2', 'GlobalParticleTransformerV3FullScore']
         - customAK15Taggers (for akAK15=True): available taggers are (refer to ak15_cff.py):
             ['GlobalParticleTransformerV2-AK15']
         - keepBranchMap: dictionary with {tagger_name: branch_list}; for specified tagger_name, only keep branches in branch_list 
    '''

    if len(customAK8Taggers) > 0:
        addCustomTaggerAK8(process, customAK8Taggers=customAK8Taggers, keepBranchMap=keepBranchMap)
    if addAK15:
        setupAK15(process, runOnMC=runOnMC, customAK15Taggers=customAK15Taggers, keepBranchMap=keepBranchMap)

    # Keep exactly the events that will have at least one row in the FatJet
    # NanoAOD table.  fatJetTable reads finalJetsAK8, whose standard NanoAOD
    # selection is pt > 170 GeV.
    process.ak8JetEventFilter = cms.EDFilter(
        "CandViewCountFilter",
        src=cms.InputTag("finalJetsAK8"),
        minNumber=cms.uint32(1),
    )
    process.nanoAOD_step.insert(0, process.ak8JetEventFilter)

    # The output module is on a separate EndPath, so explicitly select events
    # that passed nanoAOD_step; otherwise rejected events would still be saved.
    for output_name in ("NANOAODoutput", "NANOAODSIMoutput"):
        if hasattr(process, output_name):
            getattr(process, output_name).SelectEvents = cms.untracked.PSet(
                SelectEvents=cms.vstring("nanoAOD_step")
            )

    return process


def nanoTuples_customizeData(process):
    process = nanoTuples_customizeCommon(process, runOnMC=False)
    return process


def nanoTuples_customizeMC(process):
    process = nanoTuples_customizeCommon(process, runOnMC=True)
    return process
