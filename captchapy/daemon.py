#!/usr/bin/env python

import time
import sys
import os

time.sleep(int(sys.argv[2]))

os.remove(sys.argv[1])