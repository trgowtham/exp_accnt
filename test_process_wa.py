#!/usr/bin/python3

from process_wa import process_stage1, process_stage2
import sys

def test_data( teststr, input_str, exp_op):
	test_stg1 = []
	test_stg2 = []
	process_stage1( [input_str], test_stg1)
	process_stage2( test_stg1, test_stg2)
	if exp_op != test_stg2:
		print(f"{teststr} test fail ...")
		print(f"Expected {exp_op}. Read {test_stg2}")
	else:
		print(f"{teststr} test pass...")

inp_data = "[02/10/24, 7:02:14 PM] Mythri: Lego 4812"
test_op = [['02/10/24', 'Lego', 'self', '4812', 'cash']]
test_data( "Test 1", inp_data, test_op)

inp_data = "Mythri: Lego 4812"
test_op = [[None, 'Lego', 'self', '4812', 'cash']]
test_data( "Test 2", inp_data, test_op)

inp_data = "Lego W 4812"
test_op = [[None, 'Lego', 'self', '4812', 'card']]
test_data( "Test 3", inp_data, test_op)

inp_data = "Mythri: 4812 Lego"
test_op = [[None, 'Lego', 'self', '4812', 'cash']]
test_data( "Test 4", inp_data, test_op)

inp_data = "Mythri: Lego 4812 Pizza 1300"
test_op = [[None, 'Lego', 'self', '4812', 'cash'], [None, 'Pizza', 'self', '1300', 'cash']]
test_data( "Test 5", inp_data, test_op)

inp_data = "Gowtham : Lego 4812 Pizza 1300 Food W376"
test_op = [[None, 'Lego', 'self', '4812', 'cash'],
[None, 'Pizza', 'self', '1300', 'cash'],
[None, 'Food', 'self', '376', 'card'],
]
test_data( "Test 6", inp_data, test_op)

inp_data = "Mythri: Lego 4812 Pizza WA1300"
test_op = [[None, 'Lego', 'self', '4812', 'cash'], [None, 'Pizza', 'not-self', '1300', 'card']]
test_data( "Test 7", inp_data, test_op)

inp_data = "Mythri: Doctor dressing 285"
test_op = [[None, 'Doctor dressing', 'self', '285', 'cash']]
test_data( "Test 8", inp_data, test_op)

inp_data = "Mythri: Auto 163 W"
test_op = [[None, 'Auto', 'self', '163', 'card']]
test_data( "Test 9", inp_data, test_op)

inp_data = "[24/10/24, 7:42:22 PM] Gowtham: Auto W165 <This message was edited>"
test_op = [["24/10/24", 'Auto', 'self', '165', 'card']]
test_data( "Test 10", inp_data, test_op)

inp_data = "[17/10/24, 7:38:38 PM] Mythri: Birth day decor and return gifts 3100 1160W"
test_op = [["17/10/24", 'Birth day decor and return gifts', 'self', '3100', 'cash'],
["17/10/24", 'Birth day decor and return gifts', 'self', '1160', 'card']]
test_data( "Test 11", inp_data, test_op)

inp_data = "[24/10/24, 7:42:22 PM] Gowtham: W165 <This message was edited>"
test_op = []
test_data( "Test 12", inp_data, test_op)

inp_data = "[31/10/24, 9:34:42 AM] Gowtham: Blinkit 1225 A 275"
test_op = [["31/10/24", 'Blinkit', 'self', '1225', 'cash'], ["31/10/24", 'Blinkit', 'not-self', '275', 'cash']]
test_data( "Test 13", inp_data, test_op)
