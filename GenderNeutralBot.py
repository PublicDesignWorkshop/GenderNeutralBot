from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint
import time

import csv
import datetime

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#dictionary of words to replace
replace = { 
            "boy": "person",
            "boys": "people",
            "boyfriend": "partner",
            "bro": "sib",
            "brother": "sibling",
            "brothers": "siblings",
            "dad": "parent",
            "dads": "parents",
            "daughter": "child",
            "daughters": "children",
            "gal": "person",
            "girl": "person",
            "girls": "people",
            "girlfriend": "partner",
            "guy": "person",
            "he": "they",
            "him": "them",
            "his": "their",
            "husband": "partner",
            "lady": "person",
            "she": "they",
            "her": "them",
            "man": "person",
            "men": "people",
            "mom": "parent",
            "moms": "parents",
            "mother": "parent",
            "mothers": "parents",
            "sis": "sib",
            "sister": "sibling",
            "sisters": "siblings",
            "son": "child",
            "sons": "children",
            "wife": "partner",
            "woman": "person",
            "women": "people"
            }

name = '@GendrNeutralBot'


def getFollowers():
    """
    Gets details about followers of the bot
    """

    names = []                  #Name of follower
    usernames = []              #Username of follower
    ids = []                    #User id of follower
    locations = []              #Location of follower(as listed on their profile)
    follower_count = []         #How many followers the follower has
    time_stamp = []             #Date recorded

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")


    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    follower_count.append("# of their Followers")
    time_stamp.append("Time Stamp")

    next_cursor = -1

    #Get follower list (200)
    while(next_cursor):
        get_followers = twitter.get_followers_list(screen_name=name,count=200,cursor=next_cursor)
        for follower in get_followers["users"]:
            try:
                print(follower["name"].encode("utf-8").decode("utf-8"))
                names.append(follower["name"].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't Print")
            usernames.append(follower["screen_name"].encode("utf-8").decode("utf-8"))
            ids.append(follower["id_str"])

            try:
                print(follower["location"].encode("utf-8").decode("utf-8"))
                locations.append(follower["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't Print")

            follower_count.append(follower["followers_count"])
            time_stamp.append(datestamp)
            next_cursor = get_followers["next_cursor"]

    open_csv = open("followers.csv","r",newline='')                         #Read what has already been recorded in the followers file
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))

    rows = zip(names,usernames,ids,locations,follower_count,time_stamp)     #Combine lists

    oldFollowerIDs = []                                                     #Store followers that have already been recorded in the past

    oldFollowers_csv = csv.reader(open_csv)

    for row in oldFollowers_csv:
            oldFollowerIDs.append(row[2])

    open_csv.close()

    open_csv = open("followers.csv","a", newline='')        #Append new followers to the followers file
    followers_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[2] in oldFollowerIDs):                  #if the ID isn't already in the follower list
            followers_csv.writerow(row)

    open_csv.close()

def getMentionsRetweets():
    """
    Gets details of mentions/retweets of the user
    """

    names = []                  #Name of user who retweeted/mentioned
    usernames = []              #Their username
    ids = []                    #Their user id
    locations = []              #Their location (as listed on their profile)
    tweetIDs = []               #ID of the retweet/mention
    tweets = []                 #The retweet/mention text
    time_stamp = []             #Date the retweet/mention was created

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")

    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    tweetIDs.append("Tweet ID")
    tweets.append("Tweet Text")
    time_stamp.append("Time Stamp")

    #Get mentions (200)
    mentions_timeline = twitter.get_mentions_timeline(screen_name=name,count=200)
    for mention in mentions_timeline:
        try:
            print(mention['user']['name'].encode("utf-8").decode("utf-8"))
            names.append(mention['user']['name'].encode("utf-8").decode("utf-8"))
        except:
            names.append("Can't print")
        usernames.append(mention["user"]["screen_name"].encode("utf-8").decode("utf-8"))
        ids.append(mention["user"]["id_str"])
        try:
            print(mention["user"]["location"].encode("utf-8").decode("utf-8"))
            locations.append(mention["user"]["location"].encode("utf-8").decode("utf-8"))
        except:
            locations.append("Can't Print")
        tweetIDs.append(mention["id_str"])
        try:
            print(mention['text'].encode("utf-8").decode("utf-8"))
            tweets.append(mention['text'].encode("utf-8").decode("utf-8"))
        except:
            tweets.append("Can't Print")
        time_stamp.append(mention["created_at"].encode("utf-8").decode("utf-8"))

    #Get retweets (200)
    retweetedStatuses = twitter.retweeted_of_me(count = 100)                                    #Get tweets from the user that have recently been retweeted
    for retweetedStatus in retweetedStatuses:
        statusID = retweetedStatus["id_str"]
        retweets = twitter.get_retweets(id=statusID,count=100)                                  #Get the retweets of the tweet
        for retweet in retweets:
            try:
                print(retweet['user']['name'].encode("utf-8").decode("utf-8"))
                names.append(retweet['user']['name'].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't print")
            
            usernames.append(retweet["user"]["screen_name"].encode("utf-8").decode("utf-8"))

            ids.append(retweet["user"]["id_str"])

            try:
                print(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
                locations.append(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't print")
            
            tweetIDs.append(retweet["id_str"])
            
            try:
                print(retweet['text'].encode("utf-8").decode("utf-8"))
                tweets.append(retweet['text'].encode("utf-8").decode("utf-8"))
            except:
                tweets.append("Can't print")
            
            time_stamp.append(retweet["created_at"].encode("utf-8").decode("utf-8"))


    open_csv = open("mentions_retweets.csv","r",newline='')
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))
    # print(len(names))
    rows = zip(names,usernames,ids,locations,tweetIDs, tweets,time_stamp)

    oldMentionsIDs = []                             #Record mentions/retweets that have already been recorded before

    oldMentions_csv = csv.reader(open_csv)

    for row in oldMentions_csv:
            oldMentionsIDs.append(row[4])

    open_csv.close()

    open_csv = open("mentions_retweets.csv","a", newline='') #Append new mentions/retweets to the list
    mentions_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[4] in oldMentionsIDs):          #if the ID isn't already in the mentions list
            # print(row)
            mentions_csv.writerow(row)

    open_csv.close()

