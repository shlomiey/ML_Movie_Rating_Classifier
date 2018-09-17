"""
TODO: HAVE NOT PASS TESTS YET
"""

def weight_calculator(value_1, value_2):
	max_value = max(value_1, value_2)
	min_value = min(value_1, value_2)
	return 1 - (max_value - min_value)/max_value 

def line_similarity(line_1, line_2):
	"""
	TODO: new comments from pycharm
	receives 2 lines from corpus_dictionary 
	return a number represent similarity
	features to compare:
		- line size
		- set size
		- bag size
		- set diversity between the two lines
	"""
	w_list = []
	line_1_bag_size = sum(line_1['line_bag_of_words'].values())
	line_2_bag_size = sum(line_2['line_bag_of_words'].values())
	line_1_set = line_1['line_set_of_words']
	line_2_set = line_2['line_set_of_words']
	line_1_minus_2_set = line_1_set - line_2_set
	line_2_minus_1_set = line_2_set - line_1_set
	w_list.append(weight_calculator(line_1_bag_size, line_2_bag_size))
	w_list.append(weight_calculator(len(line_1_set), len(line_2_set))
	w_list.append(weight_calculator(len(line_1_minus_2_set),
	len(line_2_minus_1_set))
	
	return mean(w_list)
	
def conversation_similarity(conv_1, conv_2):
	"""
	TODO: new comments from pycharm
	receives 2 lines from corpus_dictionary 
	return a number represent similarity
	features to compare:
		- line size
		- set size
		- bag size
		- set diversity between the two lines
	"""
	w_list = []
	conv_1_bag_size = sum(conv_1['conversation_bag_of_words'].values())
	conv_2_bag_size = sum(conv_2['conversation_bag_of_words'].values())
	conv_1_set = conv_1['conversation_set_of_words']
	conv_2_set = conv_2['conversation_set_of_words']
	conv_1_minus_2_set = conv_1_set - conv_2_set
	conv_2_minus_1_set = conv_2_set - conv_1_set
	w_list.append(weight_calculator(conv_1_bag_size, conv_2_bag_size))
	w_list.append(weight_calculator(len(conv_1_set), len(conv_2_set))
	w_list.append(weight_calculator(len(conv_1_minus_2_set),
	len(conv_2_minus_1_set))
	w_list.append(weight_calculator(conv_1['total_lines'],
	conv_2['total_lines']))
	return mean(w_list)
	
	def movie_similarity(movie_1, movie_2):
	"""
	TODO: new comments from pycharm
	receives 2 lines from corpus_dictionary 
	return a number represent similarity
	features to compare:
		- line size
		- set size
		- bag size
		- set diversity between the two lines
	"""
	w_list = []
	movie_1_bag_size = sum(movie_1['conversation_bag_of_words'].values())
	movie_2_bag_size = sum(movie_2['conversation_bag_of_words'].values())
	movie_1_set = movie_1['conversation_set_of_words']
	movie_2_set = movie_2['conversation_set_of_words']
	movie_1_minus_2_set = movie_1_set - movie_2_set
	movie_2_minus_1_set = movie_2_set - movie_1_set
	
	w_list.append(weight_calculator(movie_1_bag_size, movie_2_bag_size))
	w_list.append(weight_calculator(len(movie_1_set), len(movie_1_set))
	w_list.append(weight_calculator(len(movie_1_minus_2_set),
	len(movie_2_minus_1_set))
	w_list.append(weight_calculator(movie_1['total_conversations'],
	movie_2['total_conversations']))
	w_list.append(weight_calculator(movie_1['total_movie_lines'],
	movie_2['total_movie_lines']))
	
	return mean(w_list)
