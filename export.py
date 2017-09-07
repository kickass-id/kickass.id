#!/usr/bin/env python

import distutils.dir_util
import os
import shutil
import subprocess
import sys

if len(sys.argv) != 2:
    raise ValueError('Missing argument')

print('Generating artifacts...')
output = subprocess.check_output(['hugo'])
print(output)

target = '../live/kickass-id.github.io'
print('Clearing ' + target + '...')

# Check presence of CNAME file before deleting everything!
if not os.path.isfile(os.path.join(target, 'CNAME')):
    raise ValueError('Invalid target!')

for file in os.listdir(target):
    if not file.startswith('.') and not file == 'CNAME':
        path = os.path.join(target, file)

        print('Deleting ' + path)
        if os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

print('Copying generated artifacts...')
distutils.dir_util.copy_tree('public', target)

print('Pushing to server...')
os.chdir(target)
output = subprocess.check_output('git add img/* posts/*', shell=True)
print(output)
output = subprocess.check_output('git commit -a -m "%s"' % sys.argv[1], shell=True)
print(output)
output = subprocess.check_output('git push', shell=True)
print(output)
