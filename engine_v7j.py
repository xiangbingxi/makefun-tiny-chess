import os,json
from http.client import HTTPConnection as Conn
V=[0,100,320,330,500,900,20000]
M=100000
L=160000
KN=(33,31,18,14,-14,-18,-31,-33)
KI=(1,-1,16,-16,15,17,-15,-17)
BI=(15,17,-15,-17)
RO=(1,-1,16,-16)
_s=1
def R():
 global _s; _s=(_s*6364136223846793005+1)&((1<<64)-1); return _s
ZP=[R() for _ in range(15*128)]; ZS=R(); ZC=[R() for _ in range(16)]; ZE=[R() for _ in range(8)]
def T(k,r,f):
 e=min(f,7-f)+min(r,7-r)
 if k==1: return [0,2,6,12,20,32,50,0][r]+(12 if f in (3,4) and r>2 else 0)
 if k==2: return 6*e-18
 if k==3: return 4*e-8
 if k==4: return 12 if r==6 else (4 if r==0 and f in (3,4) else 0)
 if k==5: return 2*e-6
 return 0
PS=[0]*(15*128)
for _t in range(1,6):
 for _q in range(128):
  if _q&136: continue
  _r=_q>>4; _f=_q&7
  PS[_t*128+_q]=V[_t]+T(_t,_r,_f); PS[(_t+8)*128+_q]=-(V[_t]+T(_t,7-_r,_f))
KM=[0]*64; KE=[0]*64
for _r in range(8):
 for _f in range(8):
  _c=min(_f,7-_f)+min(_r,7-_r)
  KM[_r*8+_f]=(18,24,8,0,0,8,24,18)[_f] if _r==0 else max(-40,-12*_r); KE[_r*8+_f]=8*_c-22
CK=[15]*128
CK[0]=13; CK[7]=14; CK[4]=12; CK[112]=7; CK[119]=11; CK[116]=3
bd=[0]*128; sd=0; cs=0; ep=-1; hm=0; kg=[4,116]
sc=0; np=0; ky=0; ud=[]
tt=[None]*(1<<18); TM=(1<<18)-1; kil=[[0,0] for _ in range(129)]
pl=[]; hi=set(); nn=0
class Abort(Exception): pass
def atk(q,y):
 if y==0:
  if not (q-15&136) and bd[q-15]==1: return 1
  if not (q-17&136) and bd[q-17]==1: return 1
 else:
  if not (q+15&136) and bd[q+15]==9: return 1
  if not (q+17&136) and bd[q+17]==9: return 1
 for d in KN:
  t=q+d
  if not (t&136) and bd[t]==(2|y<<3): return 1
 for i,d in enumerate(KI):
  t=q+d
  while not (t&136):
   p=bd[t]
   if p:
    if p==(5|y<<3) or (i<4 and p==(4|y<<3)) or (i>3 and p==(3|y<<3)) or (t==q+d and p==(6|y<<3)): return 1
    break
   t += d
 return 0
