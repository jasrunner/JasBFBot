# console.set_idle_timer_disabled(flag)

import ui
import console
#import scratchpad
import time
import itertools

import menu
import connectionDetails
import foxyGlobals
import accountAccess
import accountClass

flag = True

appKey = connectionDetails.getDelayedKey()
sessionToken 	=  connectionDetails.getSessionId()
foxyGlobals.headers = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json'}


accountDetails = accountAccess.getCurrentAccountDetails()

@ui.in_background
def button_tapped(sender):
	sender.title = 'Starting'
	#scratchpad.start()



	menu.testCorrectScore([ 36, 600 ])

	alert_result = console.alert('Title', 'Finished!', 'Go again (todo)', 'Exit (todo)')
	sender.title = 'Button ' + str(alert_result)

console.set_idle_timer_disabled(flag)
v = ui.load_view('runMe')
v.present('sheet')

balancelabel = v['balance']
balancelabel.text = str(accountDetails.availableToBet)

exposurelabel = v['exposure']
exposurelabel.text = str(accountDetails.exposure)

iterationslabel = v['iterations']
iterationslabel.text = str(0)
#ui.Label.text = 'hello'






