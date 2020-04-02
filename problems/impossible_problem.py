#  Copyright (c) 2020  Mark Sattolo   <epistemik@gmail.com>

###############################################################################################################################
# coding=utf-8
#
# impossible_problem.py
#
__author__ = 'Mark Sattolo'
__author_email__ = 'epistemik@gmail.com'
__python_version__ = 3.6
__created__ = '2019-09-11'
__updated__ = '2019-09-22'

# import json

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

# dictionaries to store all the possible sums and prods and each possible x,y
sums = {}
prods = {}


def tabulate_results(p_x:int, p_y:int):
    """
    for x and y:
        calculate the sum then add this x,y to the list for that sum and keep a count of each x,y
        calculate the prod then add this x,y to the list for that prod and keep a count of each x,y
    """
    # print("\ntabulate_results()")
    tr_sum = p_x + p_y
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
    sums[sum_key]['x'].append(p_x)
    # record y
    if sums[sum_key].get('y') is None:
        sums[sum_key]['y'] = []
    sums[sum_key]['y'].append(p_y)

    tr_prod = p_x * p_y
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
    prods[prod_key]['x'].append(p_x)
    # record y
    if prods[prod_key].get('y') is None:
        prods[prod_key]['y'] = []
    prods[prod_key]['y'].append(p_y)

    # print(F"x = {p_x}; y = {p_y}; sum = {tr_sum}; prod = {tr_prod}")


def find_possible_sums(p_sums:dict, p_prods:dict) -> list:
    """
    Sam: 'I don’t know x and y, and I know that you don’t know them either.'
    thus: find sums that result from at least two different x,y
          AND have ALL their prods from multiple possible x,y
    :param p_sums: all sums
    :param p_prods: all prods
    :return: list of possible sums
    """
    print("\nfind_possible_sums()")
    sum_list = []
    sum_count = 0
    for isum in p_sums:
        print(F"Try sum {isum}")
        possible = True
        sdict = p_sums[isum]
        # for each sum with multiple possible x,y
        if sdict['count'] > 1:
            posn = 0
            # for each possible x in this sum
            for ix in sdict['x']:
                # get y
                iy = sdict['y'][posn]
                # print(F"find_possible_sums() Trying x,y = {ix},{iy}")
                # get prod
                nprod = ix * iy
                nprod_key = str(nprod)
                # check if this prod has multiple possible x,y
                if p_prods[nprod_key]['count'] == 1:
                    possible = False
                    print(F"ONLY ONE x,y=({ix},{iy}) for prod {nprod_key}! Go to next sum!\n")
                    break
                # print(F"Prod {nprod_key} has multiple possible x,y ...")
                posn += 1
            if not possible: continue
        else:
            print(F"ONLY ONE possible x,y for sum {isum}! Go to next sum!\n")
            continue
        sum_count += 1
        sum_list.append(isum)
        print(F">> {isum} is a possible sum!\n\n")

    print(F"\nNumber of possible sums = {sum_count}\nlist = {sum_list}")
    return sum_list


def find_possible_prods(p_poss_sums:list, p_sums:dict) -> dict:
    """
    from the possible sum list, take all the (x,y)s and find all the possible prods
    -- the solution prod can be any of the possible prods from a unique x,y
    :param p_poss_sums: possible sums
    :param p_sums: all sums
    """
    print("\nfind_possible_prods()")
    prod_list = {}
    for isum in p_poss_sums:
        print(F"Try sum {isum}")
        sdict = p_sums[isum]
        sposn = 0
        # for each possible x in this sum
        for sx in sdict['x']:
            # get y
            sy = sdict['y'][sposn]
            # print(F"find_possible_prods() Trying x,y = {sx},{sy}")
            # get prod
            nprod = sx * sy
            nprod_key = str(nprod)
            # keep the count
            if prod_list.get(nprod_key) is None:
                prod_list[nprod_key] = {}
                prod_list[nprod_key]['count'] = 1
            else:
                prod_list[nprod_key]['count'] += 1
            # record x
            if prod_list[nprod_key].get('x') is None:
                prod_list[nprod_key]['x'] = []
            prod_list[nprod_key]['x'].append(sx)
            # record y
            if prod_list[nprod_key].get('y') is None:
                prod_list[nprod_key]['y'] = []
            prod_list[nprod_key]['y'].append(sy)
            sposn += 1

    return prod_list


