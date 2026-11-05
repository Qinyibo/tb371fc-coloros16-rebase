import gzip,os,pathlib,stat,sys
r=pathlib.Path(sys.argv[1]); trial=pathlib.Path(sys.argv[2]);out=bytearray();ino=1
def add(name,mode,data=b'',uid=0,gid=0,major=0,minor=0):
 global ino
 n=name.encode()+b'\0';v=[ino,mode,uid,gid,1,0,len(data),0,0,major,minor,len(n),0];ino+=1
 out.extend(b'070701'+''.join(f'{x:08x}' for x in v).encode());out.extend(n);out.extend(b'\0'*(-len(out)%4));out.extend(data);out.extend(b'\0'*(-len(out)%4))
for d in ['dev','proc','sys','erofs']:add(d,0o40755)
add('dev/console',0o20600,major=5,minor=1);add('dev/null',0o20666,major=1,minor=3)
add('init',0o100755,(trial/'init').read_bytes())
root=r/'mounts/com.android.runtime'
def copy(p,name):
 s=p.lstat();data=p.read_bytes() if stat.S_ISREG(s.st_mode) else os.readlink(p).encode() if stat.S_ISLNK(s.st_mode) else b''
 add(name,s.st_mode,data,s.st_uid,s.st_gid)
copy(root,'reference')
for parent,dirs,files in os.walk(root,followlinks=False):
 for n in dirs+files:
  p=pathlib.Path(parent)/n;copy(p,'reference/'+str(p.relative_to(root)))
add('TRAILER!!!',0)
(trial/'initramfs.cpio.gz').write_bytes(gzip.compress(out,mtime=0))
