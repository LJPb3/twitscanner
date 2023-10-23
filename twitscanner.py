# *- coding: utf-8 -*
##TWScan by [Redacted]##
##v1. Made with love and confusion in april of 2021##
#Get tweet locations, sources and pictures, get tweets that match a keyword, save all tweets from user to csv.
import sys
import os
import requests
import csv
import tweepy
from colorama import Fore, Style

consumer_key = "YOUR CONSUMER KEY HERE"
consumer_secret = "YOUR CONSUMER SECRET HERE"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

def usage(): ##Show help
    print(Fore.RED + Style.BRIGHT + "TWScan V1 by Replica")
    print("Drink coke, code away." + Style.NORMAL)
    print(Fore.BLUE + "The options are:")
    print(Fore.BLUE + "\t -h " + Fore.RESET + "Show these instructions")
    print(Fore.BLUE + "\t -l " + Fore.RESET + "Get locations where user has tweeted")
    print(Fore.BLUE + "\t -o " + Fore.RESET + "Get sources from where user has tweeted")
    print(Fore.BLUE + "\t -k " + Fore.RESET + "Get tweets from user that cointain a keyword")
    print(Fore.BLUE + "\t -s " + Fore.RESET + "Save tweets from user to cvs")
    print(Fore.BLUE + "\t -m " + Fore.RESET + "Save photos tweeted from user")
    print(Fore.BLUE + "Example:" + Fore.RESET)
    print("\t python %s " % str(sys.argv[0]) + Fore.BLUE + "-l " + Fore.RESET + Style.BRIGHT + "UserHandle" + Style.NORMAL)
    print("\t python %s " % str(sys.argv[0]) + Fore.BLUE + "-s " + Fore.RESET + Style.BRIGHT + "UserHandle" + Style.NORMAL)
    print("\t python %s " % str(sys.argv[0]) + Fore.BLUE + "-k " + Fore.RESET + Style.BRIGHT + "UserHandle " + Fore.CYAN + "Keyword" + Fore.RESET + Style.NORMAL)

def getthem(userhandle): ##Get all user tweets
    print(Style.BRIGHT + "Collecting all tweets...")
    alltweets = []
    new_tweets = api.user_timeline(userhandle)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
          new_tweets = api.user_timeline(screen_name = userhandle,count=200,max_id=oldest)
          alltweets.extend(new_tweets)
          oldest = alltweets[-1].id - 1
    print("All tweets collected" + Style.NORMAL)
    return alltweets ##return tweets to further process

def locations(userhandle): ##User locations
    alltweets = getthem(userhandle)
    print(Style.BRIGHT + "Getting locations..." + Style.NORMAL)
    for status in alltweets:
        if status.place != None: ##Gets rid of tweets with no location
           print(Style.BRIGHT + "Date: " + Style.NORMAL + str(status.created_at) + Style.BRIGHT + " Source: " + Style.NORMAL + status.source)
           print(Style.BRIGHT + "Country: " + Style.NORMAL + status.place.country + Style.BRIGHT + " Type: " + Style.NORMAL + status.place.place_type + Style.BRIGHT + " Name: " + Style.NORMAL + status.place.full_name)
           print(Style.BRIGHT + "Coordinates: " + Style.NORMAL + str(status.coordinates) + Style.BRIGHT + " Geo: " + Style.NORMAL + str(status.geo))
           print('='*10)
    sys.exit()

def sources(userhandle): ##Gets all sources from where the user has tweeted; web, android, iphone, etc.
    alltweets = getthem(userhandle)
    print(Style.BRIGHT + "Getting sources used..." + Style.NORMAL)
    tweeted_from = []
    for status in alltweets:
        if status.source not in tweeted_from:
           tweeted_from.append(status.source)
           print(status.source)
           print('='*10)
    sys.exit()

def keyword(userhandle, keyword): ##Get all tweets with keyword in them
    alltweets = getthem(userhandle)
    print(Style.BRIGHT + "Searching " + keyword + " in " + userhandle + Style.NORMAL)
    for status in alltweets:
        if keyword in status.text:
           print(Style.BRIGHT + "Date :" + Style.NORMAL + str(status.created_at))
           print(status.text)
           print("="*10)
    sys.exit()

def save(userhandle): ##Save all tweets to csv, containing date, text, source and location if available
    alltweets = getthem(userhandle)
    print(Style.BRIGHT + "Saving data to csv..." + Style.NORMAL)
    csvfile = open('%s.csv' % userhandle, 'w', encoding='utf-8', newline='') #Creates csv file named after user
    writer = csv.writer(csvfile)
    writer.writerow(['Date', 'Source', 'Text', 'Location'])
    for status in alltweets:
        if status.place != None: #To diferentiate if location is available or not to save
           writer.writerow([str(status.created_at), status.source, status.text, str(status.place.country + "-" + status.place.full_name)])
        else:
           writer.writerow([str(status.created_at), status.source, status.text, 'No location detected'])
    sys.exit()

def mediasave(userhandle): ##Save all photos in folder named after user
    alltweets = getthem(userhandle)
    print(Style.BRIGHT + "Saving media to folder..." + Style.NORMAL)
    if os.path.isdir(userhandle):
       pass
    else:
       os.mkdir(userhandle)
    for status in alltweets:
        if hasattr(status, 'extended_entities'): ##Check if photo in tweet
           if status.extended_entities["media"][0]["type"] == "photo":
              pic_url = status.extended_entities["media"][0]["media_url"]
              pic_data = requests.get(pic_url).content
              savepath = ('./' + userhandle + '/' + pic_url[27:])
              with open(savepath, 'wb') as handler:
                   handler.write(pic_data)
    sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    else:
       if sys.argv[1] == "-h":
          usage()
       if sys.argv[1] == "-l":
          locations(sys.argv[2])
       if sys.argv[1] == "-o":
          sources(sys.argv[2])
       if sys.argv[1] == "-k":
          keyword(sys.argv[2], sys.argv[3])
       if sys.argv[1] == "-s":
          save(sys.argv[2])
       if sys.argv[1] == "-m":
          mediasave(sys.argv[2])
       else:
         print(Fore.RED + Style.BRIGHT + "Quad the fuck?")
