#############################################
##### Name: Sachit Krishnan #################
##### Uniqname: sachit ######################
##### UMID: 30156124 ########################
#############################################
#############################################

import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import selenium
import json
import flask
from flask import Flask, render_template, request
import random
from werkzeug.datastructures import MultiDict

import requests
import json
from classes import *

def save_cache(dataToSave, fileName):
    '''
    Function to save the scraped data in a JSON cache.

    Parameters
    ----------
    1. dataToSave: Scraped perfume data, saved in a list of dictionaries

    2. fileName: User defined JSON file name with extension (str)

    Returns
    -------
    None
    '''
    fw = open(fileName, 'w')
    dm = json.dumps(dataToSave)
    fw.write(dm)
    fw.close()

def open_cache(cacheName):
    '''
    Function to open the JSON cache file (if it exists) and load the json file into perfumes_list.
    If the cache file does not exist, an empty list is returned.

    Parameters
    ----------
    cacheName: file path (str)

    Returns
    -------
    perfumes_list: list of dictionaries (the data of each perfume is saved in a dictionary)
    '''
    try:
        cache_file = open(cacheName, 'r')
        cache_contents = cache_file.read()
        perfumes_list = json.loads(cache_contents)
        cache_file.close()
    except:
        perfumes_list = []
        
    return perfumes_list

def load_cache(data, k):
    '''
    Reads perfume data loaded from the cache and returns attributes of the perfume at the k^th index.
    
    Parameters:
    1. data: perfume data loaded from cache (dict)
    2. k: index of perfume in loaded data (int)
    
    Returns: A list of the following attributes of the perfume in a relevant format:
    name, brand, gender, accords, top, mid, base, rating, votes, longevity, sillage, value, pic, description
    '''
    name = data[k]['name']
    brand = data[k]['brand']
    gender = data[k]['gender']
    accords = data[k]['accords']
    top = data[k]['top']
    mid = data[k]['mid']
    base = data[k]['base']
    rating = data[k]['rating']
    votes = data[k]['votes']
    longevity = data[k]['longevity']
    sillage = data[k]['sillage']
    value = data[k]['value']
    pic = data[k]['pic']
    description = data[k]['description']
    
    if name == brand:
        name = brand + " (Perfume)"
        
    return name, brand, gender, accords, top, mid, base, rating, votes, longevity, sillage, value, pic, description

def FragLoad(data):
    '''
    Reads perfume data loaded from the cache and returns attributes.
    Similar to load_cache() except this function does not need a list of dictionaries - just one.
    
    Parameters:
    data: perfume data loaded from cache (dict)
    
    Returns: A list of the following attributes of the perfume in a relevant format:
    name, brand, gender, accords, top, mid, base, rating, votes, longevity, sillage, value, pic, description
    '''
    name = data['name']
    brand = data['brand']
    gender = data['gender']
    accords = data['accords']
    top = data['top']
    mid = data['mid']
    base = data['base']
    rating = data['rating']
    votes = data['votes']
    longevity = data['longevity']
    sillage = data['sillage']
    value = data['value']
    pic = data['pic']
    description = data['description']
        
    return name, brand, gender, accords, top, mid, base, rating, votes, longevity, sillage, value, pic, description

def GraphConstruct(graphpath):
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

    #Adding the attribute nodes to fragraph
    for k, v in attributes.items():
        fragraph.addNode(k, v)

    #Adding the fragrance nodes to fragraph
    for k, v in frag.items():
        fg = Fragrance(FragLoad(v))
        fragraph.addNode(k, fg)
        
    #Adding the edges to fragraph
    for k, v in neigh.items():
        for n in v:
            fragraph.addEdge(k, n)
    
    return fragraph

def dictOfAttributes(frag):
    '''
    Get a dictionary of all attributes in the perfume data.
    
    Parameters:
    frag: a list of objects of the class 'Fragrance'
    
    Returns:
    dictAtt: a dict of attributes
    '''
    brands = []
    gens = []
    accs = []
    tops = []
    mids = []
    bases = []
    allnotes = []
    longs = []
    sills = []
    vals = []

    for item in frag:

        #Brand nodes
        if item.brand not in brands:
            brands.append(item.brand)

        #Gender nodes
        if item.gender not in gens:
            gens.append(item.gender)

        #Accord nodes
        if item.primaryAccord() not in accs:
            accs.append(item.primaryAccord())

        #Top note nodes
        for n in item.top:
            if n not in tops:
                tops.append(n)

        #Middle note nodes
        for n in item.mid:
            if n not in mids:
                mids.append(n)

        #Base note nodes
        for n in item.base:
            if n not in bases:
                bases.append(n)

        #Longevity nodes
        if item.longevity not in longs:
            longs.append(item.longevity)

        #Sillage nodes
        if item.sillage not in sills:
            sills.append(item.sillage)

        #Price value nodes
        if item.value not in vals:
            vals.append(item.value)

    #List containing all the fragrance notes, i.e., the union of the top, mid, and base notes
    allnotes = tops
    for n in mids:
        if n not in allnotes:
            allnotes.append(n)
    for n in bases:
        if n not in allnotes:
            allnotes.append(n)
            
    dictAtt = {
        'brands' : brands,
        'gens' : gens,
        'accs' : accs,
        'tops' : tops,
        'mids' : mids,
        'bases' : bases,
        'allnotes' : allnotes,
        'longs' : longs,
        'sills' : sills,
        'vals' : vals
    }
    
    return dictAtt

