# vim: set sw=4 noet ts=4 fileencoding=utf-8:
import logging
import pdb

class Tier_Instance_Constructor():

	def __init__(self):
		self.log = self.setup_logger(logging.INFO)
		#self.tier_instances = []

	def setup_logger(self, logger_level):
		''' 
			Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
			logger_level should be passed in in the format logging.LEVEL 
		'''

		logging.basicConfig(level=logger_level)
		logger = logging.getLogger(__name__)
		return logger

	def get_all_classes(self, custom_tier_tree):
		'''
			Returns a list of every class that has been added to tier_tree
		'''
		full_classes_list = []
		# Gets all hierarchy levels from tier_tree
		for i, hierarchy_dict in enumerate(custom_tier_tree):
			# Get all classes in each hierarchy level
			# NOTE that i is a key in the case of hierarchy_dict, not an index
			classes_list = hierarchy_dict[i]
			for cls in classes_list:
				#pass in a fucntion to perform here instead of returning things?
				# That doesn't seem to work well because it requires setup of 
				# full_classes list... hard to abstract the setup as well since
				# it isn't always needed w/ while_unpackign func
				full_classes_list.append(cls)

		return full_classes_list
		
	def get_class_by_name(self, custom_tier_tree, name_to_find):
		''' 
			Searches through the custom_tier_tree to find a class 
			with the correct name attribute and return that class object. 
		'''
		# All classes as setup by the user
		class_list = self.get_all_classes(custom_tier_tree)
		found_class = None
		for cls in class_list:
			if cls.name == name_to_find:
				found_class = cls
		return found_class

	def display_tier_types(self, custom_tier_tree):
		'''
			Displays tier type options in std out
		'''
		full_classes_list = self.get_all_classes(custom_tier_tree)
		# Show tier types / options  to choose from based on 
		# creation of tier_tree
		for cls in full_classes_list:
			self.log.info("\n Tier Type options: {} \n".format(cls))
		#return full_classes_list

	def make_connections(self, tier_instance, *selected_connections):
		'''
			Set an attribute of the instance of the tier to have a connection to
			another class tier instance. selected_connections should be a list
			of other tier_instances to connect tier_instance with. 
			Returns: Returns whether the node has a why value attached after 
				all connections are made.
		'''
		for connection in selected_connections:
			# if it is the top / root instance in tree then no
			# connections can be made
			if tier_instance.is_root == True:
				# Skips the rest of this iteration and then continues iterating
				continue

			# Check hierarchy level of connection and add connection accordingly
			if connection.hierarchy_level > tier_instance.hierarchy_level:
				# Sets the tier_instance's connections field to link 
				# to those selected
				tier_instance.connections_above.append(connection)
				# Reciprocally sets the connected to's connection to 
				# tier_instance
				connection.connections_below.append(tier_instance)

			# If the connection hierarchy level is below the tier instance level
			elif connection.hierarchy_level < tier_instance.hierarchy_level:
				tier_instance.connections_below.append(connection)
				connection.connections_above.append(tier_instance)

			# If hierarchy levels are equal
			# selected_connections is a list of connections essentially 
			# (multiple args), if the connection is an equal level, it must be
			# passed as a dict which has what type of connection (why/how)
			# {connection: instance of conn, type: either why or how}
			else:
				conn_inst = connection["conncection_inst"]
				conn_type = connection["type"]
				if conn_type == "why":
					tier_instance.connections_equal_why.append(conn_inst)
					conn_inst.connections_equal_how.append(tier_instance)
				if conn_type == "how":
					tier_instance.connections_equal_how.append(connection)
					connection.connections_equal_why.append(tier_instance)

		# After making connections, check that the node has a why
		has_why = self.check_has_why(tier_instance)
		return has_why

	def check_has_why(self, connected_tier_inst):
		''' 
			This func checks that a connected_tier_instance has a why, meaning
			either a higher up connection or an equal level connection.
		'''
		has_why = False
		tier_level = connected_tier_inst.hierarchy_level

		# Everything must have a why. Except root.
		if connected_tier_inst.is_root == False:
			empty = []
			conns_above = conn.connections_above
			conns_equal_why = conn.connections_equal_why
			if conns_above != empty or conns_equal_why != empty:
				has_why == True

		return has_why


	def set_root(self, tier_inst, is_root):
		'''
		Args:
			is_root: input from user whether the instance should be set to root

		One inst / node on the tree must be the root why / have no why 
		connections. This function sets a tier instance's attribute
		to reflect if it is the root.
		'''
		root_was_set = False
		if is_root:
			if tier_inst.hierarchy_level == 0:
				#NOTE: instance attribute not class attribute. is_root is
				# evaluated for each record
				#XXX making instance_attributes have two dicts, one for 
				# record fields and one for other attributes like is_root
				tier_inst.instance_attributes["other_attributes"]["is_root"] = True
				root_was_set = True
			else:
				self.log.error("Root was not set b/c the root must be set " +\
					"at hierarchy level 0.")
		return root_was_set

	def match_inst_name_to_inst(self, name, instances):
		matching_inst = None
		for inst in instances:
			if name == inst.name:
				matching_inst = inst
		return matching_inst

	def set_instance_attributes(
			self, tier_class, get_inst_attr, fields_to_exclude):
		'''
		This func loops through airtable fields, assuming the class attribute
		tier_class.fields has been set (get_airtable_tier_tree), and 
		forces instances to fill in these fields with instance attributes.
		It also sets up any other instance attribute defaults desired, such
		as is_root.
		Args:
			tier_class: class object of the tier instance being created
			get_inst_attr: func that takes in the field (as a str) 
				and Tier_Instance_Class as args. It must return the 
				value of the attribute.
			fields_to_exclude: a list of strs with the name of an airtable
				field that you do not want set as an instance attribute here
		Returns: a dict of attributes with set values for each field in the 
			airtable. To actually set instance attrs, use the returned val
			here to do inst = Tier_Tree(instance_attributes) when constructing.
		'''
		instance_attributes = {
			'airtable_attributes' : {}, 'other_attributes' : {}
		}
		#XXX
		# Prints and shows CLASS attributes... we want to set each instance to
		# have set an instance property for every column represented by the
		# class attribute names of columns
		for property, value in vars(tier_class).items():
			self.log.info('\n prop: {}, value: {}'.format(property, value))

		# loop through class fields and set the instance attribute
		for field in tier_class.fields:
			if field not in fields_to_exclude:
				attr_val = get_inst_attr(tier_class, field)
				instance_attributes['airtable_attributes'][field] = attr_val
				#instance_attributes[field] = attr_val

		# Set is_root instance attribute to default to False
		instance_attributes['other_attributes']['is_root'] = False

		return instance_attributes

	def get_fields_to_exclude(self, Tier_Instance_Class):
		'''
		Args: a class obj of the tier instance's desired class, ex: Main Goals
			obj
		Returns: a tuple with two lists of strings. The first is a 
			tier_class's given fields that contain the word connection 
			and can be used as a fields_to_exclude param. The second is a list
			of field (strs) that do not contain "connection".
		'''
		fields_to_exclude = []
		fields = Tier_Instance_Class.fields
		for field in fields:
			if "Connection" in field or "connection" in field:
				fields_to_exclude.append(field)

		# Hierarchy_Level gets automatically set by class and should be excluded
		fields_to_exclude.append("Hierarchy Level")

		return fields_to_exclude 

	def display_instances_and_props(self, instances):

		self.log.info('Instances: {} \n'.format(instances))
		self.log.info('Instance options: \n')
		for instance in instances:
			self.log.info('Instance: {} \n'.format(instance.name))
			self.log.info('Instance properties: {} \n'.format(instance.__dict__))


	#XXX maybe instead of making another global datatype to be passed around,
	# you could just make it so the table whch the instance belongs to is one
	# of it's class properties.... then you could do instance.__class__.table
	# and it would be much cleaner
	def get_instance_dict(self, instances, all_tables):
		'''
		Returns a dict with keys as the table which the instances belong to
		and values being a list of instances to go in the table.
		Ex: instance_dict = 
			{<Airtable Main Quests> : [<tier_tree.Main Quests object at 0x142>]}
		'''

		instance_dict = {}
		for instance in instances:
			inst_table = instance.__class__.name
			for tables_list in all_tables.values():
				for table_name, airtable in tables_list:
					if inst_table == table_name:
						instance_dict[airtable] = instance

		return instance_dict




	


