"""Finite public constructor expansion: 3 contests x 64 published parish keys x 2 native resources + 3 statewide race controls. No current vote requests."""
import concurrent.futures,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent
jobs=[]
for y,d,r in [('2024','20241105','67190'),('2022','20221108','61897'),('2020','20201103','59569')]:
 jobs.append((f'{y}-StatsRace',f'{d}/StatsRace/Stats_{r}.htm'))
 for p in range(1,65):
  for k,stem in [('VotesRaceByPrecinct','Votes'),('StatsRaceParish','Stats')]:
   jobs.append((f'{y}-{k}-{p:02}',f'{d}/{k}/{stem}_{r}_{p:02}.htm'))
def run(j):
 name,blob=j
 return subprocess.run([sys.executable,'-B',str(D/'acquire.py'),name,'https://voterportal.sos.la.gov/ElectionResults/ElectionResults/Data?blob='+blob],capture_output=True,text=True).stdout.strip()
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
 for r in e.map(run,jobs): print(r,flush=True)
