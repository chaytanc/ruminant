# vim: set sw=4 noet ts=4 fileencoding=utf-8:
import logging
import pdb
from tier_tree import Tier_Tree
from tier_tree_inputter import Tier_Tree_Inputter
from tier_instance_constructor import Tier_Instance_Constructor
from tier_instance_inputter import Tier_Instance_Inputter

class Ruminant():

	def __init__(self):
		self.log = self.setup_logger(logging.DEBUG)
		self.tt = Tier_Tree()
		self.ttin = Tier_Tree_Inputter()

		self.tic = Tier_Instance_Constructor()
		self.tii = Tier_Instance_Inputter()

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

ruminant = Ruminant()
ruminant.get_tier_tree_instances()


	
	
