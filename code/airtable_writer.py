# vim: set sw=4 noet ts=4 fileencoding=utf-8:

from airtable import Airtable
from tier_tree import Tier_Tree
from airtable_reader import Airtable_Reader
import keys
import logging


class Airtable_Writer():

	def __init__(self, ar, tt):
		#XXX this and all_tables should be a property of ruminant / needs to 
		# somehow update periodically
		# Airtable Reader and Tier Tree from Ruminant
		self.ar = ar
		self.tt = tt
		#self.ar = Airtable_Reader()
		#self.tt = Tier_Tree()
		self.log = self.setup_logger(logging.DEBUG)
		# Needs to be a dict so that we can easily update instances that have
		# already been staged
		#XXX moved to tic
		#self.staged_instances = {}

	def setup_logger(self, logger_level):
		''' 
			Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
			logger_level should be passed in in the format logging.LEVEL 
		'''

		logging.basicConfig(level=logger_level)
		logger = logging.getLogger(__name__)
		return logger

	def set_table_h_levels(self, all_tables, all_tables_records):
		'''
			Sets every Airtable table to have an h_level in the 
			Hierarchy Level Airtable that corresponds to keys.tables.
			Also makes the attr_dict that is used to construct tier_tree 
			to have the correct h_level.
		'''
		
		# For each table create a different attributes dict with different
		# names and hierarchy level
		for hierarchy_level, tables in all_tables.items():
			for (table_name, airtable) in tables:
				self.log.info("table_name: {}, airtable: {} \n".format(
					table_name, airtable))

				# set airtable to have correct h_level
				table_records = all_tables_records[table_name]
				self.set_h_level_fields(
					table_records, hierarchy_level, airtable)

	def set_h_level_fields(self, all_records, hierarchy_level, airtable):
		'''
		Args:
			all_records: every record within one airtable
			hierarchy_level: that table's associated hierarchy level as an int
			airtable: the instance of the airtable you want to write to

		Replaces h_level fields to have the correct hierarchy level for every
		record in a table.
		'''
		# for each record in the table
		for record in all_records:
			r_id = record['id']
			fields = {'Hierarchy Level' : str(hierarchy_level)}
			# set airtable record's h_level 
			airtable.update(r_id, fields)

	def set_records(self, instances, all_tables):
		'''
		Args:
			#instances: a dict of instance objects and the table they belong to. 
			#Keys are the table, value is a list of of instances 
			#of a tier_class from tier_tree representing one record in a table. 
			instances: a list of all instances of tier_classes from tier_tree.
			The list collectively represents all rows added to an 
			airtable table.  As returned by make_inputted_instances from 
			tier_instance_inputter.
			all_tables: Ruminant().all_tables

		Creates a new record in the correct table for each instance in instances
		'''

		# Each instance and it's attributes represent one record,
		# attribute names are column titles, values are the value of
		# that column for that row / record

		#NOTE: batch insertion not supported right now
		#inst_table = all_tables[instance.__class__.name]
		#records = []

		for instance in instances:
			#NOTE: instance_attributes are constructed by 
			# set_instance_attributes in tier_instance_constructor.py
			#XXX this breaks pickling
			inst_table = instance.__class__.airtable_instance
			record = instance.instance_attributes['airtable_attributes']
			# for batches: Append each column / field / instance attribute 
			# to records which will then update the table
			#records.append(record)

			# Create airtable record in that table
			inst_table.insert(record)
		#inst_table.batch_insert(records)





