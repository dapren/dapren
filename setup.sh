#!/bin/bash
###############################################################################
# This script will create required shell variables and directores
###############################################################################
# Get directory of setup.sh
DAPREN_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function setup_shell_variables(){
  # Setup DAPREN_HOME in .bashrc file
  echo "[INFO] Setting \${DAPREN_HOME} to '${DAPREN_HOME}' in ${HOME}/.bashrc"
  cat ${HOME}/.bashrc | grep -v 'export DAPREN_HOME=' > ${HOME}/.bashrc_dapren_copy
  echo "export DAPREN_HOME=\"${DAPREN_HOME}\"" >> ${HOME}/.bashrc_dapren_copy
  cp ${HOME}/.bashrc_dapren_copy ${HOME}/.bashrc
}

###############################################################################
# Main
###############################################################################
setup_shell_variables