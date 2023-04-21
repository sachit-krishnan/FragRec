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

from classes import *
from datahandling import *

def activateBrowser():
    '''
    Initialize the browser (Google Chrome).
    
    Parameters:
    None
    
    Returns:
    Open browser
    '''
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def pageSetup():
    '''
    Load the search page on Fragrantica.com and set it up to obtain URLs of the perfume pages.
    
    By default, the Fragrantica search page displays only 30 listings.
    Initially I had implemented crawling, which automated the clicking of 'See more perfumes'.
    Unfortunately, the page would sometimes be redirected to a 'Verify you are human' page.
    Hence, I ditched the crawling and decided to collect URLs of the perfume pages and automated their scraping.
    Once the user calls this function, he/she is requested to manually select 'See more perfumes'
    on the search page to maximize the number of URLs collected. Each click adds 30 listings.
    
    Parameters:
    None
    
    Returns:
    browser: Active Chrome WebDriver
    '''
    browser = activateBrowser()
    url = "https://www.fragrantica.com/search/"
    browser.visit(url)
    
    return browser

def getURLs(browser):
    '''
    Get a list of URLs of perfume pages on Fragrantica to scrape.
    
    Call this function after manually selecting 'See more perfumes' on the Fragrantica search page.
    
    By default, the Fragrantica search page displays only 30 listings.
    Initially I had implemented crawling, which automated the clicking of 'See more perfumes'.
    Unfortunately, the page would sometimes get redirected to a 'Verify you are human' page.
    Hence, I ditched the crawling and decided to collect URLs of the perfume pages and scrape them sequentially.
    
    Parameters:
    browser: Active Chrome WebDriver
    
    Returns:
    URLs: list of URLs of perfume pages on Fragrantica
    '''
    html = browser.html
    soup = bs(html, "html.parser")
    links = soup.find_all('div', class_='card-section')
    URLs = []
    for i in range(int(len(links)/2)):
        URLs.append(links[2*i + 1].a['href'])
        
    return URLs

