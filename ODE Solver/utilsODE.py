import numpy as np
from math import sin, cos, exp, log

#------------------------------------------------------------------------------
'''
This function computes the right-hand-side of expressions of the form
dyi/dx = f(x, y1, y2, ... , yi, ..., yn-2, yn-1), where n is the order of the 
ODE, for all values of i ranging from 1 to n-1.

Parameters:
    x -> The value of x
    y -> An array containing the values of y1, y2, ..., yn-1
    expression -> A string that stores the mathematical expression of the function f.

Returns:
    dydx: a numpy array containing all the values of dyi/dx
'''
def derivatives(x, y, expression):
    n = len(y)
    dydx = list(range(n))
    
    for i in range(n-1):
        dydx[i] = y[i+1]
    
    
    
    for i in range(1, n):
        expression = expression.replace("yp" + str(i), str(y[i]))
        
    expression = expression.replace("y", str(y[0]))
    dydx[n-1] = eval(expression)
    
    return np.array(dydx)
    
#------------------------------------------------------------------------------
'''
This function uses the Runge-Kutta of order 4 to compute the values of y at
x+h.

Parameters:
    x -> The value of x at the starting point, before adding h.
    y -> An array containing the values of yi at x.
    expression -> A string storing the mathematical expression of the function f.

Returns:
    y -> An array containing the approximated values of yi at x+h.
'''
def RK4(x, y, h, expression):
    k1 = derivatives(x, y, expression)
    k2 = derivatives(x + h/2, y + k1 * h / 2, expression)
    k3 = derivatives(x + h / 2, y + k2 * h / 2, expression)
    k4 = derivatives(x + h, y + k3 * h, expression)
    
    slope = (k1 + 2*(k2 + k3) + k4) / 6
    y = y + slope * h
    
    return y

#------------------------------------------------------------------------------
'''
This function uses the Runge-Kutta method repeatedly to compute values of all yi
at x, x+h, x+2h, ... until the value of xend is reached. The main use of this
function is when the user wants the computation to be performed with a certain
small step size h, but does not want all of the values of y at each one of those
fine steps to be returned by the program. Hence, the function is called on a 
larger interval specified by xend, uses the smaller step size in the computation,
and only returns the y values at the end of the larger interval.

Parameters:
     x -> Initially set to the value of x at the beginning of the interval. Will
          be updated as the function runs.
    y -> An array that is initially set to the values of yi at the beginning of the
         interval. Will be updated as the function runs.
    h -> The step size.
    xend -> The end of the interval, at which the values of yi should be returned.
    expression -> The mathematical expression of f.

Returns:
    y -> The value of y calculated at xend.
'''  
def integrator(x, y, h, xend, expression):
    while(x < xend):
        if (xend - x < h):
            h = xend - x
        y = RK4(x, y, h, expression)
        x = x + h
        
    return y

#------------------------------------------------------------------------------
'''
The function that will be called in our main program. Solves a genral ODE.

Parameters:
    xi -> The initial value of x
    y_initial -> The initial values of every yi.
    xf -> The final value of x within th interval that we wish to evaluate the ODE at.
    h -> The step size used in the computation.
    xout_step -> The larger step size that the user wants the values of yi to be returned at.
    expression -> The mathematical expression of x.

Returns:
    xout -> An array containing the values of x, x + xout_step, x + 2*cout_step, ...
    yout -> An array containing the values of y at each value in xout.
'''
def solveODE(xi, y_initial, xf, h, xout_step, expression):
    x = xi
    xout = [x]
    yout = [y_initial[0]]
    y = y_initial

    while(x < xf):
        #print('int ode')
        xend = x + xout_step
        if (xend > xf):
            xend = xf
        y = integrator(x, y, h, xend, expression)
        x = xend
        xout.append(x)
        yout.append(y[0])
        
    return xout, yout