def inputAttributes(frag):
    '''
    Get a dictionary of all input attributes to populate the HTML template file.
    
    Parameters:
    frag: a list of objects of the class 'Fragrance'
    
    Returns:
    fd: dict of input attributes
    '''
    fd = dictOfAttributes(frag)
    for item in list(fd.keys()):
        att = fd[item]
        if item == 'brands' or item == 'accs' or item == 'tops' or item == 'mids' or item == 'bases':
            att.sort()
        fd[item] = att
    return fd

def sortFrags(nodes, k = None, gen = None):
    '''
    Sort a list of k fragrances by name.
    
    Parameters:
    1. nodes: list of objects of the Fragrance class
    2. k: number of top results of the sorted list to be returned (int)
    3. gen: gender attribute (str); specify if only one targeted gender is to be returned 
    
    Returns:
    nodes: list of objects of the class Fragrance
    '''
    if k == None:
        k = min(20, len(nodes))
        
    if gen != None:
        new = []
        for item in nodes:
            if item.gender == gen:
                new.append(item)
        nodes = new

    for i in range(len(nodes)-1):
        for j in range(i+1, len(nodes)):
            if nodes[j].popularity() > nodes[i].popularity():
                temp = nodes[j]
                nodes[j] = nodes[i]
                nodes[i] = temp
                
    return nodes[:k]

def FragNameNode(graph):
    '''
    Isolate the list of fragrance nodes of a graph from its attribute nodes.
    Also obtain the corresponding list of names of the fragrances.
    
    Parameters:
    graph: Object of the Graph class
    
    Returns:
    1. nodelist: list of objects of the Fragrance class
    2. namelist: corresponding list of fragrance names
    '''
    namelist = []
    nodelist = []
    for item in graph.neighbors:
        for n in graph.neighbors[item]:
            if n not in namelist:
                namelist.append(n)
                nodelist.append(graph.nodes[n])
                
    return nodelist, namelist

def outputHTML(inpDict, graphpath):
    '''
    Prepare the fragrance recommendations based on the user input.
    
    Parameters:
    inpDict: Dictionary of processed user input to be used to extract information from the graph to generate recommendations
    
    Returns:
    [outstr, frags]
    1. outstr: String to be displayed as the title of the Fragrance Recommendations HTML page.
    2. frags: list of objects of the fragrance class
    '''
    g = GraphConstruct(graphpath)
    perf = FragRecommender(g, inpDict)
    allperf = FragRecommender(g, {})
    
    if len(perf) == len(allperf):
        frags = sortFrags(allperf, 7, 'for men') + sortFrags(allperf, 7, 'for women') + sortFrags(allperf, 6, 'for women and men')
        random.shuffle(frags)
        if len(frags) > 20:
            frags = frags[:20]
        outstr = "No selection? I got this! Check These Out..."
    elif len(perf) == 0:
        frags = sortFrags(allperf, 7, 'for men') + sortFrags(allperf, 7, 'for women') + sortFrags(allperf, 6, 'for women and men')
        random.shuffle(frags)
        if len(frags) > 20:
            frags = frags[:20]
        outstr = "No Hits... But Check These Out!"
    else:
        frags = sortFrags(perf, k = None, gen = None)
        outstr = "Your Recommendations"
    
    return [outstr, frags]

def formParse(a):
    '''
    Parse the request form.
    
    Parameters:
    a: Immutable list of tuples - raw user input attributes
    
    Return:
    inpDict: dict of processed user input attributes
    '''
    inpDict = {
        'brands' : [],
        'gens' : [],
        'accs' : [],
        'tops' : [],
        'mids' : [],
        'bases' : [],
        'allnotes' : [],
        'longs' : [],
        'sills' : [],
        'vals' : []
    }
    keylist = list(a.keys())
    
    for item in keylist:
        inpDict[item] = a.getlist(item)
        
    for i in range(len(inpDict['tops'])):
        inpDict['tops'][i] += ' (TOP)'
        
    for i in range(len(inpDict['mids'])):
        inpDict['mids'][i] += ' (MID)'
        
    for i in range(len(inpDict['bases'])):
        inpDict['bases'][i] += ' (BASE)'
        
    for i in range(len(inpDict['allnotes'])):
        inpDict['allnotes'][i] += ' (ALL)'
        
    if inpDict['allnotes'] != []:
        inpDict['tops'] = []
        inpDict['mids'] = []
        inpDict['bases'] = []
        
    return inpDict

