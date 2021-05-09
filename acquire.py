#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from requests import get
from bs4 import BeautifulSoup
import os
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def make_soup(url):
    '''
    The function takes in a url and requests and parses HTML
    returning a soup object.
    '''
    headers = {'User-Agent': 'Codeup Data Science'} 
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

urls = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
        'https://codeup.com/data-science-myths/',
        'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
        'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
        'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_blog_articles(urls, cached=False):
    '''
    This function takes in a list of blog urls and a parameter
    with default cached == False which scrapes the title and text for each url, 
    creates a list of dictionaries with the title and text for each blog, 
    converts list to df, and returns df.
    If cached == True, the function returns a df from the json file.
    '''
    if cached == True:
        df = pd.read_json('codeup_blogs.json')
        
    # cached == False completes a fresh scrape for df     
    else:

        # Create an empty list to hold dictionaries
        articles = []

        # Loop through each url in our list of urls
        for url in urls:

            # Make request and soup object using helper
            soup = make_soup(url)

            # Save the title of each blog in variable title
            title = soup.find('h1').text

            # Save the text in each blog to variable text
            content = soup.find('div', class_="jupiterx-post-content").text

            # Create a dictionary holding the title and content for each blog
            article = {'title': title, 'content': content}

            # Add each dictionary to the articles list of dictionaries
            articles.append(article)
            
        # convert our list of dictionaries to a df
        df = pd.DataFrame(articles)

        # Write df to a json file for faster access
        df.to_json('codeup_blogs.json')
    
    return df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

urls_2 = ['https://www.reuters.com/world/india/india-take-back-illegal-migrants-uk-return-visas-young-workers-2021-05-04/?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts', 
        'https://www.businessinsider.in/stock-market/news/an-anonymous-crypto-advocate-projected-messages-championing-bitcoin-on-the-walls-of-the-bank-of-england-and-the-uk-parliament/amp_articleshow/82386813.cms?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts',

        'https://www.businessinsider.in/stock-market/news/much-wow-dogecoin-jumps-26-to-record-high-after-etoro-exchange-adds-the-token-for-its-20-million-users/amp_articleshow/82388830.cms?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts',
        'https://techcrunch.com/2021/05/04/twitter-acquires-distraction-free-reading-service-scroll-to-beef-up-its-subscription-product/amp/?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts','https://yourstory.com/2021/05/accenture-pledges-25-million-dollar-covid19-india/amp?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts']

# news = get_bfp_news_articles(urls=urls, cached=False)


def get_news_articles(cached=False):
    '''
   When cached == False, the function does a fresh scrape of inshort pages with topics 
    business, sports, technology, and entertainment and writes the returned df to a json file.
    cached == True returns a df read in from the json file.
    '''
    # option to read in a json file instead of scrape for df
    if cached == True:
        df = pd.read_json('news_articles.json')
        
    # cached == False completes a fresh scrape for df    
    else:
    
        # Set base_url that will be used in get request
        base_url = 'https://inshorts.com/en/read/'
        
        # List of topics to scrape
        topics = ['business', 'sports', 'technology', 'entertainment']
        
        # Create an empty list, articles, to hold our dictionaries
        articles = []

        for topic in topics:
            
            # Create url with topic endpoint
            topic_url = base_url + topic
            
            # Make request and soup object using helper
            soup = make_soup(topic_url)

            # Scrape a ResultSet of all the news cards on the page
            cards = soup.find_all('div', class_='news-card')

            # Loop through each news card on the page and get what we want
            for card in cards:
                title = card.find('span', itemprop='headline' ).text
                author = card.find('span', class_='author').text
                content = card.find('div', itemprop='articleBody').text

                # Create a dictionary, article, for each news card
                article = ({'topic': topic, 
                            'title': title, 
                            'author': author, 
                            'content': content})

                # Add the dictionary, article, to our list of dictionaries, articles.
                articles.append(article)
            
        # Create a DataFrame from list of dictionaries
        df = pd.DataFrame(articles)
        
        # Write df to json file for future use
        df.to_json('news_articles.json')
    
    return df

