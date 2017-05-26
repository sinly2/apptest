# -*- coding: utf-8 -*-
'''
Created on 2017年3月3日

@author: guxiwen
'''
import sys
sys.path.append('/root/project/TestRequests')
from app import create_app
#test
app = create_app()
if __name__ == '__main__':
    app.run(debug=True,port=80)