#############################################
##### Name: Sachit Krishnan #################
##### Uniqname: sachit ######################
##### UMID: 30156124 ########################
#############################################
#############################################

# Standalone file to read 
from classes import *
from datahandling import *

def GraphConstruct1(graphpath):
    '''
    Load the graph from the JSON cache into the Graph data structure.
    
    Parameters:
    graphpath: Path of the JSON graph cache with extension
    
    Returns:
    fragraph: Object of the Graph class with the data from the JSON cache
    '''
    graphlist = eval(open_cache(graphpath))
    attributes = graphlist[0]['att']
    frag = graphlist[0]['frag']
    neigh = graphlist[1]
    
    #Creating the graph of fragrances:
    fragraph = Graph()

    #Populating the attribute nodes using the cache
    for k, v in attributes.items():
        fragraph.addNode(k, v)

    #Populating the fragrance nodes using the cache
    for k, v in frag.items():
        fg = Fragrance(FragLoad(v))
        fragraph.addNode(k, fg)
        
    #Populating the edges using the cache
    for k, v in neigh.items():
        for n in v:
            fragraph.addEdge(k, n)
    
    return fragraph

if __name__ == '__main__':
    graphPath = "data/fragraph.json"
    graph1 = GraphConstruct1(graphPath)
    print(list(graph1.nodes.keys()))
