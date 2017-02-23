import urllib
import urllib.request
import urllib.error
import json
import datetime
import sys
import ssl

import foxyGlobals

account = "Account"
sports  = "Sports"

#--------------------------------------------------------
def callAping( requestType, query, params ):

		url = ""

		if ( requestType == account ) :
			url = foxyGlobals.urlAccounts
		elif (requestType == sports ) :
			url = foxyGlobals.urlBetting
		else:
			print( "Unknown requestType = " + requestType )
			exit() 

		try:
				
			part1 = '{"jsonrpc": "2.0", "method": "' + requestType
			part2 = 'APING/v1.0/' + query
			part3 = '", "params":{' + params + '},  "id": 1} '
			jsonrpc_req = part1 + part2 + part3
				
			#print( jsonrpc_req )
			req = urllib.request.Request(url, jsonrpc_req.encode('utf-8'), foxyGlobals.headers)
			response = urllib.request.urlopen(req)
			jsonResponse = response.read()
			return jsonResponse.decode('utf-8')
		except urllib.error.URLError as e:
			print (e.reason) 
			print ('Oops no service available at ' + str(foxyGlobals.url))
			exit()
		except urllib.error.HTTPError:
			print ('Oops not a valid operation from the service ' + str(foxyGlobals.url))
			exit()

#--------------------------------------------------------
# Accounts
#--------------------------------------------------------

def getAccountDetails():
    params = '"locale":"en" '
    
    print ('Calling getAccountDetails')
    response = callAping(account, "getAccountDetails", params)
    responseLoads = json.loads(response)
    #print(responseLoads)
    return (responseLoads['result'])
    
    
#--------------------------------------------------------
def getAccountFunds():
        
    print ('Calling getAccountFunds')
    response = callAping(account, "getAccountFunds", "")
    responseLoads = json.loads(response)
    #print(responseLoads)
    return (responseLoads['result'])
    
    
#--------------------------------------------------------  
# Sports
#--------------------------------------------------------

def getEventTypes():
    params = '"filter":{"textQuery":"Tennis","inPlayOnly":true}'
    
    print ('Calling listEventTypes to get event Type ID')
    eventTypesResponse = callAping(sports, "listEventTypes", params )
    eventTypeLoads = json.loads(eventTypesResponse)


    print('event type loads:')
    print(eventTypeLoads)
    print('___________________')
	

    try:
        eventTypeResults = eventTypeLoads['result']
      #  print('id='+str(eventTypeLoads['id']))
       # print('jsonrpc='+str(eventTypeLoads['jsonrpc']))
        return eventTypeResults
    except:
        print ('Exception from API-NG' + str(eventTypeLoads['error']))
        exit()


#--------------------------------------------------------
def listEvents( queryText ) :
	params = '"filter":{"textQuery":"' + queryText + '", "marketTypeCodes": ["MATCH_ODDS"], "inPlayOnly":true}'
	
	#print ('Calling listEvents to get list of event ids')
	#print(list_events_req)
	listEventsResponse = callAping( sports, "listEvents", params )
	listEventsLoads = json.loads(listEventsResponse)

	return listEventsLoads['result']
    

#--------------------------------------------------------
def listMarketCatalogue( eventList, marketType ) :
	
	numberEvents = len(eventList)
	max = min( foxyGlobals.requestLimit, numberEvents )
	
	if max == 0 :
		print('No events available, returning')
		return 0
	params = '"filter":{"eventIds":[' + eventList
	params += '], "marketTypeCodes": ["' + marketType
	params += '"]},  "maxResults" : '  + str(max) + '}'

	#print ('Calling listMarketCatalogue')
	
	listMarketResponse = callAping( sports, "listMarketCatalogue", params )
	#print( listMarketResponse )
	listMarketLoads = json.loads(listMarketResponse)
	#print('___________________')
	#print(listMarketLoads)
	return (listMarketLoads['result'])
	
	

#--------------------------------------------------------
def listMarketCatalogueInPlay( queryText ) :
	
	params = '"filter":{"textQuery":"' + queryText + '","inPlayOnly":true} , "maxResults" : 2 } '
	
	#print ('Calling listMarketCatalogueInPlay')
	
	listMarketResponse = callAping( sports, "listMarketCatalogue", params )
	#print( listMarketResponse )
	listMarketLoads = json.loads(listMarketResponse)
	
	return (listMarketLoads['result'])
	
	
#--------------------------------------------------------
def listMarketBook( marketId ) :
	
	params = ' "marketIds":[ "' + marketId + '"] , "priceProjection" : {	"priceData" : [ "EX_ALL_OFFERS" ] }'
	#params = ' "marketIds":[ ' + marketId + '] '
	#print( params )
	
	
	#{"marketIds":["' + marketId + '"],"priceProjection":{"priceData":["EX_BEST_OFFERS"]}}, "id": 1}'
  
	
	
	#print ('Calling listMarketBook to get price information')
	listMarketResponse = callAping( sports, "listMarketBook", params )
	listMarketLoads = json.loads(listMarketResponse)
#	print('___________________')
	#print(listMarketLoads)
	return (listMarketLoads['result'])
	
#--------------------------------------------------------
#<TODO> make this a list.... no change here, but need work on the other rnd
def getEventNameFromMarketId( marketId ) :
#	params = '"filter":{"marketIds":["' + marketId + '"]} '
	
	params = '"filter":{"marketIds":[' + marketId + ']} '
	#print(event_info_req)


	response = callAping( sports, "listEvents", params )
	loads = json.loads(response)
	
	res = loads['result'] 
	print('res : ' + str(res))
	return (res[0]['event'] ['name'])



