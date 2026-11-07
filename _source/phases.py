import math, random, json
random.seed(5)
ORB=[(-18,330,82,5),(18,330,82,2),(0,244,74,3)]
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
def cost(phis,steps=60):
    tot=0
    for j in range(steps):
        P=pos(phis,j/steps); w=6 if j==0 else 1
        for a in range(N):
            if math.hypot(*P[a])<70: tot+=(70-math.hypot(*P[a]))*30
            for b in range(N):
                if a==b: continue
                dx=abs(P[a][0]-P[b][0]); dy=P[b][1]-P[a][1]
                if a<b: tot+=w*10*max(0,60-dx)*max(0,60-abs(dy))        # badge vs badge
                if 4<dy<78: tot+=w*max(0,56-dx)*1.0                      # label of a vs badge of b
    return tot
def stats(phis,steps=240):
    bad=0
    for j in range(steps):
        P=pos(phis,j/steps)
        bad+=any(abs(P[a][0]-P[b][0])<60 and abs(P[a][1]-P[b][1])<60 for a in range(N) for b in range(a+1,N))
    return bad/steps
best=None;bc=1e18
for restart in range(6):
    cur=[random.uniform(0,6.28) for _ in range(N)];cc=cost(cur)
    for it in range(2500):
        c=cur[:];i=random.randrange(N);c[i]+=random.gauss(0,0.6 if it<1200 else 0.1)
        x=cost(c)
        if x<=cc: cur,cc=c,x
    if cc<bc: best,bc=cur,cc
    print(restart,round(cc),stats(cur))
json.dump(best,open('phases.json','w'));print('best',bc,stats(best))
