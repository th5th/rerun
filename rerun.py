#!/usr/bin/python
#
# Rerun
#
# A Python module for batch configuration, compilation
# and execution of projects.
#
# Copyright 2013 Ed Willson <ed.willson24@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess

CONF_MARK = "###"

def write_config(f, conf):
    f.write("# Autogenerated config:" + os.linesep)
    for conf_item in conf:
        f.write(conf_item + os.linesep)

def process_files(inp_path, out_path, conf):
    """
    Scan inp_path for a ### mark and call write_config when found
    """
    with open(inp_path, 'r') as inp:
        with open(out_path, 'w') as out:
            for inp_line in inp:
                if inp_line.startswith(CONF_MARK):
                    # got insert marker
                    write_config(out, conf)
                else:
                    # just copy the line over
                    out.write(inp_line)

def rerun(inp_path, out_path, configs, cmds = []):
    """
    Produce the output Makefile and run for each of the provided configs.

    Configs should be a iterable of lines to insert into the definition file at
    inp_path. Cmds is a list of commands to be passed to subprocess.check_call.
    """
    for config in configs:
        process_files(inp_path, out_path, config)
        for cmd in cmds:
            subprocess.check_call(cmd)

if __name__ == "__main__":
    inp_path = os.path.join(os.getcwd(), "config.mk.def")
    out_path = os.path.join(os.getcwd(), "config.mk")
    configs = [[r"CFLAGS += -DFLAG1=\"first\" -DFLAG2=\"first2\""],
            [r"CFLAGS += -DFLAG1=\"second\" -DFLAG2=\"second2\""]]

    cmds = [["make", "clean"], ["make"], [os.path.join(os.getcwd(), "rerun_test")]]

    rerun(inp_path, out_path, configs, cmds)
