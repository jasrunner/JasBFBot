import foxyBotLib
import foxyGlobals
import marketClass





'''
Task 1: 
	get a list of all in-play markets, filtered for football
	return the eventId, and a meaningful name for the event
'''
def getInplayMarkets( queryText ) :
	
	eventList = foxyBotLib.listEvents( queryText )
	
	myDict = {}
	for event in eventList :
	#	print(event)
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
def getInplayMarketVols( setOfEvents, marketType ):
	
	#turn eventList into proper formatted list
	numberEvents = len(setOfEvents)
	eventString = ""
	for eventId in setOfEvents :
		eventString += '\"'
		eventString += str(eventId)
		eventString += '\"'
		if eventId  != setOfEvents[numberEvents-1] :
			eventString += ','
		
	marketCat = foxyBotLib.listMarketCatalogue( eventString, numberEvents, marketType )
	
	if marketCat == 0:
		return 0
	
	
	myDict = {}
	for market in marketCat:
		marketId = market['marketId']
		myDict[ marketId ] = market[ 'totalMatched' ]
	
	print("These market ID's found (ID, volume, name) ")
	marketList = [] 
	for id in myDict :
		name = foxyBotLib.getEventNameFromMarketId(id)
		print( '\t' + str( id ) + " :\t" + str(myDict[id] )  + " :\t" + name )
		newObject =  marketClass.Market( id, name, marketType )
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
	
	print("price: " + str(price) )
	
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
		#return marketClass.Price(getBestOdds( runner ))
		return getBestOdds( runner )
		#print(runner['ex'])
		

		
#--------------------------------------------------------

def getBestOdds( runner) :
	
	bestBackOdds = runner['ex']['availableToBack']
	if not bestBackOdds :
		bestBackOdds = 0
		#print('no back odds available')
	else :
		bestBackOdds = bestBackOdds[0]['price']
		
	bestLayOdds = runner['ex']['availableToLay']
	if not bestLayOdds :
		bestLayOdds = 0
		#print('no lay odds available')
	else :
		bestLayOdds = bestLayOdds[0]['price']
		
	backOdds = bestBackOdds
	layOdds = bestLayOdds

	return  ( backOdds, layOdds )
	
	
#--------------------------------------------------------
def getSelections ( marketId, marketType ):
	
	selections = foxyBotLib.listMarketBook( marketId )
	
	#if not 
	if not selections :
		print( 'no results from marketId')
		return 
		
	numberOfRunners = selections[0]['numberOfRunners'] 
	
	#print( 'selections[0] = ' + str(selections[0] ))
	
	selectionList = 0
	if marketType == foxyGlobals.correctScore :
		selectionList = foxyGlobals.scoreLine
	elif marketType == foxyGlobals.matchOdds :
		selectionList = foxyGlobals.matchOutcome
		
	prices = []
	
	runners = selections[0]['runners'] 
	count = 0
	for runner in runners :
		odds =   getBestOdds( runner ) 
		newPrice = marketClass.Price(odds)
		newPrice.score = selectionList[ count ]
		prices.append(newPrice)
		count += 1
		
	return prices
		
	
#--------------------------------------------------------
'''
Task 4:
		Return list of best markets based on:
			- above defined volume (e.g. 10k)
			- ordered by smallest spread
			
'''

	
#--------------------------------------------------------
'''
Task 5:
	get correct score information for all runners for given event
	use getMarketCatalogue to runners: list< RunnerCatalogue >
	from runners, get selectionId and runnerName
	
	then task 6 to add price information for each one using getMarketBook

def getCorrectScoreCatalogue( eventId, marketType ):
	

	#turn eventList into proper formatted list
	numberEvents = len(setOfEvents)
	eventString = ""
	for eventId in setOfEvents :
		eventString += '\"'
		eventString += str(eventId)
		eventString += '\"'
		if eventId  != setOfEvents[numberEvents-1] :
			eventString += ',' 
	

	marketCat = foxyBotLib.listMarketCatalogue( str(eventId), 1, foxyGlobals.correctScore )
	
	if marketCat == 0:
		return 0
	
	print( "marketCat: " + str(marketCat ))
	
 
	
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
	return
	'''
	
