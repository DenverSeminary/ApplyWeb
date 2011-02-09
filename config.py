from ConfigParser import SafeConfigParser

def get_config(section, value):
	parser = SafeConfigParser()
	parser.read('.conf')
	return parser.get(section, value)
	
