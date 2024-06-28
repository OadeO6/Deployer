#!/usr/bin/env python3
"""
A script used for changing the status of a build from pending to built
after a build
"""
from sys import argv, exit
from models.build import Build

if len(argv) != 3:
    exit(1)
_id = argv[1] # job namr can be eccesfrd using ${env.JOB_NAMR}  curr.....projectName
num = arg[2] # for build num env.BUILB_NUMBER or currentBuilb.number

# update database
try:
    Build.updateBuildStat({"id": _id, "build_num": num}, {"status": "get status from build"})
except Exception as e:
    raise 
