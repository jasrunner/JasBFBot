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
'''
	Find market ID's for the set of event ID's
	and market type (match odds, correct score, etc)
	Return : dictionary of {marketId : volumeTraded}
'''
def getInplayMarketVols( setOfEvents, marketType ):
	
	# clever python makes csv creation easy ! 
	s='","'
	eventString='"' + s.join(setOfEvents) + '"'
	

	marketCat = foxyBotLib.listMarketCatalogue( eventString, marketType )
	
	if marketCat == 0:
		return 0
	
	# Extract market ID's for target events
	myDict = {}
	for market in marketCat:
		marketId = market['marketId']
		myDict[ marketId ] = market[ 'totalMatched' ]
	
	# create a list of Market objects for those satisfying min volume 
	# populate just the volume and market id 
	marketList = [] 
	for id in myDict :
		if myDict[ id ] :
			#name = foxyBotLib.getEventNameFromMarketId(id)
			newObject =  marketClass.Market( id, marketType )
			newObject.volume = myDict[ id ]
			marketList.append( newObject  )
	
	#print('market!ist. ' + str(marketList))		
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
	#print(selections)
	#if not 
	if not selections :
		print( 'no results from marketId')
		return 
		
	numberOfRunners = selections[0]['numberOfRunners'] 
	version = selections[0]['version']
	
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
		selectionId = runner['selectionId']
		odds =   getBestOdds( runner ) 
		newPrice = marketClass.Price(odds, selectionId)
		newPrice.score = selectionList[ count ] 
		prices.append(newPrice)
		count += 1
		
	return (version, prices)
		
	
#--------------------------------------------------------
'''
	common code that gets market info based on event set
		Return list of markets ordered by volume:		
'''
def getMarketInfo( setOfEvents, marketType ) :
	
	dictOfMarketObjects = getInplayMarketVols( setOfEvents, marketType )
	if dictOfMarketObjects == 0 :
		print('Exiting')
		sys.exit(0)
	marketIdCount = str(len(dictOfMarketObjects))

		
	print('___________________')	
	print( 'List of ' + marketIdCount + ' markets above min volume size (' + str(foxyGlobals.minVolume) + '), ordered by volume')
	
	if marketIdCount == 0 :
		print( 'Exiting ')
		sys.exit (0)
	
	sortedDictOfMarketObjects = sorted( dictOfMarketObjects, key=marketClass.getkeyByVolume, reverse=True ) 
	
	return sortedDictOfMarketObjects

	
	
#--------------------------------------------------------
'''
	common code that gets Price info for given market object
	Return: market object
'''
def populatePrice( marketObject, marketType) :
	
	
	selections = getSelections(
				marketObject.id, 
					marketType
	)
	marketObject.price = selections[1]
	marketObject.version = selections[0]

	marketObject.numberOfRunners = len(marketObject.price)
	marketObject.name = foxyBotLib.getEventNameFromMarketId(marketObject.id)
	

	return marketObject


#--------------------------------------------------------


	
