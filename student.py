from enum import Enum

class Grade(Enum):
    A = (90, "Excellent")
    B = (75, "Very Good")
    C = (60, "Good")
    D = (40, "Pass")
    F = (0, "Fail")


class Student:
    scl_name = "abc School"
    country = "India"

    def __init__(self, name, marks=None):
        self._name = name
        self._marks_val = marks

    @property
    def marks(self):
        if self._marks_val is None:
            self._marks_val = 25
        return self._marks_val

    @marks.setter
    def marks(self, val):
        self._marks_val = val

    def dispn(self, word=""):
        try:
            return self._name + word
        except TypeError:
            return f"ERROR: word should be a string, got {type(word)}"

    def dispm(self):
        total = 0
        try:
            for m in self.marks:
                total += m
            percentage = round((total / len(self.marks)),2)
            self._marks_val = percentage
            return percentage
        except TypeError:
            self._marks_val = self.marks
            return self._marks_val

    def display_grade(self):
        percentage = self.dispm()
        for grade in Grade:
            if percentage >= grade.value[0]:
                return grade.name, grade.value[1]

    def pof(self):
        if self.dispm() > 40:
            return "Pass"
        else:
            return "Fail"

    @staticmethod
    def scl_rules():
        return "School starts at 9 AM"

    @classmethod
    def ch_school(cls, new_name):
        cls.scl_name = new_name

    @classmethod
    def ch_country(cls, new_name):
        cls.country = new_name

name = input("Enter student name: ")

marks_input = input("Enter marks separated by comma (or press Enter for default): ")

if marks_input.strip() == "":
    student = Student(name)
else:
    try:
        marks_list = [int(m.strip()) for m in marks_input.split(",")]
        if len(marks_list) == 1:
            student = Student(name, marks_list[0])
        else:
            student = Student(name, marks_list)
    except ValueError:
        print("Invalid marks! Please enter only numbers.")
        exit()

print("\n--- Student Details ---")
print("Marks:", student.marks)
print("Percentage:", student.dispm())#1
print("Grade:", student.display_grade())#1
print("Result:", student.pof())
print("School:", Student.scl_name)
print("Country:", Student.country)