def getTweet():
    """
    Gets tweet containing a word from the replace dictionary
    """
    keyList = list(replace)                         #Make a list of the keys from the "replace" dictionary
    search = keyList[randint(0,len(keyList)-1)]     #Pick a random word from that list and use it as a search term
    print("Searching " + search)


    results = twitter.search(q=search, count = 1)   #search twitter for search term
    for tweet in results["statuses"]:
        print("Getting tweet!")
        return tweet
    # print(tweet['text'].encode('utf8').decode('utf8'))




def getMentions():
    """
    Gets the tweets that mentioned the bot
    """
    mentions = twitter.get_mentions_timeline(screen_name=name,count=5)    #search twitter for bot username
    mentionsList = []                               #make list to contain mention tweets
    for mention in mentions:            #add tweets to list
        # print("Got a mention!")
        mentionsList.append(mention)

    mentionsFile = open('mentions.txt', 'r')        #Get IDs mentions that have already been addressed in the past
    oldMentionsList = mentionsFile.readlines()      #Put each in a list
    mentionsFile.close()

    newMentionsList = []                            #Make a list of mentions that have not been addressed
    for mention in mentionsList:                    #by comparing the mentions that were harvested to the old mentions
        mentionText = mention['text'].encode('utf8').decode('utf8')
        if not mention['id_str'] + "\n" in oldMentionsList and mentionText[0:2] != "RT" and name in mentionText:
            newMentionsList.append(mention)

    mentionsFile = open('mentions.txt', 'a')        #append new mentions to the old mentions file
    for mention in newMentionsList:
        mentionsFile.write(mention['id_str'] + "\n")
    mentionsFile.close()
    return newMentionsList


def getOembed(id_str):
    """
    Gets Embed link of a tweet
    """
    oembed_dict = twitter.get_oembed_tweet(id=id_str)
    html_to_encode = oembed_dict['html']
    return html_to_encode.encode('utf-8').decode('utf8')



def makeNewTweet(t):
    """
    Takes a list of words t (the tweet)
    and changes all mentions of men to that of women
    """
    numEdits = 0            #counter of number of changes made to tweet
    newWords = []           #put new tweet in this list
    index = 0               #index of word being currently looked at

    tweetWords = t['text'].encode('utf8').decode('utf8').split()        #Get the text of a tweet
    for x in tweetWords:                                                #For each word in the tweet
        havePunc = False                                                #whether or not it has punctuation
        punc = ''

        #The current character count of the tweet
        currLen = len(' '.join(newWords[:index]) + ' '.join(tweetWords[index:]))

        #if there is punctuation with the word being checked
        if x[-1] == ',' or x[-1] == '.' or x[-1] == '?' or x[-1] == '!' or x[-1] == ':' or x[-1] == ';':
            havePunc = True                                             #It has punctuation
            punc = x[-1:]                                               #store the punctuation for later
            X = x[:-1]                                                  #save the word w/o punctuation
        elif x[-2:].lower() == "'s":                                            #Do the same if it's possessive
            havePunc = True
            punc = "'s"
            X = x[:-2]
        else:                                                           #Else just get the word
            X = x


        # if name in tweetWords:
        #   maxCount = 140
        # else:
        #   maxCount = 116

        maxCount = 140                                                  #maximum char count

        if not name in X:                                               #disregard bot's username (the tweet is a mention)
            if X == '&amp':
                newWords.append('&')
            elif X in replace and len(replace[X] + punc) - len(X + punc) + currLen < maxCount:  #if it's a key word and adding it  doesn't put tweet over 140 char
                newWords.append(replace[X] + punc)                                              #replace it
                numEdits += 1                                                                   #add to the number of edits
            elif X.lower() in replace and len(replace[X.lower()] + punc) - len(X.lower()+ punc) + currLen < maxCount:
                if X == X.lower().capitalize():                                                 #check for capitalization
                    newWords.append(replace[X.lower()].capitalize() + punc)
                else:                                                                           #or all caps
                    newWords.append(replace[X.lower()].upper() + punc)
                numEdits += 1                                                                   #add to the number of edits
            else:                                                                               #else don't change it
                newWords.append(X + punc)
        else:                                                                                   #if word is bot's username
            newWords.append('@'+t['user']['screen_name'].encode('utf8').decode('utf8'))             #replace it with the user the bot is replying to
        index += 1                                                                              #update current index


    currLen = len(' '.join(newWords))   #update current character count
    print("Character Count:",currLen)
    if(numEdits < 1):                   #if no edits, don't return tweet
        return None
    return newWords


    

