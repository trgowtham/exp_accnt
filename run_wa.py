#!/usr/bin/python3
import csv
import re
import sys
from process_wa import load_input_file, process_stage1, process_stage2, process_stage3

if len(sys.argv) != 2:
	print("Give input file argument")
	sys.exit(0)

# Define the input and output file names
input_file_name = sys.argv[1]
output_file_name = "xl-" + input_file_name.replace('.txt', '.csv')

# Define the CSV header
csv_header = ['Date', 'Name', 'Person', 'Amount', 'Type']

# Main
process_inp = []
load_input_file( input_file_name, process_inp )

# Stage 1
# From [10/2/24, 7:02:37 PM] Mythri: Maids 2500, 3200
# To list ['10/2/24', 'Maids 2500, 3200']
process_stg1 = []
process_stage1( process_inp, process_stg1 )

# Stage 2
# From ['10/2/24', 'Maids 2500, 3200']
# To 02/10/24,Maids,self,2500,cash
#    02/10/24,Maids,self,3200,cash
process_stg2 = []
process_stage2(process_stg1, process_stg2)

# Summary
total=0
white=0
amma=0
for ln in process_stg2:
	if ln[2] == 'not-self':
		amma = amma + int(ln[3])
	if ln[4] == 'card':
		white = white + int(ln[3])
	total = total + int(ln[3])

# Write the output CSV file
with open(output_file_name, 'w', newline='') as output_file:
	# Create a CSV writer
	csv_writer = csv.writer(output_file)

	# Write the CSV header
	csv_writer.writerow(csv_header)
	csv_writer.writerows(process_stg2)

tsv_file_name="xl-" + input_file_name.replace('.txt', '.tsv')
process_stage3(process_stg2, tsv_file_name)

print(f'''{input_file_name} Total {total} White {white} Amma {amma}''')
