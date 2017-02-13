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

def callMatchOddsQuery(setOfEvents):
	# Use the event ID's to get market data, then store in a lot of Market Data objects
	dictOfMarketObjects = marketAccess.getInplayMarketVols( setOfEvents, foxyGlobals.matchOdds )
	if dictOfMarketObjects == 0 :
		print('Exiting')
		sys.exit(0)
	marketIdCount = str(len(dictOfMarketObjects))
	
	
		
	print('___________________')	
	print( 'List of ' + marketIdCount + ' markets above min volume size, ordered by volume')
	#print ( )
	
	sortedDictOfMarketObjects = sorted( dictOfMarketObjects, key=marketClass.getkeyByVolume, reverse=True ) 
	#print(sortedDictOfMarketObjects)
		
	#--------------------------------------------------------
	
	sortedDictOfMarketObjects[0].price = marketAccess.getSelections(
					sortedDictOfMarketObjects[0].id, 
					foxyGlobals.matchOdds
	)
	
	print(sortedDictOfMarketObjects)
	
	# get the price information
	#marketObj = dictOfMarketObjects.pop()
	
	
	'''for i in sortedDictOfMarketObjects :
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

#--------------------------------------------------------

def callCorrectScoreQuery( setOfEvents ):
	'''
	investigate the correct score party(soccer only)
	lets use the same set of event id's found earlier,
	this is filtered for market (soccer) and in-play
	
	
	1) get the id, name, volumes for correct score markets based on previously found set of events
	
	'''
	print('Now asking for correct score')
	dictOfCorrectScore = marketAccess.getInplayMarketVols( setOfEvents, foxyGlobals.correctScore )
	if dictOfCorrectScore == 0 :
		print('Exiting')
		sys.exit(0)
	correctScoreCount = len(dictOfCorrectScore)
	
	#print( "correctScoreCount=" + correctScoreCount)
	
	print('___________________')	
	print( 'List of ' + str(correctScoreCount) + ' correct score markets above min volume size, ordered by volume')
	#print ( )
	
	if correctScoreCount == 0 :
		print( 'Exiting ')
		exit (0)
	
	sortedCorrectScoreObjects = sorted( dictOfCorrectScore, key=marketClass.getkeyByVolume, reverse=True ) 
	print(sortedCorrectScoreObjects)
	
	
	sortedCorrectScoreObjects[0].price = marketAccess.getSelections(
					sortedCorrectScoreObjects[0].id, 
					foxyGlobals.correctScore
	)
				
	sortedCorrectScoreObjects[0].numberOfRunners = len(sortedCorrectScoreObjects[0].price)
	#marketAccess.getSelections(sortedCorrectScoreObjects[0].id)
	
	print(sortedCorrectScoreObjects[0])
	print(foxyGlobals.scoreLine[0])
	
	'''
	thoughts: is different as will get larger range of "runners
	and want to determine what current score is based on the odds returned
	
	how do i get names of runners ?
	
	looks like need marketCatalogue to get information about the runner, i,e. name, selectionId
	then marketbook to get dynamic data, i.e, price info
	
	try to get start time from market projections (note in documentaion for getmarketcatalogue)
	cant find infon on runners.... maybe not available for correct score
	'''
	#marketAccess.getCorrectScoreCatalogue( setOfEvents[0], foxyGlobals.urlBetting )


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
# get detaiks from user's account
#--------------------------------------------------------

accountAccess.getCurrentAccountDetails()


#--------------------------------------------------------
# get input from user
#--------------------------------------------------------
searchString = input ('Enter search term, s=soccer, t=tennis, c=cricket' )
if  searchString == 's'  :
	searchString = 'Soccer'
elif searchString == 't' :
	searchString = 'Tennis'
else :
	searchString = 'Cricket'



queryType = input ('Enter search term, m=match_odds, c=correct_score' )
if  queryType == 'c'  :
	queryType = foxyGlobals.correctScore
else :
	queryType = foxyGlobals.matchOdds

#--------------------------------------------------------
# common processing: identify inplay events for the chosen sports betting category
#--------------------------------------------------------

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

if  queryType == foxyGlobals.matchOdds :
	callMatchOddsQuery( setOfEvents )
else :
	callCorrectScoreQuery( setOfEvents )





#--------------------------------------------------------





