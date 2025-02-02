# SPDX-FileCopyrightText: 2020 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# SPDX-License-Identifier: Apache-2.0

import os
import re
import subprocess
from pathlib import Path


class logger:
    def __init__(self, log, target_path, dont_compress=False):
        self.log = log
        self.target_path = target_path
        self.dont_compress = dont_compress
        self.internal_log = ""

    def switch_log(self, log):
        self.log = log

    def print_control(self, message):
        if re.search(r'{{(\w+)}}(.*)', str(message)):
            self.internal_log += message
            print(str(message), flush=True)
            message = str(message).split("}}")[1]
        try:
            f = open(self.log, 'a')
            f.write(str(message) + '\n')
            f.close()
        except OSError:
            print("{{ERROR}} unable to print notification.")
            self.exit_control(255)

    def create_full_log(self):
        try:
            path = Path(self.log)
            directory = path.parent
            if not os.path.exists(directory):
                os.mkdir(directory)
            f = open(self.log, 'w+')
            f.write("FULL RUN LOG:\n")
            f.close()
        except OSError:
            print("{{ERROR}} unable to create log file.")
            self.exit_control(255)

    def dump_full_log(self):
        print("Full log could be found at %s" % str(self.log), flush=True)

    def exit_control(self, code):
        self.dump_full_log()
        if not self.dont_compress:
            print("{{PROGRESS}} Compressing the gds files")
            # Compress project items.
            run_prep_cmd = "cd {target_path}; make compress;".format(target_path=self.target_path)
            process = subprocess.Popen(run_prep_cmd, stdout=subprocess.PIPE, shell=True)
            process.communicate()[0].strip()
        else:
            print("{{WARNING}} Compression Skipped!")

        exit(code)

def paths_checker(list_of_paths):
    failed = False
    errors = []
    warnings = []
    for apath in list_of_paths:
        if not Path(apath).exists():
            failed = True
            errors.append("%s Does not exist"%apath)
    return failed, errors, warnings
