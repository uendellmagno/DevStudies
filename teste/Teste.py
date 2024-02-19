'''
import ClassTest as ct
import pandas as pd
import numpy as np
import csv
np.test()

Student1 = ct.Student('Uendell', "Python", "19")
Student2 = ct.Student("Uendell", "React", "19")
School = ct.Student

print(Student1.name, Student2.course, Student1.age)
print(School.school)

# for variable in sequence:
sum_total = 0
for i in range(1, 101):
    sum_total += i
    print(sum_total)

# group of code - name and input: def greet(name):
def sum_of_even(numbers):
    """This function returns the sum of even numbers in a list."""
    even_sum = 0
    for num in numbers:
        if num % 2 == 0:
            even_sum += num
    return even_sum

numbers_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = sum_of_even(numbers_list)
print("Sum of even numbers:", result)
'''


file_path = "./stack-overflow-developer-survey-2023/survey_results_schema.csv"
with open(file_path, "r") as file:
    pass
