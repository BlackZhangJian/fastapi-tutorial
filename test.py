#!/usr/bin/env python
# coding=utf-8
'''
Author: Bowen
Date: 2022-05-06
LastEditTime: 2022-05-13
LastEditors: Bowen
Description: 
FilePath: /fastapi-tutorial/test.py
'''
import os

# os.environ["ENVIRONMENT"]="test"

print(os.environ.keys())
print(os.getenv("ENVIRONMENT"))

print('\033[1;31mtttttttttttt\033[0m')