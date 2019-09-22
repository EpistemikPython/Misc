#  Copyright (c) 2019  Mark Sattolo   <epistemik@gmail.com>

##############################################################################################################################
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
import json

# dictionaries to track the number of different sums and prods and each possible x,y
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
                print("find_sum_list() Trying x,y = {},{}".format(ix, iy))
                # get prod
                nprod = ix * iy
                nprod_key = str(nprod)
                # check if this prod has multiple possible x,y
                if p_prods[nprod_key]['count'] == 1:
                    possible = False
                    print("ONLY ONE Prod of {},{}! Go to next sum!\n".format(ix,iy))
                    break
                print("Prod {} has multiple possible x,y ...".format(nprod_key))
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


def get_answer(p_poss_sums:list, p_sums:dict, p_prods:dict):
    """
    from the possible sum list, find a prod where only ONE possible x,y has a sum with
    multiple possible x,y
    :param p_poss_sums: possible sums
    :param p_sums: all sums
    :param p_prods: all prods
    """
    print("\nget_answer()")
    ans_count = 0
    for isum in p_poss_sums:
        print("get_answer() Trying sum {}".format(isum))
        sdict = p_sums[isum]
        sposn = 0
        # for each possible x in this sum
        for sx in sdict['x']:
            # get y
            sy = sdict['y'][sposn]
            print("get_answer() Trying x,y = {},{}".format(sx, sy))
            # get prod
            pposn = 0
            nprod = sx * sy
            nprod_key = str(nprod)
            pdict = p_prods[nprod_key]
            # for each sum for this prod
            for px in pdict['x']:
                py = pdict['y'][pposn]
                psum = px + py
                psum_key = str(psum)
                # check the count
                if p_sums[psum_key]['count'] == 1:
                    ans_count += 1
                    print("Sum = {}; Prod = {}; Possible x,y = {},{}".format(isum, nprod, sx, sy))
                pposn += 1
            sposn += 1

    print("\nNumber of possible answers = {}".format(ans_count))


def num_count_items(p_dict:dict, p_count:int=0) -> int:
    num = 0
    for item in p_dict:
        if p_dict[item]['count'] > p_count:
            num += 1
    return num


def print_dict(p_dict:dict, p_label:str, p_count:int=0):
    for item in p_dict:
        if p_dict[item]['count'] > p_count:
            print("{} = {}\ncount = {}\nx = {}\ny = {}"
                  .format(p_label, item, p_dict[item]['count'], p_dict[item]['x'], p_dict[item]['y']))
    print('\n')


def impossible_problem_main():
    # y > x > 1
    # x + y <= 100
    count = 0
    # x = 2..49
    for x in range(2, 50):
        y1 = x + 1
        y2 = 100 - x + 1
        # y = 3..98
        for y in range(y1, y2):
            tabulate_results(x, y)
            count += 1

    print("Number of possible x,y = {}".format(count))
    # print("count = {}\nsums = \n{}\nprods = \n{}\n".format(count, json.dumps(sums,indent=4), json.dumps(prods,indent=4)))
    print("Number of multi-sums = {}".format(num_count_items(sums, 1)))
    # print_dict(sums, 'sum')
    print("Number of multi-prods = {}".format(num_count_items(prods, 1)))
    # print_dict(prods, 'prod')

    asum_list = find_sum_list(sums, prods)

    get_answer(asum_list, sums, prods)

    print("\nPROGRAM ENDED.")


if __name__ == '__main__':
    impossible_problem_main()
