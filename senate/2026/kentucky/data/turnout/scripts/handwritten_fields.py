#!/usr/bin/env python3
"""Bounded visual historical transcription; uncertain glyphs stay null, no arithmetic repair."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];hier=json.load(open(R/'extracts/historical-handwritten-hierarchy.json'));out=[]
spec={
'Estill':[
 ('president','Donald J. TRUMP / Michael R. PENCE',[793,3435,4228,'23?4','?83',258,234,172,47,139,134,146,2]+[None]*6+[5100]),
 ('president','Joseph R. BIDEN / Kamala D. HARRIS',[666,579,1245,419,111,47,34,30,11,9,10,16,1]+[None]*6+[1355]),
 ('president','Jo JORGENSEN / Jeremy Spike COHEN',[15,40,55,28,11,1,1,2,0,1,2,3,None]+[None]*6+[64]),
 ('president','Kanye WEST / Michelle TIDBALL',[4,10,14,7,1,2,0,2,0,0,0,0,None]+[None]*6+[16]),
 ('president','Brock PIERCE / Karla BALLARD',[0,3,3,0,2,1,0,0,0,0,0,0,None]+[None]*6+[3]),
 ('senate','Mitch McCONNELL',[770,3228,3998,'22?7',723,238,'2?4',161,38,127,121,134,3]+[None]*6+[4783]),
 ('senate','Amy McGRATH',[683,689,1372,480,147,62,46,34,14,11,21,17,1]+[None]*6+[1515]),
 ('senate','Brad BARRON',[33,142,175,101,35,6,19,11,16,10,4,14,None]+[None]*6+[239])],
'Lyon':[
 ('president','Donald J. TRUMP / Michael R. PENCE',[295,2271,None,0,166,None,None,195,None,None,172,None,None,None,None]+[None]*12+[3100]),
 ('president','Joseph R. BIDEN / Kamala D. HARRIS',['4?1',564,None,0,18,None,None,46,None,None,33,None,None,None,None]+[None]*12+['10?2']),
 ('president','Jo JORGENSEN / Jeremy Spike COHEN',[6,10,None,0,4,None,None,4,None,None,1,None,None,None,None]+[None]*12+[25]),
 ('president','Kanye WEST / Michelle TIDBALL',[4,3,None,0,0,None,None,0,None,None,0,None,None,None,None]+[None]*12+[7]),
 ('president','Brock PIERCE / Karla BALLARD',[2,2,None,0,0,None,None,0,None,None,0,None,None,None,None]+[None]*12+[4]),
 ('senate','Mitch McCONNELL',[292,2128,None,0,147,None,None,170,None,None,146,None,None,None,None]+[None]*12+['288?']),
 ('senate','Amy McGRATH',['43?',640,None,0,26,None,None,60,None,None,47,None,None,None,None]+[None]*12+[1204]),
 ('senate','Brad BARRON',[16,79,None,0,16,None,None,15,None,None,15,None,None,None,None]+[None]*12+[141])]
}
for h in hier:
 for row,(contest,candidate,vals) in enumerate(spec[h['county']],1):
  assert len(vals)==len(h['columns']),(h['county'],len(vals),len(h['columns']))
  for i,(col,v) in enumerate(zip(h['columns'],vals),1):
   out.append({'county':h['county'],'year':2020,'contest':contest,'candidate_source_display':candidate,'source_sha256':h['source_sha256'],'page':1,'row_in_selected_contests':row,'column':i,'column_label':col,'value':v if isinstance(v,int) else None,'raw_visual_transcription':str(v) if v is not None else None,'null_status':'explicit_handwritten_integer' if isinstance(v,int) else 'ambiguous_handwriting' if v is not None else 'unfilled_source_cell','arithmetic_use':False,'warning':'Manual uncertain historical image transcription; overlapping absentee/early columns. Not a statewide priority input.'})
(R/'extracts/historical-handwritten-fields.json').write_text(json.dumps(out,indent=2)+'\n')
