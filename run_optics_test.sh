#!/bin/bash

#cmsRun optics_test.py opticssource="frontier://FrontierProd/CMS_CONDITIONS" opticstag="PPSOpticalFunctions_2021_mc_v1" runnumber=343890 xangle=150

cmsRun optics_test.py opticssource="sqlite_file:/afs/cern.ch/user/w/wcarvalh/public/CTPPS/optical_functions/PPSOpticalFunctions_2016-2022.db" opticstag="PPSOpticalFunctions_test" runnumber=343891 xangle=150
cmsRun optics_test.py opticssource="nonDB" opticstag="PPSOpticalFunctions_test" xangle=150 runnumber=343891 
