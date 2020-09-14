# vim: set sw=4 noet ts=4 fileencoding=utf-8:

import logging
import pdb

#XXX I believe this is the same class as ruminant is
class Airtable_Base():
	'''
	Contains all tables, fields of the table, corresponding tier_tree for each
	table, and all instances / records made of each table.
	'''
	
	def __init__(self):
		self.log = self.setup_logger(logging.DEBUG)
		# {'table_name / tier_class.name' : tier_tree}
		self.tier_trees = {}
		# {'table name / tier class' : [instances]}
		self.tier_instances = {}

	def setup_logger(self, logger_level):
		''' 
			Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
			logger_level should be passed in in the format logging.LEVEL 
		'''

		logging.basicConfig(level=logger_level)
		logger = logging.getLogger(__name__)
		return logger

