#!/usr/bin/env python3
"""Text to speech clip board player based on cepstral swift application.

Dependencies: padsp, swift, xsel
"""

__version__ = 1.0
__date__ = '2014-10-26'
__author__ = 'Konstantin Itskov <konstantin.itskov@kovits.com>'

import subprocess
import re

rate = 1.1
x_weak = r'[,]'
weak = r'[.:;!•—]'
skip = r'[_-]'


def main():
    """Parse the string recorded in xsel and text to speech it through swift."""
    try:
        pid = subprocess.check_output(["pgrep", "swift"])
    except Exception:
        pid = None

    if pid:
        pid = int(pid)
        subprocess.check_call(["kill", str(pid)])
    else:
        text = subprocess.check_output(["xsel"])
        text = text.decode('utf-8')
        ptn = re.compile(x_weak)
        text = re.sub(ptn, '<break strength="x-weak"/>', text)
        ptn = re.compile(weak)
        text = re.sub(ptn, '<break strength="weak"/>', text)
        ptn = re.compile(skip)
        text = re.sub(ptn, ' ', text)
        text = '<prosody rate="' + str(rate) + '">' + text + '</prosody>'
        print(text)
        cmd = "padsp swift -e \"utf-8\" " + text
        subprocess.Popen(cmd.split())

if __name__ == '__main__':
    main()
