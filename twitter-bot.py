import tweepy
from tweepy import OAuthHandler
import config as config
import argparse

# Default limit of tweets
def_limit = 5


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', required=False, action='store', help='Query')
    parser.add_argument('-l', '--limit', required=False, action='store', help='Max. number of tweets')
    parser.add_argument('-g', '--geocode', required=False, action='store', help='Geocode. Ex: "40.432,-3.708,10km"')
    parser.add_argument('-o', '--option', required=True, action='store', help='Option')
    my_args = parser.parse_args()
    return my_args


def follow_funct(query, geocode, limit, api):
    # Cursor    
    if query is not None and geocode is None:
        cursor = tweepy.Cursor(api.search, q=query, count=int(limit)).items(int(limit))        
    if query is None and geocode is not None:
        cursor= tweepy.Cursor(api.search, geocode=geocode, count=int(limit)).items(int(limit))
    if query is not None and geocode is not None:
        cursor = tweepy.Cursor(api.search, q=query, geocode=geocode, count=int(limit)).items(int(limit))
    # Start following people
    print ("Following %s people: " % limit)
    for tweet in cursor:
        screen_name = tweet.user.screen_name
        api.create_friendship(screen_name)
        print (" - " + screen_name)


def unfollow_funct(api):
    # Get info about followers/followings and whitelist
    followers = api.followers_ids()
    followings = api.friends_ids()
    whitelist = open("whitelist.txt").read().splitlines()
    # Start unfollowing
    for i in followings:
        screen_name = api.get_user(i).screen_name
        if i not in followers and screen_name not in whitelist:
            print ("Unfollowing %s" % screen_name)
            api.destroy_friendship(screen_name)

def report(api):
    followers = api.followers_ids()
    followings = api.friends_ids()
    followers_names=[]
    followings_names=[]
    for i in followers:
        screen_name = api.get_user(i).screen_name
        followers_names.append(screen_name)
    for j in followings:
        screen_name = api.get_user(j).screen_name
        followings.append(screen_name)
    didnt_follow_me = list(set(followings_names)-set(followers_names))
    didnt_follow_them = list(set(followers_names)-set(followings_names))
    counter = 0
    print ("Followers...")
    for k in followers_names:
    	counter+=1
    	print (str(counter)+") "+k)

    counter=0
    print ("Followings...")
    for k in followings_names:
    	counter+=1
    	print (str(counter)+") "+k)

    print ("I follow them but they do not follow me back...")
    for k in didnt_follow_me:
    	counter+=1
    	print (str(counter)+") "+k)

    counter=0
    print ("They follow me but i do not follow them...")
    for k in didnt_follow_them:
    	counter+=1
    	print (str(counter)+") "+k)




def main():
    # Check config file is ok
    if config.consumer_key != "" or config.consumer_secret != "" or config.access_token != "" or config.access_token_secret != "":
        consumer_key=config.consumer_key
        consumer_secret=config.consumer_secret
        access_token=config.access_token
        access_token_secret=config.access_token_secret
    else:
        print ("Fill the config file please!")
        return
    # Auth process
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
    except ValueError:
        print("Error authenticating!")
    # Different options
    args = get_args()
    option = args.option
    if option == "follow":
        limit = args.limit
        if limit is None:
            limit = def_limit
            print ("Default number of tweets: %s" % limit)
        follow_funct(args.query, args.geocode, limit, api)
    elif option == "unfollow":
        unfollow_funct(api)
    elif option == "info":
    	report(api)
    else:
        print ("Unknown function")


if __name__ == "__main__":
    main()