from pyfbsdk import *


def create_chain(nodes,bone_len):
    '''
    Creates a chain of nodes
    '''
    
    parent = None
    for i in xrange(0,nodes):
        child = FBModelSkeleton('Node')
        
        # Add a node to the chain
        if parent is not None:
            parent.Children.append(child)
            child.Translation = FBVector3d(0,bone_len,0)
            
        parent = child
        # Make sure every node is visible
        parent.Show = True
    

def create_goal(init_pos):
    '''
    Creates goal for our IK
    '''
    g = FBModelMarker('Goal')
    g.Translation = init_pos
    g.Show=True  
    
## Uncomment following block to test your script
n_nodes=10 # Always at least 2
bone_len=50
create_chain(n_nodes,bone_len)
initial_pos = FBVector3d(150,200,150)
create_goal(initial_pos)