#!/usr/bin/python
import re, os, sys
import optparse

match_dbline = re.compile('^<(?P<dbsrctree>\w+)(((:)(?P<dbname>\w+))|())>(?P<sqlfile>.+)', re.I | re.M | re.X);

def execute_sql_file(dbname, tree, file, args):
	if tree == "mangos":
		exec_tree = "mangos"
	elif tree == "scriptdev2":
		exec_tree = "mangos/src/bindings/ScriptDev2" 
	elif tree == "acid":
		exec_tree = "sd2-acid"
	elif tree == "udb":
		exec_tree = "unifieddb"
	else:
		exec_tree = "."

	if dbname == None:
		dbname = ""
	else:
		dbname = " "+dbname

	execute_str = "mysql -u "+args.username+args.password+dbname+" < "+exec_tree+file
	if args.testing:
		print execute_str
	else:
		print "Executing: "+execute_str
		os.system(execute_str)

def get_sql_entries(db_install_list):
	queries = [] 
	buffer = db_install_list.readlines()
	for line in buffer:
		db_files = match_dbline.match(line)
		if db_files != None:
			queries.append( list(db_files.group('dbsrctree', 'dbname', 'sqlfile')) )
	return queries

def parse_password_callback(option, opt, value, parser):
		parser.values.password = " --password="+value

def parse_cmd_args():
	parser = optparse.OptionParser(version="%prog 1.0")
	
	parser.add_option("-t", "--test",
		action="store_true", dest="testing", default=True)
	parser.add_option("-x", "--exec", "--execute", 
		action="store_false", dest="testing", default=True)
	parser.add_option("--update", 
		action="store_true", dest="update")
	parser.add_option("-p", "--pass", "--password", 
		action="callback", type="string", callback=parse_password_callback, dest="password", default=" -p")
	parser.add_option("-u", "--user", "--username",
		action="store", dest="username", default="root")
	parser.add_option("--db", "--dbfile", 
		action="store", dest="filename", default="mangos.dbinst")

	(options, args) = parser.parse_args()
	return options

if __name__ == '__main__':
	my_args = parse_cmd_args()
	print my_args
	db_install_list = open(my_args.filename, 'rU')
	for query in get_sql_entries(db_install_list):
		execute_sql_file(query[1], query[0], query[2], my_args)

