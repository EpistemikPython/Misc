###############################################################################################################################
# coding=utf-8
#
# test_thread_pool.py
#
#  Copyright (c) 2020  Mark Sattolo  <epistemik@gmail.com>

__author__         = 'Mark Sattolo'
__author_email__   = 'epistemik@gmail.com'
__python_version__ = 3.6
__created__ = '2020-04-09'
__updated__ = '2020-04-09'

import concurrent.futures as confut
import json
import copy


def update_rev_exps_main(param:list):
    msg = 'update_rev_exps_main'
    pcopy = copy.copy(param)
    print(F"start fxn: {msg}: {pcopy}")
    res = pcopy.append(msg)
    return res


def update_assets_main(param:list):
    msg = 'update_assets_main'
    print('start fxn: ' + msg)
    res = param.append(msg)
    return res


def update_balance_main(param:list):
    msg = 'update_balance_main'
    print('start fxn: ' + msg)
    res = param.append(msg)
    return res


UPDATE_FXNS = [update_rev_exps_main, update_assets_main, update_balance_main]
CHOICE_FXNS = {
    'REV_EXPS' : UPDATE_FXNS[0] ,
    'ASSETS'   : UPDATE_FXNS[1] ,
    'BALANCE'  : UPDATE_FXNS[2] ,
    'ALL'      : 'ALL'
}

saved_log_info = ['stuff', 'more stuff']

response_box = list()


def thread_update(thread_fxn: object, p_params: list):
    print(F"starting thread: {str(thread_fxn)}")
    if callable(thread_fxn):
        response = thread_fxn(p_params)
        print(F"response = {response}")
    else:
        msg = F"thread fxn {str(thread_fxn)} NOT callable?!"
        print(msg)
        raise Exception(msg)
    print(F"finished thread: {str(thread_fxn)}")
    return response


def button_click():
    """assemble the necessary parameters"""
    cl_params = ['one', 'two', 'three']
    exe = 'ALL'
    reply = ['hello']
    main_fxn = CHOICE_FXNS[exe]
    if callable(main_fxn):
        print('Calling main function...')
        response = main_fxn(cl_params)
        reply = {'response':response}
    elif main_fxn == 'ALL':
        # use a with statement to ensure threads are cleaned up promptly
        with confut.ThreadPoolExecutor(max_workers = len(UPDATE_FXNS)) as executor:
            # send each script to a separate thread
            future_to_update = {executor.submit(thread_update, upfxn, cl_params):upfxn for upfxn in UPDATE_FXNS}
            for future in confut.as_completed(future_to_update):
                updater = future_to_update[future]
                print(F"updater = {updater}")
                try:
                    data = future.result()
                except Exception as exc:
                    print(F"{updater} generated an exception: {exc}")
                else:
                    print(F"data = {data}")
                    reply.append(data)
    else:
        msg = F"Problem with main??!! '{main_fxn}'"
        print(msg)
        reply = {'msg':msg, 'log':saved_log_info}

    response_box.append(json.dumps(reply, indent = 4))
    return response_box


result = button_click()
print(json.dumps(result, indent = 4))
