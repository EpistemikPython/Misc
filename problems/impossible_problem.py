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
        calculate the sum then add this x,y to the list for that sum
        calculate the prod then add this x,y to the list for that prod
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


def find_sum_list(p_sums:dict, p_prods:dict) -> list:
    """
    find sums which have ALL their prods with multiple possible x,y
    :param p_sums: all sums
    :param p_prods: all prods
    :return: list of possible sums
    """
    print("\nfind_sum_list()")
    sum_list = []
    sum_count = 0
    for isum in p_sums:
        print("find_sum_list() Trying sum {}".format(isum))
        possible = True
        sdict = p_sums[isum]
        # for each sum with multiple possible x,y
        if sdict['count'] > 1:
            posn = 0
            # for each possible x in this sum
            for ix in sdict['x']:
                # get y
                iy = sdict['y'][posn]
                # print("find_sum_list() Trying x,y = {},{}".format(ix, iy))
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


def get_pairs_dict(p_poss_pairs:list, p_sums:dict) -> dict:
    """
    from the possible sum list, find a prod that has a matching sum with only ONE possible x,y
    :param p_poss_pairs: possible sums
    :param p_sums: all sums
    """
    print("\nget_pairs_dict()")
    pair_list = {}
    for isum in p_poss_pairs:
        print("get_pairs_dict() Trying sum {}".format(isum))
        sdict = p_sums[isum]
        sposn = 0
        # for each possible x in this sum
        for sx in sdict['x']:
            # get y
            sy = sdict['y'][sposn]
            # print("get_pairs_dict() Trying x,y = {},{}".format(sx, sy))
            # get prod
            nprod = sx * sy
            nprod_key = str(nprod)
            # keep the count
            if pair_list.get(nprod_key) is None:
                pair_list[nprod_key] = {}
                pair_list[nprod_key]['count'] = 1
            else:
                pair_list[nprod_key]['count'] += 1
            # record x
            if pair_list[nprod_key].get('x') is None:
                pair_list[nprod_key]['x'] = []
            pair_list[nprod_key]['x'].append(sx)
            # record y
            if pair_list[nprod_key].get('y') is None:
                pair_list[nprod_key]['y'] = []
            pair_list[nprod_key]['y'].append(sy)
            sposn += 1

    # print("\nPair list = {}".format(pair_list))
    return pair_list


def get_answer_pair(p_poss_prods:dict) -> dict:
    """
    from the possible prod list, find a sum with a unique prod
    :param p_poss_prods: possible prods
    """
    print("\nget_answer_pair()")
    pair_list = {}
    for item in p_poss_prods:
        # print("get_answer_pair() Trying prod {}".format(item))
        pdict = p_poss_prods[item]
        if pdict['count'] == 1:
            px = pdict['x'][0]
            py = pdict['y'][0]
            psum = px + py
            sum_key = str(psum)
            # keep the count
            if pair_list.get(sum_key) is None:
                pair_list[sum_key] = {}
                pair_list[sum_key]['count'] = 1
            else:
                pair_list[sum_key]['count'] += 1
            # record x
            if pair_list[sum_key].get('x') is None:
                pair_list[sum_key]['x'] = []
            pair_list[sum_key]['x'].append(px)
            # record y
            if pair_list[sum_key].get('y') is None:
                pair_list[sum_key]['y'] = []
            pair_list[sum_key]['y'].append(py)

    # print("\nPair list = {}".format(pair_list))
    return pair_list


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
            print("{} = {}\ncount = {}\nx = {}\ny = {}"
                  .format(p_label, item, key['count'], key['x'], key['y']))
    print('\n')


def print_dict_lt(p_dict:dict, p_label:str, p_count:int=10):
    count = 0
    for item in p_dict:
        key = p_dict[item]
        if key['count'] < p_count:
            print("{} = {}\ncount = {}\nx = {}\ny = {}"
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
    print("Number of multi-sums = {}".format(num_count_items(sums, 1)))
    # print_dict_gt(sums, 'sum')
    print("Number of multi-prods = {}".format(num_count_items(prods, 1)))
    # print_dict_gt(prods, 'prod')

    asum_list = find_sum_list(sums, prods)

    apair_list = get_pairs_dict(asum_list, sums)
    # print_dict_lt(apair_list, 'prod', p_count=2)
    answer_list = get_answer_pair(apair_list)
    print_dict_gt(answer_list, 'sum')

    print("\nPROGRAM ENDED.")


if __name__ == '__main__':
    impossible_problem_main()
