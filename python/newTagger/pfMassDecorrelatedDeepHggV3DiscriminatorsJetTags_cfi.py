import FWCore.ParameterSet.Config as cms

pfMassDecorrelatedDeepHggV3DiscriminatorsJetTags = cms.EDProducer(
   'BTagProbabilityToDiscriminator',
   discriminators = cms.VPSet(
      cms.PSet(
         name = cms.string('probHggvsQCD'),
         numerator = cms.VInputTag(
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probHaa'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probHaa'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probQCDbb'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probQCDcc'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probQCDb'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probQCDc'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probQCD_others'),
            ),
         ),
      cms.PSet(
         name = cms.string('probHggvsgamQCD'),
         numerator = cms.VInputTag(
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probHaa'),

            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probHaa'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probP'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probNP'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probPP'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probPNP'),
            cms.InputTag('pfMassDecorrelatedDeepHggV3JetTags', 'probNPNP'),
            ),
         ),
      )
   )
