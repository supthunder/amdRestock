# amdRestock
Checks for RX 570/580 restocks on NewEgg and BestBuy

Live on twitter [@rx570](https://www.twitter.com/rx570/)

$5 server cost: 17iSNnZcDgWnmHd2CaaXmE9rWW49ecgnR3

![gif](/images/term.gif)

## How it works:
- Python + Twitter
- Runs every 21 seconds
- Uses NewEgg/BestBuy mobile API's

## Setup:
- Download zip + open in terminal
- To run without BestBuy:
- run: ```pip install requests```
- run: ```python main.py```
- To run with BestBuy:
- Use fiddler/wireshark etc to get api keys from BestBuy mobile app
- replace ```"GET_FROM_MITM_IPHONE_APP"``` without your keys
- To use twitter, get twitter api keys form https://apps.twitter.com