def tweet(tweet):
    """
    Tweets a string
    """
    twitter.update_status(status = tweet);





lastTweet = None        #to store the last tweet that was edited by the bot


def mentionEdit():
    """
    Edits a tweet that mentioned the bot
    """
    mentionList = getMentions()             #get list of new mentions
    for mention in mentionList:             #Get the text of each mention
        tweetWords = mention['text'].encode('utf8').decode('utf8').split()
        print(' '.join(tweetWords))
        
        #Get the username of the person who mentioned you
        username = mention['user']['screen_name'].encode('utf8').decode('utf8')
        print(username)

        #Edit mention
        newTweetWords = makeNewTweet(mention)

        if newTweetWords == None:               #if no changes
            print("No changes to tweet!")
        else:
            newTweet = ' '.join(newTweetWords)  #Join words into one string
            try:
                print(newTweet)     
            except:
                print("Cannot print")

            if (not debug):                     #If not in debug mode
                try:
                    # tweet(newTweet + " " + origTweetURL)
                    tweet(newTweet)             #Tweet new tweet
                    print("I just tweeted!")
                except:
                    print("Ran into a problem tweeting!")

tries = 0

def runBot():
    print("Bot running!")

    trying = True
    global tries
    # pulledTweet = getTweet()
    while(trying):                      #Keep trying to get a tweet til you find one that works
        if tries < 15:
            try:
                pulledTweet = getTweet()
                origTweet = pulledTweet['text'].encode('utf8').decode('utf8')
                trying = False
            except:
                print("Couldn't pull tweet. Trying again.")
                trying = True
                time.sleep(10)
                tries += 1
        else:
            print("Exceeded Number of tries")
            tries = 0
            try:
                mentionEdit()                                   #check mentions, and edit those
            except:
                print("Couldn't pull mentions")

            try:
                getFollowers()
            except:
                print("Couldn't get Followers")

            try:        
                getMentionsRetweets()
            except:
                print("Couldn't get Mentions/Retweets")
            return
    
    #Get username of tweeter
    username =pulledTweet['user']['screen_name'].encode('utf8').decode('utf8')
    print(username)

    #Get the URL of the original tweet
    origTweetURL = "twitter.com/" + username + "/status/" + pulledTweet['id_str']
    print(origTweetURL)

    global lastTweet
    

    try:
        print(origTweet)
    except:
        print("Cannot print")

    if tries < 15:
        if len(origTweet) > 140:                        #check length of tweet, if too long try again
            print("Tweet too long!")
            lastTweet = origTweet
            tries += 1
            time.sleep(10)
            runBot()
            return
        elif origTweet[0] == "@" or origTweet[0:2] == "RT":                         #Check if tweet is a reply. If it is, leave it alone.
            print("Tweet is a reply!")
            lastTweet = origTweet
            time.sleep(10)
            tries += 1
            runBot()
            return
        elif origTweet != lastTweet:                    #make sure the bot hasn't edited the tweet before

            newTweetWords = makeNewTweet(pulledTweet)   #edit tweet

            if newTweetWords == None:                   #if no changes
                print("No changes to tweet!")
                lastTweet = origTweet
                tries += 1
                time.sleep(10)
                runBot()                                #try again
                return
            else:
                newTweet = ' '.join(newTweetWords)      #combine tweet words into one string
                try:
                    print(newTweet)             
                except:
                    print("Cannot print")

                if (not debug):                         #if not in debug mode
                    try:
                        # tweet(newTweet + " " + origTweetURL)
                        tweet(newTweet)                 #tweet new tweet
                        print("I just tweeted!")
                    except:
                        print("Ran into a problem tweeting!")
                tries = 0

                lastTweet = origTweet                   #set last tweet to this tweet
        else:                   
            print("No new Tweet!")                      #if no new tweet, try again
            tries += 1
            time.sleep(10)
            runBot()
            return
    else:
        print("Exceeded Number of tries!")
        tries = 0

    try:
        mentionEdit()                                   #check mentions, and edit those
    except:
        print("Couldn't pull mentions")

    try:
        getFollowers()
    except:
        print("Couldn't get Followers")

    try:        
        getMentionsRetweets()
    except:
        print("Couldn't get Mentions/Retweets")


def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t


debug = False
runOnce = False

runBot()
if not runOnce:
    setInterval(runBot, 60*60*3)        #runs every 3 hours