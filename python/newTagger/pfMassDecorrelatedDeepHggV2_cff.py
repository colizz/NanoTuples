import FWCore.ParameterSet.Config as cms

# use CustomDeepBoostedJetTagInfoProducer (to include recovered 4-vector)
from PhysicsTools.NanoTuples.pfParticleTransformerAK8TagInfos_cfi import pfParticleTransformerAK8TagInfos as pfParticleTransformerV2JetTagInfos
from RecoBTag.ONNXRuntime.boostedJetONNXJetTagsProducer_cfi import boostedJetONNXJetTagsProducer

pfMassDecorrelatedDeepHggV2TagInfos = pfParticleTransformerV2JetTagInfos.clone(
    use_puppiP4 = False,
    move_electrons_to_neutral = True,
)

pfMassDecorrelatedDeepHggV2JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfMassDecorrelatedDeepHggV2TagInfos',
    preprocess_json = 'PhysicsTools/NanoTuples/data/DeepHgg-MD/ak8/V04/preprocess.json',
    model_path = 'PhysicsTools/NanoTuples/data/DeepHgg-MD/ak8/V04/model.onnx',
    flav_names = [
        "probHaa", "probQCDbb", "probQCDcc",
        "probQCDb", "probQCDc", "probQCDothers",
    ],
    debugMode = False,
)

# declare all the discriminators
# probs
_pfMassDecorrelatedDeepHggV2JetTagsProbs = ['pfMassDecorrelatedDeepHggV2JetTags:' + flav_name
                                 for flav_name in pfMassDecorrelatedDeepHggV2JetTags.flav_names]
_pfMassDecorrelatedDeepHggV2JetTagsAll = _pfMassDecorrelatedDeepHggV2JetTagsProbs
