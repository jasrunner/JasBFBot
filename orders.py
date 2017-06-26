import foxyBotLib
import marketClass
import foxyGlobals
import calculator
import time
#import timeit
#import bs4
from decimal import *


#--------------------------------------------------------

#--------------------------------------------------------
def listCurrentOrders(  ) :
	
	result = foxyBotLib.listCurrentOrders()
	
	print('in listCurrentOrders')
	currentOrders = result['currentOrders']
	print(currentOrders)
	if currentOrders == [] :
		print('no current bets')
		return []
	
	orderList = [] 
	
	for order in currentOrders :
		betId = order['betId']
		marketId = order['marketId']
		selectionId = order['selectionId']
		side = order['side']
		status = order['status']
		
		
		newObject =  Order( betId, marketId, selectionId, side, status )
		newObject.name = foxyBotLib.getEventNameFromMarketId( marketId )
		orderList.append( newObject )
		
	return orderList
	
#--------------------------------------------------------
def getBetStatus( betId ) :
	
	orders = listCurrentOrders()
	
	for order in orders :
		if order.betId == betId :
			if order.status == 'EXECUTION_COMPLETE' :
				return True
			else :
				print('getBetStatus, returning false, order = ' + str(order) )
				return False
	
	print('orders.getBetStatus: didnt find betId =  ' + betId)
	return False
			
		
		
	

#--------------------------------------------------------
def processError( errorCode ) :
		
		if errorCode == 'INSUFFICIENT_FUNDS' :
			print('Insufficient funds ')
			return 
		
		elif errorCode == 'MARKET_SUSPENDED' :
			print('Market Suspensed')
			return
			
		elif errorCode == 'BET_TAKEN_OR_LAPSED' :
			print('Bet taken or lapsed')
			return
			
		else :
			print('orders.processError: unexpected errorCode: ' + errorCode )
			return

#--------------------------------------------------------
# if size cancelled not same as size remaining
# need to work out how much was executed and adjust the lay stake accordingly
def isPartial() :
	return
	#


#--------------------------------------------------------
def makeLayBet(backOdds, backStake, market, selection) :
	# Lay the bet
	layBet 	= calculator.calculateLayStake( Decimal(backOdds), Decimal(backStake)  )

	layStake = layBet[0]
	layOdds  = layBet[1]
	
	print( '\nlayStake \t= ' + str( layStake ) )
	print( 'layOdds \t= ' + str(layOdds ) )
	
	ret =  foxyBotLib.placeOrders( str(market.version), str( market.id ) , str( selection.selectionId ) , str( layStake ), str( layOdds), foxyGlobals.lay )
	
	print('Return from placeOrders(lay) is:  ' + str(ret) )

	status =  ret['status']
	
	if status != 'SUCCESS' :
		print( 'orders.makeLayBey: Status is: ' + status )
		
		return 'FAILURE'
	
	
	return 'SUCCESS'
	#betId = ret['betId']
	#print( 'betId is: ' + betId )

	

#--------------------------------------------------------
def makeABet( market ) :
	
	print('in Orders')
	selection = next( ( x for x in market.price if x.score == market.currentScore), None )
	
	# todo : backPrice is none - why? check
	
	backOdds = selection.backPrice
	backStake = foxyGlobals.minBetSize
	
	ret =  foxyBotLib.placeOrders( str(market.version), str( market.id ) , str( selection.selectionId ) , str( backStake ), str( backOdds), foxyGlobals.back )
	
	print('Return from placeOrders(back) is:  ' + str(ret) )
	
	status =  ret['status']
	
	# Deal with Failure
	if status == 'FAILURE' :
	
		errorCode = ret['errorCode']
		print ( 'errorCode is: ' + errorCode )
	
		processError( errorCode )
		return 'FAILURE'
	
	# Deal with success
	elif status == 'SUCCESS' :
		
		print('In SUCCESS')
	
		report = ret['instructionReports']
		print( report ) 
		
		orderStatus =  report[0]['orderStatus']
		print( 'orderStatus is: ' + orderStatus )
		
		# If back bet went through, then make the matching lay bet
		if orderStatus == 'EXECUTION_COMPLETE':
			print('In EXECUTION_COMPLETE')
			print('lets work out the lay bet')
			
			makeLayBet( backOdds, backStake, market, selection )
			return 'SUCCESS'
		

		# else wait for 10 secons, check the status of this bet, then either 
		# cancel, or make the marching lay bet
		elif orderStatus == 'EXECUTABLE' :
			print( 'In EXECUTABLE')
			print('Bet wasnt executed, waiting 10 seconds')
			
			betId = report[0]['betId']
			
			time.sleep(10)
			
			if getBetStatus(betId) == True :
				print('making lay bet')
				ret = makeLayBet( backOdds, backStake, market, selection )
			else :
				print('cancelling bet')
				
				#todo: check here the current back stake, if drifted, then cancel, o
				# or do we do cancelor-kill?  because sometimes get part cancelled
				# and need to deal with this
				
			
			
				cancelOrderRet = foxyBotLib.cancelOrder( str( market.id ), betId )
				#print( cancelOrderRet )
				
				report = cancelOrderRet['instructionReports']
				print( report ) 
		
				sizeCancelled =  report[0]['sizeCancelled']
				print( 'sizeCancelled is: ' + str(sizeCancelled ) )

				 
				if sizeCancelled != backStake :
					backStake = backStake - sizeCancelled
					print('orders.makeABet: need to make layBet of ' + str(backStake) + 'to match out')
					
					ret = makeLayBet( backOdds, backStake, market, selection )
	

				# todo : in case of partial cancel, may still need to make matching lay bet
				# use betId, marketId, selectionId to get current status
				return 'FAILURE'
			
			
		
		else :
			print( 'orders.makeABet: What am I doing here? orderStatus is: ' + orderStatus )
			return 'FAILURE'
			
	# else status is not failure or success, what is it ?
	else :
			print( 'orders.makeABet: What am I doing here? Status is: ' + status )
			return 'FAILURE'
			
	return 'SUCCESS'
	


#--------------------------------------------------------
class Order (object):
	
	
	def __init__( self, betId, marketId, selectionId, side, status  ) :
		self.betId 				= betId
		self.marketId 		= marketId
		self.selectionId  = selectionId
		self.side 			  = side
		self.status 		  = status
		self.name 				= ''
		
	def __repr__( self ) :
		
		return '''
			\tBetId: 			{}
			\t	MarketId 			{}
			\t	SelectionId:		{}
			\t	Side: 				{} 
			\t	Status: 			{}
			\t	Name:					{}
			'''.format ( 
				self.betId ,
				self.marketId ,
				self.selectionId ,
				self.side ,
				self.status,
				self.name
			)
			



	
		
#bs4.BeautifulSoup
