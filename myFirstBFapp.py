#!/usr/bin/env python3

'''
	08/09/16
	jasFBot - first cut
	
	Interactive method for getting session id is: log into BF, then accessing account demo, then copy-paste into resource file.
	
	Non-interactive method for getting sessionId comes from use getSessionId.py
	
	Notes: 
		* delayed app is about 5 mins behind real time (estimate)
		* function json.loads deserialises a json str into a python object
	
'''




import urllib
import urllib.request
import urllib.error
import json
import datetime
import sys

import connectionDetails
import foxyBotLib
import foxyGlobals
import marketClass

'''
=======================================================================

Function definitions

-----------------------------------------------------------------------
'''

'''
Task 1: 
	get a list of all in-play markets, filtered for football
	return the eventId, and a meaningful name for the event
'''
def getInplayMarkets( queryText ) :
	
	eventList = foxyBotLib.listEvents( queryText )
	
	myDict = {}
	for event in eventList :
		print(event)
		eventId = event['event'] ['id']

		myDict [ eventId ] = event['event'] ['name']
	
	return myDict
	
	
#--------------------------------------------------------
'''
Task 2:
	list all in-play markets for the query text specified
	i want to see the name, and amount matched.
	order by volume traded (is this the same as matched amount?)
'''
def getInplayMarketVols( setOfEvents ):
	
	#turn eventList into proper formatted list
	numberEvents = len(setOfEvents)
	eventString = ""
	for eventId in setOfEvents :
		eventString += '\"'
		eventString += str(eventId)
		eventString += '\"'
		if eventId  != setOfEvents[numberEvents-1] :
			eventString += ','
		
	marketCat = foxyBotLib.listMarketCatalogue( eventString, numberEvents )
	
	
	myDict = {}
	for market in marketCat:
		marketId = market['marketId']
		myDict[ marketId ] = market[ 'totalMatched' ]
	
	print("These market ID's found (ID, volume, name) ")
	marketList = [] 
	for id in myDict :
		name = foxyBotLib.getEventNameFromMarketId(id)
		print( '\t' + str( id ) + " :\t" + str(myDict[id] )  + " :\t" + name )
		newObject =  marketClass.Market( id, name )
		newObject.volume = myDict[ id ]
		if newObject.volume >= foxyGlobals.minVolume :
			marketList.append( newObject  )
		
	return marketList


#--------------------------------------------------------
'''
Task 3:
		Get back and lay prices for each market
		Which runner are we reporting on here?
'''
def getPrices ( marketId ):
	
	price = foxyBotLib.listMarketBook( marketId )
	
	#if not 
	if not price :
		print( 'no results from marketId')
		print(price)
		return 
	
	#if you pass in list of marketids, can get many results, so take first one from list
	#as result 1
	ret1 = price[0]

		
	numberOfRunners = ret1['numberOfRunners']
	print('number of runners = ' + str(numberOfRunners))
	runners = ret1['runners']
	for runner in runners :
		#print(runner['ex'])
		
		bestBackOdds = runner['ex']['availableToBack']
		if not bestBackOdds :
			bestBackOdds = 0
			print('no back odds available')
		else :
			bestBackOdds = bestBackOdds[0]['price']
			
		bestLayOdds = runner['ex']['availableToLay']
		if not bestLayOdds :
			bestLayOdds = 0
			print('no lay odds available')
		else :
			bestLayOdds = bestLayOdds[0]['price']
			
	#	print('backOdds = ' + str(bestBackOdds))
	#	print('layOdds = ' + str(bestLayOdds))
		backOdds = bestBackOdds
		layOdds = bestLayOdds
	#print (ret1['runners'])
	
		#nb: this is the last runner odds.  need to vhange to return best odds...
		#return after first one gives you the best odds!
		return  ( backOdds, layOdds )
	
#--------------------------------------------------------
'''
Task 4:
		Return list of best markets based on:
			- above defined volume (e.g. 10k)
			- ordered by smallest spread
			
'''

#======================================================================

'''
Parameter check
'''

args = len(sys.argv)

if ( args < 3):
	'''
    print ('Please provide Application key and session token')
    appKey = input('Enter your application key :')
    sessionToken = input('Enter your session Token/SSOID :')
    print ('Thanks for the input provided')
  '''
	appKey = connectionDetails.getDelayedKey()
	sessionToken 	=  connectionDetails.getSessionId()
else:
    appKey = sys.argv[1]
    sessionToken = sys.argv[2]

foxyGlobals.headers = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json'}

#--------------------------------------------------------

searchString = 'Soccer'
#searchString = 'Tennis'
#searchString = 'Cricket'

dictOfEvents = getInplayMarkets( searchString )
inplayMarketCount = str(len(dictOfEvents))

print('___________________')
print( 'List of ' + inplayMarketCount + ' inplay markets for: ' + searchString )

setOfEvents = []

print('\tevent Id :\tevent name')
for id in dictOfEvents :
	print( '\t' + str( id ) + " :\t" + dictOfEvents[id] )
	setOfEvents.append(id)


#--------------------------------------------------------
# Use the event ID's to get market data, then store in a lot of Market Data objects
dictOfMarketObjects = getInplayMarketVols( setOfEvents )
marketIdCount = str(len(dictOfMarketObjects))

'''
marketList = [] 
for id in dictOfMarketIds :
	name = foxyBotLib.getEventNameFromMarketId(id)
	print( '\t' + str( id ) + " :\t" + str(dictOfMarketIds[id] )  + " :\t" + name )
	newObject =  marketClass.Market( id, name )
	newObject.volume = dictOfMarketIds[ id ]
	marketList.append( newObject  )'''
	
print('___________________')	
print( 'List of ' + marketIdCount + ' markets above min volume size, ordered by volume')
#print ( )

sortedDictOfMarketObjects = sorted( dictOfMarketObjects, key=marketClass.getkeyByVolume, reverse=True ) 
#print(sortedDictOfMarketObjects)
	
#--------------------------------------------------------
# get the price information
#marketObj = dictOfMarketObjects.pop()


for i in sortedDictOfMarketObjects :
	priceInfo = getPrices(i.id)
	if not priceInfo :
		print('no price info... deleting object')
		sortedDictOfMarketObjects.remove(i)
	else :
		#print('priceInfo = ' + str(priceInfo) )
		i.backPrice = priceInfo[0]
		i.layPrice = priceInfo[1]
		i.spread = i.layPrice - i.backPrice
	
#print(sortedDictOfMarketObjects)
sortedDictOfMarketObjects = sorted( dictOfMarketObjects, key=marketClass.getkeyBySpread ) 
print(sortedDictOfMarketObjects)

'''	
#print(dictOfMarketObjects[0])
backOdds = 0
layOdds = 0
#priceInfo = getPrices( marketObj.id )
i = 0
while not getPrices(sortedDictOfMarketObjects[i].id) :
	i += 1
	print(i)
	
	priceInfo = getPrices(sortedDictOfMarketObjects[i].id)

	print('backOdds = ' + str(priceInfo[0]))
	print('layOdds = ' + str(priceInfo[1]))
'''




