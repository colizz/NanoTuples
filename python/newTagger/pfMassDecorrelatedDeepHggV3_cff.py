import FWCore.ParameterSet.Config as cms

# use CustomDeepBoostedJetTagInfoProducer (to include recovered 4-vector)
from PhysicsTools.NanoTuples.pfParticleTransformerAK8TagInfos_cfi import pfParticleTransformerAK8TagInfos as pfParticleTransformerV2JetTagInfos
from RecoBTag.ONNXRuntime.boostedJetONNXJetTagsProducer_cfi import boostedJetONNXJetTagsProducer
from PhysicsTools.NanoTuples.newTagger.pfMassDecorrelatedDeepHggV3DiscriminatorsJetTags_cfi import pfMassDecorrelatedDeepHggV3DiscriminatorsJetTags

pfMassDecorrelatedDeepHggV3TagInfos = pfParticleTransformerV2JetTagInfos.clone(
    use_puppiP4 = False
)

pfMassDecorrelatedDeepHggV3JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfMassDecorrelatedDeepHggV3TagInfos',
    preprocess_json = 'PhysicsTools/NanoTuples/data/DeepHgg-MD/ak8/V03/preprocess.json',
    model_path = 'PhysicsTools/NanoTuples/data/DeepHgg-MD/ak8/V03/model_full_score.onnx',
    flav_names = [
        "probHaa", 
        "probP", "probNP", "probPP", "probPNP", "probNPNP", 
        "probQCDbb", "probQCDcc", "probQCDb", "probQCDc", "probQCDothers" # 11 cls
    ], 
    debugMode = False,
)

# declare all the discriminators
# probs
_pfMassDecorrelatedDeepHggV3JetTagsProbs = ['pfMassDecorrelatedDeepHggV3JetTags:' + flav_name
                                 for flav_name in pfMassDecorrelatedDeepHggV3JetTags.flav_names]
# meta-taggers
_pfMassDecorrelatedDeepHggV3JetTagsMetaDiscrs = ['pfMassDecorrelatedDeepHggV3DiscriminatorsJetTags:' + disc.name.value()
                                      for disc in pfMassDecorrelatedDeepHggV3DiscriminatorsJetTags.discriminators]

_pfMassDecorrelatedDeepHggV3JetTagsAll = _pfMassDecorrelatedDeepHggV3JetTagsProbs + _pfMassDecorrelatedDeepHggV3JetTagsMetaDiscrs
