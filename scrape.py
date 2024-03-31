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
data_path = 'F:\webscrape\data'

file1 = open("F:\webscrape\Article_content3.txt","r+")
data = file1.read()
#print(data)
a=data.split('\n')
#print(a)

for i in a:
    #print(i)
    web_page = urlopen(i)
    soup = BeautifulSoup(web_page, 'html.parser')
    for para in soup.findAll("div", {"class" : "full_article"}):
        x=para.text
        print ("Content: ",para.text)
        file1 = open("myfile20.txt","a",encoding="utf-8")
        file1.write(x)
        file1.close()


