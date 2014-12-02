__author__ = 'serajago'
import inspect

import scrapperConstants as const


def scrapperLog(level, msg):
    pass
    '''
	# for now, print it to stdout
	callerframerecord = inspect.stack()[1]    # 0 represents this line
                                      		  # 1 represents line at caller
	frame = callerframerecord[0]
	info = inspect.getframeinfo(frame)
	print ("%s:%d:%s:[%s] %s\n") % (info.filename, \
		info.lineno,
		info.function, const.LogLevels[level], msg)
'''


__author__ = 'serajago'
