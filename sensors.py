class SoilMoistureSensor:
	
	def __init__(self, channel, name_of_associated_flower, checked_lowest_score, checked_highest_score):
		self.channel = channel
		self.associated_flower = name_of_associated_flower
		self.checked_lowest_score = checked_lowest_score
		self.checked_highest_score = checked_highest_score
		self.span_of_score = checked_highest_score - checked_lowest_score
	
	@property
	def get_lower_bound_score(self):
		return self.checked_lowest_score - 0.05 * self.span_of_score
	
	@property
	def get_upper_bound_score(self):
		return self.checked_highest_score + 0.05 * self.span_of_score
	
	@property
	def get_channel_number(self):
		return self.channel
	
	@property
	def get_flower_name(self):
		return self.associated_flower

