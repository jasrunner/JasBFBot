from enum import Enum

urlBetting  = "https://api.betfair.com/exchange/betting/json-rpc/v1"
urlAccounts = "https://api.betfair.com/exchange/account/json-rpc/v1"
headers = ""

requestLimit = 1000
# 1000

# The minumum traded volume to gauge the size of the market
minVolume = 10000

# max and min back odds
maxBackOdds		= 4.5
minBackOdds		= 1.7

# bet delay
betDelay = 5

# minimum bet
minBetSize = 2

# max spread
maxSpread = 1

# numer of prices to request
priceRequestLimit 	= 5

matchOdds 		= "MATCH_ODDS"
correctScore 	= "CORRECT_SCORE"

back = "BACK"
lay = "LAY"

defaultFilename = "backup.pickle"

scoreLine = [
        '0-0',
        '0-1',
        '0-2',
        '0-3',
        '1-0',
        '1-1',
        '1-2',
        '1-3',
        '2-0',
        '2-1',
        '2-2',
        '2-3',
        '3-0',
        '3-1',
        '3-2',
        '3-3',
        'other home',
        'other away',
        'other draw'
]

targetScores = [
        '0-0',
        '0-1',
        '1-0',
        '1-1',
        '0-2',
        '2-0'
]

matchOutcome = [
				'home',
				'away',
				'draw'
]


