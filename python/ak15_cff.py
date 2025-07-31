import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.simplePATJetFlatTableProducer_cfi import simplePATJetFlatTableProducer
from PhysicsTools.NanoAOD.simpleGenJetFlatTableProducer_cfi import simpleGenJetFlatTableProducer

from PhysicsTools.NanoTuples.jetTools import updateJetCollection as updateJetCollectionCustom

from PhysicsTools.NanoTuples.jetUtils import addCustomJets


def setupAK15(process, runOnMC=False, path=None, customAK15Taggers=[], keepBranchMap={}):
    # cluster AK15Puppi jets
    addCustomJets(process, rParam=1.5, jetAlgo='ak15', minPt=150, runOnMC=runOnMC)

    bTagDiscriminators = []
    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']
    if len(customAK15Taggers) > 0:
        branchInfo = []
        for name in customAK15Taggers:
            keep_list = keepBranchMap.get(name, None)
            disc, bchinfo = getCustomTaggerDiscriminatorsAK15(name, keep_list)
            bTagDiscriminators += disc
            branchInfo += bchinfo

    updateJetCollectionCustom(
        process,
        jetSource=cms.InputTag('packedPatJetsAK15PFPuppiSoftDrop'),
        rParam=1.5,
        jetCorrections=('AK8PFPuppi', cms.vstring(JETCorrLevels), 'None'),
        btagDiscriminators=bTagDiscriminators if len(bTagDiscriminators) else ['None'],
        postfix='AK15WithCustomTagger',
    )

    # src
    srcJets = cms.InputTag('selectedUpdatedPatJetsAK15WithCustomTagger')

    # jetID
    process.tightJetIdAK15Puppi = cms.EDProducer("PatJetIDValueMapProducer",
        filterParams=cms.PSet(
            version=cms.string('RUN2ULPUPPI'),
            quality=cms.string('TIGHT'),
        ),
        src=srcJets
    )

    process.tightJetIdLepVetoAK15Puppi = cms.EDProducer("PatJetIDValueMapProducer",
        filterParams=cms.PSet(
            version=cms.string('RUN2ULPUPPI'),
            quality=cms.string('TIGHTLEPVETO'),
        ),
        src=srcJets
    )

    process.ak15WithUserData = cms.EDProducer("PATJetUserDataEmbedder",
        src=srcJets,
        userFloats=cms.PSet(),
        userInts=cms.PSet(
            tightId=cms.InputTag("tightJetIdAK15Puppi"),
            tightIdLepVeto=cms.InputTag("tightJetIdLepVetoAK15Puppi"),
        ),
    )

    process.ak15Table = simplePATJetFlatTableProducer.clone(
        src=cms.InputTag("ak15WithUserData"),
        name=cms.string("AK15Puppi"),
        cut=cms.string(""),
        doc=cms.string("ak15 puppi jets"),
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(False),  # this is the main table for the jets
        variables=cms.PSet(P4Vars,
            jetId=Var("userInt('tightId')*2+4*userInt('tightIdLepVeto')", int, doc="Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto"),
            area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            # nPFConstituents=Var("numberOfDaughters()", int, doc="Number of PF candidate constituents"),
            tau1=Var("userFloat('NjettinessAK15Puppi:tau1')", float, doc="Nsubjettiness (1 axis)", precision=10),
            tau2=Var("userFloat('NjettinessAK15Puppi:tau2')", float, doc="Nsubjettiness (2 axis)", precision=10),
            tau3=Var("userFloat('NjettinessAK15Puppi:tau3')", float, doc="Nsubjettiness (3 axis)", precision=10),
            msoftdrop=Var("groomedMass()", float, doc="Corrected soft drop mass with PUPPI", precision=10),
            nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
            subJetIdx1=Var("?nSubjetCollections()>0 && subjets().size()>0?subjets()[0].key():-1", int,
                 doc="index of first subjet"),
            subJetIdx2=Var("?nSubjetCollections()>0 && subjets().size()>1?subjets()[1].key():-1", int,
                 doc="index of second subjet"),
        )
    )
    process.ak15Table.variables.pt.precision = 10

    # add AK15 custom taggers
    if len(customAK15Taggers) > 0:
        for name, var_info in branchInfo:
            setattr(process.ak15Table.variables, name, var_info)

    process.ak15SubJetTable = simplePATJetFlatTableProducer.clone(
        src=cms.InputTag("selectedPatJetsAK15PFPuppiSoftDropPacked", "SubJets"),
        cut=cms.string(""),
        name=cms.string("AK15PuppiSubJet"),
        doc=cms.string("ak15 puppi subjets"),
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(False),  # this is the main table for the jets
        variables=cms.PSet(P4Vars,
            area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
        )
    )
    process.ak15SubJetTable.variables.pt.precision = 10

    process.ak15Task = cms.Task(
        process.tightJetIdAK15Puppi,
        process.tightJetIdLepVetoAK15Puppi,
        process.ak15WithUserData,
        process.ak15Table,
        process.ak15SubJetTable,
    )

    if runOnMC:
        process.genJetAK15Table = simpleGenJetFlatTableProducer.clone(
            src=cms.InputTag("ak15GenJetsNoNu"),
            cut=cms.string("pt > 100."),
            name=cms.string("GenJetAK15"),
            doc=cms.string("AK15 GenJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.genJetAK15Table.variables.pt.precision = 10

        process.genSubJetAK15Table = simpleGenJetFlatTableProducer.clone(
            src=cms.InputTag("ak15GenJetsNoNuSoftDrop", "SubJets"),
            cut=cms.string(""),
            name=cms.string("GenSubJetAK15"),
            doc=cms.string("AK15 Gen-SubJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.genSubJetAK15Table.variables.pt.precision = 10

        process.ak15Task.add(process.genJetAK15Table)
        process.ak15Task.add(process.genSubJetAK15Table)
        ###############################################

    if path is None:
        process.schedule.associate(process.ak15Task)
    else:
        getattr(process, path).associate(process.ak15Task)


def getCustomTaggerDiscriminatorsAK15(name, keep_list):
    customTaggersAvailableDict = {
        'GlobalParticleTransformerV2-AK15': {
            'cff_path': 'PhysicsTools.NanoTuples.newTagger.pfMassDecorrelatedInclParticleTransformerV2_cff',
            'disc_name': '_pfMassDecorrelatedInclParticleTransformerAK15V2JetTagsAll',
            'nano_branch_name': 'globalParT2',
        },
    }

    cfg = customTaggersAvailableDict[name]
    mod = __import__(cfg['cff_path'], globals(), locals(), [cfg['disc_name']])
    btagDiscriminators = getattr(mod, cfg['disc_name'])

    if keep_list is not None:
        btagDiscriminators = [prob for prob in btagDiscriminators if prob.split(':')[1] in keep_list]

    # variables to store in NanoAOD FatJet table
    branchInfo = []
    for prob in btagDiscriminators:
        name = cfg['nano_branch_name'] + '_' + prob.split(':')[1]
        branchInfo.append([name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1)])

    return btagDiscriminators, branchInfo
