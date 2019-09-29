#  Copyright (c) 2019  Mark Sattolo   <epistemik@gmail.com>

###############################################################################################################################
# coding=utf-8
#
# impossible_problem.py
#
#
__author__ = 'Mark Sattolo'
__author_email__ = 'epistemik@gmail.com'
__python_version__ = 3.6
__created__ = '2019-09-11'
__updated__ = '2019-09-22'

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

    # print("x = {}; y = {}; sum = {}; prod = {}".format(x,y,sum,prod))


def find_possible_sums(p_sums:dict, p_prods:dict) -> list:
    """
    find sums which have ALL their prods with multiple possible x,y
    :param p_sums: all sums
    :param p_prods: all prods
    :return: list of possible sums
    """
    print("\nfind_possible_sums()")
    sum_list = []
    sum_count = 0
    for isum in p_sums:
        print("find_possible_sums() Trying sum {}".format(isum))
        possible = True
        sdict = p_sums[isum]
        # for each sum with multiple possible x,y
        if sdict['count'] > 1:
            posn = 0
            # for each possible x in this sum
            for ix in sdict['x']:
                # get y
                iy = sdict['y'][posn]
                # print("find_possible_sums() Trying x,y = {},{}".format(ix, iy))
                # get prod
                nprod = ix * iy
                nprod_key = str(nprod)
                # check if this prod has multiple possible x,y
                if p_prods[nprod_key]['count'] == 1:
                    possible = False
                    print("ONLY ONE Prod of {},{}! Go to next sum!\n".format(ix,iy))
                    break
                # print("Prod {} has multiple possible x,y ...".format(nprod_key))
                posn += 1
            if not possible: continue
        else:
            print("Sum {} has ONLY ONE possible x,y! Go to next sum!\n".format(isum))
            continue
        sum_count += 1
        sum_list.append(isum)
        print("*** Possible sum = {} ***\n\n".format(isum))

    print("\nNumber of possible sums = {}\nlist = {}".format(sum_count, sum_list))
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
        print("find_possible_prods() Trying sum {}".format(isum))
        sdict = p_sums[isum]
        sposn = 0
        # for each possible x in this sum
        for sx in sdict['x']:
            # get y
            sy = sdict['y'][sposn]
            # print("find_possible_prods() Trying x,y = {},{}".format(sx, sy))
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
            print("\n{} = {}\ncount = {}\nx = {}\ny = {}"
                  .format(p_label, item, key['count'], key['x'], key['y']))
    print('\n')


def print_dict_lt(p_dict:dict, p_label:str, p_count:int=10):
    count = 0
    for item in p_dict:
        key = p_dict[item]
        if key['count'] < p_count:
            print("{} = {};\tcount = {};\tx = {};\ty = {}"
                  .format(p_label, item, key['count'], key['x'], key['y']))
            count += 1
    print("Have {} {} items with count < {}".format(count, p_label, p_count))


def impossible_problem_main():
    """
    y > x > 1
    x + y <= 100
    """
    count = 0
    # x = 2..49
    for x in range(2, 50):
        y1 = x + 1
        y2 = 100 - x + 1
        # y = 3..98 to 50..51
        for y in range(y1, y2):
            tabulate_results(x, y)
            count += 1

    print("Number of possible x,y = {}".format(count))
    # print("count = {}\nsums = \n{}\nprods = \n{}\n".format(count, json.dumps(sums,indent=4), json.dumps(prods,indent=4)))
    print("Number of sums from multiple (x,y)s = {}".format(num_count_items(sums, 1)))
    # print_dict_gt(sums, 'sum')
    print("Number of prods from multiple (x,y)s = {}".format(num_count_items(prods, 1)))
    # print_dict_gt(prods, 'prod')

    sum_list = find_possible_sums(sums, prods)

    prod_list = find_possible_prods(sum_list, sums)
    print("\nPossible prods with a unique x,y:")
    print_dict_lt(prod_list, 'prod', p_count=2)

    answer_list = get_solution_xy(prod_list)
    print("\nPossible sums with the (x,y)s from the unique possible prods:")
    print_dict_gt(answer_list, 'sum')

    print("\nPROGRAM ENDED.")


if __name__ == '__main__':
    impossible_problem_main()
