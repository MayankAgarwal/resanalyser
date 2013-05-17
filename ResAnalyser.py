#-------------------------------------------------------------------------------
# Name:        Result Analyser (Version 2.0)
#
# Author:      Asis aka !mmorta!
#
# Created:     11/05/2013 (V1.0 - 29/11/2012)
#
# Copyright:   (c) Asis 2013
#
# Licence:     Creative Commons Attribution-ShareAlike 3.0 Unported License.
#-------------------------------------------------------------------------------

# Python version 3 or more neeeded!!!
# Imports from Python
import os, re, sys

# ATTENTION!!! UPDATE THIS EVERY TERM!!!
latest_term = ['AUTUMN 2012','RE-EXAM AUTUMN 2012']

# Global Databases & required variables -->

result_file_addresses = []
for res_file in os.listdir(os.path.join(os.getcwd(),'Result')):
    result_file_addresses.append(os.path.join(os.getcwd(),'Result',res_file))
#result_file_addresses = ["G:\Study\Programming\Py\Result analysis\testing3.txt"]
database = {} # For individual student data storing
course_data = {} # For record keeping of every course for every sem
grades = {'AA':10,'AB':9,'BB':8,'BC':7,'CC':6,'CD':5,'DD':4,'W':0,'FF':0,'SS':0}
terms = ['SPRING','AUTUMN','RE-EXAM','SUMMER']

# The Main function --> (to give all the pretty Command Line Interface like feel)
def main():
    global result_file, result_file_addresses
    # Welcome Screen
    print(" \n\tResult Analyser by !mmorta!\
            \n\tPython Library for analysing result (PDF Parser with Analyser)\
            \n\tAsk !mmorta! for Source Code!!")
    # Take in the address of the result file
    if not result_file_addresses:
        result_file_addresses = [input("\n\tAddress of the result file (e.g. C:\downloads\civ.pdf)")]
    # Check if the address is proper/correct
    for result_file_addr in result_file_addresses:
        try:
            result_file = open(result_file_addr,'r')
        except IOError:
            print("\n\tUnable to open the file!\n")
            result_file = None
            print("Exiting...")
            sys.exit(1) #Bad exit

        # File address is correct
        print("\n\tAddress %s seems correct...File Ready..."%result_file_addr)

        print("\tProcessing result file %s...Please wait..."%os.path.basename(result_file_addr))

        # Everything seems fine so just parse the file & extract the reqd data...
        PDF_Parser(result_file)

    # Analysis Options
    '''print("\n\t\tAnalysis Options -\
            \n\t1. Get Student Specific Details\
            \n\t2. Get Course Specific Details")'''

    Analyser.All_Courses(printify=True,alphabetically=True,serial=True,terms=True)
##    marklist = Analyser.Make_Marklist(course='MINI PROJECT')
##    marklist = Analyser.Make_Marklist(course='MINI PROJECT',names=True)
##    Analyser.Mean_Deviation(marklist,printify=True)
##    Analyser.Ranking(marklist,printify=True)
##    marklist = Analyser.Make_Marklist(course='COMMUNICATION SKILLS',course_term='AUTUMN 2010',names=True)
##    Analyser.Ranking(marklist,printify=True)
##    Analyser.Mean_Deviation(marklist,printify=True)
##    Analyser.Gradify(marklist,printify=True)
##    Analyser.Gradify(marklist,printify=True,cumulative=True)
##    Analyser.Individual_Record('BT10CIV059',printify=True)
##    marklist = Analyser.Make_Marklist(batch='BT10',term='AUTUMN 2010',names=True,sg=True)
    marklist = Analyser.Make_Marklist(branch='COMPUTER SCIENCE ENGINEERING',batch='BT10',cg=True,names=True)
    Analyser.Gradify(marklist,printify=True)
    Analyser.Ranking(marklist,printify=True)

