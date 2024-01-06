# -*- coding: utf-8 -*-

import argparse
parser =  argparse.ArgumentParser(description='Script to fix characters in WordPress after upgrading MySQL 5.x to 8.x.')
parser.add_argument('--convert_tables', type=str, help='Converts to InnoDB if tables are MyISAM. Needs 1 as argument.')
parser.add_argument('--backup', type=str, help='Creates a backup on the user directory. Needs 1 as argument.')
args = parser.parse_args()
convert_tables = args.convert_tables
backup = args.backup

import subprocess

def backup_database():
	backup_command = '''wp db export ~/backup`date +"%m-%d-%Y-%T"`.sql'''
	backup_run = subprocess.Popen(backup_command, shell=True, stdout=subprocess.PIPE)
	backup_output = backup_run.communicate()[0].decode('utf-8').strip()
	print(f'{backup_output}')
	backup_run.stdout.close()

if backup == '1':
	backup_database()

def convert_to_innodb():

	query = '''wp db query "SHOW TABLE STATUS WHERE Engine = 'MyISAM';" --silent --skip-column-names| awk '{ print $1}' '''


	check_myisam = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE)
	tables_to_convert = check_myisam.communicate()[0].decode('utf-8').strip()
	try:
		for table in tables_to_convert.split():
			print(f'Converting {table} to InnoDB')
			convert = f'wp db query "ALTER TABLE {table} ENGINE=InnoDB"'
			convert_process = subprocess.Popen(convert, shell=True, stdout=subprocess.PIPE)
			print(f'Process completed for {table}\n')
			convert_process.stdout.close()
	except Exception as e:
		print(f'Error converting: {e}')

	check_myisam.stdout.close()



if convert_tables == '1':
	convert_to_innodb()

import os
path = "SQLfix"
try:
	os.mkdir(f'./{path}', mode=0o777)
	print(f"Created directory as {path}")
except:
	print("Directory already exists")
	exit()

os.chdir(path)

import subprocess

wordpress_prefix = subprocess.Popen(['wp', 'config', 'get', 'table_prefix'], stdout=subprocess.PIPE)
prefix = wordpress_prefix.communicate()[0].decode('utf-8').strip()

print(f"The WordPress Prefix is {prefix}")
wordpress_prefix.stdout.close()

tables = ['comments','postmeta','posts','terms']
posts_values = ['post_excerpt', 'post_content', 'post_title']

file_name = f'{prefix}SQL8fix.sql'
with open(file_name, 'w') as file_fix:
	for table in tables:	
		if table == "comments":
			table_value = "comment_content"
			file_fix.write(f"update {prefix}{table} set {table_value} = CONVERT(CAST(CONVERT({table_value} USING latin1) AS BINARY) USING utf8);\n")
		elif table == "postmeta":
			table_value = "meta_value"
			file_fix.write(f"update {prefix}{table} set {table_value} = CONVERT(CAST(CONVERT({table_value} USING latin1) AS BINARY) USING utf8);\n")
		elif table == "terms":
			table_value = "name"
			file_fix.write(f"update {prefix}{table} set {table_value} = CONVERT(CAST(CONVERT({table_value} USING latin1) AS BINARY) USING utf8);\n")
		elif table == "posts":
			for table_value in posts_values:
				file_fix.write(f"update {prefix}{table} set {table_value} = CONVERT(CAST(CONVERT({table_value} USING latin1) AS BINARY) USING utf8);\n")
	print(f"File created as {file_name} \n Running import")
	
run_import = subprocess.Popen(['wp', 'db', 'import', file_name], stdout=subprocess.PIPE)
import_check = run_import.communicate()[0].decode('utf-8').strip()
if import_check == f"Success: Imported from '{file_name}'.":
	print(f'{import_check}\n')
else:
	print(f"Could not import file. Don't ask me, I'm a script. \nError: \n {import_check}")
	exit()
run_import.stdout.close()
import time
time.sleep(2)
print('Updating DB_CHARSET')
update_dbcharset = subprocess.Popen(['wp', 'config', 'set', 'DB_CHARSET', 'utf8'], stdout=subprocess.DEVNULL)

print('Done.')
