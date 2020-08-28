# vim: set sw=4 noet ts=4 fileencoding=utf-8:
import logging
import pdb
from tier_tree import Tier_Tree

class Tier_Tree_Inputter():

	def __init__(self):
		self.log = self.setup_logger(logging.DEBUG)
		self.tt = Tier_Tree()

	def setup_logger(self, logger_level):
		''' 
			Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
			logger_level should be passed in in the format logging.LEVEL 
		'''

		logging.basicConfig(level=logger_level)
		logger = logging.getLogger(__name__)
		return logger
	
	def input_as_int(self, input_question):
		''' 
			This function continues to ask for an integer value as 
			input until it is satisfied.
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

	def input_n_tier_classes(self):
		input_question = ("How many tier classes will there be?" + \
			" Ex: Main Goals and Tasks would be 2 different tier classes. \n")
		n_tier_classes = self.input_as_int(input_question)
		return n_tier_classes

	def input_min_attributes(self):
		''' 
			This function outlines the mandatory properties of every tier. 
			Every tier must have a class name, such as Main Goals, and must have
			a hierarchy level. Additional, variable class attributes can 
			be set for different tiers by passing in a dict when init 
			with class_constructor.
		'''
		# Garbage in, garbage out. Guard the perimeter then forget about it
		# Must be string
		name = input("What is the name of this tier class? \n")
		# Must be int
		hierarchy_question = "What is the hierarchy level of this tier?\n"
		hierarchy_level = self.input_as_int(hierarchy_question)
		min_attributes_dict = self.tt.create_minimum_attributes_dict(
			name, hierarchy_level)
		return min_attributes_dict

#	def input_tier_tree(self, n_tier_classes):
#		'''
#			Create the individual attributes each different tier class must 
#			have based on user input and then constructs the tier tree.
#		'''
#		attributes_dicts_list = []
#
#		for	tier_class in range(n_tier_classes):
#			# Ask for hierarchy level and name of class we create
#			attributes_dict = input_min_attributes()
#			name = attributes_dict["name"]
#			#  Loop and get class_attribute inputs until user is done
#			keep_inputting = True
#			while keep_inputting:
#				log.info("If you press enter without supplying input" + \
#					" no more class \n attributes will be added.")
#				class_attribute = input(
#					"Enter the name of a {} attribute: ".format(name)
#				)
#				if class_attribute.strip() == "":
#					keep_inputting = False
#					break
#				# If it is a valid class attribute, store it in attr_dict
#				else:
#
#					#NOTE Hopefully they don't enter hierarchy_level,
#					# or name because that overwrites previously setup
#					# name and hierarchy_level attributes to None
#
#					# Stores the unset class_attribute 
#					# in the dict of class attrs as a temporary None type
#					attributes_dict[class_attribute] = None
#			attributes_dicts_list.append(attributes_dict)
#
#		custom_tier_tree = self.tt.setup_tier_tree(
#			n_tier_classes, attributes_dicts_list)
#		log.info("\nCustom tier tree: \n {}".format(custom_tier_tree))
#		return custom_tier_tree

	def input_class_attributes(self, name):
		'''
			This function asks for a desired class attribute to be input
			and tells if the user has signaled to end input stream
		'''
		keep_inputting = True
		self.log.info("If you press enter without supplying input" + \
			" no more class \n attributes will be added.")
		class_attribute = input(
			"Enter the name of a {} attribute: ".format(name)
		)
		if class_attribute.strip() == "":
			keep_inputting = False

		return (keep_inputting, class_attribute)









