#############################################
##### Name: Sachit Krishnan #################
##### Uniqname: sachit ######################
##### UMID: 30156124 ########################
#############################################
#############################################

class Graph:
    '''
    A class of objects to represent directed graph data structure.
    '''
    def __init__(self):
        self.nodes = {}
        self.neighbors = {}

    def addNode(self, newKey, newVal):
        '''
        Add a node/vertex to the directed graph by assigning the value of the node to its key/name.
        '''
        self.nodes[newKey] = newVal
        self.neighbors[newKey] = []
        
    def removeNode(self, key):
        '''
        Remove a node and all its connections from the directed graph by its key.
        '''
        if key not in self.nodes:
            print('The node {} does not exist.'.format(key))
        else:
            del self.nodes[key]
            del self.neighbors[key]

    def addEdge(self, key1, key2):
        '''
        Add a neighbor to the list of neighbors of a given node.
        '''
        if key1 not in self.nodes:
            print('The node {} does not exist.'.format(key1))
        elif key2 not in self.nodes:
            print('The node {} does not exist.'.format(key2))
        elif key1 == key2:
            print('A node cannot be its own neighbor.')
        elif key2 in self.neighbors[key1]:
            pass
        else:
            self.neighbors[key1].append(key2)

    def description(self):
        '''
        Print the neighbor list of each node in the directed graph.
        '''
        if len(self.nodes) == 0:
            print('The graph is empty.')
        else:
            print('Node: List of Neighbors')
            for node, neighbors in self.neighbors.items():
                if neighbors == []:
                    print('{}: < No neighbors >'.format(node))
                else:
                    print('{}: {}'.format(node, neighbors))

class Fragrance:
    '''
    A class of objects to represent a perfume/cologne.
    '''
    def __init__(self, parse):
        self.name = parse[0]
        self.brand = parse[1]
        self.gender = parse[2]
        self.accords = parse[3]
        self.top = parse[4]
        self.mid = parse[5]
        self.base = parse[6]
        self.rating = parse[7]
        self.votes = parse[8]
        self.longevity = parse[9]
        self.sillage = parse[10]
        self.value = parse[11]
        self.pic = parse[12]
        self.description = parse[13]
    
    def popularity(self):
        '''
        A metric to measure the popularity of the fragrance as the total number of 'favorable' votes:
        
        popularity 'p' = rating (%) * number of votes
        
        Returns:
        p: Number of favorable votes (int)
        '''
        
        try:
            return round(self.rating*0.2*self.votes)
        except:
            return 0
    
    def primaryAccord(self):
        '''
        Ascertain the dominant accord of the fragrance.
        
        Returns:
        acc: primary accord (str)
        '''
        try:
            pa = list(self.accords.keys())[0].lower()
        except:
            pa = 'no accords'
            
        return pa

class Object:
    def toJSON(self):
        '''
        Prepare abstract data structures to be saved in a JSON cache.
        '''
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
