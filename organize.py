# vim: set sw=4 noet ts=4 fileencoding=utf-8:

rows = []
columns = []
row_titles = []
column_titles = []

def setup_parameters():
    parameters = {}
    n_tiers = input("Combien de tieres a ta structure?")
    parameters["n_tiers"] = n_tiers
    return parameters

# For each level of goal tiers, ask for the name of the tier. For example,
# there may be two tiers, one named "Goals" and another named "Tasks"
def setup_goal_tiers(n_tiers):

    for tier in n_tiers:
        tier_name = input("\nQu'est-ce que s'appelle de cette tier? 
            Par example, il peut-etre s'appelle 'Des Objectifs'.")
        row_titles.append(tier_name)

# This function is called when __init__ is called because it is set as class 
# attribute function for __init__. Thus, arguments passed here will get set.
#XXX may want to make able to pass multiple args
def class_contructor(arg):
	self.constructor_arg = arg
	
def create_tier_class():
	# Garbage in, garbage out. Guard the perimeter then forget about it
	# Must be string
	name = input("What is the name of this tier class?")
	# Must be int
	hierarchy_level = input("What is the hierarchy level of this tier?")

	# Dynamically create class based on user input
	# type(
		# class_name, 
		# base / inheritance, 
		# attributes (in the form of a dictionary)
		# )
	#XXX Base of type Tier??
	New_Tier_Class = type(
		name, 
		(object,), 
		{
			"__init__" : class_constructor,
			name: name,
			hierarchy_level: hierarchy_level,
		}
	)
	return New_Tier_Class

def setup_tier_tree(n_tier_classes):
	# Hierarchy level 0 is the top of the tree / most important/broad level
	# Ex: [{0: [type("Main_Goals", (object,), {attributes...})] 
	# ... other tiers}]
	tier_tree = []
	for tier in n_tier_classes:
		New_Tier_Class = create_tier_class()
		h_level = New_Tier_Class.hierarchy_level
		# If no hierarchy dict exists in tier_tree, create one for the class's 
		# hierarchy level. If exists, append to it.
		try:
			# If a dict of the hierarchy_level already exists, append the class
			hierarchy_dict = tier_tree[h_level]
			hierarchy_dict[h_level].append(New_Tier_Class)

		except IndexError:
			# Create hierarchy_level dict
			hierarchy_dict = {}
			hierarchy_dict[h_level] = New_Tier_Class
			# Append to tier_tree
			tier_tree.append(hierarchy_dict)
	return tier_tree



