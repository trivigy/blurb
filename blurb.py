#!/usr/bin/python
# coding=utf-8
"""Text to speech clip board player based on cepstral swift application.

Dependencies: padsp, swift, xsel
"""

import subprocess
import re
import sys

__version__ = 1.0
__date__ = '2014-10-26'
__author__ = 'Konstantin Itskov <konstantin.itskov@kovits.com>'

rate = 1.3
x_weak = r'[,"]'
weak = r'[.:;!•—]'
skip = r'[_-]'


def main():
    """Parse the string recorded in xsel and text to speech it through swift."""
    try:
        pid = subprocess.check_output(["pgrep", "swift"])
    except:
        pid = None

    if pid:
        pid = int(pid)
        subprocess.check_call(["kill", str(pid)])
    else:
        text = subprocess.check_output(["xsel", "--clipboard"])
        text = text.decode('utf-8')

        # Special Cases
        ptn = re.compile(r'[’]')
        text = re.sub(ptn, '\'', text)
        ptn = re.compile(r'[“”]')
        text = re.sub(ptn, '"', text)

        # Intonation and Pauses
        ptn = re.compile(x_weak)
        text = re.sub(ptn, '<break strength="x-weak"/>', text)
        ptn = re.compile(weak)
        text = re.sub(ptn, '<break strength="weak"/>', text)
        ptn = re.compile(skip)
        text = re.sub(ptn, ' ', text)

        # Globals
        text = '<prosody rate="' + str(rate) + '">' + text + '</prosody>'
        path = sys.path[0] + "/lexicon.txt"
        cmd = "padsp swift -l " + path + " -e \"utf-8\" " + text
        subprocess.Popen(cmd.split())


if __name__ == '__main__':
    main()
