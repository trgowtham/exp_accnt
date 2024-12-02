#!/usr/bin/python3
import csv
import re
import sys

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

tsv_header = [ "Date","Account","Category","Subcategory","Note","INR","Income/Expense","Description","Amount","Currency","Account" ]

def process_stage3( input_list, tsv_file_name ):
	output_list = []
	for ln in input_list:
		op_ln = ["","","","","","","","","","",""]
		op_ln[0] = ln[0]
		op_ln[1] = "Self-cash" #Account
		op_ln[2] = "Misc" #Category
		op_ln[3] = ""
		op_ln[4] = ""
		op_ln[5] = ln[3]
		op_ln[6] = "Expense" #Income/Expense
		op_ln[7] = "" #Description
		op_ln[8] = ln[3] #Amount
		op_ln[9] = "INR"
		op_ln[10] = ln[3]
		output_list.append( op_ln )
		
	# Write the output CSV file
	with open( tsv_file_name, 'w', newline='' ) as output_file:
		# Create a TSV writer
		tsv_writer = csv.writer( output_file, delimiter='\t', lineterminator='\n' )

		# Write the TSV header
		tsv_writer.writerow( tsv_header )
		tsv_writer.writerows( output_list )
