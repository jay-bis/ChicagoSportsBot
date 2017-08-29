"""
This is a Reddit bot built for personal use.  It takes twitter posts from
r/chicagobulls and r/CHIBears, and pastes the contents into a text file.
"""

from bs4 import BeautifulSoup

import praw
import time
import requests


path = 'C:/Users/jbiscupski/Desktop/Coding/RedditBearsBot/'


def authenticate():
    """
    Authenticates your reddit bot for PRAW use.
    Inputs: Client ID, client secret, username, password, user agent (hardcoded or through a praw.ini config file)
    Outputs: A 'reddit' instance
    """
    
    print('Authenticating...\n')
    #personal info goes into X'ed out forms
    reddit = praw.Reddit(client_id='XXXXXXX', client_secret='XXXXXXXX', password='XXXXXXXX', username='XXXXXXXX', user_agent ='XXXXXXX')
    print('Authenticated as {}...\n'.format(reddit.user.me()))
    return reddit

def fetchdata(url):
    """
    This simple function scrapes data from twitter posts in a human-readable format.  Currently works with twitter posts only.
    Inputs: A twitter URL.
    Outputs: A readable string (twitter post content)
    """
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    text_data = soup.title.string
    return text_data

def run_chicagobot(reddit):
    """
    This function runs your bot.  Searches through my favorite Chicago subreddits (r/CHIBears and r/chicagobulls) for
    twitter urls, runs them through my fetchdata function, and outputs unique ID's and post content to two separate text files.
    Inputs: the 'reddit' instance
    Outputs: Two text files
    """
    
    #this for loop uses PRAW's methods and the 'reddit' instance to look through new posts in each subreddit
    for post in reddit.subreddit('CHIBears+chicagobulls').new(limit=20):
        if 'https://twitter.com/' in post.url:
            twitter_url = str(post.url)
            post_id = twitter_url.replace('https://twitter.com/', '')
            
            try:
                content = fetchdata(twitter_url)
            except:
                print('Possible broken or wrong link.\n')
            else:
            
                file_obj_urls = open('postIDs.txt', 'r')
                if post_id not in file_obj_urls.read().splitlines():
                    file_obj_urls.close()
                    file_obj_urls_writing = open('postIDs.txt', 'a+')
                    file_obj_urls_writing.write(post_id + '\n')
                    file_obj_urls_writing.close()
                    file_obj_content = open('twitter.txt', 'a+')
                    file_obj_content.write(content + '\n')
                    file_obj_content.close()
                else:
                    print('Repeat link, no need to post twitter content.')
        time.sleep(5)
    print('Waiting 5 minutes...\n')
    time.sleep(300)
    
def main():
    reddit = authenticate()
    while True:
        run_chicagobot(reddit)
        
if __name__ == '__main__':
    main()
