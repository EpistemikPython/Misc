###############################################################################################################################
# coding=utf-8
#
# impossible_problem.py
#
#  Copyright (c) 2026  Mark Sattolo  <epistemik@gmail.com>

__author__ = 'Mark Sattolo'
__author_email__ = 'epistemik@gmail.com'
__python_version__ = '3.6+'
__created__ = '2019-09-11'
__updated__ = '2026-01-16'

import operator
import sys
import json

"""
x and y are whole numbers each greater than 1, where y is greater than x, 
and the sum of the two is less than or equal to 100:
y > x > 1
x + y ≤ 100

Sam knows only the sum of the two numbers (x + y), while Pam knows only their product (x * y). 
The following conversation takes place between them.
Sam: 'I don’t know x and y, and I know that you don’t know them either.'
Pam: 'I now know x and y.'
Sam: 'I also now know x and y.'

The question: What are x and y?
"""

DEBUG_MODE = False
DEFAULT_MAX_SUM = 100
# dictionaries to store all the possible sums and products, each with possible (x,y)s
possible_sums = {}
possible_prods = {}

def num_count_items(p_dict:dict, p_count:int=0) -> int:
    num = 0
    for item in p_dict:
        if p_dict[item]['count'] > p_count:
            num += 1
    return num

def print_dict(p_dict:dict, p_label:str, p_op=operator.lt, p_count:int=2):
    count = 0
    for item in p_dict:
        key = p_dict[item]
        if p_op(key['count'] , p_count):
            print(f"{p_label} = {item};\tcount = {key['count']};\tx = {key['x']};\ty = {key['y']}")
            count += 1
    print(f"Have {count} {p_label} item{'' if count == 1 else 's'} with count {'<' if p_op(0,1) else '>'} {p_count}")

def get_possible_results(p_x:int, p_y:int):
    """
    for each x,y:
        calculate the sum then add this x,y to the list for that sum and keep a count of each x,y
        calculate the product then add this x,y to the list for that product and keep a count of each x,y
    """
    tr_sum = p_x + p_y
    sum_key = str(tr_sum)
    # keep the count
    if possible_sums.get(sum_key) is None:
        possible_sums[sum_key] = {}
        possible_sums[sum_key]['count'] = 1
    else:
        possible_sums[sum_key]['count'] += 1
    # record x
    if possible_sums[sum_key].get('x') is None:
        possible_sums[sum_key]['x'] = []
    possible_sums[sum_key]['x'].append(p_x)
    # record y
    if possible_sums[sum_key].get('y') is None:
        possible_sums[sum_key]['y'] = []
    possible_sums[sum_key]['y'].append(p_y)

    tr_prod = p_x * p_y
    prod_key = str(tr_prod)
    # keep the count
    if possible_prods.get(prod_key) is None:
        possible_prods[prod_key] = {}
        possible_prods[prod_key]['count'] = 1
    else:
        possible_prods[prod_key]['count'] += 1
    # record x
    if possible_prods[prod_key].get('x') is None:
        possible_prods[prod_key]['x'] = []
    possible_prods[prod_key]['x'].append(p_x)
    # record y
    if possible_prods[prod_key].get('y') is None:
        possible_prods[prod_key]['y'] = []
    possible_prods[prod_key]['y'].append(p_y)

    if DEBUG_MODE:
        print(f"x = {p_x}; y = {p_y}; sum = {tr_sum}; product = {tr_prod}")

def find_candidate_sums(p_sums:dict, p_prods:dict) -> list:
    """
    Sam: 'I don’t know x and y, and I know that you don’t know them either.'
    thus: find sums that result from at least two different x,y
          AND have ALL their products from multiple possible x,y
    :param p_sums: all sums
    :param p_prods: all products
    :return list of candidate sums
    """
    print("\nfind_candidate_sums()")
    sum_list = []
    sum_count = 0
    for isum in p_sums:
        print(f"Try sum {isum}")
        possible = True
        sdict = p_sums[isum]
        # for each sum with multiple possible x,y
        if sdict['count'] > 1:
            posn = 0
            # for each x in this sum
            for ix in sdict['x']:
                # get y
                iy = sdict['y'][posn]
                # get product
                nprod = ix * iy
                nprod_key = str(nprod)
                # check if this product has multiple possible x,y
                if p_prods[nprod_key]['count'] == 1:
                    possible = False
                    print(f"ONLY ONE x,y=({ix},{iy}) for PRODUCT {nprod_key}! Go to next sum!\n")
                    break
                posn += 1
            if not possible: continue
        else:
            print(f"ONLY ONE x,y for SUM {isum}! Go to next sum!\n")
            continue
        sum_count += 1
        sum_list.append(isum)
        print(f">> {isum} is a candidate sum!\n\n")

    return sum_list

