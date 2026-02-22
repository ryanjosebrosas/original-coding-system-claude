#!/usr/bin/env python3
import subprocess, sys
b = subprocess.run(["git","rev-parse","--abbrev-ref","HEAD"], capture_output=True, text=True)
s = subprocess.run(["git","status","--short"], capture_output=True, text=True)
c = subprocess.run(["git","log","-10","--oneline"], capture_output=True, text=True)
print("BRANCH:", b.stdout.strip())
print("STATUS:", s.stdout.strip() or "clean")
print("COMMITS:"); [print("- "+x[:7]+" "+x[8:]) for x in c.stdout.strip().splitlines() if x]
