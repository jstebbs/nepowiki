## PYTHON MODULE IMPORTS ##
import os
import time
from collections import deque

## MODULE DEPENDCIES ##
import tweepy
from dotenv import load_dotenv

## FILE IMPORT ##
from nepowiki import *

load_dotenv()

# Now you can access the variables like this
consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_SECRET")


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)



# Create a queue to store the celebrities
celebrities = deque()

# Read the celebrities list from the text file and add them to the queue
with open("celebs.txt", "r") as file:
    for line in file:
        celebname = line.strip()
        celebrities.append(celebname)

while celebrities:
    # Get the next celebrity from the front of the queue
    celebname = celebrities.popleft()
    parents = get_parents(celebname)
    if len(parents)==0:
        momdad = get_momdad(celebname)
    else:
        momdad = ''
    relatives = get_relatives(celebname)
    text = ''
    # Construct the tweet text
    if len(parents)==0 and len(momdad)==0:
        text = f"{celebname} has 0 blue-linker parents{os.linesep}--not a nepo baby--"
    elif len(parents)>0 and len(momdad)==0:
        text = f"{parents}"
    elif len(momdad)>0 and len(parents)==0:
        text = f"{momdad}"
    
    if relatives is not None:
        text += f"{relatives}"

    if len(text) > 280:
        text = text[:240] + "[THIS WAS LITERALLY TOO LONG TO TWEET]"
    

    # Post the tweet
    api.update_status(text)
    time.sleep(2*60*60) # Sleep for 1 hour
    #Delete the celebrity from the celebs.txt file
    with open("celebs.txt", "r") as file:
        lines = file.readlines()
    with open("celebs.txt", "w") as file:
        for line in lines:
            if line.strip() != celebname:
                file.write(line)

