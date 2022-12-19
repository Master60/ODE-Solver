# import sympy
import sympy as sp
  
#x, y, z = symbols('x y z')

#f = Function("f")(x, z)



#f = log(sin(x)) + tan(cos(2 * x))
#c = Eq(f.diff(x,x), 1000*f.diff(x)+900)

#d2ydx2 = 100*f.diff(x)+200

# Use sympy.replace() method
#gfg = f.replace(f.diff(x,x), f.diff(z))
#ggg = gfg.replace(f.diff(x), z)
#sol2 = c.replace(1000, 200)
#sol1 = c.replace(f.diff(x,x), f.diff(z))
#sol = sol1.replace(f.diff(x), z)

#print(sol2)

#-------------------------------------------------------------------

#y = Function("y")(x)
#dydx = Function("dydx")(x)
#d2ydx2 = Function("d2ydx2")(x)
#dzdx = Function("dzdx")(x)

#d2ydx2, dydx, y, dzdx, z = symbols('d2ydx2 dydx y dzdx z')

#equ = Eq(d2ydx2, -1001*dydx - 1000*y)

#equ1 = Eq(dydx, z)
#equ2_1 = equ.replace(d2ydx2, dzdx)
#equ2 = equ2_1.replace(dydx, z)

#lol = equ2.subs([(dzdx,2),(z,4),(y,5)])
#print(equ)

#--------------------------------------------------------------------

x, y, z = sp.symbols('x y z')

f = sp.Function("f")(x, y, z)
g = sp.Function("f")(x, y, z)

f = z
g = -1001*z - 1000*y

xo=0
xf=5
yo=1
zo=0
h = 0.2
n = int((xf - xo) / h)

list_x = []
list_y = []
list_z = []

list_x.append(xo)
list_y.append(yo)
list_z.append(zo)

list_k1=[]
list_k2=[]
list_k3=[]
list_k4=[]
list_l1=[]
list_l2=[]
list_l3=[]
list_l4=[]

for i in range(n):

    x1 = xo
    y1 = yo
    z1 = zo

    k1 = f.subs({x:x1, y:y1, z:z1})
    l1 = g.subs({x:x1, y:y1, z:z1})

    x2 = xo + (h / 2)
    y2 = yo + ((k1 * h) / 2)
    z2 = zo + ((l1 * h) / 2)

    k2 = f.subs({x:x2, y:y2, z:z2})
    l2 = g.subs({x:x2, y:y2, z:z2})

    x3 = xo + (h / 2)
    y3 = yo + ((k2 * h) / 2)
    z3 = zo + ((l2 * h) / 2)

    k3 = f.subs({x:x3, y:y3, z:z3})
    l3 = g.subs({x:x3, y:y3, z:z3})

    x4 = xo + h
    y4 = yo + (k3 * h)
    z4 = zo + (l3 * h)

    k4 = f.subs({x:x4, y:y4, z:z4})
    l4 = g.subs({x:x4, y:y4, z:z4})

    xo = xo + ((i + 1) * h)
    yo = yo + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    zo = zo + (h / 6) * (l1 + 2 * l2 + 2 * l3 + l4)

    list_x.append(xo)
    list_y.append(yo)
    list_z.append(zo)

    list_k1.append(k1)
    list_k2.append(k2)
    list_k3.append(k3)
    list_k4.append(k4)
    list_l1.append(l1)
    list_l2.append(l2)
    list_l3.append(l3)
    list_l4.append(l4)

print(list_x[1])
print(list_y[25])
print(list_z[1])

print(list_k1[1])
print(list_l1[1])
print(list_k2[1])
print(list_l2[1])
print(list_k3[1])
print(list_l3[1])
print(list_k4[1])
print(list_l4[1])
