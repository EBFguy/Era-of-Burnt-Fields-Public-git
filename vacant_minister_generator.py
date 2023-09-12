from pathlib import Path
from argparse import ArgumentParser

def get_tags():
	tag_files = open(r'C:\Users\Marxivi\Documents\Paradox Interactive\Hearts of Iron IV\mod\era-of-burnt-fields-mod-git\common\country_tags\00_countries.txt', "r+")
	tags = []
	for line in tag_files:
		new_tag = line[:3]
		if "#" not in new_tag and "\n" not in new_tag:
			tags.append(new_tag)
	tags.sort()
	print(tags)
	print(len(tags))
	tag_files.close()
	return tags


def check_folder(find, folder_name: Path):
	found = False
	for filename in folder_name.iterdir():
		if check_file(find, filename):
			found = True
			break
	return found


def check_file(find, file: Path):
	found = False
	file = file.open(encoding="utf8")
	for line in file:
		if find in line:
			found = True
			break
	file.close()
	return found


def make_blank_chars(tags):
	output_file = open(r'C:\Users\Marxivi\Documents\Paradox Interactive\Hearts of Iron IV\mod\era-of-burnt-fields-mod-git\common\characters\_blank_characters.txt', "w+")
	output_file.write("characters = {\n")

	for tag in tags:
		if not check_folder(f'{tag}_Generic_Vacant_psi = {{', Path(r'C:\Users\Marxivi\Documents\Paradox Interactive\Hearts of Iron IV\mod\era-of-burnt-fields-mod-git\common\characters')):
			text = f"""
		{tag}_Generic_Vacant_psi = {{
			name = minister_Generic_Vacant
			portraits = {{
				civilian = {{ small = "GFX_idea_generic_minister_Vacant" }}
			}}
			advisor = {{
				slot = person_of_significant_influence
				idea_token = {tag}_Generic_Vacant_psi_min
				ledger = civilian
				cost = -1
				removal_cost = -1
				allowed = {{ original_tag = {tag} }}
				ai_will_do = {{ factor = 0 }}
			}}
		}}
  		{tag}_Generic_Vacant_pi_0 = {{
			name = minister_Generic_Vacant
			portraits = {{
				civilian = {{ small = "GFX_idea_generic_minister_Vacant" }}
			}}
			advisor = {{
				slot = person_of_influence
				idea_token = {tag}_Generic_Vacant_pi_0_min
				ledger = civilian
				cost = -1
				removal_cost = -1
				allowed = {{ original_tag = {tag} }}
				ai_will_do = {{ factor = 0 }}
			}}
		}}
  		{tag}_Generic_Vacant_pi_1 = {{
			name = minister_Generic_Vacant
			portraits = {{
				civilian = {{ small = "GFX_idea_generic_minister_Vacant" }}
			}}
			advisor = {{
				slot = person_of_influence
				idea_token = {tag}_Generic_Vacant_pi_1_min
				ledger = civilian
				cost = -1
				removal_cost = -1
				allowed = {{ original_tag = {tag} }}
				ai_will_do = {{ factor = 0 }}
			}}
		}}
  		{tag}_Generic_Vacant_pi_2 = {{
			name = minister_Generic_Vacant
			portraits = {{
				civilian = {{ small = "GFX_idea_generic_minister_Vacant" }}
			}}
			advisor = {{
				slot = person_of_influence
				idea_token = {tag}_Generic_Vacant_pi_2_min
				ledger = civilian
				cost = -1
				removal_cost = -1
				allowed = {{ original_tag = {tag} }}
				ai_will_do = {{ factor = 0 }}
			}}
		}}"""
			output_file.write(text)

	output_file.write("\n}")


