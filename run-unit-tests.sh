#!/bin/bash
###############################################################################
# This script runs all unit tests in lib folder
###############################################################################
cd ${DAPREN_HOME}/lib
for file in `ls -1 *.py | egrep -v "^(__init__.py|test.py)$"`
do 
  /usr/bin/python ${file} >> ${DAPREN_HOME}/var/logs/run_unit_tests.log 2>&1
  if [ $? -eq 0 ]; then
    echo "[INFO] Running Unit test of file ${file}: pass"
  else
    echo "[INFO] Running Unit test of file ${file}: FAILED"
    echo "[ERROR] Error Details are in file '${DAPREN_HOME}/var/logs/run_unit_tests.log'. Search for string 'AssertionError' in this file.'"
  fi 
done
echo "[INFO] Details are in file ${DAPREN_HOME}/var/logs/run_unit_tests.log'"
