# vim: set sw=4 noet ts=4 fileencoding=utf-8:

import unittest
import logging
import sys
sys.path.append('../code')
#import ruminant
#from ruminant import Ruminant
import keys
import tier_tree as t

tier_tree_path = keys.tier_tree_path
tier_instances_path = keys.tier_instances_path

def setup_logger(logger_level):
	''' Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
	logger_level should be passed in in the format logging.LEVEL '''

	logging.basicConfig(level=logger_level)
	logger = logging.getLogger(__name__)
	return logger

class Test_Tier_Tree(unittest.TestCase):

	# Use decorator to disable tests
	def disabled(self):
		def _decorator(f):
			 print(str(f) + ' has been disabled')
		return _decorator

	def setUp(self):
		self.log = setup_logger(logging.INFO)

		self.tt = t.Tier_Tree()

		class_constructor = t.class_constructor
		self.fake_attributes_dict1 = {
			"__init__" : class_constructor,
			"name" : "Main",
			"hierarchy_level" : 0,
			"airtable_instance" : "obviously wrong value for airtable_instance",
			"fields" : ["Details"],
		}
		
	#@disabled
	def test_construct_attributes_dict_90(self):
		self.log.info("\n TEST 90 \n")

		name = "Main"
		hierarchy_level = 0
		airtable_instance = "obviously wrong value for airtable_instance"


		input_min_attrs_func = lambda: self.tt.create_minimum_attributes_dict(
			name, hierarchy_level, airtable_instance)
		# A quick func that returns True for keep_inputting and
		# "Details" for the name of a class attr
		input_class_attrs_func = lambda name : (False, "Details")

		fake_attributes_dict = self.tt.construct_attributes_dict(
			input_min_attrs_func, input_class_attrs_func)
		#supposed_attributes_dict = {'fields': ['Details']}
		self.log.debug('\nfake_attr_dict: {}'.format(
			fake_attributes_dict))
		self.log.debug('\nfake_attr_dict1: {}'.format(
			self.fake_attributes_dict1))
		assert(fake_attributes_dict['fields'] == ['Details'])
		assert(fake_attributes_dict == self.fake_attributes_dict1)


	#@disabled
	def test_setup_tier_tree_attributes_100(self):
		self.log.info("\n TEST 100 \n")

		n_tier_classes = 1
		name = "Main"
		hierarchy_level = 0
		airtable_instance = "obviously wrong value for airtable_instance"

		input_min_attrs_func = lambda: self.tt.create_minimum_attributes_dict(
			name, hierarchy_level, airtable_instance)
		# A quick func that returns True for keep_inputting and
		# "Details" for the name of a class attr
		input_class_attrs_func = lambda name : (False, "Details")
		fake_tier_tree = self.tt.setup_tier_tree_attributes(
			n_tier_classes, input_min_attrs_func, 
			input_class_attrs_func)
		self.log.debug("Tier class: {}".format(
			fake_tier_tree[0][0][0].__dict__))
		Main_Class = fake_tier_tree[0][0][0]

		assert(Main_Class.fields == ['Details'])
		
	@disabled
	def test__200(self):
		self.log.info("\n TEST 200 \n")

	@disabled
	def test__name_300(self):
		self.log.info("\n TEST 300 \n")

	def tearDown(self):
		pass




if __name__ == "__main__":
	unittest.main()

