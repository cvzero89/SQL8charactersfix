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

character_to_replace = ['\'â€\', \'"\'', '\'â€“\', \'–\'', '\'â€¢\', \'-\'', '\'â€œ\', \'\"\'', '\'Â¡\', \'¡\'', '\'Â¢\', \'¢\'', '\'Â£\', \'£\'', '\'Â¤\', \'¤\'', '\'Â¥\', \'¥\'', '\'Â¦\', \'¦\'', '\'Â§\', \'§\'', '\'Â¨\', \'¨\'', '\'Â©\', \'©\'', '\'Âª\', \'ª\'', '\'Â«\', \'«\'', '\'Â¬\', \'¬\'', '\'Â\', \'\'', '\'Â®\', \'®\'', '\'Â¯\', \'¯\'', '\'Â°\', \'°\'', '\'Â±\', \'±\'', '\'Â²\', \'²\'', '\'Â³\', \'³\'', '\'Â´\', \'´\'', '\'Âµ\', \'µ\'', '\'Â¶\', \'¶\'', '\'Â·\', \'·\'', '\'Â¸\', \'¸\'', '\'Â¹\', \'¹\'', '\'Âº\', \'º\'', '\'Â»\', \'»\'', '\'Â¼\', \'¼\'', '\'Â½\', \'½\'', '\'Â¾\', \'¾\'', '\'Â¿\', \'¿\'', '\'Ã€\', \'À\'', '\'Ã\', \'Á\'', '\'Ã‚\', \'Â\'', '\'Ãƒ\', \'Ã\'', '\'Ã„\', \'Ä\'', '\'Ã…\', \'Å\'', '\'Ã†\', \'Æ\'', '\'Ã‡\', \'Ç\'', '\'Ãˆ\', \'È\'', '\'Ã‰\', \'É\'', '\'ÃŠ\', \'Ê\'', '\'Ã‹\', \'Ë\'', '\'ÃŒ\', \'Ì\'', '\'Ã\', \'Í\'', '\'ÃŽ\', \'Î\'', '\'Ã\', \'Ï\'', '\'Ã\', \'Ð\'', '\'Ã‘\', \'Ñ\'', '\'Ã’\', \'Ò\'', '\'Ã“\', \'Ó\'', '\'Ã”\', \'Ô\'', '\'Ã•\', \'Õ\'', '\'Ã–\', \'Ö\'', '\'Ã—\', \'×\'', '\'Ã˜\', \'Ø\'', '\'Ã™\', \'Ù\'', '\'Ãš\', \'Ú\'', '\'Ã›\', \'Û\'', '\'Ãœ\', \'Ü\'', '\'Ã\', \'Ý\'', '\'Ãž\', \'Þ\'', '\'ÃŸ\', \'ß\'', '\'Ã \', \'à\'', '\'Ã¡\', \'á\'', '\'Ã¢\', \'â\'', '\'Ã£\', \'ã\'', '\'Ã¤\', \'ä\'', '\'Ã¥\', \'å\'', '\'Ã¦\', \'æ\'', '\'Ã§\', \'ç\'', '\'Ã¨\', \'è\'', '\'Ã©\', \'é\'', '\'Ãª\', \'ê\'', '\'Ã«\', \'ë\'', '\'Ã¬\', \'ì\'', '\'Ã\', \'í\'', '\'Ã®\', \'î\'', '\'Ã¯\', \'ï\'', '\'Ã°\', \'ð\'', '\'Ã±\', \'ñ\'', '\'Ã²\', \'ò\'', '\'Ã³\', \'ó\'', '\'Ã´\', \'ô\'', '\'Ãµ\', \'õ\'', '\'Ã¶\', \'ö\'', '\'Ã·\', \'÷\'','\'Ã¸\', \'ø\'','\'Ã¹\', \'ù\'', '\'Ãº\', \'ú\'', '\'Ã»\', \'û\'','\'Ã¼\', \'ü\'', '\'Ã½\', \'ý\'', '\'Ã¾\', \'þ\'', '\'Ã¿\', \'ÿ\'']
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
	print(import_check)
else:
	print(f"Could not import file. Don't ask me, I'm a script. \nError: \n {import_check}")
run_import.stdout.close()
