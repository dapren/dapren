"""
This module provides a standard way of executing bash commands from a python
script. This is the preferred way of executing bash command.

Usage Example 1
# STANDALONE SCRIPT - execute and see it for yourself ##########################
# Run bash command that outputs to stdout and stderr. The stdout and stderr
# streams are returned as list.
from __future__ import print_function

import bashops
bash_res = bashops.runbash("ls")  # bash_res will be dict containing 3 keys

# Get return code of the command, if not 0 then it means command failed
print (\"""
return_code={return_code}
type(return_code)={return_code_type}

stdout={stdout}
type(stdout)={stdout_type}

stderr={stderr}
type(stderr)={stderr_type}
\""".format(
    return_code=bash_res['return_code'],
    return_code_type=type(bash_res['return_code']),
    stdout=bash_res['stdout'],
    stdout_type=type(bash_res['stdout']),
    stderr=bash_res['stderr'],
    stderr_type=type(bash_res['stderr']))
)
###############################################################################

Usage Example 2
# STANDALONE SCRIPT - execute and see it for yourself ##########################
# Run bash command that outputs stdout and stderr to files.
from __future__ import print_function

import bashops
bash_res = bashops.runbash(
    "ls",
    stdout="/tmp/output.txt",
    stdin="/tmp/errror.txt",
    stdout_file_mode="w",  # you can also append to file using "a"
    stderr_file_mode="a"
)  # bash_res will be dict containing 1 keys

# Get return code of the command, if not 0 then it means command failed
print (\"""
return_code={return_code}
type(return_code)={return_code_type}

\""".format(
    return_code=bash_res['return_code'],
    return_code_type=type(bash_res['return_code']),)
)

# See the stdout loaded to file /tmp/output.txt
print ("Contents of file /tmp/output.txt")
fp = open("/tmp/output.txt","r")
for line in fp:
    print(line.strip())
###############################################################################

"""
from __future__ import print_function
from constants import logger
import subprocess
import constants


def runbash(cmd, **kwargs):
    """
    Execute bash command

    :param cmd: Bash command to execute

    :param kwargs: Expected keys:
    - 'stdout': Provide absolute filename if you want output of 'stdout' to a
    file. If not provided then defaults to subprocess.PIPE
    - 'stderr': Provide absolute filename if you want output of 'stderr' to a
    file.If not provided then defaults to subprocess.PIPE

    :return: Returns object of type 'dict' with key 'return_code' and optionally
    keys 'stdout'and 'stderr'. The value of these keys is list
    """
    provided_stdout = kwargs.get('stdout', subprocess.PIPE)
    provided_stderr = kwargs.get('stderr', subprocess.PIPE)

    out_dict = {}

    p = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Process stdout. stdout can be a file
    if provided_stdout == subprocess.PIPE:
        stdout_list = []
        for line in p.stdout.readlines():
            stdout_list.append(line)
        out_dict['stdout'] = stdout_list
    else:  # It is path to a file
        mode = kwargs.get("stdout_file_mode", "w")
        fp = open(provided_stdout, mode)
        for line in p.stdout.readlines():
            fp.write(line)
        fp.close()

    # Process stderr. stderr can be a file
    if provided_stderr == subprocess.PIPE:
        stderr_list = []
        for line in p.stderr.readlines():
            stderr_list.append(line)
        out_dict['stderr'] = stderr_list
    else:  # It is path to a file
        mode = kwargs.get("stderr_file_mode", "w")
        fp = open(provided_stderr, mode)
        for line in p.stderr.readlines():
            fp.write(line)
        fp.close()

    out_dict['return_code'] = p.wait()

    return out_dict


if __name__ == constants.str___main__:
    if runbash(
        cmd="ls",
        stdout="/tmp/output.txt",
        stdin="/tmp/errror.txt",
        stdout_file_mode="w"
    )['return_code'] != 0:
        raise RuntimeError("Bash cmds are not executing")

    if runbash(cmd="ls")['return_code'] != 0:
        raise RuntimeError("Bash cmds are not executing")

    logger.info("All tests run fine")