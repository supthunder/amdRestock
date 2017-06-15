import requests
import tweepy
from time import gmtime, strftime
import json

def sendTweet(link, site):
	global restock
	# setup twitter
	C_KEY = ""
	C_SECRET = ""
	A_TOKEN = ""
	A_TOKEN_SECRET = ""
	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
	api = tweepy.API(auth)

	# send tweet
	alert = "\U0001f6a8 "
	sos = "\U0001f198 "
	flag = "\U0001f6a9 "
	tweet = alert+sos+flag+" NES IN STOCK "+flag+sos+alert
	tweet += "\nSite: "+site+"\n"
	tweet += link+"\n"
	tweet += strftime("%Y-%m-%d %H:%M:%S", gmtime())
	print(tweet)
	api.update_status(tweet.encode('utf-8'))


def newEgg():
	urls = [
		"http://www.ows.newegg.com/Products.egg/14-202-284",
		'http://www.ows.newegg.com/Products.egg/14-137-123',
		'http://www.ows.newegg.com/Products.egg/14-202-283',
		'http://www.ows.newegg.com/Products.egg/14-202-284',
		'http://www.ows.newegg.com/Products.egg/14-202-285',
		'http://www.ows.newegg.com/Products.egg/14-131-717',
		'http://www.ows.newegg.com/Products.egg/14-131-716',
		'http://www.ows.newegg.com/Products.egg/9SIA7HN5N17482'
	]
	user = {"User-Agent": "Newegg iPhone App / 4.1.2"}
	for url in urls:
		stock = requests.get(url, headers=user, timeout=5)
		if str(stock.status_code) != "200":
			print("NewEgg - banned! - "+str(stock.status_code))
			return
		stock = stock.json()
		if stock['Basic']['CanAddToCart'] != False:
			print("NewEgg - " + stock['Basic']['Title'] + " - In Stock")
			link = "https://www.newegg.com/Product/Product.aspx?Item=" + stock['Basic']['NeweggItemNumber']
			sendTweet(link,"NewEgg")

		else:
			print("NewEgg - " + stock['Basic']['Title'] + " - OOS")

def bestBuy():
	urls = [
		"https://app-ssl.bestbuy.com/si/v4/products/search?query=5869603&rows=10&sort=Best-Match&facetsOnly=false",
		"https://app-ssl.bestbuy.com/si/v4/products/search?query=5845205&rows=10&sort=Best-Match&facetsOnly=false",
		"https://app-ssl.bestbuy.com/si/v4/products/search?query=5845204&rows=10&sort=Best-Match&facetsOnly=false",
		"https://app-ssl.bestbuy.com/si/v4/products/search?query=5859901&rows=10&sort=Best-Match&facetsOnly=false",
		"https://app-ssl.bestbuy.com/si/v4/products/search?query=5859900&rows=10&sort=Best-Match&facetsOnly=false"
	]
	headers ={
			"Accept":"*/*",
			"Accept-Encoding":"gzip;q=1.0, compress;q=0.5",
			"Accept-Language":"en-US;q=1.0, ar-US;q=0.9, ta-US;q=0.8, ja-JP;q=0.7",
			"visitorToken":"GET_FROM_MITM_IPHONE_APP",
			"Content-Type":"application/json;charset=utf-8",
			"User-Agent":"BestBuy/10.4.0 APPSTORE (Build 201702201406; iOS 10.2.1; Model iPhone)",
			"Connection":"keep-alive",
			"X-SI-API-VERSION":"4.0",
			"X-PLATFORM":"GET_FROM_MITM_IPHONE_APP",
			"X-NewRelic-ID":"GET_FROM_MITM_IPHONE_APP"
		}

	for url in urls:
		stock  = requests.get(url,headers=headers,timeout=5)
		if str(stock.status_code) != "200":
			print("BestBuy - banned! - "+str(stock.status_code))
			return
		stock = stock.json()
		itemName = stock['searchApi']['documents'][0]['summary']['names']['short']
		itemStock = str(stock["searchApi"]["documents"][0]["priceBlock"]["buttonState"]["buttonStateID"])
		itemUrl = "http://www.bestbuy.com" + str(stock['searchApi']['documents'][0]['summary']['url'])
		if itemStock == "ADD_TO_CART":
			print("BestBuy - "+itemName+" - In Stock")
			sendTweet(itemUrl,"BestBuy")
		elif itemStock == "SOLD_OUT_ONLINE" or itemStock == "CHECK_STORES":
			print("BestBuy - "+itemName+" - OOS")


print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
newEgg()
bestBuy()
