class Account (object):
	
	
	def __init__( self, name, available, exposure ) :
		#self.id 							= id
		self.name 						= name
		self.availableToBet 	= available
		self.exposure					= exposure
		
	def __repr__( self ) :
		return '''
			\tAccount: 						{}
			\t	Name: 						{} 
			\t	Available To Bet:		{}
			\t	Exposure :				{}

			'''.format ( 
			  self.__class__.__name__,
				#self.id ,
				self.name ,
				self.availableToBet ,
				self.exposure
			)
	

