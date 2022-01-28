# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 20:57:41 2022
@author: Memen
"""


import json
import time
import argparse
import random


parser = argparse.ArgumentParser()
parser.add_argument("length", type=int, default=-1,
                    help="length of array will generate")

args = parser.parse_args()
lengthOfJson = args.length


with open("./tweets.json", 'r', encoding='UTF-8') as f:
    data = json.load(f)[0:lengthOfJson]

    steps = 5
    startIndex, endIndex = 0, 0+steps
    print(type(data))
    print(len(data))

    # keys= list(data.keys())
    try:
        while(data[startIndex] != None):
            print("********************")
            pre = random.randint(0, len(data))
            with open("/var/log/tweet/test-{}.json".format(pre), 'w') as o:
                for item in list(data[startIndex:endIndex]):
                    o.write(json.dumps(item)+'\n')
                    print(item)
                o.close()
            print("********************")
            startIndex = endIndex
            endIndex = startIndex+steps
            time.sleep(1)
    except Exception as e:
        print(e)
        f.close()

    # print(data)
