
# Import the modules needed to run the script.
import sys, os

import accountAccess
import marketAccess
import orders
import foxyGlobals
import fileOperations
import foxyBotLib

# Main definition - constants
menu_actions  = {}  


'''
=======================================================================

Function definitions for menu display and control

-----------------------------------------------------------------------
'''

# Main menu
def mainMenu( args ):
	os.system('clear')
	
	print( "Welcome " + args + "\n")
	print( "Please choose between Accounts and Sports:" )
	print( "1. Accounts" )
	print( "2. Sports" )
	print( "3. Load from file" )
	print( "4. Test " )
	print( "\n0. Quit" )
	choice = input(" >>  ")
	exec_menu( choice, '')

	return

#--------------------------------------------------------
# Execute menu
def exec_menu(choice, args):
	os.system('clear')
	ch = choice.lower()
	if ch == '':
		menu_actions['main_menu']( '' )
	else:
		try:
			menu_actions[ch]( args )
		except KeyError:
			print( "Invalid selection, please try again.\n" + menu_actions['main_menu']( '' ) )
	return

#--------------------------------------------------------
# Menu 1
def accountsMenu( args ):
	print( "\n========\nAccounts\n--------\n" )
	print( "1. Summary" )
	print( "2. List current orders")
	print( "9. Back" )
	print( "0. Quit" )
	choice = input(" >>  ")

	if choice.lower() == '1' :
		choice = '10'
		
	if choice.lower() == '2' :

		choice = '11'
		
		
	exec_menu(choice, '')
	return
 
 
#--------------------------------------------------------
# Menu 2
def sportsMenu( args ):
	print( "\n======\nSports\n------\n" )
	print( "1. Soccer" )
	print( "2. Tennis" )
	print( "3. Cricket" )
	print( "9. Back" )
	print( "0. Quit" )
	choice = input(" >>  ")
	
	if choice.lower() == '1' :
		choice = '20'	
		sportsMarket = 'Soccer'
	elif choice.lower() == '2' :
		choice = '21'
		sportsMarket = 'Tennis'
	elif choice.lower() == '3' :
		choice = '22'
		sportsMarket = 'Cricket'
	exec_menu(choice, sportsMarket)
	return
	
#--------------------------------------------------------
# Menu 3
def soccerMenu( args ):
	
	setOfEvents = getSetOfEvents( 'Soccer' )
	
	
	print( "\n======\nSoccer\n------\n" )
	print( "1. Match Odds" )
	print( "2. Correct Score" )
	print( "3. Save current data to file" )
	print( "9. Back" )
	print( "0. Quit" )
	choice = input(" >>  ")
	
	bestMarkets = ''
	
	if choice.lower() == '1' :
		bestMarkets = callMatchOddsQuery( setOfEvents )
		choice = '20'
		
		
	elif choice.lower() == '2' :
		bestMarkets = callCorrectScoreQuery( setOfEvents )
		choice = '30'
		
	elif choice.lower() == '3' :
		print( "Enter Filename, " + foxyGlobals.defaultFilename + " is default)" )
		filename = input(" >> " )
		fileOperations.saveToFile( args, filename )
		choice = '20'
	
	#print('best markets = ' + str( bestMarkets ) )
			
	exec_menu(choice, bestMarkets)
	
	return
#--------------------------------------------------------
# Menu 4

def bettingMenu( args ):
	
	
	print( "\n===========\nBettingMenu\n---------\n" )
	
	print( "1. Place a bet")
	print( "2. List current orders")
	print( "9. Back" )
	print( "0. Quit" )
	choice = input(" >>  ")
	
	if choice.lower() == '1' :
		print( "you chose to place a bet" )
		callPlaceABet( args )
		choice = '30'
	if choice.lower() == '2' :
		print( "you chose listCurrentOrders")
		choice = '30'
		callListCurrentOrders( args )
		
		
	exec_menu(choice, '')
	
	return

#--------------------------------------------------------
# Menu 5
def testMenu( args ):
	print( "\n========\nTest Menu\n--------\n" )
	print( "1. Run Correct Score test" )
	print( "9. Back" )
	print( "0. Quit" )
	choice = input(" >>  ")

	if choice.lower() == '1' :
		testCorrectScore( args )
	exec_menu(choice, '')
	return

#--------------------------------------------------------
# Back to main menu
def back( args ):
	menu_actions['main_menu']('jas')

#--------------------------------------------------------
# Exit program
def exit( args ):
	sys.exit()

