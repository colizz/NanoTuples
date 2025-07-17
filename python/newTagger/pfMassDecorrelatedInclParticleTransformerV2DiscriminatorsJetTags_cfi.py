import FWCore.ParameterSet.Config as cms

pfMassDecorrelatedInclParticleTransformerV2DiscriminatorsJetTags = cms.EDProducer(
   'BTagProbabilityToDiscriminator',
   discriminators = cms.VPSet(
      )
   )