def gen(caps):
 moves=[]
 for sq in range(128):
  if sq&136: continue
  pc=bd[sq]
  if pc==0 or pc>>3!=sd: continue
  pt=pc&7
  if pt==1:
   step=16 if sd==0 else -16; rank=sq>>4; prom_rank=6 if sd==0 else 1; home_rank=1 if sd==0 else 6; fwd=sq+step
   if bd[fwd]==0:
    if rank==prom_rank:
     for promo in (5,4,3,2): moves.append(sq|fwd<<7|promo<<14)
    elif not caps:
     moves.append(sq|fwd<<7)
     if rank==home_rank and bd[fwd+step]==0: moves.append(sq|(fwd+step)<<7)
   for diag in (step-1,step+1):
    to=sq+diag
    if (to&136)!=0: continue
    tgt=bd[to]
    if tgt!=0 and tgt>>3!=sd:
     if rank==prom_rank:
      for promo in (5,4,3,2): moves.append(sq|to<<7|promo<<14)
     else: moves.append(sq|to<<7)
    elif to==ep: moves.append(sq|to<<7)
  elif pt==2 or pt==6:
   for step in (KN if pt==2 else KI):
    dest=sq+step
    if dest&136: continue
    occ=bd[dest]
    if occ==0:
     if caps==0: moves.append(sq|dest<<7)
    elif occ>>3!=sd: moves.append(sq|dest<<7)
   if pt==6 and caps==0:
    b=112*sd
    for t,k,e,s in ((6,1,(5,6),(4,5,6)),(2,2,(3,2,1),(4,3,2))):
     if cs&k*4**sd and all(bd[b+x]==0 for x in e) and all(atk(b+x,sd^1)==0 for x in s): moves.append(b+4|(b+t)<<7)
  else:
   for step in (BI if pt==3 else RO if pt==4 else KI):
    cur=sq+step
    while (cur&136)==0 and bd[cur]==0:
     if caps==0: moves.append(sq|cur<<7)
     cur+=step
    if (cur&136)==0 and bd[cur]!=0 and bd[cur]>>3!=sd: moves.append(sq|cur<<7)
 return moves
def mk(m):
 global sd,cs,ep,hm,ky,sc,np
 f=m&127; t=(m>>7)&127; z=m>>14; p=bd[f]; y=p&7; u=sd
 v=t; g=bd[t]
 if y==1 and t==ep and not g:
  v=t-16 if u==0 else t+16; g=bd[v]
 ud.append((m,g,v,cs,ep,hm,ky,sc,np))
 ky ^= ZP[p*128+f]; sc -= PS[p*128+f]; bd[f]=0
 if g:
  ky ^= ZP[g*128+v]; sc -= PS[g*128+v]; np -= V[g&7]
  bd[v]=0
 w=(z|u<<3) if z else p
 bd[t]=w; ky ^= ZP[w*128+t]; sc += PS[w*128+t]
 if z:
  np += V[z]-100
 if y==6:
  kg[u]=t
  if t-f==2 or f-t==2:
   rf=f+3 if t>f else f-4; rt=f+1 if t>f else f-1; rk=bd[rf]
   ky ^= ZP[rk*128+rf]; sc -= PS[rk*128+rf]; bd[rf]=0; bd[rt]=rk; ky ^= ZP[rk*128+rt]; sc += PS[rk*128+rt]
 ky ^= ZC[cs]; cs &= CK[f]&CK[t]; ky ^= ZC[cs]
 if ep>=0: ky ^= ZE[ep&7]
 ep=-1
 if y==1 and abs(t-f)==32:
  e=1|(u^1)<<3
  if ((t&7)>0 and bd[t-1]==e) or ((t&7)<7 and bd[t+1]==e):
   ep=(f+t)//2; ky ^= ZE[ep&7]
 hm=0 if (y==1 or g) else hm+1
 sd ^= 1; ky ^= ZS
 if atk(kg[u],sd):
  um(); return False
 return True
def um():
 global sd,cs,ep,hm,ky,sc,np
 m,g,v,oc,oe,oh,okey,oscore,onp=ud.pop()
 sd ^= 1
 f=m&127; t=(m>>7)&127; z=m>>14; u=sd; p=bd[t]; bd[t]=0
 if g: bd[v]=g
 if z: bd[f]=1|u<<3
 else: bd[f]=p
 if (p&7)==6:
  kg[u]=f
  if t-f==2: bd[f+3]=bd[f+1]; bd[f+1]=0
  elif f-t==2: bd[f-4]=bd[f-1]; bd[f-1]=0
 cs=oc; ep=oe; hm=oh; ky=okey; sc=oscore; np=onp
def evl():
 h=min(np,6400)
 u=kg[0]>>4<<3|kg[0]&7; v=(7-(kg[1]>>4))<<3|kg[1]&7
 c=sc+(KM[u]*h+KE[u]*(6400-h))//6400-(KM[v]*h+KE[v]*(6400-h))//6400
 c+=10-20*sd
 return c*(1-2*sd)
