__author__ = 'dapren'

from __future__ import print_function
import constants
import subprocess


def runbash(cmd, **kwargs):
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


if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout,
                        level=constants.APPLICATION_LOG_LEVEL)

    if runbash(
        cmd="ls",
        stdout="/tmp/output.txt",
        stdin="/tmp/errror.txt",
        stdout_file_mode="w"
    )['return_code'] != 0:
        raise RuntimeError("Bash cmds are not executing")

    if runbash(cmd="ls")['return_code'] != 0:
        raise RuntimeError("Bash cmds are not executing")

