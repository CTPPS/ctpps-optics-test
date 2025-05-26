# CTPPS Optics Test

This repository contains tools for testing and validating CTPPS optics.

## Usage

The optics test can be run with data from three different sources:

1. **Directly from CondDB**:
```bash
cmsRun optics_test.py opticssource="frontier://FrontierProd/CMS_CONDITIONS" opticstag="PPSOpticalFunctions_prompt_v9" runnumber=391514 xangle=150
```

2. **From local SQLite file**:
```bash
cmsRun optics_test.py opticssource="sqlite_file:/afs/cern.ch/user/w/wcarvalh/public/CTPPS/optical_functions/PPSOpticalFunctions_2025_v1.db" opticstag="PPSOpticalFunctions_test" runnumber=391514 xangle=150
```

3. **From ROOT files** (as defined in `ctppsOpticalFunctions_non_DB_cff.py`):
```bash
cmsRun optics_test.py opticssource="nonDB" opticstag="PPSOpticalFunctions_test" xangle=150 runnumber=1
```

Alternatively, you can use the provided shell script `run_optics_test.sh`.

## Options for optics_test.py

The `optics_test.py` script accepts the following options:

- `opticstag`: The optics tag to use (e.g., "PPSOpticalFunctions_test")
  - Default: "PPSOpticalFunctions_test"

- `opticssource`: The source of optics data
  - Can be a CondDB , use "frontier://FrontierProd/CMS_CONDITIONS"
  - Can be a local SQLite file, use "sqlite_file:/path/to/file.db"
  - Can also be "nonDB" to read optics from ROOT files hardcoded in CMSSW
  - Default: "nonDB"

- `runnumber`: The run number to use
  - Default: 1

- `xangle`: Crossing angle value in μrad
  - Default: 150.0

## Output Files

The script generates two types of output files:

1. LHC Info: `lhcinfo_<run_number>_<xangle>.root`
2. Optics data: `optics_<source>_<run_number>_<xangle>.root`

Where `<source>` is either "DB" or "nonDB" depending on the optics data source used.