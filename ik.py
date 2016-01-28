from pyfbsdk import *
import math_utils
# A small 3DS MAX Python script that uses Cyclic Coordinate Descent(CCD) 
# algorithm to implement Inverse Kinematics
# Author: Xindong Deng

# Function to retrieve the tail of the chain
def getTail(base):
    while base.Children:
        base = base.Children[0]
    return base

# Main function: take base node of the chain and target node as parameters
def ccd(goal,chain_base):
    # Initialize variables
    i = 0
    # Max iteration
    im = 100
    # Thresh
    thresh = 0.01
    tail = getTail(chain_base)
    p = tail

    vtail = FBVector3d()
    tail.GetVector(vtail,FBModelTransformationType.kModelTranslation)
    vgoal = FBVector3d()
    goal.GetVector(vgoal,FBModelTransformationType.kModelTranslation)
    dist = vgoal-vtail
    dist = dist.Length()

    while ((dist>thresh)and(i<im)):
        # Re-initialize variables for each loop
        FBSystem().Scene.Evaluate()
        tail.GetVector(vtail,FBModelTransformationType.kModelTranslation)
        goal.GetVector(vgoal,FBModelTransformationType.kModelTranslation)
        vp = FBVector3d()
        p.Parent.GetVector(vp,FBModelTransformationType.kModelTranslation)
        
        # Vector from pivot to tail
        v1 = vtail - vp
        # Vector from pivot to goal
        v2 = vgoal-vp
        
        # Get rotation matrix
        rotMatrix = FBMatrix()
        rotMatrix = math_utils.align_matrix(v1,v2)
        # Get orintation matrix
        po = FBMatrix()
        p.Parent.GetMatrix(po,FBModelTransformationType.kModelRotation,False)
        # Rotate
        final_ori = rotMatrix * po
        ori_vec = FBVector3d()
        FBMatrixToRotation(ori_vec,final_ori)
        p.Parent.Rotation = ori_vec
       
        # If reaches the base bone
        if p.Parent==chain_base:
            p = tail
        #else
        else:
            p = p.Parent
   
        
        dist = vgoal-vtail
        dist = dist.Length()
        i=i+1
 
# Test
#goal = FBFindModelByLabelName('Goal')
#chain_base = FBFindModelByLabelName('Node')

#ccd(goal,chain_base)