#--------------------------------------------------------
def accountSummary( args ):
	accountAccess.getCurrentAccountDetails()
	exec_menu('1', args)
	#back( args )
	
#--------------------------------------------------------
def currentBetList( args ):
	orderList = orders.listCurrentOrders()
	print('List of Orders: ' + str(orderList))	
	exec_menu('1', args)
	#back( args )


#--------------------------------------------------------
def loadFromFile( args ) :

	print( "Enter Filename, " + foxyGlobals.defaultFilename + " is default)" )
	filename = input(" >> " )

	loadedData = fileOperations.loadFromFile( filename )
	print('your data : ')
	print( loadedData)
	
	mainMenu( '' )

#--------------------------------------------------------		
def callPlaceABet(args) :
	print("calling out to betting function, max 5 bets")
	
	if args == [] :
		print('Nothing found that satisfies criteria')
		back(args)
	
	print('length of marketList is ' + str(len(args)))
	
	orderList = orders.listCurrentOrders()	
	
	limit = 5
	counter = 0
	
	for market in args :
	
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
	
	back(args)

	
	
	
			
'''
=======================================================================

Operations 

-----------------------------------------------------------------------
'''
def matchOdds ( args ) :
	setOfEvents = getSetOfEvents( args )
	
	callMatchOddsQuery( setOfEvents )
		
	
	

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
#
def callMatchOddsQuery(setOfEvents):

	print( 'callMatchOddsQuery' )
	marketObjects = marketAccess.getMarketInfo(setOfEvents, foxyGlobals.matchOdds)
	
	limit = min(foxyGlobals.priceRequestLimit, len(marketObjects))
	
	bestMarkets = marketObjects[:limit]
	
	#for i in bestMarkets  :
	#	i = marketAccess.populatePrice( i, foxyGlobals.matchOdds )
	marketAccess.populatePrice( bestMarkets, foxyGlobals.matchOdds )
	
	# This is now the largest match odds markets
	print('marketObjects[0] = ' + str( bestMarkets[0]) )
	#print(bestMarkets)
	
	return bestMarkets
	
	
	#filename = 'match_odds.pickle'
	#fileOperations.saveToFile(bestMarkets, filename)
	#fileOperations.loadFromFile(filename)

#--------------------------------------------------------
# Use the event ID's to get market data, then store in a lot of Market Data objects
# This is a soccer-only market, other market types will return 0

def callCorrectScoreQuery( setOfEvents ):

	print('callCorrectScoreQuery')
	marketIdList = marketAccess.getMarketInfo(setOfEvents, foxyGlobals.correctScore)
	
	limit = min(foxyGlobals.priceRequestLimit, len(marketIdList))
	print('limit = ' + str(limit))
		
	#print('marketObjects = ' + str( marketObjects) )
	
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
		#marketObjects[i] = marketAccess.populatePrice( marketObjects[i], foxyGlobals.correctScore )
	
		selections = marketObject.price
		
		# this finds all the non-negative selections that are in the target group
		shortlist = [
					selection for selection in selections 
					if selection.spread > 0 
				]
			
		current_score = 'not defined'	
		viable = True
		#exclusion = 'Spread is negative: ' + str()
	
		
		# take a copy of TargetScores
		copyTarget = foxyGlobals.targetScores[:]

		exclusion = ''
		loop = True
		while loop :
			t = copyTarget.pop(0)
			if len(copyTarget) == 0 :
				loop = False
			
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
						print(exclusion)
						print(s.spread)
						print(foxyGlobals.maxSpread)
						break
				#counter += 1
				
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
	
	#print( str( bestMarkets ))
	
	#filename = 'current_score.pickle'
	#fileOperations.saveToFile(marketObjects, filename)
	#fileOperations.loadFromFile(filename)
	

	
#--------------------------------------------------------
def testCorrectScore( args )	 :
	
	setOfEvents = getSetOfEvents( 'Soccer' )
	bestMarkets = callCorrectScoreQuery( setOfEvents )
	callPlaceABet( bestMarkets )
	
		
	return
'''
=======================================================================

Menu definitions 

-----------------------------------------------------------------------
'''

 
# Menu definition
menu_actions = {
	'main_menu': mainMenu,
	'1': accountsMenu,
	'2': sportsMenu,
	'3': loadFromFile,
	'4': testMenu,
	'10': accountSummary,
	'11': currentBetList,
	'20': soccerMenu,
	'21': matchOdds,
	'30': bettingMenu,
	'9': back,
	'0': exit,
}