def FragRecommender(graph, attributes):
    '''
    Get the list of fragrances (objects of the class Fragrance) containing only the given attributes.
    
    Parameters:
    1. graph: an object of the class Graph
    2. attributes: a dictionary of attributes
    
    Returns:
    subgraph: an object of the class Graph, containing only the attributes listed
    and the corresponding fragrances as its nodes.
    '''
    nodelist, namelist = FragNameNode(graph)
    
    if len(attributes) == 0:
        return nodelist
            
    pdict = {
        'brands' : [],
        'gens' : [],
        'accs' : [],
        'tops' : [],
        'mids' : [],
        'bases' : [],
        'allnotes' : [],
        'longs' : [],
        'sills' : [],
        'vals' : []
    }
    plist = []
    
    try:
        if attributes['brands'] == []:
            pdict['brands'] = namelist
        else:
            for item in attributes['brands']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['brands'].append(n)
    except:
        pdict['brands'] = namelist
        
        
    
    try:
        if attributes['gens'] == []:
            pdict['gens'] = namelist
        else:   
            for item in attributes['gens']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['gens'].append(n)
    except:
        pdict['gens'] = namelist
        
        
            
    try:
        if attributes['accs'] == []:
            pdict['accs'] = namelist
        else:
            for item in attributes['accs']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['accs'].append(n)
    except:
        pdict['accs'] = namelist
        
        
    
    try:
        if attributes['longs'] == []:
            pdict['longs'] = namelist
        else:
            for item in attributes['longs']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['longs'].append(n)
    except:
        pdict['longs'] = namelist
        
        
            
    try:
        if attributes['sills'] == []:
            pdict['sills'] = namelist
        else:
            for item in attributes['sills']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['sills'].append(n)
    except:
        pdict['sills'] = namelist
        
        
            
    try:
        if attributes['vals'] == []:
            pdict['vals'] = namelist
        else:
            for item in attributes['vals']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['vals'].append(n)
    except:
        pdict['vals'] = namelist
        
        
            
    try:
        if attributes['tops'] == []:
            pdict['tops'] = namelist
        else:
            for item in attributes['tops']:
                plist.append(item)
                pdict['tops'].append(list(graph.neighbors[item]))
            lt = pdict['tops'][0]
            for i in range(1, len(pdict['tops'])):
                lt = list(set(pdict['tops'][i])&set(lt))
            pdict['tops'] = lt
    except:
        pdict['tops'] = namelist
        
        
                
    try:
        if attributes['mids'] == []:
            pdict['mids'] = namelist
        else:
            for item in attributes['mids']:
                plist.append(item)
                pdict['mids'].append(list(graph.neighbors[item]))
            lt = pdict['mids'][0]
            for i in range(1, len(pdict['mids'])):
                lt = list(set(pdict['mids'][i])&set(lt))
            pdict['mids'] = lt
    except:
        pdict['mids'] = namelist
        
        
                
    try:
        if attributes['bases'] == []:
            pdict['bases'] = namelist
        else:
            for item in attributes['bases']:
                plist.append(item)
                pdict['bases'].append(list(graph.neighbors[item]))
            lt = pdict['bases'][0]
            for i in range(1, len(pdict['bases'])):
                lt = list(set(pdict['bases'][i])&set(lt))
            pdict['bases'] = lt
    except:
        pdict['bases'] = namelist
        
        
                
    try:
        if attributes['allnotes'] == []:
            pdict['allnotes'] = namelist
        else:
            for item in attributes['allnotes']:
                plist.append(item)
                pdict['allnotes'].append(list(graph.neighbors[item]))
            lt = pdict['allnotes'][0]
            for i in range(1, len(pdict['allnotes'])):
                lt = list(set(pdict['allnotes'][i])&set(lt))
            pdict['allnotes'] = lt
    except:
        pdict['allnotes'] = namelist
                
    names = list(set(pdict['brands'])&set(pdict['gens'])&set(pdict['accs'])&
                 set(pdict['longs'])&set(pdict['sills'])&set(pdict['vals'])&
                 set(pdict['tops'])&set(pdict['mids'])&set(pdict['bases'])&set(pdict['allnotes']))
    
    perfRec = []
    for item in names:
        perfRec.append(graph.nodes[item])
            
    return perfRec

