import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var

def nanoTuples_customizeCommon(process, runOnMC):
    from PhysicsTools.NanoTuples.jetTools import updateJetCollection as updateJetCollectionCustom
    from PhysicsTools.NanoTuples.hwwTagger.pfMassDecorrelatedInclParticleTransformerV3_cff import _pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTagsProbs
    _btagDiscriminators = _pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTagsProbs

    # run GloParT V03FullScore and add scores to btagging discriminators
    # note: this custom updateJetCollection function trick is borrowed from here: https://github.com/colizz/DNNTuples/tree/dev-Run3-hww
    updateJetCollectionCustom(
       process,
       jetSource = cms.InputTag('slimmedJetsAK8'),
       pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
       svSource = cms.InputTag('slimmedSecondaryVertices'),
       rParam = 0.8,
       jetCorrections = ('AK8PFPuppi', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
       btagDiscriminators = _btagDiscriminators,
       postfix='AK8WithDeepInfo',
       printWarning = False
    )
    process.jetCorrFactorsAK8.src="selectedUpdatedPatJetsAK8WithDeepInfo"
    process.updatedJetsAK8.jetSource="selectedUpdatedPatJetsAK8WithDeepInfo"

    # add variables to NanoAOD branches
    ## you may add more scores here. See score names in PhysicsTools/NanoTuples/python/hwwTagger/pfMassDecorrelatedInclParticleTransformerV3_cff.py
    process.fatJetTable.variables.globalParT3_Xbb = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawHbb')", float, doc="Mass-decorrelated GlobalParT-3 H->bb score.", precision=10)
    process.fatJetTable.variables.globalParT3_Xcc = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawHcc')", float, doc="Mass-decorrelated GlobalParT-3 H->cc score.", precision=10)
    process.fatJetTable.variables.globalParT3_Xss = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawHss')", float, doc="Mass-decorrelated GlobalParT-3 H->ss score.", precision=10)
    process.fatJetTable.variables.globalParT3_Xqq = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawHqq')", float, doc="Mass-decorrelated GlobalParT-3 H->qq score.", precision=10)
    process.fatJetTable.variables.globalParT3_Xee = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawHee')", float, doc="Mass-decorrelated GlobalParT-3 H->ee score.", precision=10)
    process.fatJetTable.variables.globalParT3_Xmm = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawHmm')", float, doc="Mass-decorrelated GlobalParT-3 H->mu mu score.", precision=10)
    process.fatJetTable.variables.globalParT3_Xaa = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawHaa')", float, doc="Mass-decorrelated GlobalParT-3 H->gamma gamma score.", precision=10)
    process.fatJetTable.variables.globalParT3_QCDb = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawQCDb')", float, doc="Mass-decorrelated GlobalParT-3 QCD-b score.", precision=10)
    process.fatJetTable.variables.globalParT3_QCDbb = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawQCDbb')", float, doc="Mass-decorrelated GlobalParT-3 QCD-bb score.", precision=10)
    process.fatJetTable.variables.globalParT3_QCDc = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawQCDc')", float, doc="Mass-decorrelated GlobalParT-3 QCD-c score.", precision=10)
    process.fatJetTable.variables.globalParT3_QCDcc = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawQCDcc')", float, doc="Mass-decorrelated GlobalParT-3 QCD-cc score.", precision=10)
    process.fatJetTable.variables.globalParT3_QCDothers = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:probRawQCDothers')", float, doc="Mass-decorrelated GlobalParT-3 QCD-others score.", precision=10)
    ## mass regression
    process.fatJetTable.variables.globalParT3_massCorrGeneric = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:massCorrGeneric')", float, doc="GlobalParT-3 mass regression corrector with respect to the original jet mass, optimised for generic jet cases. Use (massCorrGeneric * mass * (1 - rawFactor)) to get the regressed mass", precision=10)
    process.fatJetTable.variables.globalParT3_massCorrXaa = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:massCorrRawHaa')", float, doc="GlobalParT-3 mass regression corrector with respect to the original jet mass, optimised for H->aa class", precision=10)
    process.fatJetTable.variables.globalParT3_massCorrQCDb = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:massCorrRawQCDb')", float, doc="GlobalParT-3 mass regression corrector with respect to the original jet mass, optimised for QCD-b class", precision=10)
    process.fatJetTable.variables.globalParT3_massCorrQCDbb = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:massCorrRawQCDbb')", float, doc="GlobalParT-3 mass regression corrector with respect to the original jet mass, optimised for QCD-bb class", precision=10)
    process.fatJetTable.variables.globalParT3_massCorrQCDc = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:massCorrRawQCDc')", float, doc="GlobalParT-3 mass regression corrector with respect to the original jet mass, optimised for QCD-c class", precision=10)
    process.fatJetTable.variables.globalParT3_massCorrQCDcc = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:massCorrRawQCDcc')", float, doc="GlobalParT-3 mass regression corrector with respect to the original jet mass, optimised for QCD-cc class", precision=10)
    process.fatJetTable.variables.globalParT3_massCorrQCDothers = Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:massCorrRawQCDothers')", float, doc="GlobalParT-3 mass regression corrector with respect to the original jet mass, optimised for QCD-others class", precision=10)
    ## also add all dim-256 hidden neurons
    for i in range(256):
        setattr(process.fatJetTable.variables, 'globalParT3_hidNeuron%s' % str(i).zfill(3), Var("bDiscriminator('pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTags:hidNeuron%s')" % str(i).zfill(3), float, doc="Mass-decorrelated GlobalParT-3 %d-th hidden-layer neuron." % i, precision=10))

    return process


def nanoTuples_customizeData(process):
    process = nanoTuples_customizeCommon(process, False)

    process.NANOAODoutput.fakeNameForCrab = cms.untracked.bool(True)  # hack for crab publication
    process.add_(cms.Service("InitRootHandlers", EnableIMT=cms.untracked.bool(False)))
    return process


def nanoTuples_customizeMC(process):
    process = nanoTuples_customizeCommon(process, True)

    process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)  # hack for crab publication
    process.add_(cms.Service("InitRootHandlers", EnableIMT=cms.untracked.bool(False)))
    return process
