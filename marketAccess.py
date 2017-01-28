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
