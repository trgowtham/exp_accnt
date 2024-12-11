#!/usr/bin/python3
import csv
import re
import sys
import os

DEBUG=0

def load_input_file( input_file_name, input_lst ):
	# Open the input file and read it line by line
	with open(input_file_name, 'r') as input_file:
		for line in input_file:
			line = line.strip()
			input_lst.append(line)

def process_stage1( input_lst, process_stg1 ):
	skipped_lines = 0
	previous_date = None
	for line in input_lst:
		line = line.strip()
		# Check if the line contains a date
		if '[' in line and ']' in line:
			# Extract the date from the line
			date = line.split('[')[1].split(']')[0].split(',')[0]
			previous_date = date
		else:
			# Use the previous date if no date is found in the line
			if previous_date is None:
				print(f"Warning: No date found in line and no previous date available. Line: {line}")		
				date = "01/01/24"
			date = previous_date
		# Skip lines that do not contain any numbers
		skip_line_check = line.split(':')[-1]
		if not any(char.isdigit() for char in skip_line_check):
			#print(f"Skipping line: {line}")
			skipped_lines += 1
			continue
	
		process_stg1.append([date,skip_line_check.strip()])

	if DEBUG:
		print(f"\nSkipped {skipped_lines} lines.")

def process_stage2( input_list, output_list ):
	processed_lines = 0
	error_lines = 0
	for line in input_list:
		#print(f"{' '.join(line)} => ", end = " ")
		processed_lines += 1
		data = line[1].strip()
		datas = data.split(' ')
		datastr = ""
		dataval = ""
		datactr = 0
		old_datastr = ""
		exp_type = ""
		exp_home = ""
		line_added = 0
		exp_line_added = 0
		for ds in datas:
			datactr += 1
			if not any(char.isdigit() for char in ds):
				if ds == "W" or ds == "w":
					exp_type = "card"
				elif ds == "A" or ds == "a":
					exp_home = "not-self"
				elif datastr == "":
					datastr = ds
				else:
					# multi-word expense str "Eg: Blink it"
					datastr = datastr + " " + ds
			else:
				if datastr == "" and ds.isalpha():
					datastr = ds
					continue
				ds = ds.replace(',','')
				if 'W' in ds or 'w' in ds:
					ds = ds.replace('W','')
					ds = ds.replace('w','')
					exp_type = "card"
				else:
					if exp_type == "":
						exp_type = "cash"

				if 'A' in ds or 'a' in ds:
					ds = ds.replace('A','')
					ds = ds.replace('a','')
					exp_home = "not-self"
				else:
					if exp_home == "":
						exp_home = "self"
				#print(f"{[line[0],datastr, ds, exp_home, exp_type]}")
				dataval = ds
				if datactr == len(datas)-1:
					if datas[-1] == "W" or datas[-1] == "w":
						exp_type = "card"
					elif datas[-1] == "A" or datas[-1] == "a":
						exp_home = "not-self"
				if dataval and datastr:
					output_list.append([line[0],datastr.strip(), exp_home, dataval, exp_type])
					old_datastr = datastr
					line_added += 1
				elif not datastr:
					if old_datastr:
						output_list.append([line[0], old_datastr.strip(), exp_home, dataval, exp_type])
						old_datastr = ""
						line_added += 1
					elif datactr == len(datas)-1 and datas[-1].isalpha():
						output_list.append([line[0], datas[-1].strip(), exp_home, dataval, exp_type])
						line_added += 1
				
				datastr = ""
				dataval = ""
				exp_home = ""
				exp_type = ""
		exp_line_added = len([word for word in line[1].split() if re.search(r'\d', word)])
		if line and line_added != exp_line_added:
			print(f"ERROR: {line} expected to add {exp_line_added} but added {line_added}")
			error_lines += 1

	if DEBUG:
		print(f"Processed {processed_lines} lines.")
		print(f"Errored {error_lines} lines.")

tsv_category = [
"Misc", # 0
"Food", # 1
"Grocery", # 2
"Shopping", # 3
"Lifestyle", # 4
"Travel", # 5
"Health", # 6
"Utility", # 7
"Education", # 8
"Gift", # 9
]
catStr = "1:Food, 2:Grocery, 3:Shopping, 4:Lifestyle, 5:Travel, 6:Health, 7:Utility, 8:Education, 9:Gift, 0:Misc(Default)"

def stage3_category( cat_dict, csv_data ):
	# GTT
	csv_cat = csv_data.lower()
	processed_cat = 0
	if csv_cat not in cat_dict.keys():
		print(f"Processing => \"{csv_data}\"")
		print(catStr)
		var = input("Please enter correct category: ")
		print("You entered: " + var)
		try:
			if not var or int(var) < 0 or int(var) > 9:
				processed_cat = 0
			else:
				processed_cat = int(var)
		except:
			processed_cat = 0
	else:
		processed_cat = cat_dict[csv_cat][0]

	print(f"Processed category \"{csv_data}\" as {processed_cat}:{tsv_category[processed_cat]}")
	if csv_cat in cat_dict.keys():
		if cat_dict[csv_cat][0] == processed_cat:
			cat_dict[csv_cat][1] += 1
		else:
			cat_dict[csv_cat][0] = processed_cat
			cat_dict[csv_cat][1] = 0
	else:
		cat_dict[csv_cat] = [ processed_cat, 0 ]
	return tsv_category[processed_cat]

tsv_header = [
"Date", # 0
"Account", # 1
"Category", # 2
"Subcategory", # 3
"Note", # 4
"INR", # 5
"Income/Expense", # 6
"Description", # 7
"Amount", # 8
"Currency", # 9
"Account" # 10
]

def process_stage3( input_list, tsv_file_name ):
	output_list = []

	# Open the dict file and load the map
	# { "category" : [ <category_id> , <category_freq> ]
	cat_dict = {}
	cat_filename = "cat_dist.map"
	if os.path.exists( cat_filename ):
		with open( cat_filename, 'r') as cat_file:
			for line in cat_file:
				line = line.strip()
				ln = line.split(',')
				if len(ln) == 3:
					cat_dict[ ln[0] ] = [ int(ln[1]), int(ln[2]) ]

	for ln in input_list:
		op_ln = ["","","","","","","","","","",""]
		op_ln[0] = ln[0]
		op_ln[1] = ln[2] + "-" + ln[4] # "self-cash" Account
		op_ln[2] = stage3_category( cat_dict, ln[1] ) # "Misc" Category
		op_ln[3] = ""
		op_ln[4] = ln[1].replace(' ', '-')
		op_ln[5] = ln[3]
		op_ln[6] = "Expense" #Income/Expense
		op_ln[7] = "" #Description
		op_ln[8] = ln[3] #Amount
		op_ln[9] = "INR"
		op_ln[10] = ln[3]
		output_list.append( op_ln )

	with open( cat_filename, 'w') as cat_file:
		for k in cat_dict.keys():
			cat_file.write(f"{k},{cat_dict[k][0]},{cat_dict[k][1]}\n")
		
	# Write the output CSV file
	with open( tsv_file_name, 'w', newline='' ) as output_file:
		# Create a TSV writer
		tsv_writer = csv.writer( output_file, delimiter='\t', lineterminator='\n' )

		# Write the TSV header
		tsv_writer.writerow( tsv_header )
		tsv_writer.writerows( output_list )
