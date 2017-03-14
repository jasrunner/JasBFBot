import pickle
import foxyGlobals

#--------------------------------------------------------
#
def saveToFile( marketData, filename ) :
	
	if filename == "" :
		filename = foxyGlobals.defaultFilename
	
	# Store data (serialize)
	with open( filename, 'wb') as handle:
		pickle.dump(marketData, handle, protocol=pickle.HIGHEST_PROTOCOL)
		
	print("Saves as: " + filename )
	

#--------------------------------------------------------
#
def loadFromFile( filename ) :
	
	if filename == "" :
		filename = foxyGlobals.defaultFilename
		
	# Load data (deserialize)
	with open( filename, 'rb') as handle:
		unserialized_data = pickle.load(handle)

	#print('your_data == ' )
	#print (unserialized_data)
	return unserialized_data

