#!/usr/bin/env python3
"""Optional lossless whole oldpath reconstruction into an explicit temporary destination only."""
import argparse
from pathlib import Path
from captured_core import Capture,STATE,sha
p=argparse.ArgumentParser();p.add_argument('capture',choices=['own-pre-resume','peer-final']);p.add_argument('--to',required=True);a=p.parse_args();d=Path(a.to).resolve();assert str(d).startswith(('/private/tmp/','/tmp/')) and not d.is_relative_to(STATE.resolve());d.mkdir(parents=True,exist_ok=False);c=Capture(a.capture)
for oldpath,z in c.entries.items():
 target=d/oldpath;target.parent.mkdir(parents=True,exist_ok=True);b=c.body(oldpath);target.write_bytes(b);assert sha(target.read_bytes())==z['sha256']
print('Exact whole oldpaths reconstructed',len(c.entries))
