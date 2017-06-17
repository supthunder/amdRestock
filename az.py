from amazon.api import AmazonAPI
import requests
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


def sendTweet(link, site, name):
	global restock
	# setup twitter
	C_KEY = "C_KEY"
	C_SECRET = "C_SECRET"
	A_TOKEN = "A_TOKEN"
	A_TOKEN_SECRET = "A_TOKEN_SECRET"
	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
	api = tweepy.API(auth)

	# send tweet
	alert = "\U0001f6a8 "
	sos = "\U0001f198 "
	flag = "\U0001f6a9 "
	tweet = alert+sos+flag+" IN STOCK "+flag+sos+alert
	tweet += "\n"+name
	tweet += "\nSite: "+site+"\n"
	tweet += link+"\n"
	tweet += strftime("%Y-%m-%d %H:%M:%S", gmtime())
	print(tweet)
	api.update_status(tweet.encode('utf-8'))
	restock = 1

def az():
	amazon = AmazonAPI("API_KEY", "API_SECRET_KEY", "API_TAG")
	amazon2 = AmazonAPI("API_KEY", "API_SECRET_KEY", "API_TAG")
	amazon3 = AmazonAPI("API_KEY", "API_SECRET_KEY", "API_TAG")
	amazon4 = AmazonAPI("API_KEY", "API_SECRET_KEY", "API_TAG")
	amazon5 = AmazonAPI("API_KEY", "API_SECRET_KEY", "API_TAG")
	amazon6 = AmazonAPI("API_KEY", "API_SECRET_KEY", "API_TAG")

	# To avoid 503 delays
	aznBin = [amazon, amazon2, amazon3, amazon4, amazon5, amazon6]

	# items
	items = [
		"B07197V7C7",
		'B071CMPRZZ',
		'B071L1VGQW',
		'B071D8YQJD',
		'B07197V7C7',
		'B06Y3V1K81',
		'B06Y46X4L9',
		'B06Y44TWF3',
		'B06Y3ZQPY6',
		'B06Y45GQ1L',
		'B071RW7SCT',
		'B06XZZ93FQ',
		'B06XZQMMHJ',
		'B06XZRWT8D',
		'B06Y19NMP3',
		'B071VDCCJM',
		'B0714B1GNZ',
		'B0711QH8ZS',
		'B06ZZCV9SY',
		'B071QX74F9',
		'B071CPJZSX',
		'B071XZ867C',
		'B07115GPN7',
		'B06ZXRLX3H',
		'B072B6W44N',
		'B071CD6K6Z',
		'B06Y66K3XD',
		'B06ZYB4C18'
	]
	count = 0
	for item in items:
		# randomize delay 1
		sleep(uniform(0.2,0.3))

		# diff API keys
		if count == len(aznBin):
			count = 0
			amazonNow = aznBin[count]
		else:
			amazonNow = aznBin[count]
			count += 1
		delay = True
		while delay:
			try:
				product = amazonNow.lookup(ItemId=item)
				delay = False
			except:
				# when delay 1 not enough
				print("503... delay 2 sec")
				sleep(uniform(2, 3))
		try:
			retail_price = float(product.list_price[0])
			# print(product.formatted_price)
			list_price = float(product.price_and_currency[0])
		except:
			list_price = 100.00
			retail_price = 0.00
		if list_price <= retail_price:
			print("Amazon - " + product.title + " - In Stock")
			link = "https://www.amazon.com/dp/" + item
			sendTweet(link, "Amazon", getName(str(product.title)))
		else:
			print("Amazon - " + product.title + " - OOS")


print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
az()
