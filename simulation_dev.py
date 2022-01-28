# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 20:57:41 2022
@author: Memen
"""


import json
import time
import argparse
import random
import uuid

with open("../tweets.json", 'r', encoding='UTF-8') as f:
    data = json.load(f)

    steps = 20
    startIndex, endIndex = 0, 0+steps
    print(type(data))
    print(len(data))

    # keys= list(data.keys())

    try:
        while(data[startIndex] != None):
            print("********************")
            pre = random.randint(0, len(data))
            with open("./test-{}.json".format(pre), 'w') as o:

                for item in list(data[startIndex:endIndex]):
                    item["uuid"] = str(uuid.uuid4())
                    o.write(json.dumps(item)+'\n')
                    print(item)
                o.close()
            print("********************")
            startIndex = endIndex
            endIndex = startIndex+steps
            time.sleep(40)
    except Exception as e:
        print(e)
        f.close()
