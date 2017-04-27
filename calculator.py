from decimal import *

targetROI 			= Decimal( 0.1 )
commissionRate 	= Decimal( 0.05 )

#--------------------------------------------------------
# Functions
#--------------------------------------------------------

'''
Price	Increment:
	http://docs.developer.betfair.com/docs/plugins/servlet/mobile#content/view/4391786
	placing bets outside these price increments will resuls in INVALID_ODDS error
'''
def nearestOdds( odds ) :
	if odds < 1.01 :
		print( 'Error in nearestOdds: odds = ' + odds )
		# shiuld we throw here?
		return 0
		
	if odds <= 1.01 and odds < 2 :
		return odds
		
	#if odds od
	'''

1.01 → 2	0.01
2→ 3	0.02
3 → 4	0.05
4 → 6	0.1
6 → 10	0.2
10 → 20	0.5
20 → 30	1
30 → 50	2
50 → 100	5
100 → 1000
'''

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

def testCalculateLayStake() :
	
	#getcontext().prec = 4

	backOdds 	= Decimal(3.1)
	backStake = Decimal(2.0)
		
	layBet 	= calculateLayStake( backOdds, backStake )
	
	layStake = layBet[0]
	layOdds 	= layBet[1]
	
	print( '\nlayStake \t= ' + str( layStake ) )
	print( 'layOdds \t= ' + str(layOdds ) )
	






testCalculateLayStake()



	
	
	
