import FWCore.ParameterSet.Config as cms

pfMassDecorrelatedDeepHggV3DiscriminatorsJetTags = cms.EDProducer(
   'BTagProbabilityToDiscriminator',
   discriminators = cms.VPSet(
      cms.PSet(
         name = cms.string('probHggvsQCD'),
         numerator = cms.VInputTag(
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_Haa'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_Haa'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_QCD_bb'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_QCD_cc'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_QCD_b'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_QCD_c'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_QCD_others'),
            ),
         ),
      cms.PSet(
         name = cms.string('probHggvsgamQCD'),
         numerator = cms.VInputTag(
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_Haa'),

            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_Haa'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_P'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_NP'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_PP'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_PNP'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'label_NPNP'),
            ),
         ),
      )
   )
