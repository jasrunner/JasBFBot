

class Price (object):
	
	def __init__ ( self, odds ) :
		self.layPrice		= odds[1]
		self.backPrice	= odds[0]
		self.spread 		= self.layPrice - self.backPrice
		self.score			= ''

	def __repr__( self ) :
		return '''
			\t	  Score :          {}
			\t	  Lay Price :		    {}
			\t	  Back Price :		{} 
			\t	  Spread : 			{}
			'''.format ( 
				self.score ,
				self.layPrice ,
				self.backPrice ,
				self.spread
			)

class Market (object):
	
	
	def __init__( self, id, name, marketType ) :
		self.id 				= id
		self.marketType = marketType
		self.name 			= name
		self.volume 		= 0
		self.numberOfRunners = 0
		self.price = []

		
	def __repr__( self ) :
		return '''
			\tMarket ID: 			{}
			\t	Market Type:		{}
			\t	Name: 				{} 
			\t	Volume: 			{}
			\t    Number Of Runners {}
			\t	Price :		{}
			'''.format ( 
				#self.__class__.__name__,
				self.id ,
				self.marketType ,
				self.name ,
				self.volume ,
				self.numberOfRunners ,
				self.price
			)
	
	
def getkeyByVolume ( Market ) :
	return Market.volume
	
def getkeyBySpread ( Market ) :
	return Market.spread
	
