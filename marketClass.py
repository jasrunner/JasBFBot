



class Market (object):
	
	
	def __init__( self, id, name ) :
		self.id 				= id
		self.name 			= name
		self.volume 		= 0
		self.layPrice		= 0
		self.backPrice	= 0
		self.spread 		= 0
		
	def __repr__( self ) :
		return '''
			\tMarket ID: 			{}
			\t	Name: 				{} 
			\t	Volume: 			{}
			\t	Lay Price :		{}
			\t	Back Price :		{} 
			\t	Spread : 			{}
			'''.format ( 
				#self.__class__.__name__,
				self.id ,
				self.name ,
				self.volume ,
				self.layPrice ,
				self.backPrice ,
				self.spread
			)
	
	
def getkeyByVolume ( Market ) :
	return Market.volume
	
def getkeyBySpread ( Market ) :
	return Market.spread
	
