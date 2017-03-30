from decimal import *

targetROI 			= Decimal( 0.1 )
commissionRate 	= Decimal( 0.05 )

#--------------------------------------------------------
# Functions
#--------------------------------------------------------

def calculateLayStake( backOdds, backStake ) :
	
	
	netPnL			= targetROI * backStake
	
	a = netPnL * 100
	b = commissionRate * 100
	c = 100 - b
	
	grossPnL = a / c
	
	commission 	= grossPnL * commissionRate	
	layStake 		= backStake + grossPnL
	
	
	backreturn 	= backOdds * backStake
	backWin			= backreturn - backStake
	
	liability		= - ( backWin - grossPnL )
	
	layOdds			= - 1 * ( ( liability / layStake ) - 1 )

	'''
	print('netpnl = ' + str(netPnL))
	print('grosspnl = ' + str(grossPnL))
	print('commission = ' + str(commission))
	print('backReturn = '  + str(backreturn))
	print('backWin = ' + str(backWin))
	print('liability = ' + str(liability))
	'''
	
	return  ( layStake, layOdds )


#--------------------------------------------------------
# Test
#--------------------------------------------------------

def testCalculateLayStake()
	
	#getcontext().prec = 4

	backOdds 	= Decimal(2.0)
	backStake = Decimal(10.00)
		
	layBet 	= calculateLayStake( backOdds, backStake )
	
	layStake = layBet[0]
	layOdds 	= layBet[1]
	
	print( '\nlayStake \t= ' + str( layStake ) )
	print( 'layOdds \t= ' + str(layOdds ) )
	






	
	
	
