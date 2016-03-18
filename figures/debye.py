import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import math
chebyshev_representation = np.array( [ 2.707737068327440945/2.0, 0.340068135211091751, -0.12945150184440869e-01, \
                                     0.7963755380173816e-03, -0.546360009590824e-04, 0.39243019598805e-05, \
                                    -0.2894032823539e-06, 0.217317613962e-07, -0.16542099950e-08, \
                                     0.1272796189e-09, -0.987963460e-11, 0.7725074e-12, -0.607797e-13, \
                                     0.48076e-14, -0.3820e-15, 0.305e-16, -0.24e-17] )


eps = np.finfo(np.float).eps
sqrt_eps = np.sqrt(np.finfo(np.float).eps)
log_eps = np.log(np.finfo(np.float).eps)
gas_constant = 8.31446

def _chebval(x, c):
    """
    Evaluate a Chebyshev series at points x.
    This is just a lightly modified copy/paste job from the numpy
    implementation of the same function, copied over here to put a
    jit wrapper around it.
    """
    if len(c) == 1 :
        c0 = c[0]
        c1 = 0
    elif len(c) == 2 :
        c0 = c[0]
        c1 = c[1]
    else :
        x2 = 2*x
        c0 = c[-2]
        c1 = c[-1]
        for i in range(3, len(c) + 1) :
            tmp = c0
            c0 = c[-i] - c1
            c1 = tmp + c1*x2
    return c0 + c1*x

def debye_fn_cheb(x):
    """
    Evaluate the Debye function using a Chebyshev series expansion coupled with
    asymptotic solutions of the function.  Shamelessly adapted from the GSL implementation
    of the same function (Itself adapted from Collected Algorithms from ACM).
    Should give the same result as debye_fn(x) to near machine-precision.
    """
    val_infinity = 19.4818182068004875;
    xcut = -log_eps
    
    assert(x > 0.0) #check for invalid x

    if x < 2.0*np.sqrt(2.0)*sqrt_eps:
        return 1.0 - 3.0*x/8.0 + x*x/20.0;
    elif x <= 4.0 :
        t = x*x/8.0 - 1.0;
        c = _chebval(t, chebyshev_representation)
        return c - 0.375*x;
    elif x < -(np.log(2.0) + log_eps ):
        nexp = int(np.floor(xcut/x));
        ex  = np.exp(-x);
        xk  = nexp * x;
        rk  = nexp;
        sum = 0.0;
        for i in range(nexp,0,-1):
            xk_inv = 1.0/xk;
            sum *= ex;
            sum += (((6.0*xk_inv + 6.0)*xk_inv + 3.0)*xk_inv + 1.0) / rk;
            rk -= 1.0;
            xk -= x;
        return val_infinity/(x*x*x) - 3.0 * sum * ex;
    elif x < xcut:
        x3 = x*x*x;
        sum = 6.0 + 6.0*x + 3.0*x*x + x3;
        return  (val_infinity - 3.0 * sum * np.exp(-x)) / x3;
    else:
        return ((val_infinity/x)/x)/x;

def heat_capacity_v(T,debye_T,n):
    """
    Heat capacity at constant volume.  In J/K/mol
    """
    if T <= eps:
        return 0.
    x = debye_T/T
    C_v = 3.0*n*gas_constant* ( 4.0*debye_fn_cheb(x) - 3.0*x/(np.exp(x)-1.0) )
    return C_v

def entropy( T, debye_T, n):
    """
    Entropy due to lattice vibrations in the Debye model [J/K]
    """
    if T <= eps:
        return 0.
    x = debye_T/T
    S = n * gas_constant * ( 4. * debye_fn_cheb(x) - 3. * np.log( 1.0 - np.exp(-x) ) ) 
    return S

def heat_capacity_v_einstein(T,einstein_T,n):
    """
    Heat capacity at constant volume.  In J/K/mol
    """
    if T <= eps:
        return 0.
    x = einstein_T/T
    C_v = 3.0*n*gas_constant*x*x/4/(math.sinh(x/2.)*math.sinh(x/2.))
    return C_v

temperatures = np.linspace(0.01, 1.0, 101)
heat_capacities = np.empty_like(temperatures)
entropies = np.empty_like(temperatures)

n = 1./gas_constant
T0 = 1.00
T1 = 0.95
for i, T in enumerate(temperatures):
    heat_capacities[i] = heat_capacity_v(T, T1, n) - heat_capacity_v(T, T0, n)
    #heat_capacities[i] = heat_capacity_v_einstein(T, T1, n) - heat_capacity_v_einstein(T, T0, n)
    entropies[i] = entropy(T, T1, n) - entropy(T, T0, n)

np.savetxt(fname='debye_excesses.dat', X=np.array(zip(*[temperatures, heat_capacities, entropies])), header='T/T_D, C_v_xs/NkB, S_xs/NkB')
#plt.plot(temperatures, heat_capacities)
#plt.plot(temperatures, entropies)
#plt.show()

print(entropy(1000., 0.95, n) - entropy(1000., 1.00, n))
print(3.*np.log(1.00/0.95))

