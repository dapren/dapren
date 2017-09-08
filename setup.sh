#!/bin/bash
###############################################################################
# This script will create required shell variables and directores
###############################################################################

# Get directory of setup.sh
DAPREN_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

###############################################################################
##################################################################### Functions 
function setup_shell_variables(){
  # Setup DAPREN_HOME in .bashrc file
  echo "[INFO] Setting \${DAPREN_HOME} to '${DAPREN_HOME}' in ${HOME}/.bashrc"

  cat ${HOME}/.bashrc \
    | egrep -v "(export DAPREN_HOME|export PYTHONPATH.*DAPREN_HOME|## Setup DAPREN variables)" \
    > ${HOME}/.bashrc_dapren_copy
  

  echo "## Setup DAPREN variables" >> ${HOME}/.bashrc_dapren_copy
  echo "export DAPREN_HOME=\"${DAPREN_HOME}\"" >> ${HOME}/.bashrc_dapren_copy
  echo "export PYTHONPATH=\"\${DAPREN_HOME}/lib:\${DAPREN_HOME}/xlib:\${PYTHONPATH}\" " >> ${HOME}/.bashrc_dapren_copy

  cp ${HOME}/.bashrc_dapren_copy ${HOME}/.bashrc
}


function install_required_python_packages(){
	for app in flask pgsql yahoo-finance
	do  
		echo "[INFO] Running command 'pip install ${app}'"
		pip install ${app}
	done 
}

###############################################################################
########################################################################## Main
setup_shell_variables
install_required_python_packages


