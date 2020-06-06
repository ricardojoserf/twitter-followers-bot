import tweepy
from tweepy import OAuthHandler
import config as config
import argparse
import time, datetime

# Default limit of tweets
def_limit = 5
delay_ = 1
delay_follow = 1

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', required=False, action='store', help='Query')
    parser.add_argument('-l', '--limit', required=False, action='store', help='Max. number of tweets')
    parser.add_argument('-g', '--geocode', required=False, action='store', help='Geocode. Ex: "40.432,-3.708,10km"')
    parser.add_argument('-o', '--option', required=True, action='store', help='Option')
    parser.add_argument('-i', '--input', required=False, action='store', help='Input list')
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
        time.sleep(delay_follow)


def follow_list(api, userlist):
    userlist = open(userlist).read().splitlines()
    for screen_name in userlist:
        if screen_name != '':
            print ("Following %s"%(screen_name))
            api.create_friendship(screen_name)
            time.sleep(delay_follow)


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

		
def unfollow_list(api, userlist):
    userlist = open(userlist).read().splitlines()
    for screen_name in userlist:
        if screen_name != '':
            print ("Unfollowing %s"%(screen_name))
            api.destroy_friendship(screen_name)


def ratelimit():
	print ("Rate limit. Waiting for 2 minutes nad trying again.")
	print ("If it fails again, try to regenerate Twitter Keys and Tokens")
	time.sleep(120)
	return


def report(api):
	followers = api.followers_ids()
	followings = api.friends_ids()
	followers_names=[]
	followings_names=[]

	# People following me
	print ("\nFOLLOWERS\n")
	counter = 0
	for i in followers:
		try:
			time.sleep(delay_)
			screen_name = api.get_user(i).screen_name
			followers_names.append(screen_name)
			counter+=1
			print (str(counter)+") "+screen_name)
		except:
			ratelimit()

	# People i follow
	print ("\nFOLLOWING\n")
	counter = 0
	for j in followings:
		try:
			time.sleep(delay_)
			screen_name = api.get_user(j).screen_name
			followings_names.append(screen_name)
			counter+=1
			print (str(counter)+") "+screen_name)
		except:
			ratelimit()
			screen_name = api.get_user(j).screen_name
			followings_names.append(screen_name)
			counter+=1
			print (str(counter)+") "+screen_name)

	# People who i follow but they do not follow me
	didnt_follow_me = list(set(followings_names)-set(followers_names))
	# People who follow me but i do not follow them
	didnt_follow_them = list(set(followers_names)-set(followings_names))
	
	counter = 0
	print ("\nI FOLLOW BUT THEY DO NOT FOLLOW BACK\n")
	for k in didnt_follow_me:
		counter+=1
		print (str(counter)+") "+k)

	counter=0
	print ("\nTHEY FOLLOW BUT I DO NOT FOLLOW BACK\n")
	for l in didnt_follow_them:
		counter+=1
		print (str(counter)+") "+l)

	print ("\n------------------------- SUMMARY -------------------------")
	print ("Total followers: %s"%(len(followers_names)))
	print ("Total following: %s"%(len(followings_names)))
	print ("Total people i follow but they do not follow me: %s"%(len(didnt_follow_me)))
	print ("Total people following me but i do not follow them: %s"%(len(didnt_follow_them)))
	print ("\nDate: %s"%(datetime.datetime.now()))
	print ("-----------------------------------------------------------")


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
        query = args.query
        geocode = args.geocode
        input_ = args.input

        if query is not None or geocode is not None:
            limit = args.limit
            if limit is None:
                limit = def_limit
                print ("Default number of tweets: %s" % limit)
            follow_funct(args.query, args.geocode, limit, api)
        
        elif input_ is not None:    
            follow_list(api, input_)
                
    elif option == "unfollow-back":
        unfollow_funct(api)
    elif option == "unfollow":
        input_ = args.input
        unfollow_list(api, input_)
    elif option == "info":
    	report(api)
    else:
        print ("Unknown function")


if __name__ == "__main__":
    main()
