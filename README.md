# Cttps Optics Test

Create CMSSW enviroment:

```
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram project CMSSW CMSSW_12_2_0_pre1
cd CMSSW_12_2_0_pre1
cmsenv
```


Get the code:

```
git clone ssh://git@gitlab.cern.ch:7999/lgrzanka/cttps_optics_test.git
```

Run the tests:

```
cd cttps_optics_test
bash run_optics_test.sh
```