def find_candidate_prods(p_cand_sums:list, p_poss_sums:dict) -> dict:
    """
    Pam: 'I now know x and y.'
    thus: find products that have only ONE of their possible (x,y)s giving a candidate sum
          so: from the candidate sums, take all the (x,y)s and find all the products
              >> candidate products will be those appearing in just ONE candidate sum
    :param p_cand_sums: list of candidate sums
    :param p_poss_sums: dict with possible sums
    :return dict of candidate products information
    """
    print("\nfind_candidate_prods()")
    cand_prods_dict = {}
    for isum in p_cand_sums:
        print(f"Try sum {isum}")
        poss_sum = p_poss_sums[isum]
        sposn = 0
        # for each possible x in this sum
        for sx in poss_sum['x']:
            # get y
            sy = poss_sum['y'][sposn]
            # get product
            nprod = sx * sy
            nprod_key = str(nprod)
            # keep the count
            if cand_prods_dict.get(nprod_key) is None:
                cand_prods_dict[nprod_key] = {}
                cand_prods_dict[nprod_key]['count'] = 1
            else:
                cand_prods_dict[nprod_key]['count'] += 1
            # record x
            if cand_prods_dict[nprod_key].get('x') is None:
                cand_prods_dict[nprod_key]['x'] = []
            cand_prods_dict[nprod_key]['x'].append(sx)
            # record y
            if cand_prods_dict[nprod_key].get('y') is None:
                cand_prods_dict[nprod_key]['y'] = []
            cand_prods_dict[nprod_key]['y'].append(sy)
            sposn += 1

    return cand_prods_dict

def get_solutions(p_cand_prods:dict) -> dict:
    """
    Sam: 'I also now know x and y.'
    thus: from the candidate products find all the sums and the (x,y)s they come from
          >> there should only be ONE sum with a single candidate product
             and the x,y of that sum/product is the solution
    :param p_cand_prods: dict of candidate products information
    :return dict of possible solutions
    """
    print("\nget_solutions()")
    xy_dict = {}
    for item in p_cand_prods:
        pdict = p_cand_prods[item]
        # only want the products with a unique x,y
        if pdict['count'] == 1:
            px = pdict['x'][0]
            py = pdict['y'][0]
            psum = px + py
            sum_key = str(psum)
            # keep the count
            if xy_dict.get(sum_key) is None:
                xy_dict[sum_key] = {}
                xy_dict[sum_key]['count'] = 1
            else:
                xy_dict[sum_key]['count'] += 1
            # record x
            if xy_dict[sum_key].get('x') is None:
                xy_dict[sum_key]['x'] = []
            xy_dict[sum_key]['x'].append(px)
            # record y
            if xy_dict[sum_key].get('y') is None:
                xy_dict[sum_key]['y'] = []
            xy_dict[sum_key]['y'].append(py)

    return xy_dict

def main_solve_problem(p_sum:int):
    """
    y > x > 1
    x + y <= maximum_sum
    """
    print(f"Max sum = {p_sum}")
    count = 0
    x1 = 2
    x2 = p_sum // 2
    # x = 2..49 for max sum of 100
    for x in range(x1, x2):
        y1 = x + 1
        y2 = p_sum - x + 1
        # y ranges = 3..98 (for x=2) to 50..51 (for x=49) if max sum of 100
        for y in range(y1, y2):
            get_possible_results(x, y)
            count += 1

    print(f"Number of possible x,y = {count}")
    if DEBUG_MODE:
        print(f"sums = \n{json.dumps(possible_sums, indent = 4)}\nproducts = \n{json.dumps(possible_prods, indent = 4)}\n")
    print(f"Number of sums having multiple (x,y)s = {num_count_items(possible_sums, 1)}")
    if DEBUG_MODE:
        print_dict(possible_sums, 'sum', p_op = operator.gt, p_count = 0)
    print(f"Number of products having multiple (x,y)s = {num_count_items(possible_prods, 1)}")
    if DEBUG_MODE:
        print_dict(possible_prods, 'prod', p_op = operator.gt, p_count = 0)

    candidate_sums = find_candidate_sums(possible_sums, possible_prods)
    print(f"\nNumber of candidate sums = {len(candidate_sums)}\nlist = {candidate_sums}")

    candidate_prods = find_candidate_prods(candidate_sums, possible_sums)
    print("\nCandidate products (only one x,y in the candidate sums):")
    print_dict(candidate_prods, 'prod')

    possible_solutions = get_solutions(candidate_prods)
    print("\nCandidate sums (with the (x,y)s from the candidate products):")
    print_dict(possible_solutions, 'sum', p_op = operator.gt, p_count = 0)
    print("\nPossible solutions:")
    print_dict(possible_solutions, 'sum')


if __name__ == '__main__':
    max_sum = DEFAULT_MAX_SUM
    if len(sys.argv) > 1 and sys.argv[1].isnumeric():
        max_sum = sys.argv[1]
    if len(sys.argv) > 2:
        DEBUG_MODE = True
    main_solve_problem(max_sum)
    print("\nPROGRAM ENDED.")
    exit()
