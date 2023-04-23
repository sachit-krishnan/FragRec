#############################################
##### Name: Sachit Krishnan #################
##### Uniqname: sachit ######################
##### UMID: 30156124 ########################
#############################################
#############################################

import requests
import json
import flask
from flask import Flask, render_template, request

from classes import *
from datahandling import *
from scraping import *

# GLOBAL VARIABLES
app = Flask(__name__)
dataPath = "data/PerfumesFinal.json"
graphPath = "data/fragraph.json"
templatePath = 'index.html'

#Crawling Fragrantica and scraping data
#Increase the value of the int 'lim_dat' to scrape more results.
#Remove comments and run.

#lim_dat = 3
#b1 = pageSetup()
#u1 = getURLs(b1)
#d1 = fragScrape(u1[:lim_dat])
#fdict = []
#for i in range(len(d1)):
#    fdict.append(FragDict(d1[i]))
#d2save = notesaccordsLower(fdict)

#Save the data by calling save_cache(d2save, dataPath)

#Loading fragrance data from the cache and creating a list of objects of the class 'Fragrance'
cachedData = open_cache(dataPath)
frag = []
for i in range(len(cachedData)):
    frag.append(Fragrance(load_cache(cachedData, i)))

fd = inputAttributes(frag)

#Loading the graph from the cache and creating an object of the class 'Graph'
graph = GraphConstruct(graphPath)

# HTML template rendering using Flask
@app.route('/')
def inputPage():
    return render_template(templatePath, fd = fd, result_list=None) 

@app.route('/outputPage', methods=["POST"])
def outputPage():
    
    rawinp = request.form
    inpDict = formParse(rawinp)
    outHTML = outputHTML(inpDict, graphPath)    
    
    return render_template(templatePath, fd = fd, result_list=outHTML)

if __name__ == '__main__':
    app.run()
