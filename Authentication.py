from Instructor import Instructor
from Student import Student

class Authentication():

    @staticmethod
    def authenticate_instructor(username, password):
        instructors = Instructor.get_data()
        for instructor in instructors:
            if username == instructor.username and password == instructor.password:
                return True
        return False
    
    @staticmethod
    def authenticate_student(username, password):
        students = Student.get_data()
        for student in students:
            if username == student.username and password == student.password:
                return True
        return False


