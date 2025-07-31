import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var


def getCustomTaggerDiscriminatorsAK8(process, name, keep_list):
    customTaggersAvailableDict = {
        'DeepHWWV1': {  # ParticleNet-based HWW tagger (prior to GloParTv1)
            'cff_path': 'PhysicsTools.NanoTuples.newTagger.pfMassDecorrelatedDeepHWWV1_cff',
            'disc_name': '_pfMassDecorrelatedDeepHWWV1JetTagsAll',
            'nano_branch_name': 'deepHWWMDV1',
        },
        'InclParticleTransformerV1': {  # a.k.a. GloParTv1
            'cff_path': 'PhysicsTools.NanoTuples.newTagger.pfMassDecorrelatedInclParticleTransformerV1_cff',
            'disc_name': '_pfMassDecorrelatedInclParticleTransformerV1JetTagsAll',
            'nano_branch_name': 'inclParTMDV1',
        },
        'GlobalParticleTransformerV2': {
            'cff_path': 'PhysicsTools.NanoTuples.newTagger.pfMassDecorrelatedInclParticleTransformerV2_cff',
            'disc_name': '_pfMassDecorrelatedInclParticleTransformerV2HidLayerJetTagsAll',
            'nano_branch_name': 'globalParT2',
        },
        'GlobalParticleTransformerV3FullScore': {
            'cff_path': 'PhysicsTools.NanoTuples.newTagger.pfMassDecorrelatedInclParticleTransformerV3_cff',
            'disc_name': '_pfMassDecorrelatedInclParticleTransformerV3HidLayerJetTagsAll',
            'nano_branch_name': 'globalParT3',
        },

        'GlobalParticleTransformerV3-Finetuned-DeepHgg': {  # GloParT-3 fine-tuned for H->gamgam
            'cff_path': 'PhysicsTools.NanoTuples.newTagger.pfMassDecorrelatedDeepHggV3_cff',
            'disc_name': '_pfMassDecorrelatedDeepHggV3JetTagsProbs',
            'nano_branch_name': 'globalParT3_FinetunedDeepHgg',
        },

    }

    cfg = customTaggersAvailableDict[name]
    mod = __import__(cfg['cff_path'], globals(), locals(), [cfg['disc_name']])
    btagDiscriminators = getattr(mod, cfg['disc_name'])

    if keep_list is not None:
        btagDiscriminators = [prob for prob in btagDiscriminators if prob.split(':')[1] in keep_list]

    # add variables to NanoAOD FatJet table
    for prob in btagDiscriminators:
        name = cfg['nano_branch_name'] + '_' + prob.split(':')[1]
        setattr(process.fatJetTable.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    return btagDiscriminators


def addCustomTaggerAK8(process, customAK8Taggers=[], keepBranchMap={}):
    '''Add custom taggers to AK8 jets in NanoTuples.
       Options:
         - customAK8Taggers: list of tagger names to add.
         - keepBranchMap: dictionary with {tagger_name: branch_list}; for specified tagger_name, only keep branches in branch_list
    '''

    tag_discs = []
    for name in customAK8Taggers:
        keep_list = keepBranchMap.get(name, None)
        btagDiscriminators = getCustomTaggerDiscriminatorsAK8(process, name, keep_list)
        tag_discs.extend(btagDiscriminators)

    from PhysicsTools.NanoTuples.jetTools import updateJetCollection as updateJetCollectionCustom
    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']
    # inference the tagger score
    src = 'selectedUpdatedPatJetsAK8WithDeepInfo' if hasattr(
        process, 'selectedUpdatedPatJetsAK8WithDeepInfo') else 'slimmedJetsAK8'
    updateJetCollectionCustom(
        process,
        jetSource=cms.InputTag(src),
        rParam=0.8,
        jetCorrections=('AK8PFPuppi', cms.vstring(JETCorrLevels), 'None'),
        btagDiscriminators=tag_discs,
        postfix='AK8WithCustomTagger',
    )
    process.jetCorrFactorsAK8.src = "selectedUpdatedPatJetsAK8WithCustomTagger"
    process.updatedJetsAK8.jetSource = "selectedUpdatedPatJetsAK8WithCustomTagger"
