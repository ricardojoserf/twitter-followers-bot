import os

bearer_token=os.environ["BEARERTOKEN"]
consumer_key=os.environ["APIKEY"]
consumer_secret=os.environ["APIKEYSECRET"]
access_token=os.environ["ACCESSTOKEN"]
access_token_secret=os.environ["ACCESSTOKENSECRET"]

print(f"consumer--key : {consumer_key} \nconsumer_secret : {consumer_secret} \naccess_token : {access_token} \naccess_token_secret : {access_token_secret}")

'''
Set your configuration key by running the below code in your shell/terminal : 
export APIKEY="your api key"
export BEARERTOKEN="your bearer token"
export APIKEYSECRET="your api key secret"
export ACCESSTOKEN="your access token"
export ACCESSTOKENSECRET="your access token secret"
'''

# Run this script to comfirm keys are set

