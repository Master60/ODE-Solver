import numpy as np

'''
This function is responsible for preparing all of the input variables taken from 
the user to be used later in solving the ODE.

Note: If you want to input the value of dy/dx, input yp1 (y prime 1)
                                        d2y/dx2, input yp2 (y prime 2)
                                        d3y/dx3, input yp3 (y prime 3)
                                        .
                                        .
                                        .
                                        diy/dxi, input ypi (y prime i)
'''
def getUserInput():
    n = input("Enter the order of the differential equation you wish to solve: ")
    n = int(n)
    
    expression = input("Enter the expression for the highest order derivative: ")
    
    x = input("Enter the initial value of x: ")
    y = np.array([0] * n)
    y_in = input("Enter the initial value of y: ")
    y[0] = y_in
    
    for i in range(1, n):
        y_in = input("Enter the initial value of derivative " + str(i) + " of y: ")
        y[i] = y_in
    
    xf = input("Enter the final value of x: ")
    h = input("Enter the value of h: ")
    xout_step = input("Enter the step size of the output: ")
    
    return float(x), y, float(xf), float(h), float(xout_step), expression