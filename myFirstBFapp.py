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
import marketAccess
import accountAccess

'''
=======================================================================

Function definitions

-----------------------------------------------------------------------
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
#foxyBotLib.getAccountDetails()
#foxyBotLib.getAccountFunds()
accountAccess.getCurrentAccountDetails()
#--------------------------------------------------------


searchString = input ('Enter search term, s=soccer, t=tennis, c=cricket' )
if  searchString == 's'  :
	searchString = 'Soccer'
elif searchString == 't' :
	searchString = 'Tennis'
else :
	searchString = 'Cricket'


dictOfEvents = marketAccess.getInplayMarkets( searchString )
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
dictOfMarketObjects = marketAccess.getInplayMarketVols( setOfEvents )
if dictOfMarketObjects == 0 :
	print('Exiting')
	sys.exit(0)
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
	priceInfo = marketAccess.getPrices(i.id)
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




