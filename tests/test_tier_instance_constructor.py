# vim: set sw=4 noet ts=4 fileencoding=utf-8:

import unittest
import logging
import sys
sys.path.append('../code')
from tier_instance_constructor import Tier_Instance_Constructor
import keys
from tier_tree import Tier_Tree

tier_tree_path = keys.tier_tree_path
tier_instances_path = keys.tier_instances_path

def setup_logger(logger_level):
	''' Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
	logger_level should be passed in in the format logging.LEVEL '''

	logging.basicConfig(level=logger_level)
	logger = logging.getLogger(__name__)
	return logger

class Test_Tier_Instance_Constructor(unittest.TestCase):

	# Use decorator to disable tests
	def disabled(self):
		def _decorator(f):
			 print(str(f) + ' has been disabled')
		return _decorator

	def setUp(self):
		self.log = setup_logger(logging.DEBUG)
		self.tic = Tier_Instance_Constructor()
		self.tt = Tier_Tree()
		self.setup_fake_tier_tree()

	def setup_fake_tier_tree(self):
		n_tier_classes = 1
		name = "Main"
		hierarchy_level = 0
		airtable_instance = "obviously wrong value for airtable_instance"

		input_min_attrs_func = lambda: self.tt.create_minimum_attributes_dict(
			name, hierarchy_level, airtable_instance)
		# A quick func that returns True for keep_inputting and
		# "Above_Connections" for the name of a class attr
		input_class_attrs_func = lambda name : (False, "Above_Connections")
		self.fake_tier_tree = self.tt.setup_tier_tree_attributes(
			n_tier_classes, input_min_attrs_func, 
			input_class_attrs_func)
		self.fake_tier_class = self.fake_tier_tree[0][0][0]

	#@disabled
	def test_get_instance_attributes_100(self):
		self.log.debug("\n TEST 100 \n") 
		get_inst_attr = lambda tier_class, field : 'Gather penguins'
		fields_to_exclude = []
		instance_attributes = self.tic.get_instance_attributes(
			self.fake_tier_class, get_inst_attr, fields_to_exclude)
		self.log.debug('\ninstance_attributes: {}'.format(instance_attributes))
		supposed_instance_attributes = {
			'airtable_attributes' : {'Above_Connections' : 'Gather penguins'},
			'other_attributes' : {'is_root' : False}
		}
		self.log.debug('\nsupposed_instance_attributes: {}'.format(
			supposed_instance_attributes))
		self.assertDictEqual(instance_attributes, supposed_instance_attributes)

	#@disabled
	def test_get_fields_to_exclude_200(self):
		self.log.debug("\n TEST 200 \n")
		fields_to_exclude = self.tic.get_fields_to_exclude(
			self.fake_tier_class)
		self.log.debug('\n fields_to_exclude: {}'.format(fields_to_exclude))
		supposed_fields_to_exclude = ["Above_Connections", "Hierarchy Level"]
		self.assertEqual(fields_to_exclude, supposed_fields_to_exclude)

	#@disabled
	def test_match_inst_name_to_inst_300(self):
		self.log.debug("\n TEST 300 \n")
		name = 'Gather penguins'
		#instances = 
		self.tic.match_inst_name_to_inst(name, instances)

	def tearDown(self):
		pass




if __name__ == "__main__":
	unittest.main()