##    # Super Senior data...
##    for roll in database:
##        if database[roll]['Stud Type'] == 'Super Senior':
##            print(database[roll]['Name'])
##            print(database[roll])
	input("\n\tEnter to exit..."
    # End of main()...

# Parsing stuff! -->
# A thorough overview of the raw PDF result file is necessary
# to understand the PDF_Parser function properly.

# Nasty name issues...
general_names_issues = {'SPORTS / YOGA / LIBRARY / NCC (--)':'SPORTS YOGA LIBRARY NCC',
                        'SPORTS/YOGA/LIBRARY/NCC (--)':'SPORTS YOGA LIBRARY NCC',
                        'SPORTS / YOGA/ LIBRARY/ NCC (AU)':'SPORTS YOGA LIBRARY NCC',
                        'SPORTS / YOGA / LIBRARY / NCC (AU)':'SPORTS YOGA LIBRARY NCC',
                        '& REUSE   \(DE\)':'INDUSTRIAL WASTEWATER TREATMENT, RECYCLE & REUSE',
                        'ENGINEERING   \(DE\)':'RAILWAY, AIRPORT, PORTS & HARBOR ENGINEERING'}

duplication_issues = {'BUILDING DESIGN AND DRAWING':'BUILDING DESIGN DRAWING',
                      'COMMUNICATION SKILL':'COMMUNICATION SKILLS',
                      'ENVIRONMENTAL ENGINEERING-II':'ENVIRONMENTAL ENGINEERING II',
                      'MATHEMATICS - I':'MATHEMATICS I',
                      'MINI PROJECT - I':'MINI PROJECT',
                      'PAVEMENT DESIGN':'PAVEMENT ANALYSIS DESIGN',
                      'PHYSICS - I':'PHYSICS',
                      'PHYSICS I':'PHYSICS',
                      'PROJECT PLANNING MANAGEMENT':'PROJECT PLANNING AND MANAGEMENT',
                      'PSYCHOLOGY AND HRM':'PSYCHOLOGY HRM',
                      'SPORTS YOGA/ LIBRARY/ NCC':'SPORTS/YOGA/LIBRARY/NCC',
                      'SPORTS YOGA LIBRARY NCC':'SPORTS/YOGA/LIBRARY/NCC',
                      'STRUCTURAL ANALYSIS LABORATORY':'STRUCTURAL ANALYSIS LAB',
                      'SURVEYING - I':'SURVEYING I'}


def PDF_Parser(file):

    global database, course_data

    def is_no_of_credit(char):
        try:
            no_credits = int(char)
            if no_credits == 0:
                return 10 # For type_resolving purposes
            if no_credits < 9:
                return no_credits
        except:
            return False

    def is_gpa(gpa):
        try:
            gpa = float(gpa)
            if gpa <= 10.0:
                return gpa
        except:
            return False

    def getdata(line):
        start = line.find("Td (") + 4
        end = line[start:].find(")Tj ET")+start
        result = line[start:end]
        return result

    def prettify(course): # Course names have nasty raw data & duplication issues
        if course in general_names_issues:
            return general_names_issues[course]
        if course in duplication_issues:
            return duplication_issues[course]
        else:
            course_split = course.split()
            if not len(course_split) == 1:
                legit = ''
                for each in course_split:
                    if re.match(r'[a-zA-Z0-9.-]+',each):
                        legit += each + ' '
                legit = legit[:-1]
                if legit in duplication_issues:
                    legit = duplication_issues[legit]
                general_names_issues[course] = legit
                return legit
            else:
                general_names_issues[course] = course
                return course

    def prettify_name(name):
        prettified = name
        if prettified[-1] == '\xa0':
            prettified = prettified[:-1]
        if prettified[-1] == 'Â':
            prettified = prettified[:-1]
        return prettified

    def get_stud_type(roll):
        # Classifying the student based on his Roll type...
        if roll[:2] == 'BT':
            cur_stud_type = 'B. Tech.'
        elif roll[:2] == 'MT':
            cur_stud_type = 'M. Tech.'
        elif roll[0] in ['L','N','R','S','T','U','V','W','X','Y','Z']:
            cur_stud_type = 'First Year B. Tech.'
        elif roll[:4] == 'VNIT':
            cur_stud_type = 'Super Senior'
        else:
            cur_stud_type = 'Dont Know'
        if cur_stud_type == 'B. Tech.':
            if int(roll[2:4]) <= 8:
                cur_stud_type = 'Super Senior'
        return cur_stud_type

    def get_batch(roll,stud_type):
        if stud_type == 'First Year B. Tech.':
            return latest_term[0][-4:]
        else:
            return roll[:4]

    def individual():
        all_details = {'Branch':None,'CGPA':0,'Credits Total':0,'EGP Total':0,'W':False,'FF':False}
        cur_line = file.readline()
        cur_name = getdata(file.readline())
        cur_roll = getdata(file.readline())
        cur_stud_type = get_stud_type(cur_roll)
        # Trashing out unrequired data...
        for i in range(5):
            file.readline()
        cur_branch = getdata(file.readline())
        cur_name = prettify_name(cur_name)
        all_details['Name'] = cur_name
        all_details['Roll'] = cur_roll
        all_details['Stud Type'] = cur_stud_type
        all_details['Branch'] = cur_branch
        all_details['Batch'] = get_batch(cur_roll,cur_stud_type)
        all_details['Records'] = {}
        good_to_go = True
        #if cur_stud_type in ('Super Senior','Dont Know'):
        #    good_to_go = False
        while good_to_go:
            cur_data = getdata(cur_line)
            if cur_data:
                if cur_data.split()[0] in terms:
                    cur_term = cur_data
                    if cur_term[-1] == ' ':
                        cur_term = cur_term[:-1]
                    all_details['Records'][cur_term] = {'CGPA':0,'SGPA':0,'Courses':{}}
                    cur_block = []
                    while not cur_data == "Credit":
                        cur_line = file.readline()
                        cur_data = getdata(cur_line)
                        cur_block.append(cur_data)
                        if cur_data in grades and is_no_of_credit(cur_block[-2]):
                            no_credits = is_no_of_credit(cur_block[-2])
                            if no_credits == 10:
                                no_credits = 0
                            course = cur_block[-3]
                            if course[0] == '\\':
                                course = cur_block[-4]
                            course = prettify(course)
                            cur_grade = grades[cur_data]
                            cur_block = []
                            good_to_add = True
                            # Fuck Super Senior Data
                            if int(cur_term[-4:]) <= 2008:
                                good_to_add = False
                            elif int(cur_term[-4:]) == 2009 and not cur_term in ('RE-EXAM AUTUMN 2009','AUTUMN 2009'):
                                good_to_add = False
                            if good_to_add:
                                # First adding the data to course_database
                                if course in course_data:
                                    file.readline()
                                    if cur_term in course_data[course]['Records']:
                                        course_data[course]['Records'][cur_term][cur_roll] = cur_grade
                                    else:
                                        course_data[course]['Records'][cur_term] = {}
                                        course_data[course]['Records'][cur_term][cur_roll] = cur_grade
                                else:
                                    serial = getdata(file.readline())
                                    course_data[course] = {'Serial':serial,'Records':{}}
                                    course_data[course]['Records'][cur_term] = {}
                                    course_data[course]['Records'][cur_term][cur_roll] = cur_grade

                            # Now adding stuff to the student's database
                            if cur_grade == 'W':
                                all_details['W'] = True
                            elif cur_grade == 'FF':
                                all_details['FF'] = True
                            all_details['Records'][cur_term]['Courses'][course] = cur_grade

                    if is_gpa(cur_block[-2]) and not len(cur_block) < 7:
                        cgpa_sem = is_gpa(cur_block[-2])
                        egp_tot = float(cur_block[-3])
                        creds_tot = float(cur_block[-4])
                        sgpa_sem = is_gpa(cur_block[-5])
                        #egp_sem = float(cur_block[-6])
                        #creds_sem = float(cur_block[-7])
                        all_details['Records'][cur_term]['CGPA'] = cgpa_sem
                        all_details['Records'][cur_term]['SGPA'] = sgpa_sem
                        #all_details['Records'][cur_term]['EGP'] = egp_sem
                        #all_details['Records'][cur_term]['Credits Earned'] = creds_sem
                        all_details['Records'][cur_term]['EGP Total'] = egp_tot
                        all_details['Records'][cur_term]['Credits Total'] = creds_tot
                        if cur_term == latest_term[0]:
                            all_details['CGPA'] = cgpa_sem
                            all_details['Credits Total'] = creds_tot
                            all_details['EGP Total'] = egp_tot
                        elif cur_term == latest_term[1]:
                            all_details['CGPA'] = cgpa_sem
                            all_details['Credits Total'] = creds_tot
                            all_details['EGP Total'] = egp_tot

            if cur_line == "endstream"+chr(10):
                if cur_roll not in database:
                    database[cur_roll] = all_details
                else: # Requirement for the pro 2 page long grade cards of VIPs
                    for each_term in database[cur_roll]['Records']:
                        all_details[each_term] = database[cur_roll]['Records'][each_term]
                    database[cur_roll] = all_details
                break
            cur_line = file.readline()

    cur_line = file.readline()
    while not cur_line in ["%%EOF","%%EOF"+chr(10)]:
        cur_line = file.readline()
        if cur_line == "1 1 1 rg"+chr(10):
            individual()

    print("\tFile fully parsed...")
    print("\tData ready to be analysed...")
    # End of PDF Parser...


# Analysis shit! :-P  -->
class Analyser:
    def All_Courses(printify=True, serial = False, terms = False, alphabetically = False):
        data = []
        if not printify:
            to_return = course_data.keys()
            if alphabetically:
                return sorted(to_return)
            return to_return
        for each in course_data:
            to_print = each
            if serial:
                to_print += ' || Serial - ' + course_data[each]['Serial']
            if terms:
                course_terms = list(course_data[each]['Records'].keys())
                to_print += ' || Terms - ' + str(course_terms)
            if not alphabetically:
                print(to_print,'\n')
            else:
                data.append(to_print)
        if alphabetically:
            data.sort()
            for course in data: print(course)

    def Individual_Record(roll,term=None,printify=False):
        if roll in database:
            if not term:
                if printify:
                    print(database[roll])
                return database[roll]
            else:
                if printify:
                    print(database[roll]['Records'][term])
                return database[roll]['Records'][term]

    def Make_Marklist(course=False,course_term=None,branch=None,batch=None,term=latest_term[0],cg=False,sg=False,names=False):
        mark_list = []
        if course and course in course_data:
            if course_term and course_term in course_data[course]['Records']:
                for rolls in course_data[course]['Records'][course_term]:
                    mark_list.append(course_data[course]['Records'][course_term][rolls])
                return mark_list
            else:
                for course_term in course_data[course]['Records']:
                    for rolls in course_data[course]['Records'][course_term]:
                        if names:
                            mark_list.append((course_data[course]['Records'][course_term][rolls],rolls))
                        else:
                            mark_list.append(course_data[course]['Records'][course_term][rolls])
                return mark_list

        elif cg:
            for roll in database:
                cur_cg = database[roll]['CGPA']
                should_add = True
                if branch:
                    if not database[roll]['Branch'] == branch:
                        should_add = False
                if batch:
                    if not batch == database[roll]['Batch']:
                        should_add = False
                if should_add:
                    if names:
                        name = database[roll]['Name']
                        mark_list.append((cur_cg,name))
                    else:
                        mark_list.append(cur_cg)
            return mark_list

        elif sg:
            for roll in database:
                should_add = True
                if branch:
                    if not database[roll]['Branch'] == branch:
                        should_add = False
                if batch:
                    if not batch == database[roll]['Batch']:
                        should_add = False
                if should_add:
                    for cur_term in database[roll]['Records']:
                        if cur_term == term:
                            cur_sg = database[roll]['Records'][cur_term]['SGPA']
                            if names:
                                name = database[roll]['Name']
                                mark_list.append((cur_sg,name))
                            else:
                                mark_list.append(cur_sg)
                            break
            return mark_list
        return [] # If the input was wrong, we dont want to return None.

    def Mean_Deviation(marklist, printify = False): # Takes marks, outputs mean & std deviation
        if len(marklist) > 0:
            if not isinstance(marklist[0],tuple):
                total = sum(marklist)
                fail = 0
                N = len(marklist)
                for each in marklist:
                    if not each:
                        fail += 1
                N = N - fail
                devn = 0
                if N: # Division by zero error avoidance
                    mean = total/N
                else:
                    mean = total
                for each in marklist:
                    if each:
                        devn += (mean - each)**2
                if N:
                    devn = (devn/N)**0.5
                if printify:
                    print("\n\tMean -",mean,"|| Deviation -",devn,"|| Fail -",fail)
                return mean, devn, fail
            else:
                total = 0
                fail = 0
                for each in marklist:
                    total += each[0]
                    if not each[0]:
                        fail += 1
                N = len(marklist)
                N = N - fail
                devn = 0
                if N: # Division by zero error avoidance
                    mean = total/N
                else:
                    mean = total
                for each in marklist:
                    if each[0]:
                        devn += (mean - each[0])**2
                if N:
                    devn = (devn/N)**0.5
                if printify:
                    print("\n\tMean -",mean,"|| Deviation -",devn,"|| Fail -",fail)
                return mean, devn, fail

    def Gradify(marklist, printify = False,cumulative=False):
        categories = [['F',0],[10,0],[9,0],[8,0],[7,0],[6,0],[5,0],[4,0]]
        if cumulative:
            categories = [['F',0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0],[10,0]]
        for mark in marklist:
            if isinstance(mark,tuple):
                mark = mark[0]
            if mark == 0:
                categories[0][1] += 1
            for i in range(1,len(categories)):
                if mark >= categories[i][0]:
                    categories[i][1] += 1
                    if not cumulative:
                        break
        if printify:
            print("\n\tGrade Distribution -")
            for i in range(len(categories)):
                print("\t{0} - {1}".format(categories[i][0],categories[i][1]))
            return True
        return categories

    def Ranking(marklist, printify=True):
        if printify:
            print()
        if marklist:
            if not isinstance(marklist[0],tuple):
                if not printify:
                    return sorted(marklist,reverse=True)
                else:
                    for index, mark in enumerate(sorted(marklist,reverse=True)):
                        print('\t{rank} - {mark}'.format(rank=index+1,mark=mark))
            else:
                data_dict = {}
                marks_list = []
                for each in marklist:
                    if each[0] in data_dict:
                        data_dict[each[0]].append(each[1])
                    else:
                        data_dict[each[0]] = [each[1]]
                    marks_list.append(each[0])
                marks_list = set(marks_list)
                to_return = []
                for mark in sorted(marks_list,reverse=True):
                    cur_data = sorted(data_dict[mark])
                    to_return.append((len(to_return)+1,cur_data))
                    if printify:
                        for name in cur_data:
                            print('\t{rank} - {name} ({mark})'.format(rank=len(to_return),name=name,mark=mark))
                return to_return

    # End of Analyser...


# The main() caller... Finally :)
if __name__ == '__main__':
    main()
