import FWCore.ParameterSet.Config as cms

# command line options parsing
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing('python')
options.register('opticstag', "PPSOpticalFunctions_test",
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "optics tag, i.e. PPSOpticalFunctions_test"
                 )
options.register('opticssource', "nonDB",
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "optics source (DB locations like 'frontier://FrontierProd/CMS_CONDITIONS'\n" +
                 "   'sqlite_file:/afs/cern.ch/user/w/wcarvalh/public/CTPPS/optical_functions/PPSOpticalFunctions_2025_v1.db')\n" +
                 "  or 'nonDB' which reads optics source as ROOT files from CMSSW"
                 )
options.register('runnumber', 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "run number"
                 )
options.register('xangle', 150.,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.float,
                 "crossing angle value [urad], i.e. 160."
                 )
options.parseArguments()

process = cms.Process('CTPPSOpticsTests')

# minimal logger settings
process.MessageLogger = cms.Service(
    "MessageLogger",
    statistics=cms.untracked.vstring(),
    destinations=cms.untracked.vstring('cout'),
    cout=cms.untracked.PSet(threshold=cms.untracked.string('INFO'))
)

# single event as we inspect only event setup data
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(int(1)))

# empty source, run no 1 corresponds to MC
process.source = cms.Source(
    "EmptyIOVSource",
    timetype=cms.string("runnumber"),
    firstValue=cms.uint64(options.runnumber),
    lastValue=cms.uint64(options.runnumber),
    interval=cms.uint64(1)
)

# some dummy particle generator
process.HepPDTESSource = cms.ESSource(
    "HepPDTESSource",
    pdtFileName=cms.FileInPath('SimGeneral/HepPDTESSource/data/pythiaparticle.tbl'))
process.RandomNumberGeneratorService = cms.Service(
    "RandomNumberGeneratorService",
    sourceSeed=cms.PSet(initialSeed=cms.untracked.uint32(98765)),
    generator=cms.PSet(initialSeed=cms.untracked.uint32(98766)),
)
process.load("Configuration.Generator.randomXiThetaGunProducer_cfi")

# generate LHCInfo record (xangle, energy, etc)
# see https://github.com/cms-sw/cmssw/blob/CMSSW_15_1_X/CalibPPS/ESProducers/plugins/CTPPSLHCInfoESSource.cc
# TODO consider using https://github.com/cms-sw/cmssw/blob/CMSSW_15_1_X/CalibPPS/ESProducers/plugins/CTPPSLHCInfoRandomXangleESSource.cc
process.ctppsESSourceLHCInfo = cms.ESSource(
    "CTPPSLHCInfoESSource",
    label=cms.string(""),
    validityRange=cms.EventRange("0:min - {:d}:max".format(options.runnumber)),
    beamEnergy=cms.double(7000),  # GeV
    xangle=cms.double(options.xangle)  # murad
)

if options.opticssource == 'nonDB':
    # extract CTPPS optics from ROOT files

    # see https://github.com/cms-sw/cmssw/blob/CMSSW_15_1_X/CalibPPS/ESProducers/python/ctppsOpticalFunctions_non_DB_cff.py
    from CalibPPS.ESProducers.ctppsOpticalFunctions_non_DB_cff import optics_2022

    # see https://github.com/cms-sw/cmssw/blob/CMSSW_15_1_X/CalibPPS/ESProducers/plugins/CTPPSOpticalFunctionsESSource.cc
    process.ppsESSourceOptics = cms.ESSource(
        "CTPPSOpticalFunctionsESSource",
        configuration=cms.VPSet(optics_2022)
    )

else:
    # extract CTPPS optics record from CondDB or local SQlite file
    process.ppsESSourceOptics = cms.ESSource(
        "PoolDBESSource",
        connect=cms.string(options.opticssource),
        DumpStat=cms.untracked.bool(True),
        toGet=cms.VPSet(
            cms.PSet(
                record=cms.string('CTPPSOpticsRcd'),
                tag=cms.string(options.opticstag)
            )
        )
    )

# transforms LHCOpticalFunctionsSetCollection into LHCInterpolatedOpticalFunctionsSetCollection based on xangle extracted from LHCInfo record
# see https://github.com/cms-sw/cmssw/blob/CMSSW_15_1_X/CalibPPS/ESProducers/plugins/CTPPSInterpolatedOpticalFunctionsESSource.cc
process.ctppsInterpolatedOpticalFunctionsESSource = cms.ESProducer(
    "CTPPSInterpolatedOpticalFunctionsESSource",
    lhcInfoLabel=cms.string(""),
    opticsLabel=cms.string(""),
    appendToDataLabel=cms.string("")
)

# LHCInfo plotter
# see https://github.com/cms-sw/cmssw/blob/CMSSW_15_1_X/Validation/CTPPS/plugins/CTPPSLHCInfoPlotter.cc
process.ctppsLHCInfoPlotter = cms.EDAnalyzer(
    "CTPPSLHCInfoPlotter",
    lhcInfoLabel=cms.string(""),
    outputFile=cms.string("lhcinfo_{run_number:d}_{xangle:4.3f}.root".format(
        run_number=options.runnumber, xangle=options.xangle))
)

# optics plotter, needs LHCInterpolatedOpticalFunctionsSetCollection produced by CTPPSInterpolatedOpticalFunctionsESSource
# see https://github.com/cms-sw/cmssw/blob/CMSSW_15_1_X/Validation/CTPPS/plugins/CTPPSOpticsPlotter.cc
out_file_opt_source = 'DB'
if options.opticssource == "nonDB":
    out_file_opt_source = 'nonDB'
process.ctppsOpticsPlotter = cms.EDAnalyzer(
    "CTPPSOpticsPlotter",
    opticsLabel=cms.string(""),
    rpId_45_F=cms.uint32(23),
    rpId_45_N=cms.uint32(3),
    rpId_56_F=cms.uint32(123),
    rpId_56_N=cms.uint32(103),
    outputFile=cms.string(
        "optics_{opt_source:s}_{run_number:d}_{xangle:4.3f}.root".format(
            opt_source=out_file_opt_source,
            run_number=options.runnumber,
            xangle=options.xangle)
    )
)

# processing path
process.p = cms.Path(
    process.generator
    * process.ctppsLHCInfoPlotter
    * process.ctppsOpticsPlotter
)
