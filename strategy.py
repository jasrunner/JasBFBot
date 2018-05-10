'''
Collecting the strategies together here
'''

import marketAccess
import foxyBotLib
import foxyGlobals
import orders


#--------------------------------------------------------
# common processing: identify inplay events for the chosen sports betting category
#--------------------------------------------------------
def getSetOfEvents(searchString) :

	dictOfEvents = marketAccess.getInplayMarkets( searchString )
	inplayMarketCount = str(len(dictOfEvents))
	
	print('___________________')
	print( 'List of ' + inplayMarketCount + ' inplay markets for: ' + searchString )
	
	setOfEvents = []
	
	print('\tevent Id :\tevent name')
	for id in dictOfEvents :
		print( '\t' + str( id ) + " :\t" + dictOfEvents[id] )
		setOfEvents.append(id)
	
	return setOfEvents
	
	
#--------------------------------------------------------
def getSetOfWeekendEvents(searchString, homeTeam, awayTeam) :

	dictOfEvents = marketAccess.getWeekendMarkets( searchString, homeTeam )
	inplayMarketCount = str(len(dictOfEvents))
	
	for id in dictOfEvents :
		if awayTeam in dictOfEvents[id] :
			return [id, dictOfEvents[id]]
	
	return 
	
#--------------------------------------------------------
#
def callMatchOddsQuery(setOfEvents):

	print( 'callMatchOddsQuery' )
	marketObjects = marketAccess.getMarketIds(setOfEvents, foxyGlobals.matchOdds)
	
	if marketIdList == [] :
		print( 'returning from callCorrectScoreQuery')
		return []
	
	limit = min(foxyGlobals.priceRequestLimit, len(marketObjects))
	
	bestMarkets = marketObjects[:limit]
	
	#for i in bestMarkets  :
	#	i = marketAccess.populatePrice( i, foxyGlobals.matchOdds )
	marketAccess.populatePrice( bestMarkets, foxyGlobals.matchOdds )
	
	# This is now the largest match odds markets
	print('marketObjects[0] = ' + str( bestMarkets[0]) )
	#print(bestMarkets)
	
	return bestMarkets


#--------------------------------------------------------
# added for poolpredictor - get odds of score draws
def getScoreDrawOdds( setOfEvents ):
	
	print('getMarketIds')
	marketIdList = marketAccess.getMarketIds(setOfEvents, foxyGlobals.correctScore)
	
	marketObjects = marketAccess.populatePrice( marketIdList, foxyGlobals.correctScore )
	
	print('number of marketObjects = ' + str(len(marketObjects)))
	# now marketObjects should be populated
	
	for marketObject in marketObjects :	
		print(marketObject)
		
	return

#--------------------------------------------------------
# Use the event ID's to get market data, then store in a lot of Market Data objects
# This is a soccer-only market, other market types will return 0

def callCorrectScoreQuery( setOfEvents ):

	print('callCorrectScoreQuery')
	marketIdList = marketAccess.getMarketIds(setOfEvents, foxyGlobals.correctScore)
	
	if marketIdList == [] :
		print( 'returning from callCorrectScoreQuery')
		return []
	
	
	bestMarkets = []
	excludedMarkets = []
	
	# jas: todo
	marketObjects = marketAccess.populatePrice( marketIdList, foxyGlobals.correctScore )
	
	print('number of marketObjects = ' + str(len(marketObjects)))
	# now marketObjects should be populated
	
	# Limit number of markets we want to investigate
	#counter = 0
	#i = 0
	#while counter < limit and i < len(marketObjects) :
	for marketObject in marketObjects :	
		
		exclusion = ''
		current_score = 'not defined'	
		viable = True

		selections = marketObject.price
		
		# this finds all the non-negative selections that are in the target group
		shortlist = [
					selection for selection in selections 
					if selection.spread > 0 
				]
		
		if shortlist == [] :
			exclusion = 'All spreads are negative'
			viable = False
	
		
		# take a copy of TargetScores
		copyTarget = foxyGlobals.targetScores[:]

		
		loop = True
		while loop :
			t = copyTarget.pop(0)

			# shortList are the possible current scores
			for s in shortlist :
				if t == s.score :
					current_score = t
					loop = False
					if s.backPrice > foxyGlobals.maxBackOdds or s.backPrice < foxyGlobals.minBackOdds : 
						viable = False
						exclusion = 'Back price out of bounds: ' 
						break
		
					if s.spread > foxyGlobals.maxSpread :
						viable = False
						exclusion = 'Spread too large'
						break
				
			if (loop == True) and  ( len(copyTarget) == 0 ) :
				exclusion = 'not a target score '
				viable = False			
				loop = False
				
		if viable == True :		
			
			if marketObject.totalMatched  < foxyGlobals.minVolume :
				viable = False
				exclusion = 'Volume too small'	
				
				
			elif marketObject.status != 'OPEN' :
				viable = False
				exclusion = 'Market not open'
				
			elif marketObject.betDelay > foxyGlobals.betDelay :
				viable = False
				exclusion = 'Delay too large'
			
		# record if this is viable
		marketObject.currentScore = current_score
		marketObject.viable = viable
		marketObject.exclusion = exclusion

		if viable == True :
			bestMarkets.append( marketObject )
			print('viable')
		else :
			excludedMarkets.append( marketObject )
			print('not viable')

		#i += 1
		
	# this calls the __str__ version to output user info 
	print('BestMarkets:')
	print('___________________')
	for i in bestMarkets :
		i.name = foxyBotLib.getEventNameFromMarketId( i.id )
		print( str(i) )
	
	print('ExcludedMarkets:')
	print('___________________')
	for i in excludedMarkets :
		print( str(i) )
		
	return bestMarkets
	

#--------------------------------------------------------		
def callPlaceABet(args) :
	print("calling out to betting function, max 5 bets")
	
	if args == [] :
		print('Nothing found that satisfies criteria')
		return (args)
	
	print('length of marketList is ' + str(len(args)))
	
	orderList = orders.listCurrentOrders()	
	
	limit = 5
	counter = 0
	
	for market in args :
		
		success = ''
	
		# if there are existing orders, 
		# check if we already have a bet on this market:		
		if orderList != [] :	
			
			if any( x for x in orderList if x.marketId == market.id ) :
				print('already exists, cant bet on this market')

			else :
				print(market)	
				success = orders.makeABet(market)
				#return
		
		#	else no existing bets so go ahead and make one
		else :
			print(market)	
			success = orders.makeABet(market)
			#return
		
		if success == 'SUCCESS' :
			++counter
		
			if counter == limit :
				print('Reached bet limit, returning')
				return
	
	return(args)
	

