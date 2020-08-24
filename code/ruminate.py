# vim: set sw=4 noet ts=4 fileencoding=utf-8:
import logging
import pdb

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
	constructor_arg = arg

def input_as_int(input_question):
	''' This function continues to ask for an integer value as input until
		it is satisfied.
	'''
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
		#XXX user must input connections later, but all classes have this field
		#XXX is a class attribute! I need an instance attribute!
		"connections_above" : [],
		"connections_below" : [],
		"connections_equal_how" : [],
		"connections_equal_why" : [],
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
	# Ex of tier_tree filled with hierarchy_dicts: 
	# [{0: [type("Main_Goals", (object,), {attributes...}), 
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
			#XXX this assumes that tier_tree is ordered such that the 0th
			# element corresponds to the hierarchy_dict with they key 0
			# XXX...fix later
			hierarchy_dict = tier_tree[h_level]
			log.debug("Hierarchy_dict: {} \n".format(hierarchy_dict))
			log.debug("tier_tree: {} \n".format(tier_tree))


			#XXX if out of order h_levels supplied, crashes here w KeyError
			# due to reasons above
			hierarchy_dict[h_level].append(New_Tier_Class)

		except (IndexError or KeyError):
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

# Get all class attributes from tier_tree
def get_all_classes(custom_tier_tree):
	full_classes_list = []
	# Gets all hierarchy levels from tier_tree
	for i, hierarchy_dict in enumerate(custom_tier_tree):
		log.debug("i: {}".format(i))
		# Get all classes in each hierarchy level
		# NOTE that i is a key in the case of hierarchy_dict, not an index
		classes_list = hierarchy_dict[i]
		log.debug("hierarchy_dict[i]: {}".format(classes_list))
		for cls in classes_list:
			#pass in a fucntion to perform here instead of returning things?
			# That doesn't seem to work well because it requires setup of 
			# full_classes list... hard to abstract the setup as well since
			# it isn't always needed w/ while_unpackign func
			full_classes_list.append(cls)

	return full_classes_list

#def unpack_tier_tree(custom_tier_tree, while_unpacking):
#	for i, hierarchy_dict in enumerate(custom_tier_tree):
#		log.debug("i: {}".format(i))
#		# Get all classes in each hierarchy level
#		# NOTE that i is a key in the case of hierarchy_dict, not an index
#		classes_list = hierarchy_dict[i]
#		log.debug("hierarchy_dict[i]: {}".format(classes_list))
#		for cls in classes_list:
#			while_unpacking()


# INSTANCES OF TIERS / MAKING A SPREADSHEET ENTRY
# Create instances. Each instance must have a connection to a 
# tier with a higher hierarchy level
def create_tier_instance(custom_tier_tree, tier_type):
	# Separate asking what tier instance from setting connection library
	# Ask what type of tier instance to create or pass it in
	# For the given tier ask what tier above or beside it connects to
	# Add connection attribute to class and the class above / lateral
	# If lateral, inherit connection library from connection
	pass

def input_tier_instance_class(custom_tier_tree):
	display_tier_types(custom_tier_tree)
	tier_type_input = input("What type of tier are you creating? \n")
	tier_instance_class = get_class_by_name(custom_tier_tree, tier_type_input)
	log.info("Setting tier_instance_class to {}".format(
		tier_instance_class))
	return tier_instance_class

def get_class_by_name(custom_tier_tree, name_to_find):
	''' Searches through the custom_tier_tree to find a class with the correct
		name attribute and return that class object. '''
	# All classes as setup by the user
	class_list = get_all_classes(custom_tier_tree)
	found_class = None
	for cls in class_list:
		if cls.name == name_to_find:
			found_class = cls
	return found_class

def display_tier_types(custom_tier_tree):
	full_classes_list = get_all_classes(custom_tier_tree)
	# Show tier types / options  to choose from based on creation of tier_tree
	for cls in full_classes_list:
		log.info("\n Tier Type options: {} \n".format(cls))
	#return full_classes_list

