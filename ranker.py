#!/usr/bin/env python
# Ranker...
# Licensed under Creative Commons Attribution 3.0 Unported License;

import os, re, sys, time, logging
import json

from ResAnalyser import Analyser

latest_terms = ['AUTUMN 2012','RE-EXAM AUTUMN 2012']
grades = {'AA':10,'AB':9,'BB':8,'BC':7,'CC':6,'CD':5,'DD':4,'W':0,'FF':0,'SS':0}
terms = ['SPRING','AUTUMN','RE-EXAM','SUMMER']

department_data = json.load(open(os.path.join(os.getcwd(),'department_data.txt'),'r'))

rank_data = {}
batches = {}
insti_mark_list = []
for dept in department_data:
    rank_data[dept] = {}
    dept_mark_list = []
    for batch in department_data[dept]:
        if batch not in batches:
            batches[batch] = True
        batch_mark_list = []
        for indi in department_data[dept][batch]:
            batch_mark_list.append(department_data[dept][batch][indi])
        batch_mark_list.sort(reverse=True)
        rank_data[dept][batch] = batch_mark_list
        dept_mark_list.extend(batch_mark_list)
    dept_mark_list.sort(reverse=True)
    rank_data[dept]["All"] = dept_mark_list
    insti_mark_list.extend(dept_mark_list)
insti_mark_list.sort(reverse=True)
rank_data["All"] = insti_mark_list

for batch in batches:
    insti_batch_mark_list = []
    for dept in department_data:
        if batch in department_data[dept]:
            batch_mark_list = []
            for indi in department_data[dept][batch]:
                batch_mark_list.append(department_data[dept][batch][indi])
            insti_batch_mark_list.extend(batch_mark_list)
    insti_batch_mark_list.sort(reverse=True)
    rank_data[batch] = insti_batch_mark_list

g4 = open(os.path.join(os.getcwd(),'rank_data.txt'),'w')
g4.write(json.dumps(rank_data))
g4.close()
print(len(rank_data["BT10"]))
print(rank_data["BT10"].index(9.54))
rakk_file = open(os.path.join(os.getcwd(),'rank_data.txt'),'r')
rakk_data = json.load(rakk_file)
print(len(rakk_data["CIVIL ENGINEERING"]["All"]))
print(rakk_data["All"].index(9.54))
data_file = open(os.path.join(os.getcwd(),'database.txt'),'r')
course_file = open(os.path.join(os.getcwd(),'course_data.txt'),'r')
rank_file = open(os.path.join(os.getcwd(),'rank_data.txt'),'r')
if data_file.closed:
    data_file = open(os.path.join(os.getcwd(),'database.txt'),'r')
if course_file.closed:
    course_file = open(os.path.join(os.getcwd(),'course_data.txt'),'r')
if rank_file.closed:
    rank_file = open(os.path.join(os.getcwd(),'rank_data.txt'),'r')
database = json.load(data_file)
course_data = json.load(course_file)
rank_data = json.load(rank_file)

