"""
Tomson Tai
10/18/2020

Usage: 
> python main.py courses.csv students.csv tests.csv marks.csv output.json
"""

import sys
import csv
import json
from collections import OrderedDict

class StudentReport:

    def __init__(self):
        self.parseArgs()
        
    def parseArgs(self):
        if len(sys.argv) != 6:
            self.showUsage()
            sys.exit("ERROR: Invalid Usage. Try again.")
        self.courseFile = sys.argv[1]
        self.studentsFile = sys.argv[2]
        self.testsFile = sys.argv[3]
        self.marksFile = sys.argv[4]
        self.outputFile = sys.argv[5]

    def showUsage(self):
        print('Usage:')
        print('  python main.py courses.csv students.csv tests.csv marks.csv output.json')

    def readCourses(self):
        courseMap = {}
        with open(self.courseFile) as f:
            reader = csv.DictReader(f)
            for line in reader:
                courseMap[line["id"]] = [line["name"]]
                courseMap[line["id"]].append(line["teacher"])
        return courseMap  

    def readStudents(self):
        studentMap = {}
        with open(self.studentsFile) as f:
            reader = csv.DictReader(f)
            for line in reader:
                studentMap[line["id"]] = line["name"]
        return studentMap

    def readTests(self):
        testData = {}
        with open(self.testsFile) as f:
            reader = csv.DictReader(f)
            for line in reader:
                testData[line["id"]] = [line["course_id"]]
                testData[line["id"]].append(line["weight"])
        return testData
    
    # Join Tests data with Marks Data into a single list. 
    def processTestMarks(self):
        testMap = self.readTests()
        testMarkList = []
        with open(self.marksFile) as f:
            reader = csv.DictReader(f)
            for line in reader:
                markData = []
                markData.append(line["test_id"])
                markData.append(line["student_id"])
                markData.append(line["mark"])
                markData.extend(testMap.get(markData[0]))
                testMarkList.append(markData)
        return testMarkList

    def generate(self):
        courses = self.readCourses()
        students = self.readStudents()
        studentReport = self.generateStudentReport()

        output = {}
        allStudents = []
        output['students'] = allStudents
        for sid in sorted(studentReport.keys()):
            avg = self.calculateAverage(studentReport[sid])
            studentCourses = []
            currentReport = studentReport[sid]
            for cid in sorted(currentReport.keys()):
                course = OrderedDict([('id', cid),('name', courses[cid][0]), ('teacher', courses[cid][1]), ('courseAverage', round(currentReport[cid], 2))])
                studentCourses.append(course)

            student = OrderedDict([('id', sid), ('name', students[sid]), ('totalAverage', round(avg, 2)), ('courses', studentCourses)])
            allStudents.append(student)
        
        with open(self.outputFile, 'w') as newFile:
            newFile.write(json.dumps(output, indent=4))

        return output

    def calculateAverage(self, studentCourseMap):
        sum = 0.0
        for k in studentCourseMap.keys():
            sum += studentCourseMap[k]
        return float(sum)/len(studentCourseMap)

    def generateStudentReport(self):
        marks = self.processTestMarks()
        student = {}
        for line in marks:
            try:
                temp = {}
                value = float(line[-1]) * float(line[2]) / 100
                if(line[1] not in student):
                    student[line[1]] = temp
                    if(line[3] not in temp):
                        temp[line[3]] = value
                    else:
                        temp[line[3]] += value
                else:
                    courseMap = student[line[1]]
                    if(line[3] not in courseMap):
                        courseMap[line[3]] = value
                    else:
                        courseMap[line[3]] += value
            except:
                sys.exit("ERROR: Exception generating Student Report.")

        return student

report = StudentReport()
report.generate()

print('See the student reports in %s' %(report.outputFile))
