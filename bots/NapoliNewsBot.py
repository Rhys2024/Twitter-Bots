from config import create_connections
from translate import Translator
import tweepy 
#import logging
import time
import json

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger()
                        
italian_to_english_translator = Translator(from_lang='autodetect',to_lang="en")


def set_journalists_ids(client):
    
    with open("journalists.txt", "r") as refr:
    
        journalists = [line.rstrip() for line in refr]
    temp = {}
    print("\n\nconfiguring journalists...\n\n")
        
    for name in journalists:
        
        try:
            temp[client.get_user(username=name).data.id] = name
        except:
            pass
    
    return temp

def set_good_ids(client):
    
    with open("good_accounts.txt", "r") as refr:
    
        good_accounts = [line.rstrip() for line in refr]
        
    temp = {}
    print("\n\nconfiguring good accounts...\n\n")
        
    for name in good_accounts:
        
        try:
            temp[client.get_user(username=name).data.id] = name
        except:
            pass
    
    return temp
        

class NewsListener(tweepy.StreamingClient):
    
    def on_connect(self):
        self.yeah = True
        print("\n\nConnected\n\n")
        
    def on_tweet(self, tweet):
        
        if not tweet.referenced_tweets:
            
            print("signal received...\n")
            
            if tweet.author_id in list(journalists.keys()):

                try:
                    
                    print(f"SOURCE  -  {journalists[tweet.author_id]}\n\n\n{tweet}")
                    
                    #string = italian_to_english_translator.translate(tweet)
                    
                    if self.yeah:

                        client.create_tweet(text=f"SOURCE  -  {journalists[tweet.author_id]}\n\n{str(tweet).replace('@', '')}")
                        self.yeah = False
                    else:
                        client.create_tweet(text=f"From:  {journalists[tweet.author_id]}\n\n\n{str(tweet).replace('@', '')}")
                        self.yeah = True

                    #translation = italian_to_english_translator.translate(tweet)
                    
                    print("\n\nTWEET SENT !!\n\n")
            
                    time.sleep(20)

                    #if translation == 'PLEASE SELECT TWO DISTINCT LANGUAGES':
                        #client.create_tweet(text=f"In English:\n{translation.replace('@', '')}\n\nfrom {journalists[tweet.author_id]}")
                    
                except Exception as e:
                    print("Error with tweeting !!")
            
            elif tweet.author_id in list(good_accounts.keys()):
                
                print(f"{tweet}")
                client.retweet(tweet.id)
                try:
                    #client.retweet(tweet.id)
                    print("\n\nTweet Retweeted !!\n\n")
                except Exception as e:
                    print("Error with tweeting !!")
                    
                time.sleep(15)
                
                
    def on_disconnect(self):
        #client.create_tweet(text="CURRENTLY OFFLINE\n\nRobot is being Improved by the Developers!\n\nWe appreciate your patience!")
        print("\n\nDisconnected\n\n")
            

keywords = ["Napoli", "napoli", "Azzurri","De Laurentiis", "Insigne", "Mertens", 
            "Koulibaly", "Di Lorenzo", "Zielinski",
            "Kvicha", "Kvara", "Elmas", "Rrahmani", "Kim Min-Jae", 
            "Ola Solbakken", "Lozano", "Mario Rui", "Zambo", "Anguissa", 
            "Fabian", "Fabian Ruiz", "ADL", "Politano", "Lobotka", "Meret",
            "Olivera", "Maradona"]


def main():
    
    global client, journalists, good_accounts
    
    connections = create_connections()
    
    api = connections["API"]
    client = connections["Client"]
    bearer_token = connections["Bearer"]
    
    journalists = set_journalists_ids(client=client)
    good_accounts = set_good_ids(client=client)
    
    news_stream = NewsListener(bearer_token)
    
    print(f"\n\nRULES: \n{news_stream.get_rules().data}\n\n\n")
    
    #for rule in news_stream.get_rules().data:
        #news_stream.delete_rules(rule.id)
    #print(news_stream.get_rules().data[0].id)
    #print(f"\n\nGOOD ACCOUNTS: \n{good_ids}\n\n\n")
    
    news_stream.filter(tweet_fields = ['referenced_tweets', 'author_id'])
    


if __name__ == "__main__":
    main()

