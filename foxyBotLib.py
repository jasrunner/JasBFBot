import urllib
import urllib.request
import urllib.error
import json
import datetime
import sys
import ssl

import foxyGlobals

#url = "https://api.betfair.com/exchange/betting/json-rpc/v1"

#--------------------------------------------------------
def callAping(jsonrpc_req, url):
    try:
       # print(jsonrpc_req)
       # print(url)
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
    request = '{"jsonrpc": "2.0", "method": "AccountAPING/v1.0/getAccountDetails", "params":{"locale":"en"},  "id": 1} '
    
    print ('Calling getAccountDetails')
    response = callAping(request,foxyGlobals.urlAccounts)
    responseLoads = json.loads(response)
    #print(responseLoads)
    return (responseLoads['result'])
    
    
#--------------------------------------------------------
def getAccountFunds():
    request = '{"jsonrpc": "2.0", "method": "AccountAPING/v1.0/getAccountFunds", "params":{"locale":"en"},  "id": 1} '
    
    print ('Calling getAccountFunds')
    response = callAping(request,foxyGlobals.urlAccounts)
    responseLoads = json.loads(response)
    #print(responseLoads)
    return (responseLoads['result'])
    
    
#--------------------------------------------------------  
# Sports
#--------------------------------------------------------

def getEventTypes():
    event_type_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{"textQuery":"Tennis","inPlayOnly":true}}, "id": 1} '
    
    print ('Calling listEventTypes to get event Type ID')
    eventTypesResponse = callAping(event_type_req, foxyGlobals.urlBetting)
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
	list_events_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params": {"filter":{"textQuery":"'
	list_events_req += queryText
	list_events_req += '", "marketTypeCodes": ["MATCH_ODDS"], "inPlayOnly":true}}, "id": 1} '
	
	#print ('Calling listEvents to get list of event ids')
	#print(list_events_req)
	listEventsResponse = callAping(list_events_req, foxyGlobals.urlBetting)
	listEventsLoads = json.loads(listEventsResponse)

	return listEventsLoads['result']
    

#--------------------------------------------------------
def listMarketCatalogue( eventList, numberEvents ) :
	
	max = min( foxyGlobals.requestLimit, numberEvents )
	
	if max == 0 :
		print('No events available, returning')
		return 0
	list_market_cat_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventIds":['
	list_market_cat_req += eventList
	list_market_cat_req += '], "marketTypeCodes": ["MATCH_ODDS"]},  "maxResults" : '
	list_market_cat_req += str(max)
	list_market_cat_req += '}, "id": 1} '

	#print ('Calling listMarketCatalogue')
	
	listMarketResponse = callAping(list_market_cat_req,foxyGlobals.urlBetting)
	#print( listMarketResponse )
	listMarketLoads = json.loads(listMarketResponse)
	#print('___________________')
	print(listMarketLoads)
	return (listMarketLoads['result'])
	
	

#--------------------------------------------------------
def listMarketCatalogueInPlay( queryText ) :
	
	list_market_cat_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"textQuery":"'
	list_market_cat_req += queryText
	list_market_cat_req += '","inPlayOnly":true} , "maxResults" : 2 }, "id" : 1} '
	
	#print ('Calling listMarketCatalogueInPlay')
	
	listMarketResponse = callAping(list_market_cat_req, foxyGlobals.urlB)
	#print( listMarketResponse )
	listMarketLoads = json.loads(listMarketResponse)
	
	return (listMarketLoads['result'])
	
	
#--------------------------------------------------------
def listMarketBook( marketId ) :
	
	list_market_book_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params": { "marketIds":[ '
	list_market_book_req += marketId
	list_market_book_req += '] , "priceProjection" : {	"priceData" : [ "EX_ALL_OFFERS" ] }}, "id": 1} '
	#print( list_market_book_req)
	
	
	#{"marketIds":["' + marketId + '"],"priceProjection":{"priceData":["EX_BEST_OFFERS"]}}, "id": 1}'
  
	
	
	#print ('Calling listMarketBook to get price information')
	listMarketResponse = callAping(list_market_book_req, foxyGlobals.urlBetting)
	listMarketLoads = json.loads(listMarketResponse)
#	print('___________________')
	#print(listMarketLoads)
	return (listMarketLoads['result'])
	
#--------------------------------------------------------
def getEventNameFromMarketId( marketId ) :
	event_info_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params": {"filter":{"marketIds":["'
	event_info_req += marketId
	event_info_req += '"]} }, "id": 1} '
	
	#print(event_info_req)


	response = callAping(event_info_req, foxyGlobals.urlBetting)
	loads = json.loads(response)
	
	res = loads['result'] 
	return (res[0]['event'] ['name'])



