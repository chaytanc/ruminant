# vim: set sw=4 noet ts=4 fileencoding=utf-8:

from airtable import Airtable
#from tier_tree import Tier_Tree
import keys
import logging

class Airtable_Reader():

	def __init__(self):
		self.at = self.setup_airtable("Main Quests")
		#self.tt = Tier_Tree()
		self.log = self.setup_logger(logging.DEBUG)
		self.read_all_tables()

	def setup_logger(self, logger_level):
		''' 
		Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
			logger_level should be passed in in the format logging.LEVEL 
		'''

		logging.basicConfig(level=logger_level)
		logger = logging.getLogger(__name__)
		return logger

	#XXX redundant copy paste from ruminate_new.py... clean up later
	def setup_airtable(self, table):
		'''
		Args: 
			table: an int or str matching your Airtable's desired table 
				name and corresponding to keys.tables by either key or value.
		'''
		try:
			desired_table = keys.tables[table]
		except KeyError:
			desired_table = table

		airtable = Airtable(keys.base_id, desired_table, keys.api_key)
		#self.log.info("Airtable instance: {}".format(airtable))
		return airtable

	def get_all_tables(self):
		'''
		Returns a dict of airtable tables matched with their name 
		and h_level from keys.tables
		Ex: all_tables = {0 : 
			[('Main Quests', <Airtable table: Main Quests>)]}
		'''
		all_tables = {}
		# Looping through keys.tables and getting linking airtables accordingly
		for h_level, tables in keys.tables.items():
			for table_name in tables:
				self.log.info("table name: {}".format(table_name))
				table_instance = self.setup_airtable(table_name)
				table_tuple = (table_name, table_instance)
				# Check if there are already tables in the given h_level
				# and append or create accordingly
				try: 
					all_tables[h_level].append(table_tuple)
				except KeyError:
					all_tables[h_level] = [(table_name, table_instance)]
		return all_tables

	
	def get_all_records(self, airtable):
		'''
		Returns all the records from a given table.
		'''
		all_records = airtable.get_all()
		self.log.debug("Airtable records: {}".format(all_records))
		return all_records

	def get_all_tables_records(self, all_tables):
		'''
		Args: see get_all_tables return format
		Returns a dict. Keys are a table's name, values are a table's records
		as a list of dictionary objects as returned by Airtable queries in 
		get_all_records.
		'''

		all_tables_records = {}

		# For each table loop thorugh to get individual table and 
		# names and hierarchy level
		for hierarchy_level, tables in all_tables.items():
			for (table_name, airtable) in tables:

				all_records = self.get_all_records(airtable)
				all_tables_records[table_name] = all_records
		return all_tables_records

	def get_all_field_names(self, all_records, fields_to_exclude=['']):
		'''
		Args: 
			all_records: all of one table's records, refer to get_all_records
			return format.
			fields_to_exclude: a list of field names as strings which to not
			include in get_all_field_names's return
		Returns all the field names of columns in a table given its records.
		NOTE: if the column is empty this will not work fully. Refer
		to the ruminant template.
		'''
		field_names = []
		for record in all_records:
			field_names = record['fields'].keys()
			for record_field_title in field_names:
				self.log.info('\n {} \n'.format(record_field_title))
				if record_field_title not in field_names and \
					record_field_title not in fields_to_exclude:
					field_names.append(record_field_title)

		return field_names

	def get_all_tables_field_names(self, all_tables_records):
		'''
		Args: see get_all_tables_records return format

		Returns a dict. Keys are a table's name, values are a table's field 
			names as strings.
		'''
		all_tables_field_names = {}
		for table_name, records_list in all_tables_records.items():
			field_names = self.get_all_field_names(records_list)
			all_tables_field_names[table_name] = field_names

		return all_tables_field_names

	def read_all_tables(self):
		'''
		Sets airtable_reader instance to have attributes of:
		all_tables, all_tables_records, all_tables_field_names
		to avoid redundant queries. Called in the init of Airtable_Writer.
		'''
		self.all_tables = self.get_all_tables()
		self.log.debug("\nAirtable Reader all_tables: {}".format(
			self.all_tables))
		self.all_tables_records = self.get_all_tables_records(self.all_tables) 
		self.log.debug("\nAirtable Reader all_tables_records: {}".format(
			self.all_tables_records))
		self.all_tables_field_names = self.get_all_tables_field_names(
			self.all_tables_records)
		self.log.debug("\nAirtable Reader all_tables_field_names: {}".format(
			self.all_tables_field_names))


#	def get_tier_class_names_from_fields(self, tables):
#		'''
#			This reads the fields of all tables in an airtable and should 
#			be compatible with tier_tree and returns a list of all their names.
#		'''
#		class_names = []
#		for table in tables:
#
#			name = the string inputted to keys.tables...

#XXX do this in airtable writer when setting up the h_levels and simultaneously
# reading the names of the tables etc.... should separate those funcs
#	def get_min_attributes_dict(self, airtable):
#		'''
#			Get the class name and hierarchy level and create an 
#			attributes dict based on the Airtable passed in.
#		'''
#		name =  
#		hierarchy_level = keys.tables.
#		attr_dict = self.tt.create_min_attributes_dict(name, hierarchy_level)
#		#XXX fill connections in through instances
#		return attr_dict
			
