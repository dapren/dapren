#!/bin/bash
###############################################################################
# This script refreshes the documentation in 'docs' folder. It will be run 
# manually and document changes will be pushed to version control
###############################################################################
cd ${DAPREN_HOME}/lib
pydoc -w `ls *.py | sed 's/.py$//'`
for file in `ls *.html`
do 
  html_file=`basename ${file}`
  cat ${html_file} | sed "s#/${USER}/#/dapren/#g" > ../docs/${html_file}
done
rm -rf *html *.pyc
