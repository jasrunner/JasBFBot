
# Import the modules needed to run the script.
import sys, os
import itertools
import time

import accountAccess
import orders
import foxyGlobals
import fileOperations
import strategy

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
	
	setOfEvents = strategy.getSetOfEvents( 'Soccer' )
	
	
	print( "\n======\nSoccer\n------\n" )
	print( "1. Match Odds" )
	print( "2. Correct Score" )
	print( "3. Save current data to file" )
	print( "9. Back" )
	print( "0. Quit" )
	choice = input(" >>  ")
	
	bestMarkets = ''
	
	if choice.lower() == '1' :
		bestMarkets = strategy.callMatchOddsQuery( setOfEvents )
		choice = '20'
		
		
	elif choice.lower() == '2' :
		bestMarkets = strategy.callCorrectScoreQuery( setOfEvents )
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
		strategy.callPlaceABet( args )
		choice = '30'
	if choice.lower() == '2' :
		print( "you chose listCurrentOrders")
		choice = '30'
		currentBetList( args )
	
		
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
		testCorrectScore( 1,0 )
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
	
#--------------------------------------------------------
def currentBetList( args ):
	orderList = orders.listCurrentOrders()
	print('List of Orders: ' + str(orderList))	
	exec_menu('1', args)


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
#--------------------------------------------------------
def matchOdds ( args ) :
	setOfEvents = strategy.getSetOfEvents( args )
	
	strategy.callMatchOddsQuery( setOfEvents )
		


	
#--------------------------------------------------------
def testCorrectScore( args )	 :
	numberIterations = args[0]
	delay = args[1]
	labels = args[2]
	
	if labels != [] :
		balanceLabel = labels[1]
		exposureLabel = labels[2]
		iterationsLabel = labels[3]
	
	counter = 0
	
	for _ in itertools.repeat(None, numberIterations ):
		
		print( 'testCorrectScore, loop ' )	
	
		setOfEvents = strategy.getSetOfEvents( 'Soccer' )
		bestMarkets = strategy.callCorrectScoreQuery( setOfEvents )
		strategy.callPlaceABet( bestMarkets )
		print('Iteration: ' + str(counter) + ' before sleep ' + str( time.ctime(time.time())) )
		time.sleep(delay)
		print('after sleep ' + str( time.ctime(time.time())) )
		counter += 1
		if labels != [] :
			accountDetails = accountAccess.getCurrentAccountDetails()
			balanceLabel.text = str(accountDetails.availableToBet)
			exposureLabel.text = str(accountDetails.exposure)
			iterationsLabel.text = str(counter)
		
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

