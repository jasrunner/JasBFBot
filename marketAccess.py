import sys
import foxyBotLib
import foxyGlobals
import marketClass




'''
	Generate a list of all in-play markets, filtered by query,
	e.g. soccer, cricket, etc
	Return : dictionary { eventId : eventName }
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
def getWeekendMarkets( queryText, team ) :
	
	eventList = foxyBotLib.listWeekendEvents( queryText, team )
	
	myDict = {}
	for event in eventList :
	#	print(event)
		eventId = event['event'] ['id']

		myDict [ eventId ] = event['event'] ['name']
	
	return myDict
	
#--------------------------------------------------------
'''
	Find market ID's for the set of event ID's
	and market type (match odds, correct score, etc)
	Return : dictionary of {marketId : volumeTraded}
	
	now= returns a list of market Ids.  i.e. has converted events into market ids. 
'''
def getInplayMarketVols( setOfEvents, marketType ):
	
	# clever python makes csv creation easy ! 
	s='","'
	eventString='"' + s.join(setOfEvents) + '"'
	

	marketCat = foxyBotLib.listMarketCatalogue( eventString, marketType )
	
	if marketCat == 0:
		return 0
	
	marketIdList = []
	# Extract market ID's for target events
	myDict = {}
	for market in marketCat :
		marketIdList.append ( market['marketId'] )
		

	#print('market!ist. ' + str(marketList))		
	return marketIdList



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
# getSelections now works with a list of marketIds for input,
# and returns list of marketObjects
def getSelections ( marketIds, marketType ):
	
	print('getSelections')
	
	# clever python makes csv creation easy ! 
	s='","'
	marketIdString='"' + s.join(marketIds) + '"'
	
	print('market id string = ')
	print(marketIdString)
	selections = foxyBotLib.listMarketBook( marketIdString )
	#print(selections)
	#if not 
	if not selections :
		print( 'no results from marketId')
		return 
	else:
		print( 'getSelections= number of selections found = ' + str(len(selections ) ) )
	results = []
	
	# each selection maps onto a market object
	for selection in selections :
	# here we can get market ID - changing for multiples in one call.

		marketId			  = selection['marketId']
		newObject = marketClass.Market( marketId, foxyGlobals.correctScore )

		newObject.numberOfRunners = selection['numberOfRunners'] 
		newObject.version         = selection['version']
		newObject.totalMatched    = selection['totalMatched']
		newObject.betDelay        = selection['betDelay']	
		newObject.status          = selection['status']
		
		runners         = selection['runners'] 
	
		
		#print( 'selections[0] = ' + str(selections[0] ))
		
		selectionList = 0
		if marketType == foxyGlobals.correctScore :
			selectionList = foxyGlobals.scoreLine
		elif marketType == foxyGlobals.matchOdds :
			selectionList = foxyGlobals.matchOutcome
			
		prices = []
		
		
		count = 0
		for runner in runners :
			selectionId = runner['selectionId']
			odds =   getBestOdds( runner ) 
			newPrice = marketClass.Price(odds, selectionId)
			newPrice.score = selectionList[ count ] 
			prices.append(newPrice)
			count += 1
			
		newObject.price = prices
		results.append(newObject)
		
	return ( results )
		
	
#--------------------------------------------------------
'''
	common code that gets market info based on event set
		Return list of markets ordered by volume:		
'''
def getMarketInfo( setOfEvents, marketType ) :
	
	print('getMarketInfo')
	
	marketIdList = getInplayMarketVols( setOfEvents, marketType )
	if marketIdList == 0 :
		print('Exiting')
		sys.exit(0)
	marketIdCount = len(marketIdList)

		
	print('___________________')	
	#print( 'List of ' + marketIdCount + ' markets above min volume size (' + str(foxyGlobals.minVolume) + '), ordered by volume')
	
	if marketIdCount == 0 :
		print( 'Returning [] as no marketIds found (getMarketInfo) ')
		return []
		#sys.exit (0)
	
	print( 'Number of market Ids found = ' + str(marketIdCount ) )
	return marketIdList

	
	
#--------------------------------------------------------
'''
	Input: list of market Id's
	Output: llst of market objects
	
	nb: broke request down into blocksize to fix:
	 'error': {'message': 'ANGX-0001', 'code': -32099, 'data': {'exceptionname': 'APINGException', 'APINGException': {'errorDetails': '', 'requestUUID': 'prdang005-04180837-00eecb297c', 'errorCode': 'TOO_MUCH_DATA'}}}}
'''
#jas: todo 
def populatePrice( marketIdList, marketType) :
	
	print('populatePrice')
	
	
	# split here
	
	length = len(marketIdList)
	
	#if len(marketIdList) > foxyGlobals.priceRequestLimit )
	blockSize = 5
	count = 0
	selections = []
	while (count + blockSize) < length :
		
		selections.extend ( getSelections(
				marketIdList[count:(count+blockSize)], 
				marketType
		) )
		count += blockSize
	
	if count < length :
		selections.extend ( getSelections(
				marketIdList[count:], 
				marketType
		) )

	
	
	print('number selections = ' + str(len(selections)))
	#print(str(selections))
	
	# now match each market id and populate...
	
	#marketObject.price = selections[1]
	#marketObject.version = selections[0]

	#marketObject.numberOfRunners = len(marketObject.price)
	
	# lets restrict this to just the ones we want to bet on
	# if la-di-dah
	#getSelections[0].name = foxyBotLib.getEventNameFromMarketId(marketObject.id)
	# todo ! ! ! 

	return selections



#--------------------------------------------------------


	
