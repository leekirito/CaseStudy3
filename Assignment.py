import pyodbc
from datetime import datetime 
import os 
from tabulate import tabulate
from Student import Student
from Enrollment import Enrollment
from Course import Course

def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )

class Assignment():
    
    def __init__(self, assignment_id, intructor_id, student_id, course_id, assignment_name, assigned_date, due_date, details, grade, response):
        self.assignment_id  = assignment_id
        self.intructor_id =intructor_id
        self.student_id = student_id
        self. course_id = course_id
        self.assignment_name =assignment_name
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.details = details
        self.grade = grade
        self.response = response

    @classmethod
    def get_data(cls):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Assignments")
        rows = cursor.fetchall()
        assignments = [
            cls(
                assignment_id=row.assignment_id,
                instructor_id=row.instructor_id,
                student_id=row.student_id,
                course_id=row.course_id,
                assignment_name=row.assignment_name,
                assigned_date=row.assigned_date,
                due_date=row.due_date,
                details=row.details,
                grade=row.grade,
                response=row.response
            )
            for row in rows
        ]  

        cursor.close()
        conn.close()
        return assignments

    @classmethod
    def assign_work(cls, intructor_id):
        username = input("Student Username: ")
        students = Student.get_data()
        student_id = None
        for student in students:
            if student.username == username:
                student_id = student.student_id
                break
        else:
            print("Student does not exist")
            return None

        course_id = None
        courses = Course.get_data()
        for course in courses:
            if intructor_id == course.intructor_id:
                course_id = course.course_id

        enrollments = Enrollment.get_data()
        for enroll in enrollments:
            if student_id == enroll.student_id and course_id == enroll.course_id:
                break
        else:
            print("This student is not enrolled in your course!")
            return None
        assignment_name = input("Assignment Name: ")
        assigned_date = datetime.now().date()
        due_date = input("Due Date(YYYY-MM-DD): ")
        details = input("Instructions: ")
        grade = 0
        conn = connect_to_database()  
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Assignments(intructor_id, student_id, course_id, assignment_name, assigned_date, due_date, details, grade)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """, (intructor_id, student_id, course_id, assignment_name, assigned_date, due_date, details, grade))
        conn.commit()
        cursor.close()
        conn.close()
        os.system("cls")
        print("Assigned successfully")
    
    @classmethod
    def show_all_assigned_work(cls, intructor_id):
        works = cls.get_data()
        content = []
        for work in works:
            if intructor_id == work.intructor_id:
                content.append([work.assignment_id, work.student_id, work.course_id, work.assignment_name, work.details, work.assigned_date, work.due_date, work.grade, work.response])
        header = ["Assignment ID","Student ID","Course ID","Title","Detials","Assigned Date", "Due Date", "Grade", "Response"]
        print(tabulate(content, header, tablefmt="pretty"))

    @classmethod
    def show_assigned_work(cls, student_id):
        works = Assignment.get_data()
        content = []
        for work in works:
            if student_id == work.student_id:
                content.append([work.assignment_id,work.intructor_id, work.course_id, work.assignment_name, work.details, work.assigned_date, work.due_date, work.grade, work.response])
        header = ["Assignment ID","Intructor ID","Course ID","Title","Detials","Assigned Date", "Due Date", "Grade", "Response"]
        print(tabulate(content, header, tablefmt="pretty"))

    @classmethod
    def answer_assignment(cls,student_id):
        cls.show_assigned_work(student_id)
        assignment_id = int(input("Assignment ID: "))
        assignments = cls.get_data()
        response = None
        for assignment in assignments:
            if assignment_id == assignment.assignment_id and student_id == assignment.student_id:
                response = input("Your answer: ")
                break
        else:
            print("Assignment did not exit")
            return None
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("UPDATE Assignments SET response = ? WHERE assignment_id = ?", (response, assignment_id))
        conn.commit()
        cursor.close()
        conn.close()
                