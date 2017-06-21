import requests
import re
import tweepy
import os
from time import gmtime, strftime, sleep
import json
from random import uniform

def getName(name):
	product = "RX "
	if "570" in name:
		product += "570"
	else:
		product += "580"

	if "4G" in name:
		product += " 4GB"
	else:
		product += " 8GB"
	return product


def sendTweet(link, site, name, price):
	global restock
	# setup twitter
	C_KEY = "KEYS"
	C_SECRET = "KEYS"
	A_TOKEN = "KEYS"
	A_TOKEN_SECRET = "KEYS"
	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
	api = tweepy.API(auth)

	# send tweet
	alert = "\U0001f6a8 "
	sos = "\U0001f198 "
	flag = "\U0001f6a9 "
	tweet = alert+sos+flag+" IN STOCK "+flag+sos+alert
	tweet += "\n"+name
	tweet += "\n$"+price
	tweet += "\nSite: "+site+"\n"
	tweet += link+"\n"
	tweet += strftime("%Y-%m-%d %H:%M:%S", gmtime())
	print(tweet)
	api.update_status(tweet.encode('utf-8'))
	restock = 1

def bh():
	with open('waitBh.json') as dt:
		waitCheck = json.load(dt)

	url1 = 'https://www.bhphotovideo.com/c/json/buy/Graphic-Cards/ci/6567/N/3668461602/mnp/180/mxp/350/ntt/rx+580'
	url2 = 'https://www.bhphotovideo.com/c/json/buy/Graphic-Cards/ci/6567/N/3668461602+4294272508+4294272499/mnp/175/mxp/350/ntt/rx'
	urlTest = 'https://www.bhphotovideo.com/c/json/buy/Graphic-Cards/ci/6567/N/3668461602/mnp/700/mxp/720'
	user = {"User-Agent": "Chrome 41.0.2227.1"}


	try:
		stock = requests.get(url2, headers=user, timeout=5)
	except:
		print("Could not connect...")
		exit(1)
	if str(stock.status_code) != "200":
		print("BH - banned! - "+str(stock.status_code))
		return
	stock = stock.json()

	for item in range(0,stock["resultCount"]):
		name = stock['items'][item]['shortDescriptionPlusBrand']
		inStock = stock['items'][item]["available"]
		link = stock['items'][item]["detailsUrl"]
		price = stock['items'][item]["price"]
		itemCode = stock['items'][item]["itemCode"]

		if inStock == True:
			if waitCheck[itemCode] == 180:
				waitCheck[itemCode] = 0
			elif waitCheck[itemCode] > 0:
				waitCheck[itemCode] += 1
			else:
				waitCheck[itemCode] += 1	
				print("BHPhoto - " + name + " - In Stock")
				sendTweet(link,"BHPhoto",getName(name), price)
		else:
			if waitCheck[itemCode] == 180:
				waitCheck[itemCode] = 0
			elif waitCheck[itemCode] > 0:
				waitCheck[itemCode] += 1	
			
			print("BHPhoto - " + name + " - OOS")

	with open('waitBh.json','w') as fl:
		json.dump(waitCheck, fl, indent=4)

print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
bh()
