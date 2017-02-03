import accountClass
import foxyBotLib

''' Task 1
	Get details of amount available in account, and current exposure
'''
def getCurrentAccountDetails () :
	details = foxyBotLib.getAccountDetails()
	name =  ( details ['firstName'] ) 
	funds = foxyBotLib.getAccountFunds()
	available = funds ['availableToBetBalance']
	exposure = funds ['exposure']
	
	newObject = accountClass.Account( name, available, exposure )
	print(newObject)
	
