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
	marketObjects = marketAccess.getMarketInfo(setOfEvents, foxyGlobals.matchOdds)
	
	limit = min(foxyGlobals.priceRequestLimit, len(marketObjects))
	
	bestMarkets = marketObjects[:limit]
	
	for i in bestMarkets  :
		i = marketAccess.populatePrice( i, foxyGlobals.matchOdds )
	
	# This is now the largest match odds markets
	print('marketObjects = ' + str( bestMarkets) )
	

#--------------------------------------------------------
# Use the event ID's to get market data, then store in a lot of Market Data objects
# This is a soccer-only market, other market types will return 0

def callCorrectScoreQuery( setOfEvents ):

	print('callCorrectScoreQuery')
	marketObjects = marketAccess.getMarketInfo(setOfEvents, foxyGlobals.correctScore)
	
	limit = min(foxyGlobals.priceRequestLimit, len(marketObjects))
		
	#print('marketObjects = ' + str( marketObjects) )
	
	bestMarkets = []
	
	# Limit number of markets we want to investigate
	counter = 0
	i = 0
	while counter < limit and i < len(marketObjects) :
		
		print('counter : ' + str(counter))
		
		marketObjects[i] = marketAccess.populatePrice( marketObjects[i], foxyGlobals.correctScore )
	
		selections = marketObjects[i].price
		
		# this finds all the non-negative selections that are in the target group
		shortlist = [
					selection for selection in selections 
					if selection.spread > 0 
				]
			
		current_score = 'not defined'	
		viable = False
	
		
		# take a copy of TargetScores
		copyTarget = foxyGlobals.targetScores[:]

		
		loop = True
		while loop :
			t = copyTarget.pop(0)
			if len(copyTarget) == 0 :
				loop = False
			
			for s in shortlist :
				if t == s.score :
					current_score = t
					loop = False
					if s.backPrice < foxyGlobals.maxBackOdds and s.backPrice > foxyGlobals.minBackOdds : 
						if s.spread < foxyGlobals.maxSpread :
							viable = True
							counter += 1				
					break
		
		

		# record if this is viable
		marketObjects[i].currentScore = current_score
		marketObjects[i].viable = viable

		if viable == True :
			bestMarkets.append( marketObjects[i] )

		i += 1
		
	# this calls the __str__ version to output user info 
	print( str( bestMarkets ))
		

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





