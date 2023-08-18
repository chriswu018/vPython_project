import math
import time
from vpython import*

domino = {}

l0,h0,w0,d0 = 20,200,80,80
t,dt = 0,0.001
N = 13
density = 0.54
mu = 1

td = {}

scene = canvas(width = 1000, height = 600, center = vec(0,0,0), align = 'left', background = vec(0.865,0.875,0.875))
floor = box(length=1500, height=0.01, width=1500, color=color.black)
floor.pos = vec(200,-100,0)

GRAPH = graph(width = 450, align = 'right', title = 'omega1,2 (rad/s)')
GRAPH2 = graph(width = 450, align = 'right', title = 'speed of transmission(m/s)')
funct1 = gcurve(graph = GRAPH, color=color.blue, width=4)
funct2 = gcurve(graph = GRAPH, color=color.red, width=4)
funct3 = gcurve(graph = GRAPH2, color=color.orange, width=4)

class Domino(box):
    l,h,w,d = 20,200,80,80
    M = density*l*h*w
    Ir = M*(l**2+h**2)/3
    omega = 0
    theta = pi/2
    c_point = vec(0,0,0)
    posX0 = 0
    
    def rotate(self, i):
        self.theta -= self.omega*dt
        self.axis = vec(cos(self.theta+pi/2),sin(self.theta+pi/2),0)
        self.size = vec(self.l,self.h,self.w)
        self.pos = vec(self.d*(i-5)+self.h/2*cos(self.theta)-self.l/2*(sin(self.theta)-1),self.h/2*(sin(self.theta)-1)+self.l/2*cos(self.theta),0)
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
    else:
        R1 = do1.h
        R2 = sqrt((do1.h*cos(do1.theta)+do2.l*sin(do2.theta)-80)**2+(do1.h*cos(do1.theta)-do2.l*cos(do2.theta))**2)
        
    J = 1.5*((do1.Ir*R1*do1.omega)/(R1**2+R2**2+do1.Ir/do1.M*mu) + (do2.Ir*R2*do2.omega)/(R1**2+R2**2+do2.Ir/do2.M*mu))
    do1.omega -= R1*J/do1.Ir
    do2.omega += R2*J/do2.Ir
    
    if (first):
        if(i==0):
            print("omega 1 2 :")
        print(do1.omega , do2.omega)
        funct1.plot( pos=(i, do1.omega) )
        funct2.plot( pos=(i, do2.omega) )
        td[i] = t
    return do1.omega , do2.omega

            
for i in range(N):
    domino[i] = Domino(pos = vec(d0*(i-5),0,0),axis = vec(0,0,0),size = vec(l0,h0,w0))
    domino[i].posX0 = d0*(i-5)
    domino[i].c_point = domino[i].pos +vec(domino[i].l/2,domino[i].h/2,0)
    td[i] = 0

domino[0].omega = 1
time.sleep(2)
while domino[N-1].theta > 0:
    rate(1000)
    for i in range(N-1):
        if domino[i].omega > 0 and domino[i].theta > asin(domino[i+1].l/domino[i].d):
            domino[i].omega+=9.8*dt*cos(domino[i].theta)
            if domino[i+1].theta < pi/2-0.1 and domino[i+1].theta > atan((200*sin(domino[i].theta)-20*cos(domino[i+1].theta))/(200*cos(domino[i].theta)+20*sin(domino[i+1].theta)-80)):
                domino[i].omega = 0.6*domino[i+1].omega
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
    scene.center += vec(0.08,0,0)
    t+=dt

print("collision time distance")
print(td[0])
funct3.plot( pos=(0, 80/td[0]) )
for i in range(1,N-1):
    funct3.plot( pos=(i, 80/(td[i]-td[i-1])) )
    print(td[i]-td[i-1])
