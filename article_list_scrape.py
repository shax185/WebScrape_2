#!/usr/bin/env python

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import requests
import time
import datetime
import string
import re
import json
import collections
import time
import os
#import utility
from bs4 import BeautifulSoup
#from utility import write_log
#from util import write_log
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

code_path = os.path.abspath(os.path.dirname(__file__))
#data_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data/mt')
data_path = 'D:\webscrape\data'

file1 = open("D:\webscrape\Article_list.txt","r+")
data = file1.read()
#print(data)
a=data.split('\n')
#print(a)

for i in a:
    #print("i: ",i)
    web_page = urlopen(i)
    soup = BeautifulSoup(web_page, 'html.parser')
    #print("Soup: ",soup)
    #for para in soup.findAll("div", {"class" : "seolocation"}):
    for para in soup.findAll('a'):
        x=para.get('href')
        
        if ".cms" in x:
            print ("Link: ",x)
            file2 = open("Article_list_new1.txt","a",encoding="utf-8")
            file2.write(x)
            file2.write("\n")
            file2.close()
        else:
            print("Nothing")


