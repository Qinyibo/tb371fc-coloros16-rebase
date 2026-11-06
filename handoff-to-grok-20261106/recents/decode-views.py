from pathlib import Path
import struct,zipfile,json,sys
class Decoder:
 def __init__(self,b):self.b=b;self.p=0
 def number(self,fmt):
  n=struct.calcsize(fmt);v=struct.unpack_from(fmt,self.b,self.p)[0];self.p+=n;return v
 def value(self):
  t=chr(self.b[self.p]);self.p+=1
  if t=='M':
   d={}
   while True:
    k=self.value()
    if k==0:break
    d[k]=self.value()
   return d
  if t=='R':
   n=self.number('>h');v=self.b[self.p:self.p+n].decode('utf-8',errors='replace');self.p+=n;return v
  if t=='Z':return bool(self.number('>B'))
  return self.number({'B':'>b','S':'>h','I':'>i','J':'>q','F':'>f','D':'>d'}[t])
def decode(b):
 if not b:return []
 d=Decoder(b);items=[]
 while d.p<len(b):items.append(d.value())
 names=items.pop()
 def conv(v):
  if isinstance(v,dict):return {names.get(k,str(k)):conv(x) for k,x in v.items()}
  return v
 return [conv(v) for v in items]
def fromzip(path):
 with zipfile.ZipFile(path) as z:return {n:decode(z.read(n)) for n in z.namelist()}
if __name__=='__main__':
 p=Path(sys.argv[1]);j=fromzip(p);p.with_suffix('.decoded.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('DECODED_WINDOWS',len(j))