def make_connections(tier_instance, *selected_connections):
	'''
		Set an attribute of the instance of the tier to have a connection to
		another class tier instance. selected_connections should be a list
		of other tier_instances. 
		Returns: Returns whether the node has a why value attached after 
			all connections are made.
	'''
	#XXX need to check that connections are higher or equal level??
	for connection in selected_connections:
		#XXX if it is the top / initial instance in tree then no
		# connections can be made
		if connection == "root" and tier_instance.hierarchy_level == 0:
			# Skips the rest of this iteration and then continues iterating
			continue
		# Check hierarchy level of connection and place connection accordingly
		if connection.hierarchy_level > tier_instance.hierarchy_level:
			# Sets the tier_instance's connections field to link 
			# to those selected
			tier_instance.connections_above.append(connection)
			# Sets the connection tier instance's connections to reciprocally 
			# reflect new connection to it
			connection.connections_below.append(tier_instance)

		# If the connection hierarchy level is below the tier instance level
		elif connection.hierarchy_level < tier_instance.hierarchy_level:
			tier_instance.connections_below.append(connection)
			connection.connections_above.append(tier_instance)

		# If hierarchy levels are equal
		# selected_connections is a list of connections essentially 
		# (multiple args), if the connection is an equal level, it must be
		# passed as a dict which has what type of connection (why/how)
		# {connection: instance of conn, type: either why or how}
		else:
			conn_inst = connection["conncection_inst"]
			conn_type = connection["type"]
			if conn_type == "why":
				tier_instance.connections_equal_why.append(conn_inst)
				conn_inst.connections_equal_how.append(tier_instance)
			if conn_type == "how":
				tier_instance.connections_equal_how.append(connection)
				connection.connections_equal_why.append(tier_instance)

	# After making connections, check that the node has a why
	has_why = check_has_why(tier_instance)
	return has_why

def check_has_why(connected_tier_inst):
	''' This func checks that a connected_tier_instance has a why, meaning
		either a higher up connection or an equal level connection.
	'''
	has_why = False
	tier_level = connected_tier_inst.hierarchy_level
	for conn in connected_tier_instance.connections:
		conn_level = conn.hierarchy_level
		# Everything must have a why.
		if conn_level == tier_level or conn_level > tier_level:
			has_why == True
	return has_why


def input_connections_to(tier_inst):
	''' 
		Asks / forces the user to create at least one connection between 
		the current tier instance and a lateral or above class instance.
	'''
	
	# display classes above created instance
	keep_inputting = True
	connections = []
	while keep_inputting:
		# Display options of tier instances for connections
		# Asks for inputted connections
		connection = input("Input connections to tier {}. ".format(tier_inst) +\
			"At least one must be of equal or higher hierarchy level. \n")
		connections.append(connection)
		
		# If input is empty, break the loop
		if connection.strip() == "":
			keep_inputting = False
			break
				
	return connections

def input_instance_name(tier_instance_class):
	instance_name = input("What is the name of this instance of {}".format(
		tier_instance_class))
	return instance_name

def make_instance(tier_instance_class):

	inst = tier_instance_class()
	instance_name = input_instance_name(tier_instance_class)
	inst.name = instance_name
	connections = input_connections_to(inst)
	make_connections(inst, *connections)
	return inst

def make_instances(custom_tier_tree):
	keep_inputting = True
	while keep_inputting:	
		log.info("Start creating an instance of a tier class.")
		tier_instance_class = input_tier_instance_class(custom_tier_tree)
		make_instance(tier_instance_class)

		done_inputting = input("Done creating tier instances? (y/n)")
		if done_inputting == 'y' or 'Y' or 'yes' or 'Yes': 
			keep_inputting = False
			break

def inherit_connections(tier_instance):
	pass



n_tier_classes = input_n_tier_classes()
custom_tier_tree = input_tier_tree(n_tier_classes)

#XXX When to call tier_instance_class? when making an instance, as triggered
# by a button or something. For now just testing
#tier_instance_class = input_tier_instance_class(custom_tier_tree)
#tier_instance = tier_instance_class()
#connections = input_connections_to(tier_instance)
make_instances(custom_tier_tree)

log.debug("Class of tier: {}".format(tier_instance_class))