def rst():
 global bd,sd,cs,ep,hm,kg,sc,np,ky
 bd=[0]*128; kg=[4,116]; sc=0; np=0; ky=0
 back=(4,2,3,5,6,3,2,4)
 for f in range(8):
  for q,p in ((f,back[f]),(16+f,1),(112+f,back[f]|8),(96+f,9)):
   bd[q]=p; sc += PS[p*128+q]; ky ^= ZP[p*128+q]
   if (p&7)!=1 and (p&7)!=6: np += V[p&7]
 sd=0; cs=15; ep=-1; hm=0; ky ^= ZC[15]; ud.clear()
def uc(m):
 a=m&127; b=(m>>7)&127; c=m>>14
 d='abcdefgh'[a&7]+str((a>>4)+1)+'abcdefgh'[b&7]+str((b>>4)+1)
 return d+'nbrq'[c-2] if c else d
def u2(u):
 f=(ord(u[1])-49)*16+(ord(u[0])-97); t=(ord(u[3])-49)*16+(ord(u[2])-97)
 z='nbrq'.index(u[4])+2 if len(u)>4 else 0
 return f|t<<7|z<<14
def odr(ms,p,tm):
 a,b=kil[p]
 r=[]
 for x in ms:
  q=0
  if x==tm: q=1<<20
  else:
   d=(x>>7)&127; s=x&127; z=x>>14; v=bd[d]
   if v: q=100000+10*V[v&7]-V[bd[s]&7]
   elif z: q=90000+V[z]
   elif x==a: q=8000
   elif x==b: q=7000
  r.append((-q,x))
 r.sort()
 return [x for _,x in r]
def ts(v,p):
 return v+p if v>M-1000 else v-p if v<-M+1000 else v
def ls(v,p):
 return v-p if v>M-1000 else v+p if v<-M+1000 else v
def qs(a,be,p):
 global nn
 nn += 1
 if (nn&1023)==0 and nn>L: raise Abort
 if p>=128: return evl()
 ck=atk(kg[sd],sd^1)
 if not ck:
  s=evl(); st=s
  if s>=be: return s
  if s>a: a=s
  best=s
 else: best=-M-1
 ms=odr(gen(0) if ck else gen(1),p,0)
 lg=0
 for m in ms:
  if not ck and not (m>>14) and bd[(m>>7)&127] and st+V[bd[(m>>7)&127]&7]+200<a: continue
  if not mk(m): continue
  lg += 1; s=-qs(-be,-a,p+1); um()
  if s>best: best=s
  if s>a: a=s
  if a>=be: return s
 if ck and lg==0: return -M+p
 return best
def sr(d,a,be,p):
 global nn,sd,ep,hm,ky
 nn += 1
 if (nn&1023)==0 and nn>L: raise Abort
 if p>0:
  if hm>=100: return 0
  if -M+p>a: a=-M+p
  if M-p<be: be=M-p
  if a>=be: return a
 if atk(kg[sd],sd^1): d += 1
 if d<=0: return qs(a,be,p)
 if d>=4 and np>0 and evl()>=be and not atk(kg[sd],sd^1):
  gs=sd; oe=ep; oh=hm; okey=ky
  if ep>=0: ky ^= ZE[ep&7]
  ep=-1; hm += 1; sd ^= 1; ky ^= ZS
  s=-sr(d-4,-be,-be+1,p+1)
  sd=gs; ep=oe; hm=oh; ky=okey
  if s>=be: return s
 e=tt[ky&TM]; tm=0
 if e and e[0]==ky:
  _,dd,fl,s0,mv=e; tm=mv
  if dd>=d:
   s=ls(s0,p)
   if fl==0 or (fl==1 and s>=be) or (fl==2 and s<=a): return s
 a0=a
 ms=odr(gen(0),p,tm)
 best=-M-1; bm=0; lg=0; ck=None
 for i,m in enumerate(ms):
  if i==4 and d>=3 and ck is None: ck=atk(kg[sd],sd^1)
  t=(m>>7)&127; ic=bd[t]!=0 or t==ep
  if not mk(m): continue
  lg += 1
  if ky in hi or ky in pl: s=0
  else:
   pl.append(ky)
   if lg==1 or ic or (m>>14) or ck: s=-sr(d-1,-be,-a,p+1)
   elif i>=4 and d>=3:
    s=-sr(d-2,-a-1,-a,p+1)
    if s>a: s=-sr(d-1,-a-1,-a,p+1)
    if s>a: s=-sr(d-1,-be,-a,p+1)
   else:
    s=-sr(d-1,-a-1,-a,p+1)
    if s>a: s=-sr(d-1,-be,-a,p+1)
   pl.pop()
  um()
  if s>best: best=s; bm=m
  if s>a: a=s
  if a>=be:
   if not bd[(m>>7)&127] and not (m>>14):
    if kil[p][0]!=m: kil[p][1]=kil[p][0]; kil[p][0]=m
   break
 if lg==0: return -M+p if atk(kg[sd],sd^1) else 0
 fl=0 if best>a0 and best<be else (1 if best>=be else 2)
 tt[ky&TM]=(ky,d,fl,ts(best,p),bm)
 return best
