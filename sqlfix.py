# -*- coding: utf-8 -*-
import sys

checking_version = str(sys.version_info.major) +'.'+ str(sys.version_info.minor)

if checking_version == '3.6' or checking_version > '3.5.9':
    print('Running Python version is %s' %(checking_version))
else:
    print('This script will not work on Python %s, please update before running' %(checking_version))
    exit()

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

character_to_replace = ['\'Î±\', \'α\'', '\'Î²\', \'β\'', '\'Î³\', \'γ\'', '\'Î´\', \'δ\'', '\'Îµ\', \'ε\'', '\'Î¶\', \'ζ\'', '\'Î·\', \'η\'', '\'Î¸\', \'θ\'', '\'Î¹\', \'ι\'', '\'Îº\', \'κ\'', '\'Î»\', \'λ\'', '\'Î¼\', \'μ\'', '\'Î½\', \'ν\'', '\'Î¾\', \'ξ\'', '\'Î¿\', \'ο\'', '\'Ï€\', \'π\'', '\'Ï\', \'ρ\'', '\'Ïƒ\', \'σ\'', '\'Ï„\', \'τ\'', '\'Ï…\', \'υ\'', '\'Ï†\', \'φ\'', '\'Ï‡\', \'χ\'', '\'Ïˆ\', \'ψ\'', '\'Ï‰\', \'ω\'', '\'Î‘\', \'Α\'', '\'Î’\', \'Β\'', '\'Î“\', \'Γ\'', '\'Î”\', \'Δ\'', '\'Î•\', \'Ε\'', '\'Î–\', \'Ζ\'', '\'Î—\', \'Η\'', '\'Î˜\', \'Θ\'', '\'Î™\', \'Ι\'', '\'Îš\', \'Κ\'', '\'Î›\', \'Λ\'', '\'Îœ\', \'Μ\'', '\'Î\', \'Ν\'', '\'Îž\', \'Ξ\'', '\'ÎŸ\', \'Ο\'', '\'Î \', \'Π\'', '\'Î¡\', \'Ρ\'', '\'Î£\', \'Σ\'', '\'Î¤\', \'Τ\'', '\'Î¥\', \'Υ\'', '\'Î¦\', \'Φ\'', '\'Î§\', \'Χ\'', '\'Î¨\', \'Ψ\'', '\'Î©\', \'Ω\'', '\'Î¬\', \'ά\'', '\'Î\', \'έ\'', '\'Î®\', \'ή\'', '\'Î¯\', \'ί\'', '\'ÏŒ\', \'ό\'', '\'Ï\', \'ύ\'', '\'ÏŽ\', \'ώ\'', '\'Î†\', \'Ά\'', '\'Îˆ\', \'Έ\'', '\'Î‰\', \'Ή\'', '\'ÎŠ\', \'Ί\'', '\'ÎŒ\', \'Ό\'', '\'ÎŽ\', \'Ύ\'', '\'Î\', \'Ώ\'', '\'Ï‹\', \'ϋ\'', '\'Î°\', \'υ\'', '\'ÏŠ\', \'ϊ\'', '\'Î\', \'ι\'', '\'Ï‚\', \'ς\'', '\'â€¦\', \'…\'', '\'â€™\', \'’\'', '\'àƒâ‚¬\', \'ä\'', '\'â€˜\', \'\'', '\'â€œ\', \'”\'', '\'â€�\', \'”\'', '\'â€¹\', \'‹\'', '\'â€º\', \'›\'', '\'â€”\', \'—\'', '\'â€“\', \'—\'', '\'â€?\', \'”\'', '\'àƒ’\', \'à\'', '\'â’€’™\', \'’\'', '\'â’€’œ\', \'“\'', '\'â’€?\', \'”\'', '\'àƒ’©\', \'é\'', '\'â’€’¦\', \'\'', '\'â€“\', \'•\'', '\'â‚¬\', \'€\'','\'â€\', \'"\'', '\'â€“\', \'–\'', '\'â€¢\', \'-\'', '\'â€œ\', \'"\'', '\'Â¡\', \'¡\'', '\'Â¢\', \'¢\'', '\'Â£\', \'£\'', '\'Â¤\', \'¤\'', '\'Â¥\', \'¥\'', '\'Â¦\', \'¦\'', '\'Â§\', \'§\'', '\'Â¨\', \'¨\'', '\'Â©\', \'©\'', '\'Âª\', \'ª\'', '\'Â«\', \'«\'', '\'Â¬\', \'¬\'', '\'Â\', \'\'', '\'Â®\', \'®\'', '\'Â¯\', \'¯\'', '\'Â°\', \'°\'', '\'Â±\', \'±\'', '\'Â²\', \'²\'', '\'Â³\', \'³\'', '\'Â´\', \'´\'', '\'Âµ\', \'µ\'', '\'Â¶\', \'¶\'', '\'Â·\', \'·\'', '\'Â¸\', \'¸\'', '\'Â¹\', \'¹\'', '\'Âº\', \'º\'', '\'Â»\', \'»\'', '\'Â¼\', \'¼\'', '\'Â½\', \'½\'', '\'Â¾\', \'¾\'', '\'Â¿\', \'¿\'', '\'Ã€\', \'À\'', '\'Ã\', \'Á\'', '\'Ã‚\', \'Â\'', '\'Ãƒ\', \'Ã\'', '\'Ã„\', \'Ä\'', '\'Ã…\', \'Å\'', '\'Ã†\', \'Æ\'', '\'Ã‡\', \'Ç\'', '\'Ãˆ\', \'È\'', '\'Ã‰\', \'É\'', '\'ÃŠ\', \'Ê\'', '\'Ã‹\', \'Ë\'', '\'ÃŒ\', \'Ì\'', '\'Ã\', \'Í\'', '\'ÃŽ\', \'Î\'', '\'Ã\', \'Ï\'', '\'Ã\', \'Ð\'', '\'Ã‘\', \'Ñ\'', '\'Ã’\', \'Ò\'', '\'Ã“\', \'Ó\'', '\'Ã”\', \'Ô\'', '\'Ã•\', \'Õ\'', '\'Ã–\', \'Ö\'', '\'Ã—\', \'×\'', '\'Ã˜\', \'Ø\'', '\'Ã™\', \'Ù\'', '\'Ãš\', \'Ú\'', '\'Ã›\', \'Û\'', '\'Ãœ\', \'Ü\'', '\'Ã\', \'Ý\'', '\'Ãž\', \'Þ\'', '\'ÃŸ\', \'ß\'', '\'Ã \', \'à\'', '\'Ã¡\', \'á\'', '\'Ã¢\', \'â\'', '\'Ã£\', \'ã\'', '\'Ã¤\', \'ä\'', '\'Ã¥\', \'å\'', '\'Ã¦\', \'æ\'', '\'Ã§\', \'ç\'', '\'Ã¨\', \'è\'', '\'Ã©\', \'é\'', '\'Ãª\', \'ê\'', '\'Ã«\', \'ë\'', '\'Ã¬\', \'ì\'', '\'Ã\', \'í\'', '\'Ã®\', \'î\'', '\'Ã¯\', \'ï\'', '\'Ã°\', \'ð\'', '\'Ã±\', \'ñ\'', '\'Ã²\', \'ò\'', '\'Ã³\', \'ó\'', '\'Ã´\', \'ô\'', '\'Ãµ\', \'õ\'', '\'Ã¶\', \'ö\'', '\'Ã·\', \'÷\'','\'Ã¸\', \'ø\'','\'Ã¹\', \'ù\'', '\'Ãº\', \'ú\'', '\'Ã»\', \'û\'','\'Ã¼\', \'ü\'', '\'Ã½\', \'ý\'', '\'Ã¾\', \'þ\'', '\'Ã¿\', \'ÿ\'', '\'Á©\', \'é\'', '\'Á³\', \'ó\'', '\'Á\', \'í\'', '\'í§\', \'ç\'', '\'í¡\', \'á\'', '\'íª\', \'ê\'', '\'í£\', \'ã\'', '\'íº\', \'ú\'']
file_name = f'{prefix}SQL8fix.sql'
with open(file_name, 'w') as file_fix:
	for table in tables:
		table_value = ""
		if table == "comments":
			table_value = "comment_content"
			for character in character_to_replace:
				file_fix.write(f"update {prefix}{table} set {table_value} = replace({table_value}, {character});\n")
		elif table == "postmeta":
			table_value = "meta_value"
			for character in character_to_replace:
				file_fix.write(f"update {prefix}{table} set {table_value} = replace({table_value}, {character});\n")
		elif table == "terms":
			table_value = "name"
			for character in character_to_replace:
				file_fix.write(f"update {prefix}{table} set {table_value} = replace({table_value}, {character});\n")
		elif table == "posts":
			for post_value in posts_values:
				for character in character_to_replace:
					file_fix.write(f"update {prefix}{table} set {post_value} = replace({post_value}, {character});\n")
	print(f"File created as {file_name} \n Running import")
run_import = subprocess.Popen(['wp', 'db', 'import', file_name], stdout=subprocess.PIPE)
import_check = run_import.communicate()[0].decode('utf-8').strip()
if import_check == f"Success: Imported from '{file_name}'.":
	print(f'{import_check}\n)
else:
	print(f"Could not import file. Don't ask me, I'm a script. \nError: \n {import_check}")
	exit()
run_import.stdout.close()
import time
time.sleep(2)
print('Updating DB_CHARSET')
update_dbcharset = subprocess.Popen(['wp', 'config', 'set', 'DB_CHARSET', 'utf8'], stdout=subprocess.DEVNULL)

print('Done.')
