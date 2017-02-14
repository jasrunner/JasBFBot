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

#--------------------------------------------------------
# Use the event ID's to get market data, then store in a lot of Market Data objects

def callMatchOddsQuery(setOfEvents):

	print( 'callMatchOddsQuery' )

	dictOfMarketObjects = marketAccess.getInplayMarketVols( setOfEvents, foxyGlobals.matchOdds )
	if dictOfMarketObjects == 0 :
		print('Exiting')
		sys.exit(0)
	marketIdCount = str(len(dictOfMarketObjects))
		
	print('___________________')	
	print( 'List of ' + marketIdCount + ' markets above min volume size, ordered by volume')
	
	if marketIdCount == 0 :
		print( 'Exiting ')
		sys.exit (0)
	
	sortedDictOfMarketObjects = sorted( dictOfMarketObjects, key=marketClass.getkeyByVolume, reverse=True ) 

	
	sortedDictOfMarketObjects[0].price = marketAccess.getSelections(
					sortedDictOfMarketObjects[0].id, 
					foxyGlobals.matchOdds
	)
	
	sortedDictOfMarketObjects[0].numberOfRunners = len(sortedDictOfMarketObjects[0].price)
	
	print('sortedDict = ' + str(sortedDictOfMarketObjects) )
	



#--------------------------------------------------------
# Use the event ID's to get market data, then store in a lot of Market Data objects

def callCorrectScoreQuery( setOfEvents ):

	print('callCorrectScoreQuery')
	dictOfCorrectScore = marketAccess.getInplayMarketVols( setOfEvents, foxyGlobals.correctScore )
	
	if dictOfCorrectScore == 0 :
		print('Exiting')
		sys.exit(0)
	correctScoreCount = len(dictOfCorrectScore)
	
	print('___________________')	
	print( 'List of ' + str(correctScoreCount) + ' correct score markets above min volume size, ordered by volume')
	
	if correctScoreCount == 0 :
		print( 'Exiting ')
		sys.exit (0)
	
	sortedCorrectScoreObjects = sorted( dictOfCorrectScore, key=marketClass.getkeyByVolume, reverse=True ) 
	
	
	sortedCorrectScoreObjects[0].price = marketAccess.getSelections(
					sortedCorrectScoreObjects[0].id, 
					foxyGlobals.correctScore
	)
				
	sortedCorrectScoreObjects[0].numberOfRunners = len(sortedCorrectScoreObjects[0].price)
	
	print(sortedCorrectScoreObjects[0])



'''
=======================================================================

Main:

-----------------------------------------------------------------------
'''


# Parameter check


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
# get details from user's account
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
elif queryType == foxyGlobals.correctScore :
	callCorrectScoreQuery( setOfEvents )
else :
	print( 'Unknown queryType: ' + queryType )
	sys.exit(0)





#--------------------------------------------------------





