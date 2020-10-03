# vim: set sw=4 noet ts=4 fileencoding=utf-8:

import unittest
import logging
import sys
sys.path.append('../code')
import ruminant
from ruminant import Ruminant
import keys

tier_tree_path = keys.tier_tree_path
tier_instances_path = keys.tier_instances_path

def setup_logger(logger_level):
	''' Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
	logger_level should be passed in in the format logging.LEVEL '''

	logging.basicConfig(level=logger_level)
	logger = logging.getLogger(__name__)
	return logger

class Test_Ruminant(unittest.TestCase):

	# Use decorator to disable tests
	def disabled(self):
		def _decorator(f):
			 self.log.info(str(f) + ' has been disabled')
		return _decorator

	def setUp(self):
		self.log = setup_logger(logging.DEBUG)
		self.r = Ruminant(tier_tree_path, tier_instances_path)
		#XXX class_constructor is now in tier_tree
		self.class_constructor = self.r.tt.class_constructor
		self.fake_attributes_dict1 = {
			"__init__" : self.class_constructor,
			"name" : "Upper_Fake_Tier1",
			"hierarchy_level" : 0,
		}
		self.Fake_Class1 = type(
			"Upper_Fake_Tier1", (object,), self.fake_attributes_dict1)
		self.fake_attributes_dict2 = {
			"__init__" : self.class_constructor,
			"name" : "Lower_Fake_Tier2",
			"hierarchy_level" : 1,
		}
		self.Fake_Class2 = type(
			"Lower_Fake_Tier2", (object,), self.fake_attributes_dict2)
		self.fake_attributes_dicts_list = [
			self.fake_attributes_dict1, self.fake_attributes_dict2
		]
		self.n_tier_classes = 2
#		self.fake_tier_tree = self.r.setup_tier_tree(
#			self.n_tier_classes,
#			self.fake_attributes_dicts_list
#		)
		self.fake_tier_tree = [
			{0: [self.Fake_Class1]}, {1: [self.Fake_Class2]}
		]

		self.fake_inst_attr_dict = {
			'Name' : 'fake instance', 'Status' : 'hot mess'
		}
		self.fake_inst_attr_func = lambda x : self.fake_inst_attr_dict
#	@disabled
#	def test_create_tier_class_90(self):
#		self.log.debug("\n TEST 90 \n")
#		New_Tier_Class = self.r.create_tier_class(fake_attributes_dict1)
		
	@disabled
	def test_setup_tier_tree_100(self):
		self.log.debug("\n TEST 100 \n")
		# Need a way to simulate input of create_tier_class()
		fake_tier_tree = [
			{0: [self.Fake_Class1]}, {1: [self.Fake_Class2]}
		]
		self.log.debug("tier_tree: {}".format(tier_tree))
		self.log.debug("fake_tier_tree: {}".format(fake_tier_tree))
		#XXX need to test that tree_tier's classes have the same attributes
		# and structure, but since they are constructed in different places
		# this assert fails to do so.
		assert(len(self.fake_tier_tree) == len(fake_tier_tree))
		#XXX I wish the below assert could work
		#assert(tier_tree == fake_tier_tree)

	def test_make_instances_150(self):
		self.log.debug("\n TEST 150 \n")
		instance = self.r.tic.make_instance(
			self.Fake_Class1, self.fake_inst_attr_func, None)
		instance_two = self.r.tic.make_instance(
			self.Fake_Class1, self.fake_inst_attr_func, None)
		instances = [instance, instance_two]
		self.log.debug("Instances: {}".format(instances))

	#@disabled
	def test_make_cucumber_200(self):
		'''
		Check that we make the correct cucumber from a fake setup of inputs
		'''
		self.log.debug("\n TEST 200 \n")

		instance = self.r.tic.make_instance(
			self.Fake_Class1, self.fake_inst_attr_func, None)
		instance_two = self.r.tic.make_instance(
			self.Fake_Class1, self.fake_inst_attr_func, None)
		instances = [instance, instance_two]
		self.r.make_cucumber(instances, self.tier_tree)



	#@disabled
	def test_load_cucumber_300(self):
		self.log.debug("\n TEST 300 \n")

	def tearDown(self):
		pass




if __name__ == "__main__":
	unittest.main()

