#!/usr/bin/env python3
# -*- coding: utf-8 -*- #
# Description: Generate a JSON file containing a list of 
# notable people who studied at University of Strasbourg
# Author: Samuel Guebo
# Licence: MIT

import aiohttp
import async_timeout
import asyncio
from bs4 import BeautifulSoup
import json
import os
import urllib.parse
import re
import requests

async def async_fetch(url):
    async with aiohttp.ClientSession() as session:
        async with async_timeout.timeout(20):
            async with session.get(url) as response:
                return await response.text()


def export_alumni(nodes):
    """ Create a JSON file with all alumni names """

    f = open("data/alumni.json", "w+")
    f.write(json.dumps(nodes))
    f.close()


def generate_wikidata_query():
    """ Loads a Sparql query from a file """
    
    query = ""
    wikidata_file = "data/wikidata-query.rd"
    try:
        f = open(wikidata_file)
        query = f.read()
        f.close()
    except:
        pass
    
    return query
    

async def fetch_alumni(query):
    wiki = "https://en.wikipedia.org/"
    alumni = []
    endpoint_url = "https://query.wikidata.org/sparql?query="

    request_url = endpoint_url + urllib.parse.quote(query)
    request_url += "&format=json&redirects=1"

    results = requests.get(request_url)
    results = json.loads(results.content)["results"]["bindings"]
    
    # restructure array
    for student in results:
        if len(student["fullname"]["value"]) > 0:
            url = wiki + "w/api.php?action=parse&format=json&page=" + student["fullname"]["value"] + "&prop=text"
            
            wiki_article = await async_fetch(url)
            json_output = json.loads(wiki_article)
            
            # Filter erroneous links out
            if("parse" in json_output):
                html_text = json.loads(wiki_article)["parse"]["text"]["*"]
                parser = BeautifulSoup(html_text, 'html.parser')
                student_biography = parser.p.getText()
                
                # Exclude bios that are too short
                if(len(student_biography) > 10):
                    alumni.append({
                        "fullname": student["fullname"]["value"],
                        "photo": student["photo"]["value"],
                        "occupations": student["occupations"]["value"],
                        "birthyear": student["birthyear"]["value"],
                        "biograhy": student_biography,
                        "article": student["article"]["value"],
                    })
        
    return alumni

# Async task
wikidata_query = generate_wikidata_query()
loop = asyncio.get_event_loop()
results = loop.run_until_complete(fetch_alumni(wikidata_query))

# Save to JSON file
export_alumni(results)
