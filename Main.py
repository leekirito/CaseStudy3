from Assignment import Assignment
from Authentication import Authentication
from Course import Course
from Enrollment import Enrollment
from Grade import Grade
from Instructor import Instructor
from PlatformAdmin import PlatformAdmin
from Register import Register
from Schedule import Schedule
from Student import Student
import pyodbc
from getpass import getpass

class main():
    def __init__(self):
        self.current_student = None
        self.current_instructor = None
        self.students = Student.get_data()

    def Start_menu(self):

        start_options = {
            "1": self.log_in_instructor_menu(),
            "2": self.log_in_student_menu(),
            "3": self.log_in_admin_menu(),
            "4": self.register_as_instructor_menu(),
            "5": self.register_as_student_menu()
        }
        while True:
            self.students = Student.get_data()
            print("1. Log In As Instructor")
            print("2. Log In As Student")
            print("3. Log In As Admin")
            print("4. Register As a Instructor")
            print("5. Register as a Student")

            choice = input("Please enter your choice: ")
            action = start_options.get(choice)
            if action:
                action()
            else:
                print("Invalid choice, please try again.")

    def log_in_instructor_menu(self):
        while True:
            username = input("Username: ")
            password = getpass("Password: ")
            if not Authentication.authenticate_instructor(username, password):
                print("Username or Password is wrong")
            else:
                self.current_instructor = Authentication.authenticate_instructor(username, password)
                self.instructor_menu()
    def log_in_student_menu(self):
        while True:
            username = input("Username: ")
            password = getpass("Password: ")
            if not Authentication.authenticate_student(username, password):
                print("Username or Password is wrong")
            else:
                self.current_student = Authentication.authenticate_student(username, password)
                self.student_menu()

    def log_in_admin_menu(self):
        while True:
            username = input("Username: ")
            password = getpass("Password: ")
            if not Authentication.authenticate_admin(username, password):
                print("Username or Password is wrong")
            else:
                self.admin_menu()



