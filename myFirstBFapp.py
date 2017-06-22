#!/usr/bin/env python3

'''
	08/09/16
	jasFBot - first cut
	
	Interactive method for getting session id is: log into BF, then accessing account demo, then copy-paste into resource file.
	
	Non-interactive method for getting sessionId comes from use getSessionId.py
	
	Notes: 
		* delayed app is about 5 mins behind real time (estimate)
		* function json.loads deserialises a json str into a python object
	
'''



import urllib
import urllib.request
import urllib.error
import json
import datetime
import sys
import pickle

import menu
import connectionDetails
import foxyBotLib
import foxyGlobals
import marketClass
#import marketAccess
#import accountAccess

'''
=======================================================================

Function definitions

-----------------------------------------------------------------------
'''


#--------------------------------------------------------
# Use the event ID's to get market data, then store in a lot of Market Data objects


		

'''
=======================================================================

Main:

-----------------------------------------------------------------------
'''


# Parameter check

args = len(sys.argv)

if ( args < 3):
	'''
    print ('Please provide Application key and session token')
    appKey = input('Enter your application key :')
    sessionToken = input('Enter your session Token/SSOID :')
    print ('Thanks for the input provided')
  '''
	appKey = connectionDetails.getDelayedKey()
	sessionToken 	=  connectionDetails.getSessionId()
else:
    appKey = sys.argv[1]
    sessionToken = sys.argv[2]

foxyGlobals.headers = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json'}



#--------------------------------------------------------
# Call menu
#--------------------------------------------------------

menu.mainMenu( 'test' )






