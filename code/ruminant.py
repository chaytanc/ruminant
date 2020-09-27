# vim: set sw=4 noet ts=4 fileencoding=utf-8:
import logging
import pdb
from tier_tree import Tier_Tree
from tier_tree_inputter import Tier_Tree_Inputter
from tier_instance_constructor import Tier_Instance_Constructor
from tier_instance_inputter import Tier_Instance_Inputter
from airtable_reader import Airtable_Reader
from airtable_writer import Airtable_Writer
import pickle as pkl
import dill
import os
import keys
from airtable import Airtable

tier_tree_path = keys.tier_tree_path
tier_instances_path = keys.tier_instances_path



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

		self.ar = Airtable_Reader()

		self.tt = Tier_Tree(
			self.ar, keys.attr_dict_path1, keys.attr_dict_path2)
		self.ttin = Tier_Tree_Inputter(self.tt)

		self.aw = Airtable_Writer(self.ar, self.tt)

		self.tic = Tier_Instance_Constructor(self.tt)
		self.tii = Tier_Instance_Inputter(self.tic)

		#XXX may need to update all_tables_records periodically
		#Ex: all_tables = {0 : 
			#[('Main Quests', <Airtable table: Main Quests>)]}
		self.all_tables = self.ar.get_all_tables()
		self.all_tables_records = self.ar.get_all_tables_records(
			self.all_tables)
		#XXX keep track of field accepted types? Like Status = To Do or Done
		self.all_tables_field_names = self.ar.get_all_tables_field_names(
			self.all_tables_records)
		
		self.tier_tree_path = tier_tree_path
		self.tier_instances_path = tier_instances_path

		#tier_tree Ex: 
			#[{0 : [<Main class object>]}, {1 : [<Tasks class object>]}]

		self.tier_tree = None
		#XXX this would probably be more useful if it was 
		# {airtable table object : [instances]}  not
		# {'table name / tier class' : [instances]}
		self.tier_instances = {}

		self.staged_instances = None

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
		#XXX may not be necessary
		self.tier_tree = custom_tier_tree
		return custom_tier_tree

	def get_tier_tree_instances(self, custom_tier_tree, stage=False):
		'''
			Args: tier tree as constructed by get_airtable_tier_tree 
				in tier_tree.py for example
			Makes instances of classes within the tier tree
		'''
		instances = self.tii.make_inputted_instances(custom_tier_tree, stage)
		self.log.debug('tier_tree_instances: {}'.format(instances))
		self.tic.display_instances_and_props(instances)
		#self.update_ruminant_instances(instances)
		return instances

	def update_ruminant_instances(self, instances):
		'''
		Takes the given instances and overwrites Ruminant().tier_instances with
		instances provided. self.tier_instances key is instance's class name, 
		value is the instances list.
		'''
		# Gets the class_name from the 0th element assuming that all instances
		# in the given list are of the same type
		class_name = instances[0].__class__.name
		self.tier_instances[class_name] = instances

	def update_airtable_h_levels(self):
		self.aw.set_table_h_levels(self.all_tables, self.all_tables_records)

	def set_staged_instances(self):
		#self.staged_instances = self.tic.get_staged_instances()
		self.staged_instances = self.tic.staged_instances
		self.log.info('\n Staged instances = {}'.format(self.staged_instances))

	def get_unconnected_instances(self, tier_tree):
		# Initially sync self.staged_instances to self.tic.staged_instances
		self.set_staged_instances()
		# Make instances w/out connections
		#instances = self.tii.make_inputted_instances(
			#custom_tier_tree, stage=False)
		#tier_tree = self.tt.get_airtable_tier_tree(
			#self.all_tables, self.all_tables_field_names, load_attr_dict=False)
		self.update_airtable_h_levels()
		unconnected_instances = self.get_tier_tree_instances(
			tier_tree, stage=False)
		self.save_obj(unconnected_instances, self.tier_instances_path)
		return unconnected_instances


	#XXX DOWNSIZE this function
	def update_airtable_staged_records(self, 
		load_connected_instances=False, 
		load_unconnected_instances=False):
		'''
		This func will get tier_tree from airtable and then get instances
		from user input. It will then stage the instances after connections
		have been input and finally push the changes to airtable.
		It attempts to pickle staged instances after connections are made.
		Args:
			load_instances: if True this will load pickled instances rather
				than inputting new ones.
		'''
		
		# Init staged_instances
		#staged_instances = None
		if load_connected_instances:
			#XXX workign here to load cucumber
			#self.staged_instances = self.load_obj(self.tier_instances_path)

			#[({class_attr_dict}, [{inst_attr_dicts},]),]
			cucumber = self.load_obj('./ruminant_objs/cucumber.pkl')
			# remake tier tree using cucumber attr dicts, not airtable reading
			#XXX this no longer works b/c changed cucumber datatype
			#tier_class_attr_dicts = cucumber.keys()
			tier_class_attr_dicts = self.get_cucumber_tier_class_dicts(
				cucumber)
			#XXX may not need tier_tree since we're directly constructing
			# instance classes from
			tier_tree = self.tt.get_airtable_tier_tree(
				load_attr_dict=True, 
				tier_tree_attr_dicts=tier_class_attr_dicts)
			# use tier tree to remake instances, applying cucumber attr dicts
			# instead of input
			instances = self.tic.make_cucumber_instances(cucumber, tier_tree)
			self.set_staged_instances()
			self.log.info('loaded connected instances: {}'.format(
				self.staged_instances))
			#XXX working to apply class attributes to loaded pkls
			# not necessary since make_instance gets and applies attribute dict
		else:
			# Init unconnected_instances & tier_tree
			unconnected_instances = None
			tier_tree = None

			#XXX not sure this part works
			if load_unconnected_instances:
				unconnected_instances = self.load_obj(self.tier_instances_path)

			else:
				tier_tree = self.tt.get_airtable_tier_tree(
					load_attr_dict=False,
					all_tables=self.all_tables, 
					all_tables_field_names=self.all_tables_field_names
				)
				unconnected_instances = self.get_unconnected_instances(
					tier_tree)

			# Make connections
			self.tii.input_all_connections(unconnected_instances, stage=True)
			#NOTE staged_instances has {'name' : instance} format
			self.set_staged_instances()
			#XXX working to pickle class attributes and inst attrs as cucumber
			cucumber = self.make_cucumber(
				self.staged_instances.values(), tier_tree)
			#self.save_obj(self.staged_instances, self.tier_instances_path)
			self.save_obj(cucumber, './ruminant_objs/cucumber.pkl')

		staged_instances_values = self.staged_instances.values()
		self.aw.set_records(staged_instances_values, self.all_tables)

	def make_cucumber(self, instances, tier_tree):
		'''
		Returns a dict, keys are the tier class attributes dict, 
		keys are a list of instance attribute dicts.
		Ex: {
				{hierarchy_level : 0, 'name' : 'Main Quests'} : 
				[{'Name' : 'Conquer Europa'}]
			}

			new type returned: 
				[({class_attr_dict}, [{inst_attr_dicts},]),]
		'''

		cucumber = []

		all_classes = self.get_tier_tree_classes(tier_tree)
		
		for cls in all_classes:
			cls_instance_attrs_list = []
			cls_attr_dict = self.tt.get_class_attributes(cls)
			for instance in instances:
				if instance.__class__.name == cls.name:
					inst_attr_dict = instance.instance_attributes
					cls_instance_attrs_list.append(inst_attr_dict)
			# (cls_attr_dict, [inst attr dicts])
			attr_dicts_tuple = (cls_attr_dict, cls_instance_attrs_list)
			cucumber.append(attr_dicts_tuple)
		return cucumber

	def get_tier_tree_classes(self, tier_tree):
		all_classes = []
		for h_level_dict in tier_tree:
			for tier_class_list in h_level_dict.values():
				for tier_class in tier_class_list:
					all_classes.append(tier_class)
		return all_classes

	def get_cucumber_tier_class_dicts(self, cucumber):
		tier_attr_dicts = []
		for tier_attr_dict, _ in cucumber:
			tier_attr_dicts.append(tier_attr_dict)
		return tier_attr_dicts



	def update_connections(self):
		'''
		This function will ask each instance that is not the root to form a why
		connection why something above it, starting with the top down 
		hierarchy_levels
		'''
		# Setup each instance to have connection instance attributes from fields
		#NOTE are the connections fields excluded?
		# For each connection field, ask for a connection and set instance
		# attribute. set inst attr to be literal other instance, not just
		# name of other instance so that later we can actually link records
		# add to instance.instance_attributes['airtable_attributes']
		# After setting inst attrs, push inst attrs to airtable w 
		# self.aw.set_records(instances, self.all_tables)

		#self.tii.input_all_connections(instances)
		#staged_instances = self.tii.staged_instances

		#for instance in staged_instances:
			# 

