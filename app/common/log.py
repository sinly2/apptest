# -*- coding: utf-8 -*-
'''
Created on 2017年4月28日

@author: guxiwen
'''
import logging
import logging.config
logging.config.fileConfig("logger.conf")
logger = logging.getLogger("example01")
logger.debug('This is debug message')
logger.info('This is info message')
logger.warning('This is warning message')