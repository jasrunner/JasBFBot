
# Import the modules needed to run the script.
import sys, os

import accountAccess
import marketAccess
import foxyGlobals
import fileOperations

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
	print( "9. Back" )
	print( "0. Quit" )
	choice = input(" >>  ")

	if choice.lower() == '1' :
		choice = '10'
	exec_menu(choice, '')
	return
 
 
#--------------------------------------------------------
# Menu 2
def sportsMenu( args ):
	print( "\n======\nSports\n------\n" )
	print( "S. Soccer" )
	print( "T. Tennis" )
	print( "C. Cricket" )
	print( "9. Back" )
	print( "0. Quit" )
	choice = input(" >>  ")
	
	if choice.lower() == 's' :
		choice = '20'	
		sportsMarket = 'Soccer'
	elif choice.lower() == 't' :
		choice = '21'
		sportsMarket = 'Tennis'
	elif choice.lower() == 'c' :
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
		choice = '20'
		
	elif choice.lower() == '3' :
		print( "Enter Filename, " + foxyGlobals.defaultFilename + " is default)" )
		filename = input(" >> " )
		fileOperations.saveToFile( args, filename )
		choice = '20'
	
	print('best markets = ' + str( bestMarkets ) )
			
	exec_menu(choice, bestMarkets)
	
	return
#--------------------------------------------------------
# Menu 4
'''
def saveMenu( args ):
	
	
	print( "\n======\nSave\n------\n" )
	
	print( "9. Back" )
	print( "0. Quit" )
	choice = input(" >>  ")
	
	if choice.lower() == '1' :
		print( "Enter Filename, " + foxyGlobals.defaultFilemame + " is default)" )
		filename = input(" >> " )
		savetoFile( args, filename )
		choice = '20'
		
		
	exec_menu(choice, '')
	
	return
'''

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
	back( args )
	

#--------------------------------------------------------
def loadFromFile( args ) :

	print( "Enter Filename, " + foxyGlobals.defaultFilename + " is default)" )
	filename = input(" >> " )

	loadedData = fileOperations.loadFromFile( filename )
	print('your data : ')
	print( loadedData)
	
	mainMenu( '' )
	
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
	
	for i in bestMarkets  :
		i = marketAccess.populatePrice( i, foxyGlobals.matchOdds )
	
	# This is now the largest match odds markets
	print('marketObjects = ' + str( bestMarkets) )
	
	return bestMarkets
	
	
	#filename = 'match_odds.pickle'
	#fileOperations.saveToFile(bestMarkets, filename)
	#fileOperations.loadFromFile(filename)

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
	for i in bestMarkets :
		print( str(i) )
		
	return bestMarkets
	
	#print( str( bestMarkets ))
	
	#filename = 'current_score.pickle'
	#fileOperations.saveToFile(marketObjects, filename)
	#fileOperations.loadFromFile(filename)
	
	
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
	'10': accountSummary,
	'20': soccerMenu,
	'21': matchOdds,
	'9': back,
	'0': exit,
}