#-----------------------------PICKLING---------------------------------------
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

		self.log.debug('Trying to pickle {} \n'.format(obj))
		if obj == None:
			raise(ValueError('', 'Empty obj passed to save_obj'))

		#NOTE this overwrites the existing object, "a" would append
		with open(obj_file_path, "wb") as f:
			try:
				pkl.dump(obj, f)
				#dill.dump(obj, f)
				self.log.info("Pickled obj {} to file {}".format(
					obj, obj_file_path))
			except Exception as e:
				self.log.critical("Pickling failed due to {}".format(e))
				#bad = dill.detect.baditems(obj)
				#self.log.critical("Bad pickling items: {}".format(bad))
				#errors = dill.detect.errors(obj)
				#self.log.critical("Pickling errors: {}".format(errors))

			f.close()

	def load_obj(self, obj_file_path):
		'''
			This function unpickles and loads an object such as tier_tree or 
			tier tree instances from a given file.
		'''

		obj = None
		try:
			with open(obj_file_path, "rb") as f:
				#obj = pkl.load(f)
				obj = dill.load(f)
				self.log.info("Loaded obj {} from file {}".format(
					obj, obj_file_path))
				f.close()
		except FileNotFoundError as e:
			self.log.critical(
				'You have not processed and saved the data yet!' +\
				'\n Call save_obj on the obj you are trying to save first!'
			)
		except Exception as e:
			self.log.critical('Unpickling failed due to {}'.format(e))

		return obj

	
if __name__ == "__main__":

	r = Ruminant(tier_tree_path, tier_instances_path)
	#instances = ruminant.make_and_save_objs()
	tier_tree = r.tt.get_airtable_tier_tree(
		all_tables=r.all_tables, 
		all_tables_field_names=r.all_tables_field_names, 
		load_attr_dict=False)
	r.update_airtable_h_levels()
	#instances = r.get_tier_tree_instances(tier_tree)
	#r.update_airtable_records(tier_tree)
	#XXX False, True doesn't seem to work as it should.
	# Should be same as False False
	r.update_airtable_staged_records(
		load_connected_instances=False, load_unconnected_instances=False)
	
	
