# vim: set sw=4 noet ts=4 fileencoding=utf-8:
import logging
import pdb

class Tier_Instance_Constructor():

	def __init__(self):
		self.log = self.setup_logger(logging.DEBUG)

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
			self.log.debug("i: {}".format(i))
			# Get all classes in each hierarchy level
			# NOTE that i is a key in the case of hierarchy_dict, not an index
			classes_list = hierarchy_dict[i]
			self.log.debug("hierarchy_dict[i]: {}".format(classes_list))
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
			of other tier_instances. 
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
			One node on the tree must be the root why / have no why 
			connections. This function sets a tier instance's attribute
			to reflect if it is the root.
		'''
		root_was_set = False
		if is_root:
			if tier_inst.hierarchy_level == 0:
				tier_inst.is_root = True
				root_was_set = True
			else:
				self.log.error("Root was not set b/c the root must be set " +\
					"at hierarchy level 0.")
		return root_was_set


