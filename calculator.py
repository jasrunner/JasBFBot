from decimal import *


#--------------------------------------------------------
# Definitions
#--------------------------------------------------------

targetROI 			= Decimal( 0.1 )
commissionRate 	= Decimal( 0.05 )

'''
Price	Increment:
	http://docs.developer.betfair.com/docs/plugins/servlet/mobile#content/view/4391786
	placing bets outside these price increments will result in INVALID_ODDS error
'''

# start price, stop price, increment, accuracy
PRICE_INCREMENTS = (
    ( 1.01,   2,  0.01, '0.01' ),
    ( 2,      3,  0.02, '0.01' ),
    ( 3,      4,  0.05, '0.01' ),
    ( 4,      6,  0.1,  '0.1'  ),
    ( 6,     10,  0.2,  '0.1'  ),
    ( 10,    20,  0.5,  '0.1'  ),
    ( 20,    30,  1,    '1.'   ),
    ( 30,    50,  2,    '1.'   ),
    ( 50,   100,  5,    '1.'   ),
    ( 100, 1000, 10,    '1.'   )
)

MIN_PRICE = 1.01
MAX_PRICE = 1000


#--------------------------------------------------------
# Functions
#--------------------------------------------------------


# take target price, and find closest increment
#--------------------------------------------------------
def nearest_increment( myPrice ) :
	
	# guard the min and max to ensure stake within allowable bounds
	if myPrice <= MIN_PRICE :
		return MIN_PRICE
		
	if myPrice >= MAX_PRICE :
		return MAX_PRICE 

	# first locate which price data group myPrice belongs to
	for price in PRICE_INCREMENTS :
		if myPrice < Decimal(str(price[1])) :
			break

	# for clarity, define these locals
	start = Decimal(str(price[0]))
	stop = myPrice
	increment = Decimal(str(price[2]))
	
	nextUp = start
	while nextUp < stop :
		nextUp += increment	
		
	nextDown = nextUp
	while nextDown > myPrice :
		nextDown -= increment
		
	distanceUp = nextUp - myPrice
	distanceDown = myPrice - nextDown
	
	if distanceUp < distanceDown :
		result = nextUp
	
	else :
		result = nextDown
	
	return Decimal ( str(result)).quantize( Decimal(str(price[3])) )


	
	
#--------------------------------------------------------
def calculateLayStake( backOdds, backStake ) :
	
	netPnL			= targetROI * backStake
	
	a = netPnL * 100
	b = commissionRate * 100
	c = 100 - b
	
	grossPnL = a / c
	
	commission 	= grossPnL * commissionRate	
	layStake 		= backStake + grossPnL
	
	# format 2 sig places
	layStake = layStake.quantize( Decimal(str('0.01')))
	
	
	backreturn 	= backOdds * backStake
	backWin			= backreturn - backStake
	
	liability		= - ( backWin - grossPnL )
	
	layOdds			= - 1 * ( ( liability / layStake ) - 1 )
	
	# round the layOdds to the nearest allowable value
	layOdds = nearest_increment( layOdds )

	
	return  ( layStake, layOdds )


#--------------------------------------------------------
# Test
#--------------------------------------------------------

def testCalculateLayStake() :

	backOdds 	= Decimal(2.76)
	backStake = Decimal(2.0)
		
	layBet 	= calculateLayStake( backOdds, backStake )
	
	layStake = layBet[0]
	layOdds 	= layBet[1]
	
	print( '\nlayStake \t= ' + str( layStake ) )
	print( 'layOdds \t= ' + str(layOdds ) )
	
	return layStake, layOdds



testPrice = testCalculateLayStake()


