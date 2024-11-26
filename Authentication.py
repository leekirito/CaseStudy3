from Instructor import Instructor
from Student import Student
from PlatformAdmin import PlatformAdmin

class Authentication():

    @staticmethod
    def authenticate_instructor(username, password):
        instructors = Instructor.get_data()
        for instructor in instructors:
            if username == instructor.username and password == instructor.password:
                return instructor
        print("User Does not exist")
        return False
    
    @staticmethod
    def authenticate_student(username, password):
        students = Student.get_data()
        for student in students:
            if username == student.username and password == student.password:
                return student
        print("User Does not exist")
        return False
    
    def authenticate_admin(username, password):
        if username == PlatformAdmin.username and password == PlatformAdmin.password:
            return True
        else:
            return False