def recruit_blank_chars(tags):
	history_folder = Path(r'C:\Users\Marxivi\Documents\Paradox Interactive\Hearts of Iron IV\mod\era-of-burnt-fields-mod-git\history\countries')
	for file in history_folder.iterdir():
		flag = False
		for tag in tags:
			text = f"""
# Vacant
recruit_character = {tag}_Generic_Vacant_psi
recruit_character = {tag}_Generic_Vacant_pi_0
recruit_character = {tag}_Generic_Vacant_pi_1
recruit_character = {tag}_Generic_Vacant_pi_2

fill_empty_minister_nochecks = yes # Please remove if you're adding ministers.
"""
			old_file = ""
			if tag == file.name[:3]:
				with file.open('r+', encoding="utf8") as history_file:
					for line in history_file:
						if "capital = " in line:
							old_file = line + text + old_file
						elif f"{tag}_Generic_Vacant_psi" not in line and "# Vacant\n" != line:
							old_file += line
				with file.open('w+', encoding="utf8") as history_file:
					history_file.write(old_file)
				flag = True
		if not flag:
			print(f"Extra History File: {file.name}")


def traits_to_text(traits):
	text = "\t\t\ttraits = {\n"
	for trait in traits:
		text += f'\t\t\t\t{trait}\n'
	text += "\t\t\t}\n"
	return text


def add_slots_as_traits():
	characters_folder = Path(r'C:\Users\Marxivi\Documents\Paradox Interactive\Hearts of Iron IV\mod\era-of-burnt-fields-mod-git\common\characters')
	for file in characters_folder.iterdir():
		if "_blank_characters" in file.name:
			break
		advisor = False
		scope_count = 0
		slot = ""
		traits = []
		trait_flag = False
		advisor_count = 0
		old_file = ""
		with file.open('r+', encoding="utf8") as characters_file:
			for line in characters_file:
				if advisor:
					for character in line:
						if character == '{':
							scope_count += 1
						if character == '}':
							scope_count -= 1
				if "advisor = " in line:
					advisor = True
					scope_count = 1
				if trait_flag:
					if '}' in line:
						trait_flag = False
						old_file += traits_to_text(traits)
					if slot != line.split('\t')[-1].rstrip('\n').strip():
						traits.append(line.split('\t')[-1].rstrip('\n').strip())
					continue
					advisor_count += 1
				if "slot = " in line and advisor:
					slot = line.split(' ')[-1].rstrip('\n')
				if "\ttraits = " in line and advisor:
					traits = [slot]
					for word in line.split('{')[1].split('}')[0].split(' '):
						if word.rstrip('\n') != "" and word.rstrip('\n') != slot:
							traits.append(word.rstrip('\n'))
					if '}' not in line:
						trait_flag = True
					else:
						old_file += traits_to_text(traits)
				else:
					old_file += line
				if scope_count == 0:
					advisor = False
		with file.open('w+', encoding="utf8") as characters_file:
			characters_file.write(old_file)


def add_trains_to_history():
	history_folder = Path(r'C:\Users\Marxivi\Documents\Paradox Interactive\Hearts of Iron IV\mod\era-of-burnt-fields-mod-git\history\countries')
	for file in history_folder.iterdir():
		flag = False
		old_file = ""
		with file.open('r+', encoding="utf8") as history_file:
			for line in history_file:
				old_file += line
				if "set_technology" in line and not flag:
					old_file += "\tbasic_train = 1\r\n"
					flag = True
		with file.open('w+', encoding="utf8") as history_file:
			history_file.write(old_file)


if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument('function', metavar='function', type=str, help='''The name of the function you want to run
	- 'make_blank_chars' recreates the _blank_characters.txt file with an empty person for every country that doesn't have one
	- 'recruit_blank_chars' adds the empty characters to the history file of countries
	- 'add_slots_as_traits' adds the slot of ministers as one of their traits, if it's missing
	- 'add_trains_to_history' choo choo, chugga chugga ''')
	args = parser.parse_args()
	taggerinos = get_tags()
	if args.function == 'make_blank_chars':
		make_blank_chars(taggerinos)
	elif args.function == 'recruit_blank_chars':
		recruit_blank_chars(taggerinos)
	elif args.function == 'add_slots_as_traits':
		add_slots_as_traits()
	elif args.function == 'add_trains_to_history':
		add_trains_to_history()
