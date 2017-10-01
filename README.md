# twitter-bot
Twitter bot for following/unfollowing people automatically and get more followers!


## Requirements
#### 1 - Pip modules
*sudo pip install tweepy argparse*
#### 2 - Create a twitter account and a twitter app, and fill the config.py file

-

## Usage

**python twitter-bot.py -q {query} -g {geocode} -l {limit} -o {option}**

*-q: Query, the word to search (Optional)*

*-g: Geocode location, formatted as* LAT,LON,N*km (Optional)*

*-l: Limit, max number of tweets (Optional)*

*-o: Option,* "follow" *or* "unfollow"


**python twitter-bot.py -q {query} -g {geocode} -l {limit} -o follow**: Follow users tweeting the query value in the geocode location, limited to the limit value

**python twitter-bot.py -q {query} -g {geocode} -l {limit} -o unfollow**: Follow users who do not follow you back and are not included in the whitelist.txt file

-

## Example
**python twitter-bot.py -q "le pen" -l 100 -g "40.432,-3.708,10km"**
