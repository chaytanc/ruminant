# vim: set sw=4 noet ts=4 fileencoding=utf-8:
import logging
import pdb
from tier_tree import Tier_Tree
from tier_tree_inputter import Tier_Tree_Inputter
from tier_instance_constructor import Tier_Instance_Constructor
from tier_instance_inputter import Tier_Instance_Inputter
import pickle as pkl
import os
import keys
from airtable import Airtable

tier_tree_path = './ruminant_objs/tier_tree.pkl'
tier_instances_path = './ruminant_objs/tier_instances.pkl'


class Ruminant():
	'''
	Airtable setup: each tier class corresponds to a different table within
	a base in Airtable. Class attributes of the tier class each correspond to
	a fied within the class's base in Airtable. An instance of a class
	corresponds to a record within a particular base in Airtable.

	Now, the real functionality of this program is within each class's 
	connections attributes. These must correspond to fields in a class's table, 
	and running this program will automatically ensure that they are sensibly
	organized in a why/how logical fashion.

	You must manually setup the base with the proper tables and fields
	because the current Airtable API does not support programmatic creation.
	#XXX template link for github / others to use

	You also must setup your account API key and base id and other parameters
	found in the keys.py template.
	'''

	def __init__(self, tier_tree_path, tier_instances_path):
		self.log = self.setup_logger(logging.DEBUG)
		self.tt = Tier_Tree()
		self.ttin = Tier_Tree_Inputter()

		self.tic = Tier_Instance_Constructor()
		self.tii = Tier_Instance_Inputter()

		self.tier_tree_path = tier_tree_path
		self.tier_instances_path = tier_instances_path

	def setup_logger(self, logger_level):
		''' 
			Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
			logger_level should be passed in in the format logging.LEVEL 
		'''

		logging.basicConfig(level=logger_level)
		logger = logging.getLogger(__name__)
		return logger

	def get_tier_tree(self):
		'''
			Mixes inputter and tier tree to actually setup a tier tree with
			all desired tier classes based on inputs.
		'''
		n_tier_classes = self.ttin.input_n_tier_classes()
		input_class_attrs_func = self.ttin.input_class_attributes
		input_min_attributes = self.ttin.input_min_attributes
		custom_tier_tree = self.tt.setup_tier_tree_attributes(
			n_tier_classes, input_min_attributes, input_class_attrs_func)
		return custom_tier_tree

	def get_tier_tree_instances(self):
		'''
			Makes instances of classes within the tier tree
		'''
		custom_tier_tree = self.get_tier_tree()
		instances = self.tii.make_inputted_instances(custom_tier_tree)
		self.log.info("Instances: {}".format(instances))
		return instances

	def save_obj(self, obj, obj_file_path):
		'''
			This function pickles and saves an object such as tier_tree or 
			tier tree instances to a given file in binary format.
		'''
		# Makes the directory storing the pkl file if it doesn't exist
		directory = os.path.dirname(obj_file_path)
		self.log.debug("Dir: {}".format(directory))
		if not os.path.exists(directory):
			os.makedirs(directory)

		#NOTE this overwrites the existing object, "a" would append
		with open(obj_file_path, "wb") as f:
			pkl.dump(obj, f)
			self.log.info("Saved obj {} to file {}}".format(obj, obj_file_path))
			f.close()

	def load_obj(self, obj_file_path):
		'''
			This function unpickles and loads an object such as tier_tree or 
			tier tree instances from a given file.
		'''

		try:
			with open(obj_file_path, "rb") as f:
				obj = pkl.load(f)
				self.log.info("Loaded obj {} from file {}}".format(
					obj, obj_file_path))
				f.close()
		except FileNotFoundError as e:
			obj = None
			self.log.critical(
				'You have not processed and saved the data yet!' +\
				'\n Call save_obj on the obj you are trying to save first!'
			)
		return obj

	def make_and_save_objs(self):
		'''
			This function makes both the user's custom defined tier tree and 
			all instances of its classes and pickles them to local files.
		'''
		custom_tier_tree = self.get_tier_tree()
		#XXX can't pickle a class or class attributes. 
		# Need a different way of saving and retrieviing classes that 
		# the user made. Maybe just upload and download that data to 
		# Airtable immediately without local file intermediate.
		self.save_obj(custom_tier_tree, self.tier_tree_path)
		instances = self.tii.make_inputted_instances(custom_tier_tree)
		self.save_obj(instances, self.tier_instances_path)
		return instances

	def update_airtable(self, airtable, tier_tree, instances):
		'''
			Using the instances that have been created, update the corresponding
			fields based on tier_tree with those records.
		'''
		# for instance in instances:
			# Check if any instance Name fields match any airtable Name fields
			# If they match, update
				# Identify fields to update
				# match the instance's class with airtable field to update
				# (using keys.py?)
				# Replace any fields that instance has filled in the airtable
			# Else, create new record in the airtable and update fields that
			# the instance has filled in
		
	


ruminant = Ruminant(tier_tree_path, tier_instances_path)
#instances = ruminant.get_tier_tree_instances()
#instances = ruminant.make_and_save_objs()
ruminant.tt.get_airtable_tier_tree()
	
	
