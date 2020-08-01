# vim: set sw=4 noet ts=4 fileencoding=utf-8:
import logging

def setup_logger(logger_level):
	''' Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
	logger_level should be passed in in the format logging.LEVEL '''

	logging.basicConfig(level=logger_level)
	logger = logging.getLogger(__name__)
	return logger

log = setup_logger(logging.DEBUG)

# This function is called when __init__ is called because it is set as class 
# attribute function for __init__. Thus, arguments passed here will get set.
# Pass in a dict or list for args to init multiple parameters
def class_constructor(arg):
	self.constructor_arg = arg

def input_as_int(input_question):

	input_not_satisfied = True
	while input_not_satisfied:
		user_in = input(input_question)
		try:
			user_in = int(user_in)
			input_not_satisfied = False
		except TypeError:
			log.info("Please enter an integer value.")

	return user_in

def input_n_tier_classes():
	input_question = ("How many tier classes will there be?" + \
		" Ex: Main Goals and Tasks would be 2 different tier classes. \n")
	n_tier_classes = input_as_int(input_question)
	return n_tier_classes

def create_minimum_attributes_dict(name, hierarchy_level):
	'''
		The idea behind this is that this attributes_dict is the MINIMUM for all
		tier_classes created. They may include more class attributes, but MUST
		satisfy these.
	'''
	attributes_dict = {
		"__init__" : class_constructor,
		"name" : name,
		"hierarchy_level" : hierarchy_level,
	}
	return attributes_dict

def input_attributes():
	''' This function outlines the mandatory properties of every tier. 
		Every tier must have a class name, such as Main Goals, and must have
		a hierarchy level. Additional, variable class attributes can be set for
		different tiers by passing in a dict when init with class_constructor.
	'''
	# Garbage in, garbage out. Guard the perimeter then forget about it
	# Must be string
	name = input("What is the name of this tier class? \n")
	# Must be int
	hierarchy_question = "What is the hierarchy level of this tier?\n"
	hierarchy_level = input_as_int(hierarchy_question)
	min_attributes_dict = create_minimum_attributes_dict(name, hierarchy_level)
	return min_attributes_dict

def create_tier_class(attributes_dict):

	# Dynamically create class based on user input
	# type(
		# class_name, 
		# base / inheritance, 
		# attributes (in the form of a dictionary)
		# )
	name = attributes_dict["name"]
	#XXX Base of type Tier??
	New_Tier_Class = type(
		name, 
		(object,), 
		attributes_dict	
	)
	return New_Tier_Class

#XXX should sort attributes_dict_list so that it is in ascending hierachy_level
# order
#XXX do we need the tier_tree to be ordered? if so, keep separate dict for each 
# tier and put each dict in a list. If not, just make one dict with an entry
# per hierarchy_level
# Having one dictionary per hierarchy level allows the tier_tree to be ordered
# and easily searchable
def setup_tier_tree(n_tier_classes, attributes_dicts_list):
	log.debug("attributes_dicts_list: {}".format(attributes_dicts_list))
	# Hierarchy level 0 is the top of the tree / most important/broad level
	# Ex: [{0: [type("Main_Goals", (object,), {attributes...}), 
	# ... other tiers on hierarchy_level 0..., ]}, {1: [...]}, ]
	tier_tree = []
	#XXX could also just iterate over len of attributes_dicts_list
	for i, tier in enumerate(range(n_tier_classes)):
		attributes_dict = attributes_dicts_list[i]
		New_Tier_Class = create_tier_class(attributes_dict)
		h_level = New_Tier_Class.hierarchy_level
		# If no hierarchy dict exists in tier_tree, create one for the class's 
		# hierarchy level. If exists, append to it.
		try:
			# If a dict of the hierarchy_level h_level already exists, 
			# append the class to the dict
			# [{0: []}]
			hierarchy_dict = tier_tree[h_level]

			hierarchy_dict[h_level].append(New_Tier_Class)

		except IndexError:
			# Create hierarchy_level dict
			hierarchy_dict = {}
			# [{0: []}]
			h_dict_inner_list = [New_Tier_Class]
			hierarchy_dict[h_level] = h_dict_inner_list
			# Append to tier_tree
			tier_tree.append(hierarchy_dict)
	return tier_tree

def input_tier_tree(n_tier_classes):
	'''
		Create the individual attributes each different tier class must 
		have based on user input and then construct the tier tree.
	'''
	attributes_dicts_list = []
	for	tier_class in range(n_tier_classes):
		attributes_dict = input_attributes()
		name = attributes_dict["name"]
		keep_inputting = True
		while keep_inputting:
			log.info("If you press enter without supplying input" + \
				" no more class \n attributes will be added.")
			class_attribute = input(
				"Enter the name of a {} attribute: ".format(name)
			)
			if class_attribute.strip() == "":
				keep_inputting = False
				break
			else:
				# Hopefully they don't enter hierarchy_dict, name, or __init__
				# Store the unset class_attribute in the dict of class attrs
				# as a temporary None type
				attributes_dict[class_attribute] = None
		attributes_dicts_list.append(attributes_dict)

	custom_tier_tree = setup_tier_tree(n_tier_classes, attributes_dicts_list)
	log.info("\nCustom tier tree: \n {}".format(custom_tier_tree))
	return custom_tier_tree

# Create instances. Each instance must have a connection to a 
# tier with a higher hierarchy level
def create_tier_instance():
	pass

n_tier_classes = input_n_tier_classes()
input_tier_tree(n_tier_classes)