def get_solution_xy(p_poss_prods:dict) -> dict:
    """
    from the possible prod list find each prod that comes from a single x,y
    then find the sum and keep track of how many unique prods for each possible sum
    -> there should only be ONE sum with a single unique prod and the x,y of that sum is the solution
    :param p_poss_prods: possible prods
    """
    print("\nget_solution_xy()")
    xy_list = {}
    for item in p_poss_prods:
        # print("get_solution_xy() Trying prod {}".format(item))
        pdict = p_poss_prods[item]
        # only want the prods with a unique x,y
        if pdict['count'] == 1:
            px = pdict['x'][0]
            py = pdict['y'][0]
            psum = px + py
            sum_key = str(psum)
            # keep the count
            if xy_list.get(sum_key) is None:
                xy_list[sum_key] = {}
                xy_list[sum_key]['count'] = 1
            else:
                xy_list[sum_key]['count'] += 1
            # record x
            if xy_list[sum_key].get('x') is None:
                xy_list[sum_key]['x'] = []
            xy_list[sum_key]['x'].append(px)
            # record y
            if xy_list[sum_key].get('y') is None:
                xy_list[sum_key]['y'] = []
            xy_list[sum_key]['y'].append(py)

    return xy_list


def num_count_items(p_dict:dict, p_count:int=0) -> int:
    num = 0
    for item in p_dict:
        if p_dict[item]['count'] > p_count:
            num += 1
    return num


def print_dict_gt(p_dict:dict, p_label:str, p_count:int=0):
    for item in p_dict:
        key = p_dict[item]
        if key['count'] > p_count:
            print(F"\n{p_label} = {item}\ncount = {key['count']}\nx = {key['x']}\ny = {key['y']}")
    print('\n')


def print_dict_lt(p_dict:dict, p_label:str, p_count:int=10):
    count = 0
    for item in p_dict:
        key = p_dict[item]
        if key['count'] < p_count:
            print(F"{p_label} = {item};\tcount = {key['count']};\tx = {key['x']};\ty = {key['y']}")
            count += 1
    print(F"Have {count} {p_label} items with count < {p_count}")


def impossible_problem_main():
    """
    y > x > 1
    x + y <= 100
    """
    count = 0
    max_sum = 100
    x1 = 2
    x2 = max_sum // 2
    # x = 2..49
    for x in range(x1, x2):
        y1 = x + 1
        y2 = max_sum - x + 1
        # y = 3..98 to 50..51
        for y in range(y1, y2):
            tabulate_results(x, y)
            count += 1

    print(F"Max sum = {max_sum}")
    print(F"Number of possible x,y = {count}")
    # print(F"sums = \n{json.dumps(sums,indent=4)}\nprods = \n{json.dumps(prods,indent=4)}\n")
    print(F"Number of sums having multiple (x,y)s = {num_count_items(sums, 1)}")
    # print_dict_gt(sums, 'sum')
    print(F"Number of prods having multiple (x,y)s = {num_count_items(prods, 1)}")
    # print_dict_gt(prods, 'prod')

    sum_list = find_possible_sums(sums, prods)

    prod_list = find_possible_prods(sum_list, sums)
    print("\nPossible prods (have a unique x,y):")
    print_dict_lt(prod_list, 'prod', p_count=2)

    answer_list = get_solution_xy(prod_list)
    print("\nPossible sums with the (x,y)s from the unique possible prods:")
    print_dict_gt(answer_list, 'sum')
    print("\nPossible solutions:")
    print_dict_lt(answer_list, 'sum', p_count=2)

    print("\nPROGRAM ENDED.")


if __name__ == '__main__':
    impossible_problem_main()
    exit()
