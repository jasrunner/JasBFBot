from enum import Enum

urlBetting  = "https://api.betfair.com/exchange/betting/json-rpc/v1"
urlAccounts = "https://api.betfair.com/exchange/account/json-rpc/v1"
headers = ""

requestLimit = 1000

# The minumum traded volume to gauge the size of the market
minVolume = 000

matchOdds 		= "MATCH_ODDS"
correctScore 	= "CORRECT_SCORE"


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
        '0-2',
        '1-0',
        '1-1',
        '2-0'
]

matchOutcome = [
				'home',
				'away',
				'draw'
]
