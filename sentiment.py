from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt
from credentials import *

def senti():

    def percentage(part, whole):
        return 100 * float(part) / float(whole)


    auth = tweepy.OAuthHandler(Consumer_Key, Consumer_Secret)
    auth.set_access_token(Access_Token, Access_Token_Secret)
    api = tweepy.API(auth)

    searchTerm = "Bitcoin"
    noOfSearchTerms = 100

    tweets = tweepy.Cursor(api.search, q=searchTerm).items(noOfSearchTerms)
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0



    for tweet in tweets:
         #print(tweet.text)
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity

        if (analysis.sentiment.polarity == 0):
            neutral += 1
        elif (analysis.sentiment.polarity < 0.00):
            negative += 1
        elif (analysis.sentiment.polarity > 0.00):
            positive += 1

    positive = percentage(positive, noOfSearchTerms)
    negative = percentage(negative, noOfSearchTerms)
    neutral = percentage(neutral, noOfSearchTerms)
    polarity = percentage(polarity, noOfSearchTerms)

    positive = format(positive, '.2f')
    neutral = format(neutral, '.2f')
    negative = format(negative, '.2f')

#print('\nThe pie graph has been successfully plotted!!')
##print("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " Tweets.")
##
##if (polarity == 0):
##    print("Neutral")
##elif (polarity < 0.00):
##    print("Negative")
##elif (polarity > 0.00):
##    print("Positive")


    labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
    sizes = [positive, neutral, negative]
    colors = ['#0EE0E0', '#D8E811', '#F73703']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on ' + searchTerm + ' based on twitter feed ')
    plt.axis('equal')
    plt.tight_layout()

    plt.show()