D=lambda s:''.join(chr(97+(n:=ord(c)-33)%8)+str(n//8+1)for c in s)
BK=[D(',<+;"3-5$+#,;D\'63B'),D('SCTLC<_NNTXP\\JWOUE`_ZTQITNNH^UJSULS336H>'),D("-='6&;+3*:,<%':B&%$</?<W6GGX'0XN"),D('UEZK_NN==GGMKESKTD[T^L\\N][M<`H\\]'),D(',<+;\'6"3)9#,-=08$#9A,5!16,&44+AJ1Q#!'),D('UETL_NZT^USKN?TERBULL0\\@@HH8')]
def th(moves,g):
 global nn
 rst(); hi.clear()
 for u in moves:
  if not mk(u2(u)): break
  hi.add(ky)
 hi.discard(ky); pl.clear(); pl.append(ky); nn=0
 lg=[]
 for m in gen(0):
  if mk(m): um(); lg.append(m)
 if not lg: return None
 s=''.join(moves[1-g%2::2])
 L=BK[g-1] if g<7 else ''
 if L[:len(s)]==s and len(s)<len(L):
  b=L[len(s):len(s)+4]
  if b in [uc(m) for m in lg]: return b
 od=[(0,m) for m in lg]; best=lg[0]; d=0
 while d<64:
  d += 1
  try:
   a=-M-1; rs=[]
   for _,m in od:
    mk(m)
    if ky in hi or ky in pl: s=0
    else:
     pl.append(ky); s=-sr(d-1,-M-1,-a,1); pl.pop()
    um(); rs.append((s,m))
    if s>a: a=s
   rs.sort(key=lambda x: -x[0]); od=[(s,m) for s,m in rs]; best=rs[0][1]
   if rs[0][0]>=M-1000: break
  except Abort: break
 pl.clear(); return uc(best)
def post(pa,o):
 global conn
 for _ in range(2):
  try:
   y=json.dumps(o).encode(); conn.request('POST',pa,y,{'Content-Type': 'application/json'}); r=conn.getresponse(); return json.loads(r.read())
  except Exception: conn=Conn(_host,_port,timeout=30)
 raise IOError('post failed')
def main():
 global conn,_host,_port
 _host,_port=os.environ['MAKEFUN_ENV_URL'].split('://')[1].rsplit(':',1);_port=int(_port);conn=Conn(_host,_port,timeout=30)
 while True:
  st=post('/game',{})
  if st.get('status')=='done': return
  g=st['game']
  while st.get('status')=='your_move':
   mv=th(st['moves'],st['game'])
   if mv is None: st=post('/resign',{'game': g})
   else: st=post('/move',{'game': g,'move': mv})
if __name__=='__main__':
 main()
