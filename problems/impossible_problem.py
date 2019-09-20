##############################################################################################################################
# coding=utf-8
#
# impossible_problem.py
#
# Copyright (c) 2019 Mark Sattolo <epistemik@gmail.com>
#
__author__ = 'Mark Sattolo'
__author_email__ = 'epistemik@gmail.com'
__python_version__ = 3.6
__created__ = '2019-09-11'
__updated__ = '2019-09-20'

"""
x and y are whole numbers each greater than 1, where y is greater than x, 
and the sum of the two is less than or equal to 100:
y > x > 1
x + y ≤ 100

Sam knows only the sum of the two numbers (x + y), while Peter knows only their product (x * y). 
The following conversation takes place between them.
Sam: 'I don’t know x and y, and I know that you don’t know them either.'
Peter: 'I now know x and y.'
Sam: 'I also now know x and y.'
The question: What are x and y?
"""

import json

sums = {}
prods = {}


def tabulate_results(px,py):
	tr_sum = px + py
	sum_key = str(tr_sum)
	# keep the count
	if sums.get(sum_key) is None:
		sums[sum_key] = {}
		sums[sum_key]['count'] = 1
	else:
		sums[sum_key]['count'] += 1
	# record x
	if sums[sum_key].get('x') is None:
		sums[sum_key]['x'] = []
	sums[sum_key]['x'].append(px)
	# record y
	if sums[sum_key].get('y') is None:
		sums[sum_key]['y'] = []
	sums[sum_key]['y'].append(py)

	tr_prod = px * py
	prod_key = str(tr_prod)
	# keep the count
	if prods.get(prod_key) is None:
		prods[prod_key] = {}
		prods[prod_key]['count'] = 1
	else:
		prods[prod_key]['count'] += 1
	# record x
	if prods[prod_key].get('x') is None:
		prods[prod_key]['x'] = []
	prods[prod_key]['x'].append(px)
	# record y
	if prods[prod_key].get('y') is None:
		prods[prod_key]['y'] = []
	prods[prod_key]['y'].append(py)

	# print("x = {}; y = {}; sum = {}; prod = {}".format(x,y,sum,prod))
	return 1


# y > x > 1
# x + y <= 100
count = 0
for x in range(2,50):
	y1 = x + 1
	y2 = 100 - x + 1
	if y2 >= y1:
		for y in range(y1,y2):
			count += tabulate_results(x,y)

# print("count = {}\nsums = \n{}\nprods = \n{}\n".format(count, json.dumps(sums,indent=4), json.dumps(prods,indent=4)))

for item in sums:
	if sums[item]['count'] > 1:
		print("sum = {}; item = {}".format(item, json.dumps(sums[item],indent=4)))
		# print("sum {} has {} x,y tuples".format(item, sums[item]['count']))
print('\n')
for item in prods:
	if prods[item]['count'] > 1:
		pass
		print("prod = {}; item = {}".format(item, json.dumps(prods[item],indent=4)))
		# print("prod {} has {} x,y tuples".format(item, prods[item]['count']))
