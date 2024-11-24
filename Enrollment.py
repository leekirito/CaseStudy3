import pyodbc
from datetime import datetime 
import os 
from tabulate import tabulate
from Course import Course
from Student import Student
from Course import Course


def connect_to_database():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LIECODEX\\SQLEXPRESS;"
        "DATABASE=E_Learning_Platform;"
        "Trusted_Connection=yes;"
    )

class Enrollment():
    def __init__(self, enrollment_id, student_id, course_id, enrollment_date, status, progress):
        self.enrollment_id = enrollment_id
        self.student_id =student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date
        self.status = status
        self.progress = progress

    @classmethod
    def get_data(cls):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Enrollments")
        rows = cursor.fetchall()
        
        # Create Enrollment objects for each row in the database
        enrollments = [
            cls(
                enrollment_id=row.enrollment_id,
                student_id=row.student_id,
                course_id=row.course_id,
                enrollment_date=row.enrollment_date,
                status=row.status,
                progress=row.progress
            )
            for row in rows
        ]
        
        cursor.close()
        conn.close()
        return enrollments

    @classmethod
    def show_enrolled_course(cls):
        enrolls = cls.get_data()
        content = []
        for enroll in enrolls:
            content.append([enroll.enrollment_id, enroll.student_id, enroll.course_id, enroll.enrollment_date, enroll.status, enroll.progress])

        header = ["Enrollment ID","Student ID","Course ID","Enrolled Date","Status","Progress",]
        print(tabulate(content, header, tablefmt="pretty"))

    @classmethod
    def take_course(username):
        Course.show_all_courses()
        studetns = Student.get_data()
        student_id = None
        for student in studetns:
            if student.username == username:
                student_id = student.student_id
        Course.show_all_courses()
        course_id = input("Course ID: ")
        courses = Course.get_data()
        for course in courses:
            if course.course_id == course_id:
                break
        else:#for else logic, else statement will execute if and only if for loop doesn't hit a break statement
            print("Course ID does not exist!")
            return None 
        enrollment_date = datetime.now().date()
        status = "active"
        progress = "0%"
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Enrollments(student_id, course_id, enrollment_date, status, progress)
            VALUES(?, ?, ?, ?, ?)
        """, (student_id, course_id, enrollment_date, status, progress))
        conn.commit()
        cursor.close()
        conn.close()
        Course.add_student(course_id)
        print("succesfuly took course!")
