import foxyBotLib
import marketClass
import foxyGlobals
import calculator

def makeABet( market ) :
	
	print('in Orders')
	selection = next( ( x for x in market.price if x.score == market.currentScore), None )
	
	backOdds = selection.backPrice
	backStake = foxyGlobals.minBetSize
	
	ret =  foxyBotLib.placeOrders( str(market.version), str( market.id ) , str( selection.selectionId ) , str( backStake ), str( backOdds), foxyGlobals.back )
	
	print('Return from placeOrders(back) is:  ' + str(ret) )
	
	status =  ret['status']
	print( 'Status is: ' + status )
	
	'''
	# check for error
	errorCode = ret['errorCode']
	if errorCode == 'INSUFFICIENT_FUNDS' :
		print('Insufficient funds, exiting ')
		return 
	'''
	
	
	# how to check for sucessful bet ?
	orderStatus =  ret['orderStatus']
	print( 'orderStatus is: ' + orderStatus )
	
	
	if orderStatus == 'EXECUTION_COMPLETE':
		print('lets work out the lay bet')
	
	# Lay the bet
		
		layBet 	= calculateLayStake( Decimal(backOdds), Decimal(backStake) )
	
		layStake = layBet[0]
		layOdds 	= layBet[1]
		
		print( '\nlayStake \t= ' + str( layStake ) )
		print( 'layOdds \t= ' + str(layOdds ) )
	
	'''
	ret =  foxyBotLib.placeOrders( str( market.id ) , str( selection.selectionId ) , str( backStake ), str( backOdds), foxyGlobals.lay )
	
	print('Return from placeOrders(lay) is:  ' + str(ret) )
	
	status =  ret['status']
	print( 'Status is: ' + status )
	
	# check for error
	errorCode = ret['errorCode']
	if errorCode == 'INSUFFICIENT_FUNDS' :
		print('Insufficient funds, exiting ')
		return 
	
	error == 'INVALID_ODDS '
	# how to check for sucessful lay ?
	'''
	
	return
