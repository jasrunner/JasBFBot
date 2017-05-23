import foxyBotLib
import marketClass
import foxyGlobals
import calculator
import timeit
import bs4
from decimal import *

#--------------------------------------------------------
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
	
	'''
	Return from placeOrders(back) is:  {'marketId': '1.131475201', 'instructionReports': [
		{'betId': '92890636267', 
		
		'instruction': 
			{'orderType': 'LIMIT', 'side': 'BACK', 'selectionId': 1, 'limitOrder': {'persistenceType': 'LAPSE', 'price': 3.0, 'size': 2.0}}, '
			
			
			status': 'SUCCESS',
			 'placedDate': '2017-05-14T20:05:30.000Z',
			  'sizeMatched': 2.0, 
			  'averagePriceMatched': 3.0, 
			  'orderStatus': 'EXECUTION_COMPLETE'}
		], 'status': 'SUCCESS'}
	'''
	# how to check for sucessful bet ?
	print(ret['instructionReports'])
	orderStatus =  ret['instructionReports'][0]['orderStatus']
	print( 'orderStatus is: ' + orderStatus )
	
	
	if orderStatus == 'EXECUTION_COMPLETE':
		print('lets work out the lay bet')
	
		# Lay the bet
		layBet 	= calculator.calculateLayStake( Decimal(backOdds), Decimal(backStake)  )
	
		layStake = layBet[0]
		layOdds  = layBet[1]
		
		print( '\nlayStake \t= ' + str( layStake ) )
		print( 'layOdds \t= ' + str(layOdds ) )
		
		ret =  foxyBotLib.placeOrders( str(market.version), str( market.id ) , str( selection.selectionId ) , str( layStake ), str( layOdds), foxyGlobals.lay )
		
		print('Return from placeOrders(lay) is:  ' + str(ret) )
	
		status =  ret['status']
		print( 'Status is: ' + status )
		
		betId = ret['betId']
		print( 'betId is: ' + betId )
		market.betId = betId
	
	elif orderStatus == 'EXECUTABLE' :
		print('Bet wasnt executed, wait 10 seconds then kill it')
		
		betId = ret['betId']
		print( 'betId is: ' + betId )
		market.betId = betId
		
		time.sleep(10)
		
		#need to use betId, marketId, selectionId to get current status
		
	
	else :
		print('in else, why are we here? \n what do we do here?')
		
	return
	
	'''
	Status is: SUCCESS
[{'betId': '92893366442', 'instruction': {'orderType': 'LIMIT', 'side': 'BACK', 'selectionId': 4, 'limitOrder': {'persistenceType': 'LAPSE', 'price': 1.81, 'size': 2.0}}, 'status': 'SUCCESS', 'placedDate': '2017-05-14T20:36:04.000Z', 'sizeMatched': 0.0, 'averagePriceMatched': 0.0, 'orderStatus': 'EXECUTABLE'}]
orderStatus is: EXECUTABLE
	'''

#--------------------------------------------------------
class Order (object):
	
	
	def __init__( self, betId, marketId, selectionId, side, status  ) :
		self.betId 				= betId
		self.marketId 		= marketId
		self.selectionId  = selectionId
		self.side 			  = side
		self.status 		  = status
		
	def __repr__( self ) :
		
		return '''
			\tBetId: 			{}
			\t	MarketId 			{}
			\t	SelectionId:		{}
			\t	Side: 				{} 
			\t	Status: 			{}
			'''.format ( 
				self.betId ,
				self.marketId ,
				self.selectionId ,
				self.side ,
				self.status
			)
			
	#def getkeyByMarketId ( Order ) :
	#	return Order.marketId


#--------------------------------------------------------
def listCurrentOrders(  ) :
	
	result = foxyBotLib.listCurrentOrders()
	
	print('in listCurrentOrders')
	currentOrders = result['currentOrders']
	#print(currentOrders)
	if currentOrders == [] :
		print('no current bets')
		return []
	
	'''
	{"betId":"93505375296","marketId":"1.131711693","selectionId":1,"handicap":0.0,"priceSize":{"price":3.7,"size":2.0},"bspLiability":0.0,"side":"BACK","status":"EXECUTION_COMPLETE","persistenceType":"LAPSE","orderType":"LIMIT","placedDate":"2017-05-21T20:04:13.000Z","matchedDate":"2017-05-21T20:05:01.000Z","averagePriceMatched":3.7,"sizeMatched":2.0,"sizeRemaining":0.0,"sizeLapsed":0.0,"sizeCancelled":0.0,"sizeVoided":0.0,"regulatorCode":"GIBRALTAR REGULATOR"}
	'''
	
	orderList = [] 
	
	for order in currentOrders :
		betId = order['betId']
		marketId = order['marketId']
		selectionId = order['selectionId']
		side = order['side']
		status = order['status']
		
		
		newObject =  Order( betId, marketId, selectionId, side, status )
		orderList.append( newObject )
		
		#print('Bet Info: ')
		#print(newObject)
		
	return orderList
	
		
#bs4.BeautifulSoup
