# console.set_idle_timer_disabled(flag)

import ui
import console
import scratchpad
import time
import itertools

import menu
import connectionDetails
import foxyGlobals

flag = True

appKey = connectionDetails.getDelayedKey()
sessionToken 	=  connectionDetails.getSessionId()
foxyGlobals.headers = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json'}

@ui.in_background
def button_tapped(sender):
	sender.title = 'Starting'
	#scratchpad.start()


	menu.testCorrectScore([ 24, 600 ])

	alert_result = console.alert('Title', 'Finished!', 'Go again (todo)', 'Exit (todo)')
	sender.title = 'Button ' + str(alert_result)

console.set_idle_timer_disabled(flag)
ui.load_view('runMe').present('sheet')





