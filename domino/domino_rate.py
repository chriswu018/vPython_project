import math
import time
from vpython import*

domino = {}

l0,h0,w0,d0 = 20,200,80,80
t,dt = 0,0.001
RatE = 1.3
N = 13
density = 0.54
mu = 0.5

scene = canvas(width = 1000, height = 600, center = vec(0,0,0), align = 'left', background = vec(0.865,0.875,0.875))
floor = box(length=150*(RatE**(N)-1)/(RatE-1), height=0.01, width=150*(RatE**(N)-1)/(RatE-1), color=color.black)
floor.pos = vec(d0*(RatE**(N)-1)/(RatE-1)/2 , 0, 0)

GRAPH = graph(width = 450, align = 'right', title = 'Kinetic(W)(log scale)')
funct1 = gcurve(graph = GRAPH, color=color.blue, width=4)


class Domino(box):
    l,h,w,d = 20,200,80,80
    M = density*l*h*w
    Ir = M*(l**2+h**2)/3
    omega = 0
    theta = pi/2
    c_point = vec(0,0,0)
    posX0 = 0
    posY0 = 0
    
    def rotate(self, i):
        self.theta -= self.omega*dt
        self.axis = vec(cos(self.theta+pi/2),sin(self.theta+pi/2),0)
        self.size = vec(self.l,self.h,self.w)
        self.pos = vec(self.posX0,self.posY0,0) + vec(self.h/2*cos(self.theta)-self.l/2*(sin(self.theta)-1),self.h/2*(sin(self.theta)-1)+self.l/2*cos(self.theta),0)
        self.c_point = self.pos + vec(self.l/2*sin(self.theta)+self.h/2*cos(self.theta),-self.l/2*cos(self.theta)+self.h/2*sin(self.theta),0)
        return 1

def collision(do1,do2,i):
    R1 = 0
    R2 = 0
    J = 0
    first = 0
    if do2.theta == pi/2:
        R1 = do1.h
        R2 = do1.h*sin(do1.theta)
        first = 1
        if i==0:
            funct1.plot( pos=(i, log(domino[i].Ir*(domino[i].omega**2)/2)) )
            print(domino[i].Ir*(domino[i].omega**2)/2)
    else:
        R1 = do1.h
        R2 = sqrt((do1.h*cos(do1.theta)+do2.l*sin(do2.theta)-80)**2+(do1.h*cos(do1.theta)-do2.l*cos(do2.theta))**2)
        
    J = 2*((do1.Ir*R1*do1.omega)/(R1**2+R2**2+do1.Ir/do1.M*mu) + (do2.Ir*R2*do2.omega)/(R1**2+R2**2+do2.Ir/do2.M*mu))
    do1.omega -= R1*J/do1.Ir
    do2.omega += R2*J/do2.Ir

    if(first):
        funct1.plot( pos=(i+1, log((domino[i+1].Ir*(domino[i+1].omega**2)/2))))
        print(domino[i+1].Ir*(domino[i+1].omega**2)/2)
    
    return do1.omega , do2.omega

            
for i in range(N):
    domino[i] = Domino(axis = vec(0,0,0))
    domino[i].l = l0*(RatE**(i))
    domino[i].h = h0*(RatE**(i))
    domino[i].w = w0*(RatE**(i))
    domino[i].d = d0*(RatE**(i))
    domino[i].pos = vec(d0*(RatE**(i)-1)/(RatE-1),domino[i].h/2,0)
    domino[i].posX0 = domino[i].pos.x
    domino[i].posY0 = domino[i].pos.y
    domino[i].size = vec(domino[i].l,domino[i].h,domino[i].w)
    domino[i].c_point = domino[i].pos +vec(domino[i].l/2,domino[i].h/2,0)
    domino[i].M = density*domino[i].l*domino[i].h*domino[i].w
    domino[i].Ir = domino[i].M*(domino[i].l**2+domino[i].h**2)/3

domino[0].omega = 1
time.sleep(2)
while domino[N-1].theta > 0:
    rate(1000)
    for i in range(N-1):
        if domino[i].omega > 0 and domino[i].theta > asin(2*RatE/8):
            domino[i].omega+=9.8*dt*cos(domino[i].theta)
            if domino[i+1].theta < pi/2-0.1 and domino[i+1].theta > atan((domino[i].h*sin(domino[i].theta)-domino[i+1].l*cos(domino[i+1].theta))/(domino[i].h*cos(domino[i].theta)+domino[i+1].l*sin(domino[i+1].theta)-domino[i].d)):
                domino[i+1].omega *= 1.01
                domino[i].omega = domino[i+1].omega*0.5
            domino[i].rotate(i)
            if (domino[i].c_point.x ) > (domino[i].posX0 + domino[i].d  - domino[i+1].l/2):
                if domino[i+1].omega == 0 :
                    domino[i].omega,domino[i+1].omega = collision(domino[i],domino[i+1],i)
                elif (tan(domino[i+1].theta)*(domino[i].c_point.x-domino[i+1].pos.x+domino[i+1].l/2/cos(domino[i+1].theta))+(domino[i].c_point.y-domino[i+1].pos.y)<=0):
                    domino[i].omega,domino[i+1].omega = collision(domino[i],domino[i+1],i)

    if (domino[N-2].c_point.x ) > (domino[N-2].posX0 + domino[N-2].d  - domino[N-1].l/2):
        if domino[N-1].theta > 0:
            if domino[N-1].omega == 0:
                domino[N-2].omega,domino[N-1].omega = collision(domino[N-2],domino[N-1])
            domino[N-1].omega += 9.8*dt*cos(domino[N-1].theta)
            domino[N-1].rotate(N-1)     
    scene.center += vec(RatE**N*0.03,0,0)

print("Initial Kinetic", domino[0].Ir*1/2)
print("Final Kinetic", domino[N-1].Ir*(domino[N-1].omega**2)/2)
print("Magnification",domino[N-1].Ir*(domino[N-1].omega**2)/domino[0].Ir*1)