def fragScrape(urls):
    '''
    Scrape perfume pages on Fragrantica to obtain fragrance data.
    
    Parameters:
    1. urls: list of URLs obtained from getURLs()
    
    Returns:
    perfumesDict: list of dictionaries containing the scraped, unprocessed perfume data
    '''
    perfumesDict = []
    
    for i in range(len(urls)):
        
        browser = activateBrowser()
        url = urls[i]
        
        try:
            browser.visit(url)
        except:
            break
        
        html = browser.html
        soup = bs(html, "html.parser")
        
        #Getting the fragrance name
        name = soup.find_all("div", class_="cell small-12")[3].find_all("b")[0].get_text()
        
        #Getting the fragrance brand
        brand = soup.find_all("div", class_="cell small-12")[3].find_all("b")[1].get_text()
        
        #Getting the targeted/suggested fragrance gender
        gender = soup.find("small").get_text()

        #Getting the main accords of the fragrance
        try:
            main_accords = soup.find_all("div", class_="cell accord-box")
            accords_dict = {}
            for m in range(len(main_accords)):
                accord_name = main_accords[m].get_text()
                accord_value = float(main_accords[m].find("div", class_="accord-bar")["style"].rsplit("width: ")[1].strip("%;"))
                accords_dict[accord_name] = accord_value
        except:
            accords_dict = {}
            print(f"{name} has no accords.")

        #Getting the fragrance notes
        notes = soup.find_all("div", attrs={"style": "display: flex; justify-content: center; text-align: center; flex-flow: row wrap; align-items: flex-end; padding: 0.5rem;"})

        if len(notes) == 3:
            number = 2
            top_notes_list = []
            middle_notes_list = []
            base_notes_list = []

            for n in range(len(notes[0].find_all("span", class_="link-span"))):
                top_notes_list.append(notes[0].find_all("div")[number].get_text())
                number += 3

            number = 2
            for p in range(len(notes[1].find_all("span", class_="link-span"))):
                middle_notes_list.append(notes[1].find_all("div")[number].get_text())
                number += 3

            number = 2
            for q in range(len(notes[2].find_all("span", class_="link-span"))):
                base_notes_list.append(notes[2].find_all("div")[number].get_text())
                number += 3
                
        elif len(notes) == 2:
            number = 2
            top_notes_list = []
            middle_notes_list = []
            base_notes_list = []

            for r in range(len(notes[0].find_all("span", class_="link-span"))):
                top_notes_list.append(notes[0].find_all("div")[number].get_text())
                number += 3

            number = 2
            for s in range(len(notes[1].find_all("span", class_="link-span"))):
                middle_notes_list.append(notes[1].find_all("div")[number].get_text())
                number += 3
                
        elif len(notes) == 1:
            number = 2
            top_notes_list = []
            middle_notes_list = []
            base_notes_list = []

            for v in range(len(notes[0].find_all("span", class_="link-span"))):
                middle_notes_list.append(notes[0].find_all("div")[number].get_text())
                number += 3
                
        else:
            top_notes_list = []
            middle_notes_list = []
            base_notes_list = []
        
        #Getting the fragrance rating and number of votes
        try:
            rating = float(soup.find("p", class_="info-note").find_all("span")[0].get_text())
            votes = int(soup.find("p", class_="info-note").find_all("span")[2].get_text().replace(',', ''))
        except:
            rating = 0
            votes = 0
            print(f"{name} does not have a ranking")

        #Getting the public votes
        voting = soup.find_all("div", class_="cell small-1 medium-1 large-1")

        #Getting the votes on the fragrance longevity
        long_v_weak = int(voting[0].get_text())
        long_weak = int(voting[1].get_text())
        long_moderate = int(voting[2].get_text())
        long_long_last = int(voting[3].get_text())
        long_eternal = int(voting[4].get_text())

        #Getting the votes on the fragrance sillage
        sill_intimate = int(voting[5].get_text())
        sill_moderate = int(voting[6].get_text())
        sill_strong = int(voting[7].get_text())
        sill_enormus = int(voting[8].get_text())

        #Getting the votes on the fragrance price value
        value_w_over = int(voting[14].get_text())
        value_over = int(voting[15].get_text())
        value_ok = int(voting[16].get_text())
        value_good = int(voting[17].get_text())
        value_great = int(voting[18].get_text())
        
        #Getting the link for a picture of the fragrance
        pic = soup.find_all("div", class_="cell small-12")[1].find("img")["src"]
        
        #Getting the description of the fragrance
        try:
            description = soup.find_all("div", class_="cell small-12")[3].get_text()
        except:
            description = "NA"
            print(f"{name} does not have a description.")

        #Loading the perfume data into a dictionary
        perfume_dict = {"name": name,
                        "brand": brand,
                        "gender": gender,
                        "rating": rating,
                        "votes": votes,
                        "accords": accords_dict,
                        "top": top_notes_list,
                        "mid": middle_notes_list,
                        "base": base_notes_list,
                        "longevity":   {"very weak": long_v_weak,
                                        "weak": long_weak,
                                        "moderate": long_moderate,
                                        "long lasting": long_long_last,
                                        "eternal": long_eternal},
                        "sillage":     {"intimate": sill_intimate,
                                        "moderate": sill_moderate,
                                        "strong": sill_strong,
                                        "enormous": sill_enormus},
                        "value": {"way overpriced": value_w_over,
                                        "overpriced": value_over,
                                        "ok": value_ok,
                                        "good value": value_good,
                                        "great value": value_great},
                        "pic": pic,
                        "description": description}

        perfumesDict.append(perfume_dict)
        time.sleep(120)
    
    return perfumesDict

def FragDict(data):
    '''
    Function to process the scraped perfume data (one data point at a time).
    
    Parameters:
    data: Unprocessed, scraped perfume data (dict)
    
    Returns:
    fragdict: Processed perfume data ready to be saved in a JSON cache (dict)
    '''
    fragdict = {}
    
    fragdict['name'] = data['name']
    fragdict['brand'] = data['brand']
    fragdict['gender'] = data['gender']
    fragdict['accords'] = data['accords']
    fragdict['top'] = data['top']
    fragdict['mid'] = data['mid']
    fragdict['base'] = data['base']
    fragdict['rating'] = data['rating']
    fragdict['votes'] = data['votes']
    
    for j, val in data['longevity'].items():
        if val == max(data['longevity'].values()):
            break
    fragdict['longevity'] = j
    
    for j, val in data['sillage'].items():
        if val == max(data['sillage'].values()):
            break
    fragdict['sillage'] = j
    
    for j, val in data['value'].items():
        if val == max(data['value'].values()):
            break
    fragdict['value'] = j
    
    fragdict['pic'] = data['pic']
    fragdict['description'] = data['description'].split(sep = 'Read about this')[0][:-1]
        
    return fragdict

def notesaccordsLower(data):
    '''
    Turns all the frangrance notes into lower case and load in a dictionary to save in a JSON cache for later use.
    
    Parameters:
    data: list of dictionaries of processed perfume data
    
    Returns:
    data: Same data with fragrance notes in lower case, to be saved in a JSON cache.
    '''
    for i in range(len(data)):
        for j in range(len(data[i]['top'])):
            data[i]['top'][j] = data[i]['top'][j].lower()
        for j in range(len(data[i]['mid'])):
            data[i]['mid'][j] = data[i]['mid'][j].lower()
        for j in range(len(data[i]['base'])):
            data[i]['base'][j] = data[i]['base'][j].lower()
            
    return data
