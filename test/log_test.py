import logging
import auxiliary_module
from datetime import datetime as dt

def mymain():
	# create logger with 'spam_application'
	logger = logging.getLogger(__file__)
	logger.setLevel("logging.DEBUGg")
	# create file handler which logs even debug messages
	fh = logging.FileHandler('spam.log')
	fh.setLevel(logging.DEBUG)
	# create console handler with a higher log level
	ch = logging.StreamHandler()
	ch.setLevel(logging.ERROR)
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(fh)
	logger.addHandler(ch)

	logger.info('creating an instance of auxiliary_module.Auxiliary')
	a = auxiliary_module.Auxiliary()
	logger.info('created an instance of auxiliary_module.Auxiliary')
	logger.info('calling auxiliary_module.Auxiliary.do_something')
	a.do_something()
	logger.info('finished auxiliary_module.Auxiliary.do_something')
	logger.info('calling auxiliary_module.some_function()')
	auxiliary_module.some_function()
	logger.info('done with auxiliary_module.some_function()')


if __name__ == "__main__":
	print(F"time = {dt.now().strftime('%Y-%m-%d %H:%M:%S')}")
	mymain()
	exit()
