import os
import subprocess
path = "SQLfix"
try:
	os.mkdir(f'./{path}', mode=0o777)
except:
	print("Directory already exists")
	exit()

os.chdir(path)

tables = ['comments','postmeta','posts','terms']
posts_values = ['post_excerpt', 'post_content', 'post_title']
prefix = "wpimportant_"
character_to_replace = ['\'â€\', \'"\'', '\'â€“\', \'–\'', '\'â€¢\', \'-\'', '\'â€œ\', \'\"\'', '\'Â¡\', \'¡\'', '\'Â¢\', \'¢\'', '\'Â£\', \'£\'', '\'Â¤\', \'¤\'', '\'Â¥\', \'¥\'', '\'Â¦\', \'¦\'', '\'Â§\', \'§\'', '\'Â¨\', \'¨\'', '\'Â©\', \'©\'', '\'Âª\', \'ª\'', '\'Â«\', \'«\'', '\'Â¬\', \'¬\'', '\'Â\', \'\'', '\'Â®\', \'®\'', '\'Â¯\', \'¯\'', '\'Â°\', \'°\'', '\'Â±\', \'±\'', '\'Â²\', \'²\'', '\'Â³\', \'³\'', '\'Â´\', \'´\'', '\'Âµ\', \'µ\'', '\'Â¶\', \'¶\'', '\'Â·\', \'·\'', '\'Â¸\', \'¸\'', '\'Â¹\', \'¹\'', '\'Âº\', \'º\'', '\'Â»\', \'»\'', '\'Â¼\', \'¼\'', '\'Â½\', \'½\'', '\'Â¾\', \'¾\'', '\'Â¿\', \'¿\'', '\'Ã€\', \'À\'', '\'Ã\', \'Á\'', '\'Ã‚\', \'Â\'', '\'Ãƒ\', \'Ã\'', '\'Ã„\', \'Ä\'', '\'Ã…\', \'Å\'', '\'Ã†\', \'Æ\'', '\'Ã‡\', \'Ç\'', '\'Ãˆ\', \'È\'', '\'Ã‰\', \'É\'', '\'ÃŠ\', \'Ê\'', '\'Ã‹\', \'Ë\'', '\'ÃŒ\', \'Ì\'', '\'Ã\', \'Í\'', '\'ÃŽ\', \'Î\'', '\'Ã\', \'Ï\'', '\'Ã\', \'Ð\'', '\'Ã‘\', \'Ñ\'', '\'Ã’\', \'Ò\'', '\'Ã“\', \'Ó\'', '\'Ã”\', \'Ô\'', '\'Ã•\', \'Õ\'', '\'Ã–\', \'Ö\'', '\'Ã—\', \'×\'', '\'Ã˜\', \'Ø\'', '\'Ã™\', \'Ù\'', '\'Ãš\', \'Ú\'', '\'Ã›\', \'Û\'', '\'Ãœ\', \'Ü\'', '\'Ã\', \'Ý\'', '\'Ãž\', \'Þ\'', '\'ÃŸ\', \'ß\'', '\'Ã \', \'à\'', '\'Ã¡\', \'á\'', '\'Ã¢\', \'â\'', '\'Ã£\', \'ã\'', '\'Ã¤\', \'ä\'', '\'Ã¥\', \'å\'', '\'Ã¦\', \'æ\'', '\'Ã§\', \'ç\'', '\'Ã¨\', \'è\'', '\'Ã©\', \'é\'', '\'Ãª\', \'ê\'', '\'Ã«\', \'ë\'', '\'Ã¬\', \'ì\'', '\'Ã\', \'í\'', '\'Ã®\', \'î\'', '\'Ã¯\', \'ï\'', '\'Ã°\', \'ð\'', '\'Ã±\', \'ñ\'', '\'Ã²\', \'ò\'', '\'Ã³\', \'ó\'', '\'Ã´\', \'ô\'', '\'Ãµ\', \'õ\'', '\'Ã¶\', \'ö\'', '\'Ã·\', \'÷\'','\'Ã¸\', \'ø\'','\'Ã¹\', \'ù\'', '\'Ãº\', \'ú\'', '\'Ã»\', \'û\'','\'Ã¼\', \'ü\'', '\'Ã½\', \'ý\'', '\'Ã¾\', \'þ\'', '\'Ã¿\', \'ÿ\'']
for table in tables:
	table_value = ""
	if table == "comments":
		table_value = "comment_content"
		with open(f'{table}_fix.sql', 'w') as file_fix: 
			for character in character_to_replace:
				print(f"update {prefix}{table} set {table_value} replace({table_value}, {character});")
				file_fix.write(f"update {prefix}{table} set {table_value} replace({table_value}, {character});\n")
	elif table == "postmeta":
		table_value = "meta_value"
		with open(f'{table}_fix.sql', 'w') as file_fix: 
			for character in character_to_replace:
				print(f"update {prefix}{table} set {table_value} replace({table_value}, {character});")
				file_fix.write(f"update {prefix}{table} set {table_value} replace({table_value}, {character});\n")
	elif table == "terms":
		table_value = "name"
		with open(f'{table}_fix.sql', 'w') as file_fix: 
			for character in character_to_replace:
				print(f"update {prefix}{table} set {table_value} replace({table_value}, {character});")
				file_fix.write(f"update {prefix}{table} set {table_value} replace({table_value}, {character});\n")
	elif table == "posts":
		with open(f'{table}_fix.sql', 'w') as file_fix: 
			for post_value in posts_values:
				for character in character_to_replace:
					print(f"update {prefix}{table} set {post_value} replace({post_value}, {character});")
					file_fix.write(f"update {prefix}{table} set {post_value} replace({post_value}, {character});\n")