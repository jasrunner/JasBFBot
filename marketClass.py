import pickle 

class Price (object):
	
	def __init__ ( self, odds, s_id ) :
		self.selectionId = s_id
		self.layPrice		= odds[1]
		self.backPrice	= odds[0]
		self.spread 		= self.layPrice - self.backPrice
		self.score			= ''

	def __repr__( self ) :
		return '''
			\t	  Score :          {}
			\t	  Lay Price :		    {}
			\t	  Back Price :		{} 
			\t    Spread : 			{}
			\t    Selection Id : 	{}
			'''.format ( 
				self.score ,
				self.layPrice ,
				self.backPrice ,
				self.spread,
				self.selectionId
			)

#def getkeyBySpread ( Price ) :
#	return Price.spread
	
#def getkeyByBackPrice ( Price ) :
#	return Price.backPrice	
	
#def getKeyByScore ( Price ) :
#	return Price.score
	
class Market (object):
	
	
	def __init__( self, id,  marketType ) :
		self.id 				= id
		self.marketType = marketType
		self.name 			= 'not defined'
		self.volume 		= 0
		self.numberOfRunners = 0
		self.price = []
		self.currentScore = 'not defined'
		self.viable = False

		
	def __repr__( self ) :
		
		return '''
			\tMarket ID: 			{}
			\t	Market Type:		{}
			\t	Name: 				{} 
			\t	Volume: 			{}
			\t	Number Of Runners: {}
			\t	Current Score 	{}
			\t	Viable 	{}
			\t	Price :		{}
			'''.format ( 
				#self.__class__.__name__,
				self.id ,
				self.marketType ,
				self.name ,
				self.volume ,
				self.numberOfRunners ,
				self.currentScore ,
				self.viable ,
				#priceInfo
				self.price
			)
			
	
	def __str__( self ) :
		
		# just interested in the matching current score
		#selection = next( x for x in self.price if x.score == self.currentScore )
		
		selection = next( ( x for x in self.price if x.score == self.currentScore), None )
		
		return '''
			\tMarket ID: 			{}
			\t	Market Type:		{}
			\t	Name: 				{} 
			\t	Volume: 			{}
			\t	Current Score 	{}
			\t	Viable 			{}
			\t  Selection		{}
			'''.format ( 
				self.id ,
				self.marketType ,
				self.name ,
				self.volume ,
				self.currentScore ,
				self.viable ,
				selection
			)	
	
def getkeyByVolume ( Market ) :
	return Market.volume
	
def getkeyBySpread ( Market ) :
	return Market.spread
	
