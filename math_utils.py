from pyfbsdk import *


def skew_sym(v):
    '''
    Returns skew-symetric matrix for vector v
    '''
    m = FBMatrix([
    0, -v[2], v[1], 0,
    v[2], 0, -v[0], 0,
    -v[1], v[0], 0, 0,
    0, 0, 0, 1
    ])
    # IMPORTANT!: In MoBu, matrices are row-major, need to transpose it
    m.Transpose()
    return m
    
def align_matrix(a,b):
    '''
    Returns matrix that rotates vector a onto vector b
    '''
    # Turn them into unit vectors
    a.Normalize()
    b.Normalize()
    
    
    v = a.CrossProduct(b)
    s = v.Length() # Sin of angle
    c = a.DotProduct(b) # Cos of angle
    
    # Load identity
    I = FBMatrix()
 
    # a is prallel to b ( return identity)
    if v.Length() == 0:
        return I
        
    
    skew_M = skew_sym(v)
    
    R = I +  skew_M + (skew_M*skew_M)*((1-c)/(s*s))
    R[15] = 1 # Can' use 3x3 here
    return R
    
## Uncomment following lines to test this code
# a = FBVector3d(-1,1,2)
# b = FBVector3d(1,0,1)
# R = align_matrix(a,b)