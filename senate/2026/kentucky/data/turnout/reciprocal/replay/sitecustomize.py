
import os,sys,json,pathlib
CFG=json.load(open(os.environ['KY_GUARD_CONFIG']));T=pathlib.Path(CFG['temporary_root']).resolve();S=pathlib.Path(CFG['real_state']).resolve();ALLOW={pathlib.Path(x).resolve() for x in CFG['original_read_paths']};SCRIPTS={pathlib.Path(x).resolve() for x in CFG['allowed_script_paths']}
def inside(p,root):
 try:return p.is_relative_to(root)
 except:return False
def path(x):
 if isinstance(x,(str,bytes,os.PathLike)):return pathlib.Path(os.fsdecode(x)).resolve()
 return None
def deny(reason):raise PermissionError('KY_EXERCISED_DENIAL:'+reason)
def writable(p):
 p=path(p)
 if p is not None and not inside(p,T):deny('writes outside isolated temporary root')
def guard(event,args):
 if event.startswith('socket.'):deny('network sockets/DNS')
 if event=='open':
  p=path(args[0]);mode=args[1];flags=args[2]
  writing=(isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)))
  if writing:writable(args[0])
  elif p is not None and inside(p,S) and not inside(p,T) and p not in ALLOW:deny('mutable producer/peer/news/coordinator read')
 if event in ('os.listdir','os.scandir'):
  p=path(args[0])
  if p is not None and inside(p,S) and not inside(p,T):deny('peer/producer discovery')
 if event in ('os.mkdir','os.remove','os.rmdir','os.unlink','os.truncate'):writable(args[0])
 if event in ('os.rename','os.replace'):writable(args[0]);writable(args[1])
 if event=='subprocess.Popen':
  cmd=args[1];cmd=list(cmd) if isinstance(cmd,(list,tuple)) else [cmd];exe=pathlib.Path(os.fsdecode(cmd[0])).name
  if exe in ['pdftotext','pdfinfo','pdftoppm']:
   for a in cmd[1:]:
    if isinstance(a,str) and '/' in a and not a.startswith('-'):
     p=path(a)
     if p is not None and not inside(p,T):deny('external tool path outside temporary root')
  elif exe.startswith('python'):
   if len(cmd)<2 or path(cmd[1]) not in SCRIPTS:deny('producer helper/writer execution')
  else:deny('unapproved subprocess/network helper')
sys.addaudithook(guard)
