# vim: set sw=4 noet ts=4 fileencoding=utf-8:

from airtable import Airtable
from tier_tree import Tier_Tree
from airtable_reader import Airtable_Reader
import keys
import logging


class Airtable_Writer():

	def __init__(self):
		self.ar = Airtable_Reader()
		self.tt = Tier_Tree()
		self.log = self.setup_logger(logging.DEBUG)
		#XXX only want to query for tables once so stored it here
		self.ar.read_all_tables()
		#self.all_tables = self.ar.get_all_tables()

	def setup_logger(self, logger_level):
		''' 
			Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
			logger_level should be passed in in the format logging.LEVEL 
		'''

		logging.basicConfig(level=logger_level)
		logger = logging.getLogger(__name__)
		return logger

	def set_h_levels(self, all_tables):
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

				#XXX moved attr_dict out of here, separation of powers & whatnot

				# set airtable to have correct h_level
				table_records = self.ar.all_tables_records[table_name]
				self.update_h_level_fields(
					table_records, hierarchy_level, airtable)

	def update_h_level_fields(self, all_records, hierarchy_level, airtable):
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


#	#XXX belongs in tier_tree.py
#	def get_tier_tree(self):
#		'''
#		Returns a tier_tree object based on the fields setup in Airtable.
#		Use Ruminant Template to see an example.
#		'''
#
#		tier_tree = []
#		# For each table create a different attributes dict with different
#		# names and hierarchy level
#		for hierarchy_level, tables in self.ar.all_tables.items():
#			for (table_name, airtable) in tables:
#				self.log.info("table_name: {}, airtable: {} \n".format(
#					table_name, airtable))
#
#				# set tier_tree attr_dict with name and h_level for each 
#				# table
#				attr_dict = self.tt.create_minimum_attributes_dict(
#					table_name, hierarchy_level)
#
#				# set all the tier_tree class attributes based on table fields
#				fields = self.ar.all_tables_field_names
#				table_fields = fields[table_name]
#				for field_name in table_fields:
#					attr_dict[field_name] = None
#				# create and store tier_trees based on the fields
#				tier_tree = self.tt.construct_tier_tree(tier_tree, attr_dict)
#
#		return tier_tree



#XXX call this from main of ruminate_new.py once cleaned up
aw = Airtable_Writer()
aw.set_h_levels(aw.ar.all_tables)



