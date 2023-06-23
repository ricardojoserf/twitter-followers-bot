'''
Set your configuration key by running the below code in your shell/terminal : 
export bearer_token="your bearer token"
export consumer_key="your api key"
export consumer_secret="your api key secret"
export access_token="your access token"
export access_token_secret="your access token secret"
'''

import os

bearer_token=os.environ["bearer_token"]
consumer_key=os.environ["consumer_key"]
consumer_secret=os.environ["consumer_secret"]
access_token=os.environ["access_token"]
access_token_secret=os.environ["access_token_secret"]

print(f"bearer_token : {bearer_token}\n\nconsumer_key : {consumer_key} \n\nconsumer_secret : {consumer_secret} \n\naccess_token : {access_token} \n\naccess_token_secret : {access_token_secret}")

if __name__ == '__main__':
    main()

