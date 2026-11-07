import math, random, json, sys
random.seed(3)
BW=float(sys.argv[1]) if len(sys.argv)>1 else 50
ORB=[(-20,336,92,5),(20,336,92,2),(0,238,70,3)]
N=sum(o[3] for o in ORB)
def pos(phis,t):
    pts=[];k=0
    for tilt,rx,ry,n in ORB:
        c,s=math.cos(math.radians(tilt)),math.sin(math.radians(tilt))
        for i in range(n):
            th=2*math.pi*t+phis[k]; k+=1
            x=-rx*math.cos(th); y=ry*math.sin(th)
            pts.append((x*c-y*s, x*s+y*c))
    return pts
def cost(phis,steps=90):
    tot=0
    for j in range(steps):
        P=pos(phis,j/steps); w=8 if j==0 else 1
        for a in range(N):
            r=math.hypot(*P[a])
            if r<66: tot+=(66-r)*30
            for b in range(a+1,N):
                dx=abs(P[a][0]-P[b][0]); dy=abs(P[a][1]-P[b][1])
                tot+=w*max(0,BW-dx)*max(0,BW-dy)
                if dy<80 and dx<56 and (P[b][1]-P[a][1]>0 or P[a][1]-P[b][1]>0): tot+=w*0.15*(56-dx)*(80-dy)/10  # label zone, soft
    return tot
def stats(phis,steps=360):
    bad=0
    for j in range(steps):
        P=pos(phis,j/steps)
        bad+=any(abs(P[a][0]-P[b][0])<BW and abs(P[a][1]-P[b][1])<BW for a in range(N) for b in range(a+1,N))
    return bad/steps
best=None;bc=1e18
for restart in range(14):
    cur=[random.uniform(0,6.28) for _ in range(N)];cc=cost(cur);T=2000.0
    for it in range(3000):
        c=cur[:];i=random.randrange(N);c[i]+=random.gauss(0,0.5 if it<1500 else 0.08)
        x=cost(c)
        if x<=cc or random.random()<math.exp((cc-x)/max(T,1e-9)): cur,cc=c,x
        T*=0.998
    if cc<bc: best,bc=cur[:],cc
    print(restart,round(cc),round(stats(cur),3),flush=True)
json.dump(best,open('phases.json','w'));print('best',round(bc),stats(best))
