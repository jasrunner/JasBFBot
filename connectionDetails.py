import requests
import ssl
import sys

sys.path.append('../client_certs/')
import userCredentials


payload = 'username='+ userCredentials.bfUsername + '&password=' + userCredentials.bfPassword
headers = {'X-Application': 'jasBetfairTest', 'Content-Type': 'application/x-www-form-urlencoded'}

def getSessionId( ):

	resp = requests.post('https://identitysso.betfair.com/api/certlogin', data=payload, cert=('../client_certs/client-2048.crt', '../client_certs/client-2048.key'), headers=headers)

	if resp.status_code == 200:
 	 	resp_json = resp.json()
 	 	print(resp_json['loginStatus'])
 	 	return(resp_json['sessionToken'])
	else:
 	 print("Request failed.")
 	 return 0

def getDelayedKey( ) :
	return ( userCredentials.delayedAppKey ) 

print('\n___________________')

print( 'Session ID:    ' + getSessionId( ) )
print( 'DelayedAppKey: ' + getDelayedKey( ) )

print('___________________')
