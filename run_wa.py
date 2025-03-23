#!/usr/bin/python3
import csv
import re
import sys, os
from process_wa import load_input_file, process_stage1, process_stage2, process_stage3

if len(sys.argv) != 2:
	print("Give input file argument")
	sys.exit(0)

# Define the input and output file names
input_file_name = sys.argv[1]
file_name = os.path.basename(input_file_name)
csv_file_name = "csv/" + file_name.replace('.txt', '.csv')
tsv_file_name = "tsv/" + file_name.replace('.txt', '.tsv')
summary_file = "gen/" + file_name

# Define the CSV header
csv_header = [ 'Date', 'Account', 'Category', 'Description', 'Amount' ]

# Main
process_inp = []
load_input_file( input_file_name, process_inp )

# Stage 1
# From [10/2/24, 7:02:37 PM] Mythri: Maids 2500, 3200
# To list ['10/2/24', 'Maids 2500, 3200']
process_stg1 = []
process_stage1( process_inp, process_stg1, False)

# Stage 2
# From ['10/2/24', 'Maids 2500, 3200']
# To 02/10/24,Maids,self,2500,cash
#    02/10/24,Maids,self,3200,cash
process_stg2 = []
process_stage2(process_stg1, process_stg2)

# Stage 3
# Add category
# From CSV "02/02/25,Pan cake,self,372,cash"
# To TSV "02/02/25	self-cash	Food		Pan-cake	372	Expense		372	INR	372"
process_stg3 = []
process_stage3(process_stg2, process_stg3, tsv_file_name)

# All processing done. Just write summary files
# Write the data to CSV file
print( "Writing to", csv_file_name )
with open(csv_file_name, 'w', newline='') as output_file:
	# Create a CSV writer
	csv_writer = csv.writer(output_file)

	# Write the CSV header
	csv_writer.writerow(csv_header)
	csv_writer.writerows(process_stg3)

# Write monthly summary files
sum_dict = {}
sum_dict["self-cash"] = 0
sum_dict["self-card"] = 0
sum_dict["not-self-cash"] = 0
sum_dict["not-self-card"] = 0
for ln in process_stg3:
	if not ln[2] in sum_dict.keys():
		sum_dict[ln[2]] = {}
		sum_dict[ln[2]]["self-cash"] = 0
		sum_dict[ln[2]]["self-card"] = 0
		sum_dict[ln[2]]["not-self-cash"] = 0
		sum_dict[ln[2]]["not-self-card"] = 0

	sum_dict[ln[2]][ln[1]] += int(ln[4])
	sum_dict[ln[1]] += int(ln[4])

with open( summary_file, 'w') as sum_file:
	tot = {}
	tot[ "Total" ] = 0
	sum_file.write( f"Summary of {file_name}\n\n" )
	for k in sum_dict.keys():
		if not isinstance( sum_dict[k], dict ):
			sum_file.write( f"{k} : {sum_dict[k]}\n" )
			tot[ "Total" ]  += sum_dict[k]

	for k in sum_dict.keys():
		if isinstance( sum_dict[k], dict ):
			sum_file.write( "\n" )
			tot[ k ] = 0;
			for v in sum_dict[k].keys():
				sum_file.write(f"{k} - {v} : {sum_dict[k][v]}\n")
				tot[ k ] += sum_dict[k][v]

	sum_file.write( "\n" )
	for k in tot.keys():
		if k != "Total":
			sum_file.write( f"{k} : {tot[ k ]}\n" )
	sum_file.write( f"Total : {tot[ 'Total' ]}\n" )

# Write ALL summary file
total=0
white=0
amma=0
for ln in process_stg2:
	if ln[2] == 'not-self':
		amma = amma + int(ln[3])
	if ln[4] == 'card':
		white = white + int(ln[3])
	total = total + int(ln[3])

sum_line = f'Total {total} White {white} Amma {amma}'

all_sum = "gen/Summary.txt"
with open( all_sum, 'r' ) as f:
	lines = f.readlines()

upd_lines = []
found = False

for ln in lines:
	ln = ln.strip()
	month, val = ln.split( '-', 1 )
	month = month.strip()
	if month == file_name:
		upd_lines.append( f"{month} - {sum_line}\n")
		found = True
	else:
		upd_lines.append( ln + "\n" )

if not found:
	upd_lines.append( f"{file_name} - {sum_line}\n")

print( f"Updating {all_sum}" )
with open( all_sum, 'w' ) as f:
	f.writelines( upd_lines )

#print(sum_line)
