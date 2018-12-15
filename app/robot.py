#!/usr/bin/python
# -*- coding: UTF-8 -*-



class Employee:

    '所有员工的基类'
    empcount = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee.empcount += 1

    def display_count(self):
        print "Total Employee %d" % Employee.empcount

    def display_employee(self):
        print "Name : ", self.name, ", Salary: ", self.salary

