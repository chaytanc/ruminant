# vim: set sw=4 noet ts=4 fileencoding=utf-8:
import logging
import pdb
from tier_instance_constructor import Tier_Instance_Constructor

class Tier_Instance_Inputter():

	def __init__(self):
		self.log = self.setup_logger(logging.DEBUG)
		self.tic = Tier_Instance_Constructor()
		self.instances = []

	def setup_logger(self, logger_level):
		''' 
			Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
			logger_level should be passed in in the format logging.LEVEL 
		'''

		logging.basicConfig(level=logger_level)
		logger = logging.getLogger(__name__)
		return logger

	def input_tier_instance_class(self, custom_tier_tree):
		'''
			Asks what type of tier_instance is being created / which Tier
			Class it uses. For example, is it an instance of Main Goals?
		'''
		self.tic.display_tier_types(custom_tier_tree)
		tier_type_input = input("What type of tier are you creating? \n")
		tier_instance_class = self.tic.get_class_by_name(
			custom_tier_tree, tier_type_input)
		self.log.info("Setting tier_instance_class to {}".format(
			tier_instance_class))
		return tier_instance_class

	def input_connections_to(self, tier_inst, instances):
		''' 
			Asks / forces the user to create at least one connection between 
			the current tier instance and a lateral or above class instance.
			#XXX Input must be in the format of a literal tier instance, doesn't
			search by name from possible instances for the correct one
		'''
		
		# display classes above created instance
		# Continuously ask to make connections if the tier is not the root tier
		if tier_inst.is_root:
			keep_inputting = False
		else: 
			keep_inputting = True

		connections = []
		while keep_inputting:
			# Display options of tier instances for connections
			# Asks for inputted connections
			connection = input("Input connections to tier {}. ".format(
				tier_inst) +\
				"At least one must be of equal or higher hierarchy level," +\
				" or the 'root' tier instance. \n")
			
			# If input is empty, break the loop
			if connection.strip() == "":
				keep_inputting = False
				break

			# User inputs a instance name as a string and we match it to the
			# actual instance object
			matching_inst = self.tic.match_inst_name_to_inst(
				connection, instances)
			# Don't want to input an empty str
			connections.append(matching_inst)
					
		return connections

	#XXX working to abstractize this for all attr
	def input_instance_attr(self, tier_instance_class, attr):
		instance_attr = input("What is the {} of this instance of {}".format(
			attr, tier_instance_class))
		return instance_attr

	def input_is_root(self, tier_inst):
		'''
			Set is_root to true if the user responds yes. If the user tries to 
			set the root on a hierarchy level that isn't 0, it fails.
		'''
		is_root = False
		root_inp = input("Is this instance of a tier the root of your whys?" +\
			" The ultimate goal? (y/n)")
		if root_inp == "yes" or \
				root_inp == "Yes" or \
				root_inp == "y" or \
				root_inp == "Y":
			is_root = True
		root_was_set = self.tic.set_root(tier_inst, is_root)
		# root_was_set not used right now
		return root_was_set

	def make_inputted_instance(self, Tier_Instance_Class):
		'''
			Makes one instance of a Tier Class based on input
		'''
		#XXX working here to setup instance arguments before instantiating
		# list of all fields to set
		fields_to_exclude = self.tic.get_fields_to_exclude(
			Tier_Instance_Class)
		instance_attrs = self.tic.set_inst_attributes(
			Tier_Instance_Class, self.input_instance_attr, fields_to_exclude)
		inst = Tier_Instance_Class(instance_attrs)

		#XXX inst.name is redundant since the Name field forces it to be set
		instance_name = self.input_instance_attr(Tier_Instance_Class, "name")
		inst.name = instance_name
		root_was_set = self.input_is_root(inst)
		#XXX need to refactor order of calls to functions such that I can pass
		# in correct things
		connections = self.input_connections_to(inst, instances)
		self.tic.make_connections(inst, *connections)
		return inst

	def make_inputted_instances(self, custom_tier_tree):
		'''
			Continuously makes instances of Tier Classes until the user
			inputs an empty string so as to signal the end.
		'''
		instances = []
		keep_inputting = True
		while keep_inputting:	
			self.log.info("Start creating an instance of a tier class.")
			self.display_instances(instances)
			tier_instance_class = self.input_tier_instance_class(
				custom_tier_tree)
			tier_inst = self.make_inputted_instance(tier_instance_class)
			#XXX working here to setup instance attributes and actually store
			# instance
			#self.tic.set_inst_attributes(tier_instance_class)
			instances.append(tier_inst)

			done_inputting = input("Done creating tier instances? (y/n)")
			if done_inputting == 'y' or \
				done_inputting == 'Y' or \
				done_inputting == 'yes' or \
				done_inputting == 'Yes': 
				keep_inputting = False
				break
		return instances

	def display_instances(self, instances):
		self.log.info('Instance options: \n')
		for instance in instances:
			self.log.info('{} \n'.format(instance.name))




		
		
