#!/usr/bin/env python

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
from datetime import date


today = date.today()
today=str(today)

code_path = os.path.abspath(os.path.dirname(__file__))
#data_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data/mt')
data_path = 'D:\webscrape\data'

URL='https://www.bhaskar.com/'
def get_article_from_url(article_url):
    response = requests.get(article_url)
    if response.status_code==404:
        return -1

    html = str(BeautifulSoup(response.content))
    soup=BeautifulSoup(html,"html.parser")
    metadata={}
    article = collections.OrderedDict()

    source_type='news_article'
    source_name='maharashtratimes.com'


    for anchor in soup.select('a'):
        anchor.unwrap()

    for title in soup.find_all('title'):
        title=str(title)
        title=re.sub('</title>', '', title)
        title=re.sub('<title>', '', title)
        title=re.sub(' - Times of India', '', title)
        title=re.sub('\|.*', '', title)
        title=title.strip()
        metadata['title']=title


    for meta in soup.find_all('meta'):
        attrs=meta.attrs
        if('description' in attrs.values()):
            metadata['desc']=str(attrs["content"])


        if('datePublished' in attrs.values()):
            metadata['date_published']=str(attrs["content"])


        if('dateModified' in attrs.values()):
            metadata['date_modified']=str(attrs["content"])

        if('Last-Modified-Date' in attrs.values()):
            metadata["date_modified"]=str(attrs["content"])

        if('Last-Modified-Time' in attrs.values()):
            metadata["date_modified"]=str(attrs["content"])

        if('og:type' in attrs.values()):
            metadata['og_type']=str(attrs["content"])

        if('og:image' in attrs.values()):
            metadata['image_link']=str(attrs["content"])

        if('articleSection' in attrs.values()):
            metadata['article_section']=str(attrs["content"])

        if('news_keywords' in attrs.values()):
            metadata['article_keywords']=str(attrs["content"])

    for div in soup.select('div'):
        div.unwrap()

    for div in soup.select('meta'):
        div.unwrap()

    for strr in soup.find_all('arttextxml'):
        print('for executing')
        s = re.sub('<a class=.*\">', '', str(strr))
        s = re.sub('</a>', '', s)
        s = re.sub('<br>', '', s)
        s = re.sub('<br/>', '', s)
        s = re.sub('</br>', '', s)
        s = re.sub('<p>', '', s)
        s = re.sub('<p/>', '', s)
        s = re.sub('</p>', '', s)
        s = re.sub('<arttextxml>', '', s)
        s = re.sub('</arttextxml>', '', s)
        s = re.sub('[\n]+', '\n', s)
        body=s
        metadata['article_body']=body
        break

    patterns = re.search('[0-9][0-9][0-9][0-9][0-9]+', article_url)
    if patterns:
        articleid = patterns.group(0)
        metadata['article_id']=articleid
    else:
        metadata['article_id']='dummy_id'

    article['source_type'] = source_type
    article['source_name'] = source_name

    if('title' in metadata.keys()):
        article['title'] = metadata['title']
    else:
         article['title'] = 'dummy_title'

    article['source_article_id'] = metadata['article_id']
    article['id'] = metadata['article_id']

    if('date_published' in metadata.keys()):
        article['date_published'] = metadata['date_published']
    else:
         article['date_published'] = str(datetime.datetime.now())

    if('image_link' in metadata.keys()):
        article['image_link'] = metadata['image_link']
    else:
         article['image_link'] = 'dummy_link'

    if('description' in metadata.keys()):
        article['description'] = metadata['desc']
    else:
         article['description'] = 'dummy_desc'

    article['source_article_link'] = article_url

    if('article_body' in metadata.keys()):
        article['article_body'] = metadata['article_body']
    else:
         article['article_body'] = 'dummy_body'

    return article

def get_all_urls_from_homepage(homepage_url):
    urls={}
    url=homepage_url
    response = requests.get(url)
    if response.status_code==404:
        return None
    html = str(BeautifulSoup(response.content))
    soup=BeautifulSoup(html,"html.parser")
    for a in soup.find_all('a'):
        attrs=a.attrs
        url=str(a.get('href'))
        if url:
            patterns = re.search('[0-9][0-9][0-9][0-9][0-9]+', url)
            if (patterns and ('mobileapplist' not in url) and ('photo-features' not in url) and ('photostory' not in url) and ('humour' not in url) and ('debateshow' not in url)):
                if(url.startswith("https://www.bhaskar.com/")):
                    urls[url]=url
                if(url.startswith("/")):
                    url="https://www.bhaskar.com/"+url
    return urls

def url_absent(url):
    print('error')
continue_scan = True
curr_page = 1
total_articles_scraped = 0

#Home page to scrape off article links
while continue_scan:
    homepage_url = URL
    urls_on_homepage=get_all_urls_from_homepage(homepage_url)
    if(urls_on_homepage is None):
        print('Error while fetching urls from the home')
    else:
        for url in urls_on_homepage.values():

                print('Downloading ' + url)
                article=get_article_from_url(url)
                print('article downloaded'+'\n')
                article_link = article['source_article_link']
                articleid = article_link[article_link[:-1].rfind('/') + 1:-1]
                print(articleid)
                article_filename = articleid[:12] + '.json'
                print(article_filename)
                with open(data_path + "/" + article_filename, 'w') as f:
                    f.write(json.dumps(article, indent=4))
                    f.close()
                with open(code_path + "/data/" + today + 'mt_downloaded_urls.txt' , 'a+') as f:
                    f.write(url+"\n")
                    f.close()

        print('error')
        break