def SubGraph(graph, attributes):
    '''
    Get a subgraph of the original graph containing only the attributes listed
    and the fragrances corresponding to them as its nodes.
    Similar to FragRecommender except this function returns an entire subgraph including
    both kinds of nodes - fragrances and attributes, and the edges connecting them.
    
    Parameters:
    1. graph: an object of the class Graph
    2. attributes: a dictionary of attributes
    
    Returns:
    subgraph: an object of the class Graph, containing only the attributes listed
    and the corresponding fragrances as its nodes.
    '''
    if len(attributes) == 0:
        return graph
    
    pdict = {
        'brands' : [],
        'gens' : [],
        'accs' : [],
        'tops' : [],
        'mids' : [],
        'bases' : [],
        'allnotes' : [],
        'longs' : [],
        'sills' : [],
        'vals' : []
    }
    plist = []
    
    try:
        if attributes['brands'] == []:
            pdict['brands'] = list(graph.nodes.keys())
        else:
            for item in attributes['brands']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['brands'].append(n)
    except:
        pdict['brands'] = list(graph.nodes.keys())
        
        
    
    try:
        if attributes['gens'] == []:
            pdict['gens'] = list(graph.nodes.keys())
        else:   
            for item in attributes['gens']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['gens'].append(n)
    except:
        pdict['gens'] = list(graph.nodes.keys())
        
        
            
    try:
        if attributes['accs'] == []:
            pdict['accs'] = list(graph.nodes.keys())
        else:
            for item in attributes['accs']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['accs'].append(n)
    except:
        pdict['accs'] = list(graph.nodes.keys())
        
        
    
    try:
        if attributes['longs'] == []:
            pdict['longs'] = list(graph.nodes.keys())
        else:
            for item in attributes['longs']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['longs'].append(n)
    except:
        pdict['longs'] = list(graph.nodes.keys())
        
        
            
    try:
        if attributes['sills'] == []:
            pdict['sills'] = list(graph.nodes.keys())
        else:
            for item in attributes['sills']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['sills'].append(n)
    except:
        pdict['sills'] = list(graph.nodes.keys())
        
        
            
    try:
        if attributes['vals'] == []:
            pdict['vals'] = list(graph.nodes.keys())
        else:
            for item in attributes['vals']:
                plist.append(item)
                for n in graph.neighbors[item]:
                    pdict['vals'].append(n)
    except:
        pdict['vals'] = list(graph.nodes.keys())
        
        
            
    try:
        if attributes['tops'] == []:
            pdict['tops'] = list(graph.nodes.keys())
        else:
            for item in attributes['tops']:
                plist.append(item)
                pdict['tops'].append(list(graph.neighbors[item]))
            lt = pdict['tops'][0]
            for i in range(1, len(pdict['tops'])):
                lt = list(set(pdict['tops'][i])&set(lt))
            pdict['tops'] = lt
    except:
        pdict['tops'] = list(graph.nodes.keys())
        
        
                
    try:
        if attributes['mids'] == []:
            pdict['mids'] = list(graph.nodes.keys())
        else:
            for item in attributes['mids']:
                plist.append(item)
                pdict['mids'].append(list(graph.neighbors[item]))
            lt = pdict['mids'][0]
            for i in range(1, len(pdict['mids'])):
                lt = list(set(pdict['mids'][i])&set(lt))
            pdict['mids'] = lt
    except:
        pdict['mids'] = list(graph.nodes.keys())
        
        
                
    try:
        if attributes['bases'] == []:
            pdict['bases'] = list(graph.nodes.keys())
        else:
            for item in attributes['bases']:
                plist.append(item)
                pdict['bases'].append(list(graph.neighbors[item]))
            lt = pdict['bases'][0]
            for i in range(1, len(pdict['bases'])):
                lt = list(set(pdict['bases'][i])&set(lt))
            pdict['bases'] = lt
    except:
        pdict['bases'] = list(graph.nodes.keys())
        
        
                
    try:
        if attributes['allnotes'] == []:
            pdict['allnotes'] = list(graph.nodes.keys())
        else:
            for item in attributes['allnotes']:
                plist.append(item)
                pdict['allnotes'].append(list(graph.neighbors[item]))
            lt = pdict['allnotes'][0]
            for i in range(1, len(pdict['allnotes'])):
                lt = list(set(pdict['allnotes'][i])&set(lt))
            pdict['allnotes'] = lt
    except:
        pdict['allnotes'] = list(graph.nodes.keys())
                
    names = list(set(pdict['brands'])&set(pdict['gens'])&set(pdict['accs'])&
                 set(pdict['longs'])&set(pdict['sills'])&set(pdict['vals'])&
                 set(pdict['tops'])&set(pdict['mids'])&set(pdict['bases'])&set(pdict['allnotes']))
    
    subgraph = Graph()
    for item in plist:
        val = graph.nodes[item]
        subgraph.addNode(item,val)
        
    for item in names:
        val = graph.nodes[item]
        subgraph.addNode(item,val)
        
    for i in plist:
        for j in names:
            subgraph.addEdge(i,j)
            
    return subgraph
